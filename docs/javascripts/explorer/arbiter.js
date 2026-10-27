// kinds: arbiter
//   arbiter                0054        4 requesters over 16 cycles drawn by hand or from presets: the grants of a fixed priority, a round robin (with an optional bug) and a weighted round robin, the longest wait of each requester against its bound, the double-request trick at the chosen cycle, and the assertions that fail
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, f, ltr, mulberry32, seedControls } = dvqExplorers.lib;

  // Arbiters (0054) over a trace of request vectors: fixed priority (the lowest set bit),
  // round robin by the double-request trick with a one-hot pointer (bug: "stuck" never
  // moves the pointer, "winner" moves it onto the winner, "double" grants the lowest
  // requester too), weighted round robin (the pointer stays on the winner for up to its
  // weight in a row), and the rules of the checker counted on a trace.
  const arbFixed = (reqs) => reqs.map((r) => r & -r);
  const arbTrick = (req, pri, n) => {
    const mask = (1 << (2 * n)) - 1, dbl = (req << n) | req, minus = (dbl - pri) & mask, inv = ~minus & mask, sel = dbl & inv;
    return { dbl, minus, inv, sel, gnt: (sel | (sel >> n)) & ((1 << n) - 1) };
  };
  const rot = (g, n) => ((g << 1) | (g >> (n - 1))) & ((1 << n) - 1);
  const arbRRTrace = (reqs, n, bug = "none") => {
    let pri = 1;
    const out = [];
    reqs.forEach((r) => {
      let g = arbTrick(r, pri, n).gnt;
      const before = pri;
      if (bug === "double") g |= r & -r;
      if (g && bug !== "stuck") pri = bug === "winner" ? arbTrick(r, before, n).gnt : rot(arbTrick(r, before, n).gnt, n);
      out.push({ g, pri: before });
    });
    return out;
  };
  const arbRR = (reqs, n, bug = "none") => arbRRTrace(reqs, n, bug).map((x) => x.g);
  const arbWRR = (reqs, w) => {
    const n = w.length;
    let pri = 1, used = 0;
    return reqs.map((r) => {
      const g = arbTrick(r, pri, n).gnt;
      if (g) {
        const i = 31 - Math.clz32(g);
        used = g === pri ? used + 1 : 1;
        if (used === w[i]) { pri = rot(g, n); used = 0; } else pri = g;
      }
      return g;
    });
  };
  // the rules: per cycle (one-hot, no grant without a request), per requester and cycle
  // (the hold rule of the environment, fairness within maxw cycles); the cycles of each
  // failure are returned too (fairness at the start of the attempt)
  const arbFails = (reqs, grants, n, maxw) => {
    const T = reqs.length, at = { onehot: [], spurious: [], hold: [], fair: [] };
    for (let t = 0; t < T; t++) {
      const g = grants[t];
      if (g & (g - 1)) at.onehot.push(t);
      if (g & ~reqs[t]) at.spurious.push(t);
      for (let i = 0; i < n; i++) {
        const asked = (reqs[t] >> i) & 1, got = (g >> i) & 1;
        if (t + 1 < T && asked && !got && !((reqs[t + 1] >> i) & 1)) at.hold.push(t);
        if (asked && t + maxw < T) {
          let ok = false;
          for (let u = t; u <= t + maxw; u++) if ((grants[u] >> i) & 1) ok = true;
          if (!ok) at.fair.push(t);
        }
      }
    }
    return at;
  };
  const arbCheck = (reqs, grants, n, maxw) => Object.fromEntries(Object.entries(arbFails(reqs, grants, n, maxw)).map(([k, v]) => [k, v.length]));
  const arbMaxWait = (reqs, grants, i) => {
    let best = 0, run = 0;
    reqs.forEach((r, t) => { if ((r >> i) & 1 && !((grants[t] >> i) & 1)) { run++; best = Math.max(best, run); } else run = 0; });
    return best;
  };

  // The box (0054): 4 requesters and 16 cycles; the request grid drawn by a click (a cell is
  // a button), or a preset; the grants of the three arbiters under it, each row with the
  // longest wait of every requester against its bound; a cycle picked by the steps (the
  // column lit) with the trick of the round robin at that cycle; a bug for the round robin,
  // and the assertions of part c with the cycles where each fails.
  const N = 4, T = 16;
  const RULES = [["onehot", `מענק אחד לכל היותר : ${code("$onehot0(gnt)")}`], ["spurious", "אין מענק בלי בקשה"], ["hold", "הסביבה : בקשה שמחכה נשארת"], ["fair", "הוגנות : מענק תוך N − 1 = 3"]];
  const arbiterView = () => ({
    mount(box) {
      const st = { reqs: Array(T).fill(0b1001), k: 0, bug: "none", w: [1, 2, 3, 4] };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<span class="wv-presets">דוגמאות : <button type="button" class="md-button arb-preset" data-p="03">0 ו-3 תמיד</button> <button type="button" class="md-button arb-preset" data-p="all">כולם תמיד</button> <button type="button" class="md-button arb-preset" data-p="none">ריק</button></span>` +
        `<button type="button" class="md-button arb-rand">בקשות אקראיות</button><span class="arb-anchor"></span>` +
        `<label>באג ב-round robin <select class="arb-bug" aria-label="באג להכניס"><option value="none">בלי באג</option><option value="stuck">המצביע לא זז</option><option value="winner">המצביע עובר אל המנצח</option><option value="double">גם הנמוך מקבל</option></select></label>` +
        `<span class="arb-weights">משקלים ל-WRR : ${[0, 1, 2, 3].map((i) => `<label><span>${i}</span><select class="arb-w" data-i="${i}" aria-label="המשקל של מבקש ${i}">${[1, 2, 3, 4].map((v) => `<option value="${v}"${v === st.w[i] ? " selected" : ""}>${v}</option>`).join("")}</select></label>`).join(" ")}</span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">מחזור 0</button>` +
        `<button type="button" class="md-button ex-prev">המחזור הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">המחזור הבא</button>` +
        `<button type="button" class="md-button ex-end">המחזור האחרון</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary arb-sum" aria-live="polite"></p>` +
        `<div class="arb-grid" data-edits></div>` +
        `<span class="viz-legend"><span><i class="arb-key-req"></i>בקשה (לחיצה מדליקה ומכבה)</span><span><i class="arb-key-gnt"></i>מענק</span><span><i class="arb-key-wait"></i>מבקש ומחכה</span><span><i class="arb-key-bad"></i>הפרה של assertion</span></span>` +
        `<div class="arb-trick"></div>` +
        `<div class="arb-rules"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const bits = (v, w) => (v >>> 0).toString(2).padStart(w, "0").slice(-w);
      const grid = (rr, fx, wr, fails) => {
        const S = 30, L = 118, top = 26, gap = 22, W = L + T * S + 64;
        const blocks = [["req", null], ["fixed", fx], [`RR${st.bug !== "none" ? " ✗" : ""}`, rr], ["WRR", wr]];
        const H = top + blocks.length * (N * S + gap);
        const bad = new Set([...fails.onehot, ...fails.spurious]);
        let s = `<svg class="figure arb-live" viewBox="0 0 ${W} ${H}" role="group" aria-label="רשת הבקשות והמענקים : 4 מבקשים, 16 מחזורים">`;
        s += `<rect class="arb-cursor" x="${L + st.k * S - 1}" y="${top - 8}" width="${S + 1}" height="${H - top}" rx="3"/>`;
        for (let c = 0; c < T; c++) s += `<text class="tick" x="${L + c * S + S / 2}" y="${top - 12}" text-anchor="middle">${c}</text>`;
        blocks.forEach(([name, g], b) => {
          const y0 = top + b * (N * S + gap);
          s += `<text class="arb-name" x="${L - 46}" y="${y0 + (N * S) / 2 + 4}" text-anchor="middle">${name}</text>`;
          for (let i = 0; i < N; i++) {
            const y = y0 + i * S;
            s += `<text class="tick" x="${L - 6}" y="${y + S / 2 + 4}" text-anchor="end">${i}</text>`;
            for (let c = 0; c < T; c++) {
              const asked = (st.reqs[c] >> i) & 1;
              if (!g) {
                s += `<rect class="arb-cell arb-req${asked ? " is-on" : ""}" data-c="${c}" data-i="${i}" x="${L + c * S}" y="${y}" width="${S - 3}" height="${S - 3}" rx="3" tabindex="0" role="button" aria-pressed="${asked ? "true" : "false"}" aria-label="מבקש ${i}, מחזור ${c}"/>`;
              } else {
                const got = (g[c] >> i) & 1, wrong = b === 2 && bad.has(c) && got;
                s += `<rect class="arb-cell ${got ? "is-gnt" : asked ? "is-wait" : "is-idle"}${wrong ? " is-bad" : ""}" x="${L + c * S}" y="${y}" width="${S - 3}" height="${S - 3}" rx="3"/>`;
                if (got) s += `<text class="arb-mark" x="${L + c * S + S / 2 - 1}" y="${y + S / 2 + 4}" text-anchor="middle">G</text>`;
              }
            }
            if (g) {
              const wait = arbMaxWait(st.reqs, g, i), bound = b === 1 ? "∞" : b === 2 ? String(N - 1) : String(st.w.reduce((x, v) => x + v, 0) - st.w[i]);
              const over = bound !== "∞" && wait > Number(bound);
              s += `<text class="arb-wait${over ? " is-over" : ""}" x="${L + T * S + 6}" y="${y + S / 2 + 4}">${wait}/${bound}</text>`;
            }
          }
        });
        return s + `<text class="legend" x="${L + T * S + 6}" y="${top + N * S + gap - 6}">wait/bound</text></svg>`;
      };
      const draw = () => {
        const fx = arbFixed(st.reqs), tr = arbRRTrace(st.reqs, N, st.bug), rr = tr.map((x) => x.g), wr = arbWRR(st.reqs, st.w);
        const fails = arbFails(st.reqs, rr, N, N - 1);
        $(".ex-pos").textContent = `מחזור ${st.k} מתוך ${T - 1}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T - 1;
        const w3 = arbMaxWait(st.reqs, fx, 3);
        $(".arb-sum").innerHTML = `עדיפות קבועה : מבקש 3 חיכה עד ${ltr(w3)} מחזורים${w3 >= 8 ? " (הרעבה)" : ""}. ‏round robin : ההמתנה הארוכה ביותר ${ltr(Math.max(...[0, 1, 2, 3].map((i) => arbMaxWait(st.reqs, rr, i))))} מחזורים, והחסם ${ltr(N - 1)}` +
          (st.bug !== "none" ? `, עם הבאג "${$(".arb-bug").selectedOptions[0].textContent}"` : "") + `. ‏WRR : המשקלים ${ltr(st.w.join(", "))}.`;
        $(".arb-grid").innerHTML = grid(rr, fx, wr, fails);
        const r = st.reqs[st.k], pri = tr[st.k].pri, t = arbTrick(r, pri, N), row = (name, v, w, what) => `<tr><td><code>${name}</code></td><td><code>${bits(v, w)}</code></td><td>${what}</td></tr>`;
        $(".arb-trick").innerHTML = `<p class="ex-title">הטריק של round robin במחזור ${ltr(st.k)} : העדיפות אצל מבקש ${ltr(31 - Math.clz32(pri))}</p>` +
          `<table class="arb-tt"><tbody>` + row("req", r, N, "הבקשות") + row("pri", pri, N, "המצביע, one-hot") + row("dbl", t.dbl, 2 * N, "הבקשות פעמיים") +
          row("dbl − pri", t.minus, 2 * N, "הלווה מאפס את הבקשה הראשונה מ-pri") + row("~(dbl − pri)", t.inv, 2 * N, "ההיפוך") +
          row("sel", t.sel, 2 * N, "רק הבקשה הראשונה מ-pri והלאה") + row("gnt", t.gnt, N, t.gnt ? `מבקש ${31 - Math.clz32(t.gnt)} זוכה` : "אין בקשות, אין מענק") + `</tbody></table>` +
          (st.bug === "double" ? `<p class="wv-bad">עם הבאג, גם ${code("req & -req")} מקבל : ${code(bits(rr[st.k], N))}.</p>` : "");
        $(".arb-rules").innerHTML = `<p class="ex-title">ה-assertions של סעיף ג על ה-round robin</p>` + RULES.map(([k, name]) => {
          const at = fails[k];
          return `<p class="arb-rule">${at.length ? `<span class="wv-bad">✗ ${name} : נכשלה ${ltr(at.length)} פעמים, במחזורים ${ltr([...new Set(at)].slice(0, 8).join(", "))}${at.length > 8 ? "…" : ""}</span>` : `<span class="wv-ok">✓ ${name}</span>`}</p>`;
        }).join("");
      };
      const toggle = (c, i) => { st.reqs[c] ^= 1 << i; draw(); };
      $(".arb-grid").addEventListener("click", (e) => { const el = e.target.closest("[data-c]"); if (el) toggle(Number(el.dataset.c), Number(el.dataset.i)); });
      $(".arb-grid").addEventListener("keydown", (e) => { const el = e.target.closest("[data-c]"); if (el && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); toggle(Number(el.dataset.c), Number(el.dataset.i)); } });
      box.querySelectorAll(".arb-preset").forEach((b) => b.addEventListener("click", () => { st.reqs = Array(T).fill(b.dataset.p === "all" ? 0b1111 : b.dataset.p === "03" ? 0b1001 : 0); draw(); }));
      // random requests that keep a waiting request against the round robin's grants
      const seed = seedControls(box, $(".arb-anchor"), (rng) => {
        const reqs = [];
        let pri = 1, prev = 0, gPrev = 0;
        for (let c = 0; c < T; c++) {
          let nxt = 0;
          for (let i = 0; i < N; i++) if (((prev >> i) & 1 && !((gPrev >> i) & 1)) || rng() < 0.55) nxt |= 1 << i;   // a waiting request stays
          gPrev = arbTrick(nxt, pri, N).gnt;
          if (gPrev) pri = rot(gPrev, N);
          reqs.push(nxt); prev = nxt;
        }
        st.reqs = reqs; draw();
      }, { fresh: false });
      $(".arb-rand").addEventListener("click", () => seed.draw());
      $(".arb-bug").addEventListener("change", () => { st.bug = $(".arb-bug").value; draw(); });
      box.querySelectorAll(".arb-w").forEach((s) => s.addEventListener("change", () => { st.w[Number(s.dataset.i)] = Number(s.value); draw(); }));
      $(".ex-start").addEventListener("click", () => { st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(T - 1, st.k + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { st.k = T - 1; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { arbiter: arbiterView },
    help: {
      arbiter: "הרשת העליונה היא הבקשות : לחיצה על משבצת מדליקה או מכבה בקשה, או שבוחרים דוגמה. מתחת, המענקים של עדיפות קבועה, ‏round robin ו-WRR, ובסוף כל שורה ההמתנה הארוכה ביותר מול החסם. ״המחזור הבא״ בוחר מחזור, והטבלה מראה את הטריק של round robin בו. ״באג״ מכניס באג ל-round robin, והרשימה מראה איזו assertion נכשלת ומתי.",
    },
    models: { arbFixed, arbTrick, arbRR, arbWRR, arbCheck, arbMaxWait },
  });
})();
