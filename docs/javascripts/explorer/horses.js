// kinds: horses
//   horses                 0043        a horses, b per race, the c fastest in order (or the page's numbers with data-fixed): hidden seeded speeds, the plan played race by race on a grid of the groups with the race table and who was ruled out and why; a reveal toggle; the proof panel: a tapped horse's known-faster set and the chain of results behind it
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, X0, answer, autoplay, f, ltr, mulberry32, seedControls, speedSel } = dvqExplorers.lib;

  // Horse races (0043): a horses with hidden speeds, b per race, the c fastest in order.
  // For every horse the set of horses known faster and known slower (transitively
  // closed); the groups, the winners, then the most promising open candidates with the
  // most comparisons still missing, until ranks 1..c are settled. The log keeps, per
  // race, who ran, the finishing order, who was newly ruled out (with the horses known
  // faster), who was newly settled, and the open candidates.
  const horsesSpeeds = (a, rnd) => { const p = Array.from({ length: a }, (_, i) => i); for (let i = a - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; } return p; };
  const horsesPlan = (a, b, c, speed) => {
    const faster = Array.from({ length: a }, () => new Set()), slower = Array.from({ length: a }, () => new Set());
    const out = new Set(), settled = new Map(), log = [];
    const beats = (x, y) => {
      if (slower[x].has(y)) return;
      const up = [...faster[x], x], down = [...slower[y], y];
      up.forEach((u) => down.forEach((v) => { slower[u].add(v); faster[v].add(u); }));
    };
    const run = (group, what) => {
      const order = [...group].sort((u, v) => speed[u] - speed[v]);
      for (let i = 0; i < order.length; i++) for (let k = i + 1; k < order.length; k++) beats(order[i], order[k]);
      const gone = [], placed = [], known = {};
      for (let x = 0; x < a; x++) {
        if (!out.has(x) && faster[x].size >= c) { out.add(x); gone.push(x); known[x] = [...faster[x]].sort((u, v) => u - v); }
        if (!settled.has(x) && faster[x].size + slower[x].size === a - 1 && faster[x].size < c) { settled.set(x, faster[x].size + 1); placed.push(x); }
      }
      const open = []; for (let x = 0; x < a; x++) if (!out.has(x) && !settled.has(x)) open.push(x);
      log.push({ what, horses: [...group], order, gone, placed, open, faster: known });
    };
    const groups = []; for (let k = 0; k < a; k += b) groups.push(Array.from({ length: Math.min(b, a - k) }, (_, i) => k + i));
    groups.forEach((g, k) => run(g, ["group", k]));
    if (groups.length > 1) run(groups.map((g) => g.reduce((u, v) => (speed[u] < speed[v] ? u : v))), ["winners", null]);
    const done = () => { for (let r = 1; r <= c; r++) if (![...settled.values()].includes(r)) return false; return true; };
    while (!done()) {
      const pool = []; for (let x = 0; x < a; x++) if (!out.has(x) && !settled.has(x)) pool.push(x);
      pool.sort((u, v) => faster[u].size - faster[v].size || slower[v].size - slower[u].size || u - v);
      const chosen = [];
      while (chosen.length < b && pool.length) {
        let best = 0, bs = null;
        pool.forEach((x, i) => {
          const score = [chosen.filter((y) => !faster[x].has(y) && !slower[x].has(y)).length, -faster[x].size, slower[x].size];
          if (bs === null || score[0] > bs[0] || (score[0] === bs[0] && (score[1] > bs[1] || (score[1] === bs[1] && score[2] > bs[2])))) { bs = score; best = i; }
        });
        chosen.push(pool.splice(best, 1)[0]);
      }
      run(chosen, ["final", null]);
    }
    const ranking = []; for (let r = 1; r <= c; r++) for (const [x, rk] of settled) if (rk === r) ranking.push(x);
    return { ranking, log };
  };

  // The proof of a known-faster set: after `step` races, every horse known faster than x
  // with a shortest chain of direct results down to x (each link [faster, slower, race]),
  // and the races those chains use.
  const horsesChain = (log, step, x) => {
    const above = new Map();                         // v -> [[u, race]]: u beat v in that race
    log.slice(0, step).forEach((e, r) => e.order.forEach((u, i) => e.order.slice(i + 1).forEach((v) => {
      if (!above.has(v)) above.set(v, []);
      above.get(v).push([u, r]);
    })));
    const below = new Map([[x, null]]), queue = [x];   // below: y -> [the next horse down the chain, race]
    for (let h = 0; h < queue.length; h++) {
      (above.get(queue[h]) || []).forEach(([u, r]) => { if (!below.has(u)) { below.set(u, [queue[h], r]); queue.push(u); } });
    }
    const chains = queue.slice(1).map((y) => {
      const links = [];
      for (let u = y; u !== x; ) { const [v, r] = below.get(u); links.push([u, v, r]); u = v; }
      return { y, links };
    });
    return { chains, races: [...new Set(chains.flatMap((c) => c.links.map((l) => l[2])))].sort((a, b) => a - b) };
  };

  // The horse races box (0043): the page's numbers (data-fixed) or a, b and c to set;
  // hidden speeds drawn from a seed, the plan played race by race: a grid of the groups
  // (rows in the winners' order once they raced) with every horse coloured out /
  // candidate / settled and the horses of the current race framed, a growing race table,
  // a line that says who was ruled out and why, and a reveal toggle for the true ranks.
  const horsesView = () => ({
    mount(box) {
      const d = box.dataset, fixed = d.fixed === "1", AMAX = 64, BMAX = 8, CMAX = 6, L = "ABCDEFGHIJ";
      const A0 = Number(d.a || 36), B0 = Number(d.b || 6), C0 = Number(d.c || 4), S0 = Number(d.seed || 1);
      const st = { a: A0, b: B0, c: C0, seed: S0, speed: [], plan: null, step: 0, reveal: false, names: {}, pick: null };   // pick: the horse whose chain is shown
      box.innerHTML =
        (fixed ? "" :
          `<div class="ex-controls">` +
          `<label><span>סוסים a</span><input type="number" class="ex-num hr-a" min="2" max="${AMAX}" step="1" value="${st.a}" dir="ltr" inputmode="numeric" aria-label="מספר הסוסים, עד ${AMAX}"></label>` +
          `<label><span>במסלול b</span><input type="range" class="hr-b" min="2" max="${BMAX}" step="1" value="${st.b}" dir="ltr" aria-label="סוסים בכל תחרות"><output class="out-b">${st.b}</output></label>` +
          `<label><span>ראשונים c</span><input type="range" class="hr-c" min="1" max="${CMAX}" step="1" value="${st.c}" dir="ltr" aria-label="כמה ראשונים"><output class="out-c">${st.c}</output></label>` +
          `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err hr-err"></span></div>`) +
        `<div class="ex-controls"><button type="button" class="md-button ex-random">הגרלת מהירויות</button>` +
        `<label class="hr-reveal"><input type="checkbox" class="hr-show"> חשיפת המהירויות</label></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">התחרות הבאה</button>` +
        `<button type="button" class="md-button ex-prev">התחרות הקודמת</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(2200, 1200, 500) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span></div>` +
        `<p class="ex-summary hr-sum" aria-live="polite"></p><p class="hr-step"></p>` +
        `<span class="viz-legend"><span><i class="hr-key-placed"></i>נקבע</span><span><i class="hr-key-cand"></i>מועמד</span><span><i class="hr-key-out"></i>נפסל (המספר : כמה מהירים ידועים)</span><span><i class="hr-key-now"></i>רץ בתחרות הזו</span></span>` +
        `<div class="hr-gridbox"></div><p class="ex-title">התחרויות עד כה</p><div class="hr-table"></div>` +
        `<section class="ex-proof hr-proof"><p class="ex-proof-title">שלב ההוכחה : השרשרת מאחורי ההכרעה</p><p class="hr-chain"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const compute = () => {
        st.speed = horsesSpeeds(st.a, mulberry32(st.seed));
        st.plan = horsesPlan(st.a, st.b, st.c, st.speed);
        st.names = {};
        st.plan.log.forEach((e) => { if (e.what[0] === "group") e.order.forEach((x, i) => { st.names[x] = `${L[Math.floor(x / st.b)]}${i + 1}`; }); });
        st.step = Math.min(st.step, st.plan.log.length);
        st.pick = null;
      };
      const nm = (x) => st.names[x] || `${L[Math.floor(x / st.b)]}?`;
      const rankOf = (x) => st.speed.filter((v) => v < st.speed[x]).length + 1;
      // the state after `step` races: known-faster counts, out / settled, and the row order
      const after = (step) => {
        const faster = Array.from({ length: st.a }, () => new Set()), slower = Array.from({ length: st.a }, () => new Set());
        st.plan.log.slice(0, step).forEach((e) => {
          for (let i = 0; i < e.order.length; i++) for (let k = i + 1; k < e.order.length; k++) {
            const x = e.order[i], y = e.order[k];
            if (slower[x].has(y)) continue;
            [...faster[x], x].forEach((u) => [...slower[y], y].forEach((v) => { slower[u].add(v); faster[v].add(u); }));
          }
        });
        const winners = st.plan.log.slice(0, step).find((e) => e.what[0] === "winners");
        const groups = []; for (let k = 0; k < st.a; k += st.b) groups.push(Array.from({ length: Math.min(st.b, st.a - k) }, (_, i) => k + i));
        const raced = new Set(st.plan.log.slice(0, step).filter((e) => e.what[0] === "group").map((e) => e.what[1]));
        const rows = groups.map((g, k) => ({ k, horses: raced.has(k) ? [...g].sort((u, v) => st.speed[u] - st.speed[v]) : g }));
        if (winners) rows.sort((r1, r2) => winners.order.indexOf(r1.horses[0]) - winners.order.indexOf(r2.horses[0]));
        return { faster, slower, rows, winners: !!winners, raced };
      };
      const grid = (s) => {
        const CW = 64, CH = 40, X0 = 70, Y0 = 30, W = X0 + st.b * CW + 10, H = Y0 + s.rows.length * CH + 10;
        const now = new Set(st.step ? st.plan.log[st.step - 1].horses : []);
        const ch = st.pick === null ? null : horsesChain(st.plan.log, st.step, st.pick), lit = new Set(ch ? ch.chains.map((c) => c.y) : []);
        const at = {};                                   // the centre of every horse's cell
        s.rows.forEach((row, j) => row.horses.forEach((x, i) => { at[x] = [X0 + i * CW + CW / 2, Y0 + j * CH + CH / 2]; }));
        let h = `<svg class="figure hr-grid hr-live" viewBox="0 0 ${W} ${H}" style="max-width : ${(W / 16).toFixed(0)}rem" role="img" aria-label="הסוסים אחרי ${st.step} תחרויות : שורה לכל קבוצה, הצבע אומר נפסל, מועמד או נקבע">`;
        for (let i = 0; i < st.b; i++) h += `<text class="tick" x="${X0 + i * CW + CW / 2}" y="${Y0 - 10}" text-anchor="middle">${i + 1}</text>`;
        s.rows.forEach((row, j) => {
          h += `<text class="tick" x="${X0 - 8}" y="${Y0 + j * CH + CH / 2 + 4}" text-anchor="end">${L[row.k]}${s.winners ? ` (${j + 1})` : ""}</text>`;
          row.horses.forEach((x, i) => {
            const nf = s.faster[x].size, cls = nf + s.slower[x].size === st.a - 1 && nf < st.c ? "is-placed" : nf >= st.c ? "is-out" : "is-cand";
            const X = X0 + i * CW, Y = Y0 + j * CH;
            const label = s.raced.has(row.k) ? nm(x) : `${L[row.k]}?`;        // a name only once the group raced
            const name = `${label} ${nf}${st.reveal ? ` #${rankOf(x)}` : ""}`;   // the visible texts, in order
            h += `<g class="hr-cell ${cls}${now.has(x) ? " is-now" : ""}${lit.has(x) ? " is-chain" : ""}${x === st.pick ? " is-pick" : ""}" data-x="${x}" tabindex="0" role="button" aria-pressed="${x === st.pick}" aria-label="${name}, השרשרת של הסוס"><rect x="${X + 2}" y="${Y + 2}" width="${CW - 4}" height="${CH - 4}" rx="4"><title>${label} : ${nf} מהירים ידועים, ${s.slower[x].size} איטיים ידועים${st.reveal ? `, מקום אמיתי ${rankOf(x)}` : ""}</title></rect>` +
              `<text class="hr-name" x="${X + CW / 2}" y="${Y + CH / 2 + 5}" text-anchor="middle">${label}</text><text class="hr-count" x="${X + CW - 6}" y="${Y + 13}" text-anchor="end">${nf}</text>` +
              (st.reveal ? `<text class="hr-rank" x="${X + 6}" y="${Y + CH - 6}">#${rankOf(x)}</text>` : "") + `</g>`;
          });
        });
        if (ch) {
          const links = new Map();
          ch.chains.forEach((c) => c.links.forEach(([u, v]) => links.set(`${u}-${v}`, [u, v])));
          links.forEach(([u, v]) => {
            const [x1, y1] = at[u], [x2, y2] = at[v], d = Math.hypot(x2 - x1, y2 - y1) || 1, k = Math.min(16, d / 3);
            h += `<line class="hr-link" x1="${f(x1 + ((x2 - x1) / d) * k)}" y1="${f(y1 + ((y2 - y1) / d) * k)}" x2="${f(x2 - ((x2 - x1) / d) * (k + 2))}" y2="${f(y2 - ((y2 - y1) / d) * (k + 2))}" marker-end="url(#hr-arrow)"/>`;
          });
          h = h.replace(">", `><defs><marker id="hr-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="ink-fill"/></marker></defs>`);
        }
        return h + "</svg>";
      };
      // the proof line: who is known faster than the picked horse, and the chain of results
      // that proves each, with the races that hold them lit in the table
      const chainText = () => {
        if (st.pick === null) return `לחצו על סוס ברשת, ויסומנו הסוסים שידוע שהם מהירים ממנו, החצים של התוצאות שמוכיחות את זה, והשורות של התחרויות האלה בטבלה.`;
        const x = st.pick, ch = horsesChain(st.plan.log, st.step, x), n = ch.chains.length, s = after(st.step);
        if (!s.raced.has(Math.floor(x / st.b))) return `הסוס הזה עוד לא רץ, ולכן אין עליו שום מידע.`;
        const fast = s.faster[x].size, slow = s.slower[x].size;
        const verdict = fast >= st.c ? `<span class="wv-bad">נפסל</span> : ${ltr(fast)} סוסים מהירים ממנו, ו-${ltr(st.c)} מספיקים כדי שלא יהיה בין ${ltr(st.c)} הראשונים.`
          : fast + slow === st.a - 1 ? `<span class="wv-ok">נקבע במקום ${ltr(fast + 1)}</span> : ${ltr(fast)} מהירים ממנו וכל השאר איטיים ממנו.`
          : `עדיין מועמד : רק ${ltr(fast)} ${fast === 1 ? "סוס מהיר" : "סוסים מהירים"} ממנו.`;
        const SHOW = 8, sorted = ch.chains.slice().sort((p, q) => p.links.length - q.links.length || (nm(p.y) < nm(q.y) ? -1 : 1));
        const line = (c) => `${ltr([c.y, ...c.links.map((l) => l[1])].map(nm).join(" > "))} (${c.links.length === 1 ? "תחרות" : "תחרויות"} ${ltr([...new Set(c.links.map((l) => l[2] + 1))].join(", "))})`;
        return `הסוס ${nm(x)} ${verdict} ` + (n
          ? `השרשראות : ${sorted.slice(0, SHOW).map(line).join("; ")}${n > SHOW ? `; ועוד ${ltr(n - SHOW)}` : ""}. ` +
            `כל חץ הוא תוצאה של תחרות אחת, והשרשרת מעבירה את "מהיר מ-" הלאה, ולכן אין צורך שהשניים ירוצו יחד.`
          : `אף סוס לא ידוע כמהיר ממנו.`);
      };
      const whatText = (e) => (e.what[0] === "group" ? `קבוצה ${L[e.what[1]]}` : e.what[0] === "winners" ? "המנצחים" : "המועמדים");
      const table = () => {
        if (!st.step) return `<p class="ex-note">עוד לא רצה תחרות.</p>`;
        const used = new Set(st.pick === null ? [] : horsesChain(st.plan.log, st.step, st.pick).races);
        let h = `<table class="hr-races"><thead><tr><th>תחרות</th><th>מי רץ</th><th>התוצאה</th><th>נפסלו</th><th>נקבעו</th><th>פתוחים</th></tr></thead><tbody>`;
        st.plan.log.slice(0, st.step).forEach((e, r) => {
          const gone = e.gone.map(nm).sort().join(", ") || "—";
          const placed = e.placed.slice().sort((u, v) => rankOf(u) - rankOf(v)).map((x) => `${nm(x)} מקום ${rankOf(x)}`).join(", ") || "—";
          const cls = [r === st.step - 1 ? "is-now" : "", used.has(r) ? "is-proof" : ""].filter(Boolean).join(" ");
          h += `<tr${cls ? ` class="${cls}"` : ""}><td>${r + 1}</td><td>${whatText(e)}${e.what[0] === "group" ? "" : ` (${e.horses.length})`}</td><td dir="ltr">${e.order.map(nm).join(" > ")}</td><td>${gone}</td><td>${placed}</td><td>${e.open.length}</td></tr>`;
        });
        return h + "</tbody></table>";
      };
      const draw = () => {
        const s = after(st.step), done = st.step === st.plan.log.length, R = st.plan.log.length, g = Math.ceil(st.a / st.b);
        if (!fixed) { $(".hr-a").value = st.a; $(".hr-b").value = st.b; $(".out-b").textContent = String(st.b); $(".hr-c").value = st.c; $(".out-c").textContent = String(st.c); }
        $(".hr-gridbox").innerHTML = grid(s);
        $(".hr-table").innerHTML = table();
        $(".hr-chain").innerHTML = chainText();
        $(".ex-pos").textContent = `תחרות ${st.step} מתוך ${R}`;
        $(".ex-prev").disabled = st.step === 0; $(".ex-next").disabled = done; $(".ex-end").disabled = done;
        const n = (st.c * (st.c + 1)) / 2 - 1;
        $(".hr-sum").innerHTML = `${ltr(st.a)} סוסים, ${ltr(st.b)} במסלול, ${ltr(st.c)} ראשונים : <b>${ltr(R)} תחרויות</b> (${ltr(g)} קבוצות${g > 1 ? ", המנצחים" : ""}${R > g + 1 ? `, ועוד ${ltr(R - g - 1)} על המועמדים` : ""}); מועמדי המדרגות אחרי המנצחים : ${ltr(Math.min(n, st.a - 1))}. ` +
          (done ? `הדירוג : ${ltr(st.plan.ranking.map((x, i) => `${i + 1}. ${nm(x)}`).join(", "))} ✓` : `זרע ${ltr(st.seed)}; המהירויות נסתרות${st.reveal ? ", והמתג חושף אותן" : ""}.`);
        let step;
        if (!st.step) step = `לפני התחרות הראשונה : ${ltr(st.a)} סוסים, אף אחד לא רץ, וכל סוס יכול להיות הראשון.`;
        else {
          const e = st.plan.log[st.step - 1];
          const reasons = e.gone.slice().sort((u, v) => (nm(u) < nm(v) ? -1 : 1)).map((x) => {
            const f = e.faster[x].slice().sort((u, v) => (nm(u) < nm(v) ? -1 : 1));
            return `${nm(x)} (${f.slice(0, st.c).map(nm).join(", ")}${f.length > st.c ? ` ועוד ${f.length - st.c}` : ""})`;
          });
          step = `תחרות ${ltr(st.step)}, ${whatText(e)} : ${ltr(e.order.map(nm).join(" > "))}. ` +
            (e.gone.length ? `<span class="wv-bad">נפסלו ${ltr(e.gone.length)}</span>` + (e.what[0] === "final" || e.gone.length <= 6 ? ` : ${ltr(reasons.join("; "))}` : ` : ${ltr(e.gone.map(nm).sort().join(", "))}`) + ` (בסוגריים : מהירים ידועים). ` : "אף סוס לא נפסל. ") +
            (e.placed.length ? `<span class="wv-ok">נקבעו</span> : ${ltr(e.placed.slice().sort((u, v) => rankOf(u) - rankOf(v)).map((x) => `${nm(x)} מקום ${rankOf(x)}`).join(", "))}. ` : "") +
            (done ? `<b>סיימנו אחרי ${ltr(st.step)} תחרויות.</b>` : `נשארו ${ltr(e.open.length)} מועמדים פתוחים${st.step < R ? `; התחרות הבאה : ${ltr(st.plan.log[st.step].horses.map(nm).join(", "))}` : ""}.`);
        }
        $(".hr-step").innerHTML = step;
        answer(box, done ? `${ltr(st.c)} הראשונים, לפי הסדר : ${ltr(st.plan.ranking.map(nm).join(", "))}, אחרי ${ltr(R)} תחרויות.` : null,
          st.plan.ranking.map((x) => box.querySelector(`.hr-gridbox .hr-cell[data-x="${x}"] rect`)));
      };
      let stop = () => {};
      const setParams = (a, b, c) => {
        const err = !Number.isInteger(a) || a < 2 || a > AMAX ? `מספר סוסים שלם מ-2 עד ${AMAX}` : a > b * b ? `עם ${b} במסלול, לכל היותר ${b * b} סוסים (המנצחים צריכים להיכנס לתחרות אחת)` : c > Math.min(a, b) ? "לא יותר ראשונים מסוסים במסלול" : "";
        if (!fixed) $(".hr-err").textContent = err;
        if (err) return;
        stop(); st.a = a; st.b = b; st.c = c; st.step = 0; compute(); draw();
      };
      if (!fixed) {
        $(".hr-a").addEventListener("change", () => setParams(Math.round(Number($(".hr-a").value)), st.b, st.c));
        $(".hr-a").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".hr-a").blur(); });
        $(".hr-b").addEventListener("input", () => setParams(st.a, Number($(".hr-b").value), Math.min(st.c, Number($(".hr-b").value))));
        $(".hr-c").addEventListener("input", () => setParams(st.a, st.b, Number($(".hr-c").value)));
        $(".ex-reset").addEventListener("click", () => { st.seed = S0; setParams(A0, B0, C0); });
      }
      $(".hr-show").addEventListener("change", () => { st.reveal = $(".hr-show").checked; draw(); });
      // a tap or Enter on a horse shows its chain, again hides it
      const pick = (cell, keyboard) => {
        const x = Number(cell.dataset.x);
        st.pick = st.pick === x ? null : x;
        draw();
        if (keyboard) { const again = box.querySelector(`.hr-cell[data-x="${x}"]`); if (again) again.focus(); }
      };
      $(".hr-gridbox").addEventListener("click", (e) => { const cell = e.target.closest(".hr-cell"); if (cell) pick(cell, false); });
      $(".hr-gridbox").addEventListener("keydown", (e) => {
        const cell = e.target.closest(".hr-cell");
        if (cell && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(cell, true); }
      });
      const seed = seedControls(box, $(".ex-random"), (rng, sd) => { stop(); st.seed = sd; st.step = 0; compute(); draw(); }, { seed: S0 });
      $(".ex-random").addEventListener("click", () => seed.draw());
      $(".ex-next").addEventListener("click", () => { stop(); if (st.step < st.plan.log.length) { st.step++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.step > 0) { st.step--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.step = st.plan.log.length; draw(); });
      stop = autoplay(play, speed, { step: () => { st.step++; draw(); }, done: () => st.step >= st.plan.log.length, restart: () => { st.step = 0; draw(); } });
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { horses: horsesView },
    help: {
      horses: "המהירויות מוגרלות מזרע ונסתרות, כמו בחידה. ״התחרות הבאה״ ו״הפעלה״ מריצים את התוכנית תחרות אחרי תחרות : הרשת צובעת כל סוס (נפסל, מועמד, נקבע) עם מספר המהירים הידועים ממנו, הטבלה גדלה, והשורה מתחת מסבירה מי נפסל ולמה. בתיבה הכללית קובעים a, b ו-c, ומתג החשיפה מראה את הדירוג האמיתי. לחיצה על סוס ברשת מראה בשלב ההוכחה את שרשרת התוצאות שמוכיחה מי מהיר ממנו.",
    },
    models: { horsesSpeeds, horsesPlan, horsesChain },
  });
})();
