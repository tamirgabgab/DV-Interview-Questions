// kinds: seqarb
//   seqarb                 0114        one sequencer, three sequences (A and B back to back, I with three items and a slot waiting for its answer): the arbitration mode, I's priority, its lock or grab and its start as controls; a slot cursor over the items the driver gets, with the queue, the lock and why the arbitration chose what it chose
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr } = dvqExplorers.lib;
  const NB = " ";

  // The model of uvm_sequencer of tools/figures/q0114.py (sequencer()), line for line: the
  // steps of a sequence are ["item", name], ["wait", slots], ["lock"], ["grab"], ["unlock"],
  // ["ungrab"] and ["run", child]. snaps[t] is what the arbitration of slot t saw: the queue
  // ([kind, sequence, item or lock / grab]), the lock holders and the choice ("-": none);
  // sleeping and top (not in the Python) are the sequences waiting for a slot and the
  // highest priority among the free requests, for the box's explanation.
  const saSeq = (name, steps, start = 0, priority = 100) => ({ name, steps, start, priority, parent: null, pc: 0, wake: start });
  const saRun = (seqs, mode = "FIFO") => {
    const queue = [], locks = [], ready = [], out = [], snaps = [];
    const everyone = seqs.slice();
    let busy = null;
    const above = (h, s) => s !== null && (s === h || above(h, s.parent));
    const blocked = (s) => locks.some((h) => !above(h, s));
    const grantLocks = () => {                             // the lock requests at the head of the queue
      while (queue.length && queue[0][0] === "lock" && !blocked(queue[0][1])) {
        const s = queue.shift()[1];
        locks.push(s);
        ready.push(s);
      }
    };
    const run = (s, now) => {
      while (s.pc < s.steps.length) {
        const [op, arg] = s.steps[s.pc];
        s.pc += 1;
        if (op === "item") { queue.push(["item", s, arg]); return; }   // start_item: wait for the arbitration
        if (op === "wait") { s.wake = now + arg; return; }
        if (op === "lock" || op === "grab") {
          const request = ["lock", s, op];
          if (op === "lock") queue.push(request); else queue.unshift(request);
          grantLocks();
          return;
        }
        if (op === "unlock" || op === "ungrab") { locks.splice(locks.indexOf(s), 1); grantLocks(); }
        if (op === "run") {
          arg.parent = s;
          arg.wake = null;
          everyone.push(arg);
          ready.push(arg);
          return;
        }
      }
      if (s.parent) ready.push(s.parent);                  // a child ended: its parent goes on
    };
    let t = 0;
    while (t === 0 || queue.length || busy || everyone.some((s) => s.wake !== null)) {
      if (t >= 100) throw new Error("a sequence waits forever");
      if (busy) { ready.push(busy); busy = null; }         // item_done: the sequence goes on at once
      for (const now of [t, t + 0.5]) {                    // a slot's start, then its middle
        for (const s of everyone) if (s.wake === now) { s.wake = null; ready.push(s); }
        while (ready.length) run(ready.shift(), now);
        if (now === t) {                                   // the driver asks for the next item
          grantLocks();
          while (ready.length) run(ready.shift(), now);
          let free = queue.filter((r) => r[0] === "item" && !blocked(r[1]));
          const top = free.length ? Math.max(...free.map((r) => r[1].priority)) : 0;
          if (mode === "STRICT_FIFO") free = free.filter((r) => r[1].priority === top);
          snaps.push({
            queue: queue.map((r) => [r[0], r[1].name, r[2]]), locks: locks.map((h) => h.name),
            out: free.length ? free[0][2] : "-", top,
            blocked: queue.filter((r) => r[0] === "item" && blocked(r[1])).map((r) => r[2]),
            sleeping: everyone.filter((s) => s.wake !== null).map((s) => s.name),
            priority: Object.fromEntries(queue.map((r) => [r[1].name, r[1].priority])),
          });
          if (free.length) { queue.splice(queue.indexOf(free[0]), 1); busy = free[0][1]; }
          out.push(free.length ? free[0][2] : "-");
        }
      }
      t += 1;
    }
    while (out.length && out[out.length - 1] === "-") out.pop();
    snaps.length = out.length;
    return { out, snaps };
  };
  // The page's sequences (its Python block of part ג): A and B, six items each from slot 0;
  // I from the middle of a slot: I0, a slot waiting for its answer, I1 and I2, inside a lock
  // or a grab when how names one.
  const saTraffic = (name, n = 6) => saSeq(name, Array.from({ length: n }, (_, i) => ["item", `${name}${i}`]));
  const saIrq = (how = null, priority = 100, start = 1.5) => {
    let steps = [["item", "I0"], ["wait", 1], ["item", "I1"], ["item", "I2"]];
    if (how) steps = [[how]].concat(steps, [[`un${how}`]]);
    return saSeq("I", steps, start, priority);
  };
  const saCase = (mode, how, priority, start) => saRun([saTraffic("A"), saTraffic("B"), saIrq(how, priority, start)], mode);
  // I0 to I2 with nothing of A or B between them
  const saTogether = (out) => {
    const at = out.map((x, i) => (x.startsWith("I") ? i : -1)).filter((i) => i >= 0);
    return out.slice(at[0], at[at.length - 1] + 1).every((x) => x === "-" || x.startsWith("I"));
  };

  const MODES = ["FIFO", "STRICT_FIFO"], HOWS = ["", "lock", "grab"], PRIOS = [100, 500], STARTS = ["0.5", "1.5", "2.5"];
  // every setting has the same number of columns, so changing one moves nothing
  const SLOTS = Math.max(...MODES.flatMap((m) => HOWS.flatMap((h) => PRIOS.flatMap((p) => STARTS.map((s) => saCase(m, h || null, p, Number(s)).out.length)))));
  const opts = (vals, labels, sel) => vals.map((v, i) => `<option value="${v}"${v === sel ? " selected" : ""}>${labels[i]}</option>`).join("");
  const isI = (x) => x.startsWith("I");
  const list = (xs) => ltr(xs.join(", "));
  const name = (op) => code(`${op}()`);

  const seqarbView = () => ({
    mount(box) {
      const st = { mode: "FIFO", how: "", prio: "100", start: "1.5", k: 0 };
      box.innerHTML =
        `<div class="ex-controls sa-set">` +
        `<label>המצב <select class="sa-mode" dir="ltr" aria-label="מצב ה-arbitration של ה-sequencer">${opts(MODES, MODES, st.mode)}</select></label>` +
        `<label>העדיפות של I <select class="sa-prio" dir="ltr" aria-label="העדיפות של I, לשאר 100">${opts(["100", "500"], ["100", "500"], st.prio)}</select></label>` +
        `<label>‏I נועל <select class="sa-how" dir="ltr" aria-label="האם I נועל את ה-sequencer, ואיך">${opts(HOWS, ["לא", "lock()", "grab()"], st.how)}</select></label>` +
        `<label>‏I מתחיל במשבצת <select class="sa-start" dir="ltr" aria-label="המשבצת שבה I מתחיל">${opts(STARTS, STARTS, st.start)}</select></label></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-start">המשבצת הראשונה</button>` +
        `<button type="button" class="md-button ex-prev">המשבצת הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המשבצת הבאה</button>` +
        `<button type="button" class="md-button ex-end">המשבצת האחרונה</button>` +
        `<span class="ex-pos sa-pos"></span></div>` +
        `<p class="ex-summary sa-sum" aria-live="polite"></p>` +
        `<div class="sa-line" dir="ltr" role="img"></div>` +
        `<span class="viz-legend sa-legend"><span><i class="sa-key-i"></i>פריט של I</span><span><i class="sa-key-now"></i>המשבצת של התור</span></span>` +
        `<section class="sa-card"><p class="sa-ctitle">התור לפני הבחירה (הראש משמאל)</p><div class="sa-queue" dir="ltr"></div><p class="sa-lock"></p></section>` +
        `<p class="wv-step sa-now" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      $(".sa-line").style.setProperty("--sa-slots", String(SLOTS));
      let run = null;
      const compute = () => {
        run = saCase(st.mode, st.how || null, Number(st.prio), Number(st.start));
        st.k = Math.min(st.k, run.out.length - 1);
      };
      const verdict = () => {
        const out = run.out, idle = out.filter((x) => x === "-").length;
        const at = out.map((x, t) => (isI(x) ? t : -1)).filter((t) => t >= 0);
        const ok = saTogether(out);
        return `ה-driver מקבל את I0, ‏I1 ו-I2 במשבצות ${ltr(at.join(", "))}. ` +
          (ok ? `<span class="wv-ok">‏I ברצף</span>` : `<span class="wv-bad">פריטים של A ו-B נכנסים בין הפריטים של I</span>`) +
          (idle ? `, ${idle === 1 ? "ומשבצת אחת ריקה" : `ו-${ltr(idle)} משבצות ריקות`} בזמן ש-A ו-B מחכים.` : ".");
      };
      const describe = (k) => {
        const s = run.snaps[k], prev = k ? run.snaps[k - 1] : null, parts = [];
        const how = st.how;
        if (s.locks.includes("I") && !(prev && prev.locks.includes("I"))) parts.push(`‏I קיבל את הנעילה (${name(how)})`);
        if (prev && prev.locks.includes("I") && !s.locks.includes("I")) parts.push(`‏I שחרר את הנעילה`);
        const req = s.queue.findIndex(([kind]) => kind === "lock");
        if (req >= 0) {
          const before = s.queue.slice(0, req).map(([, , x]) => x);
          parts.push(`בקשת ה-${name(s.queue[req][2])} של I מחכה בתור${before.length ? ` מאחורי ${list(before)}` : ""}`);
        }
        const x = s.out;
        if (x === "-") {
          const why = s.sleeping.includes("I") ? "‏I מחכה לתשובה ואין לו בקשה בתור" : "ל-I אין בקשה בתור";
          parts.push(s.blocked.length
            ? `<span class="wv-bad">${why}, וה-sequencer נעול${NB}: ה-driver לא מקבל כלום, ו-${list(s.blocked)} מחכים</span>`
            : "אין בקשות בתור");
        } else {
          const items = s.queue.filter(([kind]) => kind === "item");
          const older = items.slice(0, items.findIndex(([, , y]) => y === x)).map(([, , y]) => y);
          const passed = older.filter((y) => !s.blocked.includes(y));
          let why;
          if (st.mode === "STRICT_FIFO" && passed.length) why = `העדיפות ${ltr(s.top)} עוקפת את ${list(passed)}, שביקשו קודם`;
          else if (s.blocked.length && older.length) why = `${list(older)} חסומים בנעילה של I`;
          else if (st.mode === "STRICT_FIFO") why = `הוותיקה מבין הבקשות בעדיפות ${ltr(s.top)}`;
          else why = "הבקשה הוותיקה בתור";
          const fifoIgnores = st.mode === "FIFO" && st.prio === "500" && !isI(x) && items.some(([, who]) => who === "I");
          parts.push(`ה-driver מקבל את ${ltr(x)}${NB}: ${why}${fifoIgnores ? `. ‏${code("FIFO")} לא מסתכל על העדיפות 500 של I` : ""}`);
        }
        return `משבצת ${ltr(k)}${NB}: ${parts.join(". ")}.`;
      };
      const draw = () => {
        const k = st.k, T = run.out.length, s = run.snaps[k];
        $(".sa-pos").textContent = `משבצת ${k} מתוך ${T - 1}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T - 1;
        $(".sa-sum").innerHTML = verdict();
        const line = $(".sa-line");
        line.setAttribute("aria-label", `הפריטים שה-driver קיבל עד משבצת ${k}${NB}: ${run.out.slice(0, k + 1).map((x) => (x === "-" ? "כלום" : x)).join(", ")}`);
        line.innerHTML = Array.from({ length: SLOTS }, (_, t) => {
          const x = t < T ? run.out[t] : "";
          const cls = ["sa-cell", t > k || t >= T ? "is-future" : "", t <= k && isI(x) ? "is-i" : "", t === k ? "is-now" : ""].filter(Boolean).join(" ");
          return `<span class="${cls}" data-t="${t}"><small>${t}</small><b>${t <= k ? (x === "-" ? "·" : x) : " "}</b></span>`;
        }).join("");
        $(".sa-queue").innerHTML = s.queue.length
          ? s.queue.map(([kind, who, x]) => {
            const label = kind === "lock" ? `${x}(${who})` : x;
            const cls = ["sa-req", kind === "lock" ? "is-lockreq" : "", kind === "item" && s.blocked.includes(x) ? "is-blocked" : "", kind === "item" && x === s.out ? "is-pick" : ""].filter(Boolean).join(" ");
            const p = kind === "item" && s.priority[who] !== 100 ? `<small>${s.priority[who]}</small>` : "";
            return `<span class="${cls}">${label}${p}</span>`;
          }).join("")
          : `<span class="sa-empty">empty</span>`;
        $(".sa-lock").innerHTML = s.locks.length
          ? `נעילה${NB}: ‏I מחזיק את ה-sequencer, ורק הפריטים שלו עוברים.`
          : `נעילה${NB}: אין. כל בקשה בתור משתתפת בבחירה.`;
        $(".sa-now").innerHTML = describe(k);
      };
      const reload = () => { compute(); draw(); };
      [["sa-mode", "mode"], ["sa-prio", "prio"], ["sa-how", "how"], ["sa-start", "start"]].forEach(([cls, key]) => {
        const el = $(`.${cls}`);
        el.addEventListener("change", () => { st[key] = el.value; reload(); });
      });
      const go = (k) => { st.k = Math.max(0, Math.min(run.out.length - 1, k)); draw(); };
      $(".ex-start").addEventListener("click", () => go(0));
      $(".ex-prev").addEventListener("click", () => go(st.k - 1));
      $(".ex-next").addEventListener("click", () => go(st.k + 1));
      $(".ex-end").addEventListener("click", () => go(run.out.length - 1));
      // a click on a slot of the line moves the cursor there
      $(".sa-line").addEventListener("click", (e) => {
        const cell = e.target.closest(".sa-cell");
        if (cell && Number(cell.dataset.t) < run.out.length) go(Number(cell.dataset.t));
      });
      // the link and the remembered state: the cursor rides after the controls
      box.dvqExtra = {
        get: () => (st.k ? String(st.k) : ""),
        set: (text) => { const v = Number(text); if (!/^\d+$/.test(text) || v >= run.out.length) return false; go(v); return true; },
      };
      reload();
    },
  });

  dvqExplorers.register({
    views: { seqarb: seqarbView },
    help: {
      seqarb: `על sequencer אחד רצים A ו-B, שישה פריטים כל אחד מהמשבצת הראשונה, ו-I, ששולח את I0, מחכה משבצת לתשובה, ואז שולח את I1 ו-I2. הבוררים קובעים את מצב ה-arbitration, את העדיפות של I, אם הוא נועל ב-lock() או ב-grab(), ובאיזו משבצת הוא מתחיל. בכל משבצת ה-driver לוקח פריט אחד${NB}: השורה מראה מה הוא קיבל עד המשבצת המסומנת, והכרטיס מראה את התור לפני הבחירה, את הנעילה ולמה נבחר מה שנבחר. זה מודל של uvm_sequencer לפי IEEE 1800.2, אותו מודל שהטסטים של השאלה בודקים.`,
    },
    // the line and its key on the left; the queue and the slot's explanation beside them
    cols: { seqarb: { side: ".sa-card, .sa-now", w: "minmax(0, 1fr)" } },
    models: { saSeq, saRun, saTraffic, saIrq, saCase, saTogether, SA_SLOTS: SLOTS },
  });
})();
