// kinds: hourglass
//   hourglass              0018, 0019  A, B (and C) and D: the plan on a time axis and event by event (BFS or Dijkstra), the page's objective or the fewest flips
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { H, W, f, frame, ltr, speedSel } = dvqExplorers.lib;

  // Hourglasses (0018, 0019): A and B minutes, flipped only when one runs out. A plan is a
  // list of events [t, action] (action "", "A", "B" or "AB"). hourglassSolve is the BFS of
  // 0018 (measure D from time 0); hourglassInterval is the Dijkstra of 0019 (the earliest
  // measurement of D between two events). Both follow the page code line by line.
  const hourglassStep = (A, B, a, b, fa, fb) => {
    const a2 = fa ? A - a : a, b2 = fb ? B - b : b;
    const running = [a2, b2].filter((s) => s > 0);
    if (!running.length) return null;
    const w = Math.min(...running);
    return [w, Math.max(a2 - w, 0), Math.max(b2 - w, 0)];
  };
  const hourglassSolve = (A, B, D) => {
    const seen = new Set(["0,0,0"]);
    const queue = [[0, 0, 0, []]];
    for (let head = 0; head < queue.length; head++) {
      const [t, a, b, plan] = queue[head];
      if (t === D) return plan;
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r || t + r[0] > D) continue;
        const key = `${t + r[0]},${r[1]},${r[2]}`;
        if (seen.has(key)) continue;
        seen.add(key);
        queue.push([t + r[0], r[1], r[2], [...plan, [t, (fa ? "A" : "") + (fb ? "B" : "")]]]);
      }
    }
    return null;
  };
  const hourglassInterval = (A, B, D) => {
    const best = new Map([["0,0,-1", 0]]);
    const queue = [[0, 0, [0, 0, -1], null, []]];      // [t, tie, state, start, plan]
    let tie = 1;
    const pop = () => { queue.sort((u, v) => u[0] - v[0] || u[1] - v[1]); return queue.shift(); };
    while (queue.length) {
      const [t, , state, start, plan] = pop();
      const key = state.join();
      if (t > best.get(key)) continue;
      const [a, b, m] = state;
      if (m === D) return { start, plan };
      const options = [];
      if (m === -1) options.push([[a, b, 0], t, t, plan]);
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r) continue;
        const m2 = m === -1 ? -1 : m + r[0];
        if (m2 > D) continue;
        options.push([[r[1], r[2], m2], t + r[0], start, [...plan, [t, (fa ? "A" : "") + (fb ? "B" : "")]]]);
      }
      options.forEach(([s2, t2, st2, pl2]) => {
        const k2 = s2.join();
        if (!best.has(k2) || t2 < best.get(k2)) { best.set(k2, t2); queue.push([t2, tie++, s2, st2, pl2]); }
      });
    }
    return null;
  };
  // Replay a plan from rest: the events as [t, action, [a, b] on arrival, [a, b] after].
  const hourglassReplay = (A, B, plan, end) => {
    let t = 0, a = 0, b = 0;
    const events = [];
    const acts = new Map(plan.map(([w, act]) => [w, act]));
    for (;;) {
      const act = acts.has(t) ? acts.get(t) : null;
      if (act === null) { events.push([t, "", [a, b], null]); return events; }
      const r = hourglassStep(A, B, a, b, act.includes("A"), act.includes("B"));
      const fa = act.includes("A"), fb = act.includes("B");
      events.push([t, act, [a, b], [fa ? A - a : a, fb ? B - b : b]]);
      if (!r) return events;
      t += r[0]; a = r[1]; b = r[2];
      if (end !== undefined && t > end) return events;
    }
  };
  // Every D that can be measured from time 0, up to a bound.
  const hourglassReachable = (A, B, bound) => {
    const seen = new Set(["0,0,0"]), times = new Set([0]);
    const queue = [[0, 0, 0]];
    for (let head = 0; head < queue.length; head++) {
      const [t, a, b] = queue[head];
      for (const fa of [0, 1]) for (const fb of [0, 1]) {
        const r = hourglassStep(A, B, a, b, fa, fb);
        if (!r || t + r[0] > bound) continue;
        const key = `${t + r[0]},${r[1]},${r[2]}`;
        if (seen.has(key)) continue;
        seen.add(key); times.add(t + r[0]);
        queue.push([t + r[0], r[1], r[2]]);
      }
    }
    return [...times].sort((u, v) => u - v).filter((v) => v > 0);
  };

  // The follow-ups of 0018 and 0019 in one search: `sizes` is [A, B] or [A, B, C] (letters
  // A, B, C in the actions), `interval` measures between two events as 0019 does, and
  // `objective` is "events" (every event costs 1: the BFS of 0018), "time" (the earliest
  // end: the Dijkstra of 0019) or "flips" (every hourglass flipped costs 1, a wait is
  // free, equal flips settled by time). Dijkstra on a binary heap. Returns
  // { start, plan, end, events, flips, explored } or null.
  const hourglassStepN = (sizes, tops, mask) => {
    const next = tops.map((v, i) => ((mask >> i) & 1 ? sizes[i] - v : v));
    const running = next.filter((v) => v > 0);
    if (!running.length) return null;
    const w = Math.min(...running);
    return [w, next.map((v) => Math.max(v - w, 0))];
  };
  const hourglassSearch = (sizes, D, { interval = false, objective = "events" } = {}) => {
    const n = sizes.length, letters = (mask) => sizes.map((_, i) => ((mask >> i) & 1 ? "ABC"[i] : "")).join("");
    const heap = [];
    const push = (item) => { heap.push(item); let i = heap.length - 1; while (i > 0) { const j = (i - 1) >> 1; if (heap[j][0] < item[0] || (heap[j][0] === item[0] && heap[j][1] < item[1])) break; heap[i] = heap[j]; i = j; } heap[i] = item; };
    const pop = () => { const top = heap[0], last = heap.pop(); if (!heap.length) return top; let i = 0; for (;;) { let m = i; const l = 2 * i + 1, r = l + 1; const lt = (x, y) => x[0] < y[0] || (x[0] === y[0] && x[1] < y[1]); if (l < heap.length && lt(heap[l], last) && (r >= heap.length || lt(heap[l], heap[r]))) m = l; else if (r < heap.length && lt(heap[r], last)) m = r; if (m === i) break; heap[i] = heap[m]; i = m; } heap[i] = last; return top; };
    // the flips objective breaks ties by time (a flip is worth more than any wait)
    const cost = (w, mask) => (objective === "flips" ? [...Array(n)].reduce((c, _, i) => c + ((mask >> i) & 1), 0) * 10000 + w : objective === "time" ? w : 1);
    // state: tops (and m, the minutes measured so far, -1 before the start, in the interval mode)
    const best = new Map();
    let tie = 0, explored = 0;
    const start0 = { t: 0, tops: sizes.map(() => 0), m: interval ? -1 : 0, start: interval ? null : 0, plan: [] };
    const key = (st) => (interval ? `${st.tops.join()},${st.m}` : `${st.t},${st.tops.join()}`);
    best.set(key(start0), 0);
    push([0, tie++, start0]);
    while (heap.length) {
      const [c, , st] = pop();
      if (c > best.get(key(st))) continue;
      explored += 1;
      const measured = interval ? st.m : st.t;
      if (measured === D) {
        const flips = st.plan.reduce((f, [, act]) => f + act.length, 0);
        return { start: st.start, plan: st.plan, end: st.t, events: st.plan.length, flips, explored };
      }
      const options = [];
      if (interval && st.m === -1) options.push([0, { ...st, m: 0, start: st.t }]);
      for (let mask = 0; mask < 1 << n; mask++) {
        const r = hourglassStepN(sizes, st.tops, mask);
        if (!r) continue;
        const [w, tops] = r, m2 = interval ? (st.m === -1 ? -1 : st.m + w) : st.t + w;
        if ((interval ? m2 : st.t + w) > D) continue;
        options.push([cost(w, mask), { t: st.t + w, tops, m: interval ? m2 : 0, start: st.start, plan: [...st.plan, [st.t, letters(mask)]] }]);
      }
      options.forEach(([dc, s2]) => {
        const k2 = key(s2), c2 = c + dc;
        if (!best.has(k2) || c2 < best.get(k2)) { best.set(k2, c2); push([c2, tie++, s2]); }
      });
    }
    return null;
  };
  // Replay a plan on any number of hourglasses: [t, action, tops on arrival, tops after].
  const hourglassReplayN = (sizes, plan, end) => {
    let t = 0, tops = sizes.map(() => 0);
    const events = [], acts = new Map(plan.map(([w, act]) => [w, act]));
    for (;;) {
      const act = acts.has(t) ? acts.get(t) : null;
      if (act === null) { events.push([t, "", tops, null]); return events; }
      const mask = sizes.reduce((m, _, i) => m | (act.includes("ABC"[i]) ? 1 << i : 0), 0);
      const r = hourglassStepN(sizes, tops, mask);
      events.push([t, act, tops, tops.map((v, i) => ((mask >> i) & 1 ? sizes[i] - v : v))]);
      if (!r) return events;
      t += r[0]; tops = r[1];
      if (end !== undefined && t > end) return events;
    }
  };
  const hourglassReachableN = (sizes, bound) => {
    const n = sizes.length, seen = new Set([`0,${sizes.map(() => 0).join()}`]), times = new Set();
    const queue = [[0, sizes.map(() => 0)]];
    for (let head = 0; head < queue.length; head++) {
      const [t, tops] = queue[head];
      for (let mask = 0; mask < 1 << n; mask++) {
        const r = hourglassStepN(sizes, tops, mask);
        if (!r || t + r[0] > bound) continue;
        const k = `${t + r[0]},${r[1].join()}`;
        if (seen.has(k)) continue;
        seen.add(k); times.add(t + r[0]); queue.push([t + r[0], r[1]]);
      }
    }
    return [...times].sort((u, v) => u - v);
  };

  // The hourglass box (0018: measure D from 0 by BFS; 0019: the earliest interval by
  // Dijkstra): sliders for A, B and D, the plan on a time axis with the flips marked and the
  // measured window framed, and the events one at a time with the two hourglasses.
  const hourglassView = (box) => ({
    mount(box2) {
      const interval = box.dataset.mode === "interval";
      const defaults = { A: Number(box.dataset.a || 7), B: Number(box.dataset.b || 11), D: Number(box.dataset.d || (interval ? 1 : 15)), C: null, objective: "page" };
      const st = { ...defaults, s: 0 };
      // sizes: [A, B] or [A, B, C]; the page's objective ("page": fewest events on 0018,
      // the earliest end on 0019) or the fewest flips of the follow-up
      const sizes = () => (st.C === null ? [st.A, st.B] : [st.A, st.B, st.C]);
      const LET = "ABC";
      box.innerHTML =
        `<div class="ex-controls">` +
        [["A", "שעון A (דקות)", 1, 30], ["B", "שעון B (דקות)", 1, 30], ["D", "המטרה D (דקות)", 1, 60]].map(([k, label, min, max]) =>
          `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="1" value="${st[k]}" dir="ltr"><output class="out-${k}"></output></label>`).join("") +
        `<label>שעון C (דקות, ריק = בלי) <input type="number" class="ex-num ex-C" min="1" max="30" step="1" dir="ltr" placeholder="–" aria-label="שעון חול שלישי בדקות, ריק בלי שעון שלישי"></label>` +
        `<label>המטרה <select class="ex-obj" aria-label="מטרת החיפוש"><option value="page">${interval ? "הסיום המוקדם ביותר (השאלה)" : "הכי מעט אירועים (השאלה)"}</option><option value="flips">הכי מעט היפוכים</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<div class="hg-axis"></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">האירוע הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">האירוע הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1100, 400) + `<span class="ex-pos"></span></div>` +
        `<div class="hg-frame"></div><p class="hg-caption"></p><p class="ex-note hg-compare"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play");
      let timer = null, uid = 0;
      const HEB = (act) => (act ? `הופכים את ${[...act].join(" ואת ")}` : "לא הופכים כלום");
      const plus = (act) => [...act].join("+");
      // one hourglass glyph, as tools/figures/hourglass.py draws it
      const glass = (x, y, top, total, kind) => {
        const W = 30, H = 50, NECK = 3, cx = x + W / 2, mid = y + H / 2;
        uid += 1;
        const id = `exhg${uid}`;
        const bt = `${x},${y} ${x + W},${y} ${cx + NECK},${mid} ${cx - NECK},${mid}`;
        const bb = `${cx - NECK},${mid} ${cx + NECK},${mid} ${x + W},${y + H} ${x},${y + H}`;
        const th = (H / 2) * top / total, bh = (H / 2) * (total - top) / total;
        let s = `<clipPath id="${id}t"><polygon points="${bt}"/></clipPath><clipPath id="${id}b"><polygon points="${bb}"/></clipPath>`;
        if (top) s += `<rect class="sand-${kind}" clip-path="url(#${id}t)" x="${x}" y="${f(mid - th)}" width="${W}" height="${f(th)}"/>` +
                      `<line class="stream-${kind}" x1="${cx}" y1="${mid}" x2="${cx}" y2="${f(y + H - bh - 1)}"/>`;
        if (total - top) s += `<rect class="sand-${kind}" clip-path="url(#${id}b)" x="${x}" y="${f(y + H - bh)}" width="${W}" height="${f(bh)}"/>`;
        s += `<polygon class="glass" points="${bt}"/><polygon class="glass" points="${bb}"/>` +
             `<line class="frame" x1="${x - 4}" y1="${y}" x2="${x + W + 4}" y2="${y}"/><line class="frame" x1="${x - 4}" y1="${y + H}" x2="${x + W + 4}" y2="${y + H}"/>` +
             `<text class="tick" x="${x + W + 7}" y="${y + 12}">${top}</text><text class="tick" x="${x + W + 7}" y="${y + H - 2}">${total - top}</text>` +
             `<text class="legend" x="${cx}" y="${y + H + 15}" text-anchor="middle">${kind.toUpperCase()}</text>`;
        return s;
      };
      const group = (x, y, tops) => tops.map((v, i) => glass(x + 64 * i, y, v, sizes()[i], "abc"[i])).join("");
      const frameSvg = (ev, measuring, verdict) => {
        const [t, act, before, after] = ev, cy = 12 + 25, n = sizes().length, gw = 64 * (n - 1) + 30;
        const left = 92 - (n - 2) * 40, ax0 = left + gw + 22, ax1 = ax0 + 84, right = ax1 + 30, W = right + gw + 30;
        let s = `<svg class="figure hourglass-fig" viewBox="0 0 ${W} 92" style="max-width:${(W / 16).toFixed(0)}rem" role="img" aria-label="אירוע ברגע ${t}">`;
        if (measuring) s += `<rect class="measure" x="2" y="2" width="${W - 4}" height="88" rx="6"/>`;
        s += `<text class="legend" x="10" y="${cy - 4}" font-weight="700">t = ${t}</text><text class="tick" x="10" y="${cy + 14}">${verdict.event}</text>` + group(left, 12, before);
        if (after === null) s += `<text class="legend" x="${ax0 + 4}" y="${cy + 5}" font-weight="700">${verdict.text}</text>`;
        else s += `<line class="ink-line" x1="${ax0}" y1="${cy}" x2="${ax1}" y2="${cy}" stroke-width="1.5"/><polygon class="ink-fill" points="${ax1 + 6},${cy} ${ax1 - 2},${cy - 4} ${ax1 - 2},${cy + 4}"/>` +
                  `<text class="legend" x="${(ax0 + ax1) / 2}" y="${cy - 8}" text-anchor="middle">${verdict.text}</text>` + group(right, 12, after);
        return s + "</svg>";
      };
      const axisSvg = (events, start, end) => {
        const w = 640, x0 = 30, x1 = 610, y = 40, last = Math.max(end, 1);
        const X = (t) => x0 + (t / last) * (x1 - x0);
        let s = `<svg class="perf-chart hg-live" viewBox="0 0 ${w} 78" role="img" aria-label="ציר הזמן של התוכנית : האירועים, ההיפוכים וחלון המדידה">`;
        if (start !== null) s += `<rect class="measure" x="${f(X(start))}" y="${y - 22}" width="${f(X(end) - X(start))}" height="44" rx="4"/>`;
        s += `<line class="axis" x1="${x0}" x2="${x1}" y1="${y}" y2="${y}"/>`;
        events.forEach(([t, act], i) => {
          const cur = i === st.s;
          s += `<line class="${cur ? "s2-line" : "ink-line"}" x1="${f(X(t))}" x2="${f(X(t))}" y1="${y - 10}" y2="${y + 10}" stroke-width="${cur ? 3 : 1.5}"/>` +
               `<text class="tick" x="${f(X(t))}" y="${y + 26}" text-anchor="middle">${t}</text>` +
               (act ? `<text class="legend" x="${f(X(t))}" y="${y - 14}" text-anchor="middle" style="font-size:11px">${plus(act)}</text>` : "");
        });
        return s + "</svg>";
      };
      // the page's code for two hourglasses and the page's objective; the general search otherwise
      const solveFor = (objective) => {
        const sz = sizes();
        if (objective === "page" && sz.length === 2) {
          let res;
          if (interval) { const r = hourglassInterval(st.A, st.B, st.D); res = r ? { start: r.start, plan: r.plan, end: r.start + st.D } : null; }
          else { const plan = hourglassSolve(st.A, st.B, st.D); res = plan ? { start: 0, plan, end: st.D } : null; }
          if (res) { res.events = res.plan.length; res.flips = res.plan.reduce((c, [, act]) => c + act.length, 0); res.explored = null; }
          return res;
        }
        return hourglassSearch(sz, st.D, { interval, objective: objective === "page" ? (interval ? "time" : "events") : "flips" });
      };
      const solve = () => solveFor(st.objective);
      const replay = (res) => hourglassReplayN(sizes(), res.plan, res.end);
      const reach = () => hourglassReachableN(sizes(), 60);
      const draw = () => {
        ["A", "B", "D"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); });
        const res = solve(), sz = sizes(), names = sz.map((v, i) => `${LET[i]} = ${v}`);
        const sizesText = sz.length === 2 ? `${ltr(st.A)} ו-${ltr(st.B)}` : `${ltr(st.A)}, ${ltr(st.B)} ו-${ltr(st.C)}`;
        const summary = $(".ex-summary");
        if (!res) {
          const g = (u, v) => (v ? g(v, u % v) : u), gAll = sz.reduce(g);
          st.s = 0;
          summary.innerHTML = `עם שעונים של ${sizesText} דקות אי אפשר למדוד ${ltr(st.D)} דקות${interval ? "" : " מרגע 0"}` +
            (st.D % gAll ? ` : ‏${ltr(st.D)} איננו כפולה של ${ltr(`gcd(${sz.join(", ")}) = ${gAll}`)}.` : ".") +
            (interval ? "" : ` מרגע 0 אפשר למדוד : ${ltr(reach().join(", "))} (עד 60).`);
          $(".hg-axis").innerHTML = ""; $(".hg-frame").innerHTML = ""; $(".hg-caption").textContent = ""; $(".ex-pos").textContent = ""; $(".hg-compare").textContent = "";
          $(".ex-prev").disabled = $(".ex-next").disabled = true;
          return;
        }
        const events = replay(res);
        st.s = Math.min(Math.max(st.s, 0), events.length - 1);
        const flips = res.plan.map(([t, act]) => `${ltr(t)}: ${HEB(act)}`).join("; ");
        summary.innerHTML = (interval ? `${st.objective === "page" ? "המדידה שמסתיימת הכי מוקדם" : "המדידה עם הכי מעט היפוכים"} : מרגע ${ltr(res.start)} עד רגע ${ltr(res.end)}, ‏${ltr(`${res.end} − ${res.start} = ${st.D}`)}. ` : `מודדים ${ltr(st.D)} דקות מרגע 0 ב-${ltr(events.length - 1)} אירועים${st.objective === "page" ? "" : ` ו-${ltr(res.flips)} היפוכים`}. `) +
          `התוכנית : ${flips}.` + (interval ? "" : ` מרגע 0 אפשר למדוד גם : ${ltr(reach().filter((v) => v !== st.D).slice(0, 12).join(", "))}, ...`);
        // the other objective, for comparison
        const other = solveFor(st.objective === "page" ? "flips" : "page");
        const describe = (r) => (interval ? `מסתיימת ברגע ${ltr(r.end)}, ${ltr(r.events)} אירועים ו-${ltr(r.flips)} היפוכים` : `${ltr(r.events)} אירועים ו-${ltr(r.flips)} היפוכים`);
        $(".hg-compare").innerHTML = `התוכנית הזו : ${describe(res)}. ` +
          (other ? `במטרה האחרת (${st.objective === "page" ? "הכי מעט היפוכים" : interval ? "הסיום המוקדם ביותר" : "הכי מעט אירועים"}) : ${describe(other)}${other.flips === res.flips && other.events === res.events && other.end === res.end ? ", אותו דבר" : ""}.` : "") +
          (res.explored !== null ? ` החיפוש בדק ${ltr(res.explored)} מצבים${sz.length === 3 ? " (עם שעון שלישי: 8 אפשרויות בכל אירוע)" : ""}.` : "");
        $(".hg-axis").innerHTML = axisSvg(events, interval ? res.start : null, res.end);
        const ev = events[st.s], [t, act, before, after] = ev;
        // which hourglasses ran out: those whose sand on top after the previous action equals the wait
        const prevEv = st.s > 0 ? events[st.s - 1] : null;
        const out = [];
        if (prevEv) { const w = t - prevEv[0]; prevEv[3].forEach((v, i) => { if (v === w) out.push(LET[i]); }); }
        const what = st.s === 0 ? "start" : `${out.join(" + ")} run${out.length === 1 ? "s" : ""} out`;
        const ran = st.s === 0 ? "התחלה" : out.length > 1 ? `שעונים ${out.join(" ו-")} נגמרים` : `שעון ${out[0]} נגמר`;
        const done = st.s === events.length - 1;
        const flip = act ? `flip ${[...act].join(" + ")}` : "";
        let verdict;
        if (done) verdict = { event: what, text: interval ? `STOP ✓ ${res.end} − ${res.start} = ${st.D}` : `✓ D = ${st.D}` };
        else if (interval && t === res.start) verdict = { event: what, text: flip ? `START, ${flip}` : "START" };
        else verdict = { event: what, text: flip || "wait" };
        $(".hg-frame").innerHTML = frameSvg(ev, interval && t >= res.start, verdict);
        const tops = (arr) => ltr(arr.map((v, i) => `${LET[i]} = ${v}`).join(", "));
        $(".hg-caption").innerHTML = `רגע ${ltr(t)} : ${ran}. חול למעלה : ${tops(before)}. ` +
          (done ? (interval ? `מסיימים : נמדדו ${ltr(st.D)} דקות מרגע ${ltr(res.start)}.` : `עברו בדיוק ${ltr(st.D)} דקות מרגע 0.`)
            : `${interval && t === res.start ? "מתחילים למדוד, ו" : ""}${HEB(act)}${act ? `; אחרי ההיפוך למעלה ${tops(after)}` : ""}.`);
        void names;
        $(".ex-pos").textContent = `אירוע ${st.s + 1} מתוך ${events.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const count = () => { const r = solve(); return r ? replay(r).length : 0; };
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!count()) return;
        if (st.s >= count() - 1) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= count() - 1) { stop(); return; } st.s += 1; draw(); }, Number($(".ex-speed").value));
        draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      ["A", "B", "D"].forEach((k) => $(`.ex-${k}`).addEventListener("input", () => { stop(); st[k] = Number($(`.ex-${k}`).value); st.s = 0; draw(); }));
      $(".ex-C").addEventListener("change", () => {
        const v = Math.round(Number($(".ex-C").value));
        stop(); st.C = $(".ex-C").value.trim() === "" || !Number.isFinite(v) || v < 1 ? null : Math.min(30, v); $(".ex-C").value = st.C === null ? "" : st.C; st.s = 0; draw();
      });
      $(".ex-C").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ex-C").blur(); });
      $(".ex-obj").addEventListener("change", () => { stop(); st.objective = $(".ex-obj").value; st.s = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0 }); ["A", "B", "D"].forEach((k) => { $(`.ex-${k}`).value = st[k]; }); $(".ex-C").value = ""; $(".ex-obj").value = "page"; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { hourglass: hourglassView },
    help: {
      hourglass: "A, B (ו-C) הם שעוני החול ו-D הזמן למדידה. התכנית מצוירת על ציר הזמן, ״הצעד הבא״ ו״הפעלה״ עוברים אירוע אחרי אירוע, ובורר היעד בוחר בין היעד של העמוד למספר ההפיכות הקטן ביותר.",
    },
    models: { hourglassSolve, hourglassInterval, hourglassReplay, hourglassReachable, hourglassStepN, hourglassSearch, hourglassReplayN, hourglassReachableN },
  });
})();
