// kinds: bridge
//   bridge                 0031        crossing times, a bridge of two or three: the Dijkstra plan (or one of the two classic plans, or the reader's own) played crossing by crossing; a toggle for the greedy rule round by round
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { f, frame, ltr, speedSel } = dvqExplorers.lib;

  // Bridge and torch (0031): Dijkstra over (who is across, torch side); a crossing of one
  // or two people from the torch's bank costs the time of the slower. Returns the least
  // time and the crossings as arrays of indices, as the page code does.
  // bridgeSolve: Dijkstra over (who is across, torch side); `cap` people fit on the bridge
  // (2 on the page, 3 in the follow-up). Groups are tried as i <= j <= k so that the
  // tie-break of the page's figure is kept.
  const bridgeSolve = (times, cap = 2) => {
    const n = times.length, everyone = (1 << n) - 1, S = 2 << n;
    const reach = new Array(S).fill(Infinity), prev = new Array(S).fill(-1), via = new Array(S).fill(0), closed = new Array(S).fill(false);
    reach[0] = 0;
    for (;;) {
      let cur = -1;
      for (let s = 0; s < S; s++) if (!closed[s] && (cur < 0 || reach[s] < reach[cur])) cur = s;
      if (cur < 0 || reach[cur] === Infinity) break;
      closed[cur] = true;
      const across = cur >> 1, side = cur & 1;
      if (across === everyone) break;
      const bank = [];
      for (let i = 0; i < n; i++) if (((across >> i) & 1) === side) bank.push(i);
      const relax = (g) => {
        const mask = g.reduce((m, i) => m | (1 << i), 0), cost = Math.max(...g.map((i) => times[i]));
        const nxt = ((across ^ mask) << 1) | (1 - side);
        if (reach[cur] + cost < reach[nxt]) { reach[nxt] = reach[cur] + cost; prev[nxt] = cur; via[nxt] = mask; }
      };
      bank.forEach((i, a) => bank.slice(a).forEach((j, b) => {
        if (cap >= 3) bank.slice(a + b).forEach((k) => relax([i, j, k]));
        else relax([i, j]);
      }));
    }
    const moves = [];
    for (let s = (everyone << 1) | 1; prev[s] >= 0; s = prev[s]) {
      const g = [];
      for (let i = 0; i < n; i++) if (via[s] & (1 << i)) g.push(i);
      moves.unshift(g);
    }
    return { time: reach[(everyone << 1) | 1], moves };
  };
  const bridgeEscort = (times) => { const s = [...times].sort((u, v) => u - v); return s.length < 3 ? s[s.length - 1] : s[0] * (s.length - 2) + s.slice(1).reduce((u, v) => u + v, 0); };
  // The two classic plans of the page as crossings (a bridge of two): the fastest escorts
  // everyone one by one; or, round after round, the two slowest cross together (the fast
  // pair goes first, the fastest brings the torch back, the slowest pair crosses, the
  // second brings it back), with three or fewer left done directly. bridgeTime replays.
  const bridgeTime = (times, moves) => moves.reduce((t, g) => t + Math.max(...g.map((i) => times[i])), 0);
  const bridgeOrder = (times) => times.map((t, i) => i).sort((u, v) => times[u] - times[v] || u - v);
  const bridgeEscortMoves = (times) => {
    const o = bridgeOrder(times), moves = [];
    if (o.length === 1) return [[o[0]]];
    o.slice(1).forEach((p, k) => { moves.push([o[0], p]); if (k < o.length - 2) moves.push([o[0]]); });
    return moves;
  };
  const bridgePairMoves = (times) => {
    const o = bridgeOrder(times), moves = [];
    let rest = o;
    while (rest.length > 3) {
      const [f, s] = rest, slow2 = rest.slice(-2);
      moves.push([f, s], [f], slow2, [s]);
      rest = rest.slice(0, -2);
    }
    if (rest.length === 3) moves.push([rest[0], rest[1]], [rest[0]], [rest[0], rest[2]]);
    else moves.push(rest);
    return moves;
  };

  // The greedy rule of the page, round by round (a bridge of two): sorted t1 <= t2 <= ...,
  // the two slowest leave each round by the cheaper of "the slow pair together"
  // (t1 + 2 t2 + tn) and "the fastest escorts both" (2 t1 + t(n-1) + tn); three left cost
  // t1 + t2 + t3, two cost t2, one costs t1.
  const bridgeGreedy = (times) => {
    const o = bridgeOrder(times), rounds = [];
    let rest = o, total = 0;
    while (rest.length > 3) {
      const t = (k) => times[rest[k]], n = rest.length;
      const pair = t(0) + 2 * t(1) + t(n - 1), escort = 2 * t(0) + t(n - 2) + t(n - 1), take = pair <= escort ? "pair" : "escort";
      total += Math.min(pair, escort);
      rounds.push({ slow: [rest[n - 2], rest[n - 1]], pair, escort, take, total });
      rest = rest.slice(0, -2);
    }
    const last = rest.length === 3 ? times[rest[0]] + times[rest[1]] + times[rest[2]] : rest.length === 2 ? times[rest[1]] : rest.length ? times[rest[0]] : 0;
    return { rounds, left: rest, last, time: total + last };
  };

  // The bridge box (0031): type the crossing times, the Dijkstra of the page runs in the
  // browser, and the crossings play one at a time on the banks figure. The times are kept
  // in hundredths of a minute, as integers, so sums and comparisons are exact (1.1 + 2.2
  // + ... as floats gave 17.599999999999998); fm() prints them. One screen: the plans
  // table (time and number of crossings) beside the greedy rule's table, the crossings of
  // the shown plan on one line that scrolls inside itself, the bridge beside its caption.
  const bridgeView = () => ({
    mount(box) {
      const NAMES = "ABCDEFGH", NB = " ";
      const defaults = box.dataset.times || "1 2 5 10";
      const PLANS = { best: "החיפוש (הקצרה ביותר)", escort: "המהיר מלווה את כולם", pair: "שני האיטיים חוצים יחד", mine: "התוכנית שלי" };
      // mine (V4): the reader's own crossings, picked from the torch's bank one at a time;
      // fails counts the finished plans that were not the best (the hint waits for the second)
      const st = { times: [], s: 0, cap: 2, plan: "best", mine: [], pick: [], fails: 0, cut: "" };
      const fm = (c) => String(c / 100);                 // hundredths -> "17.6"
      const mins = (c) => (c === 100 ? "דקה אחת" : `${ltr(fm(c))} דקות`);
      const passed = (c) => (c === 100 ? "עברה דקה אחת" : `עברו ${ltr(fm(c))} דקות`);
      box.innerHTML =
        `<div class="ex-controls"><label>הזמנים (עד שמונה) <input type="text" class="ex-times" value="${defaults}" size="22" dir="ltr" inputmode="decimal" aria-label="זמני החצייה, מופרדים ברווחים"></label>` +
        `<label>הגשר מחזיק <select class="ex-cap" aria-label="כמה אנשים הגשר מחזיק"><option value="2" selected>שניים</option><option value="3">שלושה</option></select></label>` +
        `<label>התוכנית <select class="ex-plan" aria-label="התוכנית שמוצגת">${Object.entries(PLANS).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="ex-note br-cut" role="status"></p>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="bridge-tables"><div class="bridge-plans"></div>` +
        `<div class="bridge-gwrap"><label><input type="checkbox" class="ex-greedy" checked> הכלל החמדני, סיבוב אחרי סיבוב</label><div class="bridge-greedy"></div></div></div>` +
        `<div class="bridge-line" role="region" tabindex="0" aria-label="החציות של התוכנית המוצגת, לפי הסדר"></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">החצייה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">החצייה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 1000, 400) + `<span class="ex-pos"></span></div>` +
        `<div class="ex-controls br-mine" hidden><span class="ex-title">מי חוצה עכשיו?</span><span class="br-who" role="group" aria-label="האנשים בגדה של הלפיד"></span>` +
        `<button type="button" class="md-button md-button--primary br-go">חצייה</button><button type="button" class="md-button br-undo">ביטול החצייה האחרונה</button>` +
        `<button type="button" class="md-button br-show" hidden>הצגת התוכנית הקצרה</button></div>` +
        `<div class="bridge-frame"></div><p class="bridge-caption"></p><p class="br-msg" role="status"></p>` +
        `<span class="viz-legend"><span><i class="st-cell"></i>על הגדה הקרובה</span><span><i class="st-stack"></i>חוצים עכשיו</span><span><i class="st-ok"></i>כבר על הגדה הרחוקה</span><span><i class="torch"></i>הלפיד</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), input = $(".ex-times");
      let timer = null;
      // the field -> up to eight positive times in hundredths; what was left out is said, not hidden
      const parse = () => {
        const words = input.value.split(/[\s,]+/).filter(Boolean);
        const good = words.map((w) => Math.round(Number(w) * 100)).filter((v) => Number.isFinite(v) && v > 0);
        const bad = words.length - good.length;
        st.cut = [good.length > 8 ? `נלקחו שמונת הזמנים הראשונים מתוך ${good.length}.` : "",
          bad ? (bad === 1 ? "ערך אחד שאינו מספר חיובי הושמט." : `${bad} ערכים שאינם מספרים חיוביים הושמטו.`) : ""].filter(Boolean).join(" ");
        return good.slice(0, 8);
      };
      const frameSvg = (times, across, side, moving, forward, t) => {
        const n = times.length, per = Math.max(34, Math.min(40, 170 / Math.max(n, 1)));
        // five or more people: a bank may hold two rows, so the rows sit closer (their names
        // stay clear of the bank's label) and the torch stands at the bridge's end of the bank
        const two = n > 4, y0 = two ? 54 : 60, dy = 50;
        let s = `<svg class="figure bridge-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="הגשר, שתי הגדות, הלפיד והאנשים בזמן ${fm(t)}">` +
          `<rect class="bank" x="0" y="20" width="190" height="150" rx="8"/><rect class="bank" x="450" y="20" width="190" height="150" rx="8"/>` +
          `<rect class="river" x="190" y="20" width="260" height="150"/><rect class="bridge" x="190" y="78" width="260" height="34" rx="4"/>` +
          `<text class="legend" x="95" y="160" text-anchor="middle" direction="rtl">הגדה הקרובה</text><text class="legend" x="545" y="160" text-anchor="middle" direction="rtl">הגדה הרחוקה</text>`;
        const person = (i, x, y, cls) => `<g><circle class="${cls}" cx="${f(x)}" cy="${y}" r="17"/><text class="st-text${fm(times[i]).length > 3 ? " st-sm" : ""}" x="${f(x)}" y="${y + 5}" text-anchor="middle">${fm(times[i])}</text>` +
          `<text class="st-small" x="${f(x)}" y="${y + 30}" text-anchor="middle">${NAMES[i]}</text></g>`;
        const near = [], far = [];
        for (let i = 0; i < n; i++) { if (moving.includes(i)) continue; ((across >> i) & 1 ? far : near).push(i); }
        near.forEach((i, k) => { s += person(i, (two ? 26 : 40) + per * (k % 4), y0 + dy * Math.floor(k / 4), "st-cell"); });
        far.forEach((i, k) => { s += person(i, (two ? 500 : 490) + per * (k % 4), y0 + dy * Math.floor(k / 4), "st-ok"); });
        moving.forEach((i, k) => { s += person(i, 320 - 30 * (moving.length - 1) + 60 * k, 95, "st-stack"); });
        if (moving.length) {
          const [x0, x1] = forward ? [236, 404] : [404, 236], d = forward ? 9 : -9;
          s += `<line class="ink-line" x1="${x0}" y1="128" x2="${x1}" y2="128" stroke-width="2"/><polygon class="ink-fill" points="${x1},128 ${x1 - d},123 ${x1 - d},133"/>`;
        }
        const tx = moving.length ? 320 : side === 0 ? (two ? 174 : 150) : (two ? 466 : 490), ty = moving.length ? 150 : 118;
        s += `<polygon class="torch" points="${tx},${ty - 14} ${tx + 6},${ty - 2} ${tx},${ty + 2} ${tx - 6},${ty - 2}"/><rect class="ink-fill" x="${tx - 1.5}" y="${ty + 2}" width="3" height="10"/>` +
             `<text class="legend" x="630" y="182" text-anchor="end" font-weight="700">t = ${fm(t)}</text>`;
        return s + "</svg>";
      };
      // the plans on the current times: the search (for the chosen capacity) and, on a
      // bridge of two, the two classic plans of the page
      const plansOf = () => {
        const times = st.times, best = bridgeSolve(times, st.cap);
        const out = { best, mine: { moves: st.mine, time: bridgeTime(times, st.mine) } };
        if (st.cap === 2) {
          out.escort = { moves: bridgeEscortMoves(times) }; out.escort.time = bridgeTime(times, out.escort.moves);
          out.pair = { moves: bridgePairMoves(times) }; out.pair.time = bridgeTime(times, out.pair.moves);
        }
        return out;
      };
      const acrossOf = (moves) => moves.reduce((m, g) => m ^ g.reduce((u, i) => u | (1 << i), 0), 0);
      // a crossing to the far bank (drawn on the right) as "A+B →", a return as "← A", apart by
      // dots; the crossing on the screen is marked (a tint, not a weight: the line never rewraps)
      const planLine = (moves, now) => moves.map((g, k) => `<span class="bl-x${k === now ? " is-now" : ""}">${k % 2 ? `← ${g.map((i) => NAMES[i]).join("+")}` : `${g.map((i) => NAMES[i]).join("+")} →`}</span>`).join(" · ");
      const draw = () => {
        const times = st.times;
        $(".br-cut").textContent = st.cut;
        if (!times.length) {
          $(".ex-summary").textContent = "הקלידו זמני חצייה חיוביים, מופרדים ברווחים."; $(".bridge-plans").innerHTML = ""; $(".bridge-greedy").innerHTML = "";
          $(".bridge-line").innerHTML = ""; $(".bridge-frame").innerHTML = ""; $(".bridge-caption").textContent = ""; $(".ex-pos").textContent = ""; return;
        }
        const plans = plansOf();
        if (!plans[st.plan]) { st.plan = "best"; $(".ex-plan").value = "best"; }
        const r = plans[st.plan], best = plans.best;
        st.s = Math.min(Math.max(st.s, 0), r.moves.length);
        const names = (g) => g.map((i) => `${NAMES[i]} (${fm(times[i])})`).join(" ו-");
        const people = times.length === 1 ? "אדם אחד" : `${ltr(times.length)} אנשים`, cap = st.cap === 2 ? "שניים" : "שלושה";
        // the reader's own plan hides the best one (the summary, the tables) until everyone is across
        const hide = st.plan === "mine" && acrossOf(st.mine) !== (1 << times.length) - 1;
        $(".bridge-tables").hidden = hide;
        if (hide) $(".ex-summary").innerHTML = `${people} על גשר של ${cap}${NB}: בנו תוכנית משלכם. הזמן הקצר ביותר יופיע כשכולם יעברו.`;
        else $(".ex-summary").innerHTML = `${people} על גשר של ${cap}${NB}: הזמן הקצר ביותר הוא ${mins(best.time)} ב-${ltr(best.moves.length)} חציות.` +
          (st.plan === "best" || st.plan === "mine" ? "" : ` מוצגת התוכנית "${PLANS[st.plan]}"${NB}: ${mins(r.time)}${r.time > best.time ? `, ${ltr(fm(r.time - best.time))} יותר מהקצרה ביותר` : ", בדיוק כמו הקצרה ביותר"}.`);
        $(".bridge-plans").innerHTML = st.cap === 2 && times.length >= 2
          ? `<table class="bridge-table"><thead><tr><th>התוכנית</th><th>חציות</th><th>הזמן</th></tr></thead><tbody>` +
            Object.keys(PLANS).filter((k) => k !== "mine" || st.mine.length).map((k) => `<tr${k === st.plan ? ' class="is-now"' : ""}${plans[k].time === best.time ? ' data-best="1"' : ""}><td>${PLANS[k]}</td><td>${ltr(plans[k].moves.length)}</td><td>${ltr(fm(plans[k].time))}</td></tr>`).join("") + `</tbody></table>`
          : st.cap === 3 ? `<p class="ex-note">שתי התוכניות הקלאסיות מוגדרות לגשר של שניים; לגשר של שלושה מוצג החיפוש בלבד${times.length >= 3 ? `, לעומת ${mins(bridgeSolve(times, 2).time)} על גשר של שניים` : ""}.</p>` : "";
        $(".ex-plan").querySelectorAll("option").forEach((o) => { o.disabled = !plans[o.value]; });
        if (st.plan === "mine") mineDraw(plans);
        else { $(".br-mine").hidden = true; $(".br-msg").textContent = ""; $(".br-msg").className = "br-msg"; }
        // the greedy rule: each round the two slowest leave by the cheaper of the two ways
        $(".ex-greedy").disabled = st.cap !== 2;
        const gr = st.cap === 2 && times.length >= 2 && $(".ex-greedy").checked ? bridgeGreedy(times) : null;
        const who = (g) => ltr(g.map((i) => `${NAMES[i]} (${fm(times[i])})`).join(", "));
        $(".bridge-greedy").innerHTML = st.cap !== 2 ? `<p class="ex-note">הכלל החמדני מוגדר לגשר של שניים, ולכן הוא כבוי בגשר של שלושה.</p>` : !gr ? "" :
          `<table class="bridge-table"><thead><tr><th>הסיבוב</th><th>שני האיטיים</th><th>יחד, ${ltr("t1 + 2t2 + tn")}</th><th>מלווה, ${ltr("2t1 + tn−1 + tn")}</th><th>עד עכשיו</th></tr></thead><tbody>` +
          gr.rounds.map((r, k) => `<tr><td>${k + 1}</td><td>${who(r.slow)}</td>` +
            `<td${r.take === "pair" ? ' class="is-take"' : ""}>${ltr(fm(r.pair))}</td><td${r.take === "escort" ? ' class="is-take"' : ""}>${ltr(fm(r.escort))}</td><td>${ltr(fm(r.total))}</td></tr>`).join("") +
          `<tr><td>${gr.rounds.length + 1}</td><td>${who(gr.left)}</td><td colspan="2">${gr.left.length === 3 ? "שלושה נשארו" : gr.left.length === 2 ? "שניים נשארו" : "אחד נשאר"}${NB}: ${ltr(fm(gr.last))}</td><td>${ltr(fm(gr.time))}</td></tr></tbody></table>` +
          `<p class="ex-note">בכל סיבוב שני האיטיים עוברים בזולה מבין שתי הדרכים (המודגשת). הסכום ${ltr(fm(gr.time))}${gr.time === best.time ? " שווה לזמן של החיפוש ✓" : ` לעומת ${ltr(fm(best.time))} של החיפוש`}.</p>`;
        let across = 0, side = 0, t = 0, caption = `רגע 0${NB}: כולם והלפיד על הגדה הקרובה.`;
        let moving = [], forward = true;
        for (let k = 0; k < st.s; k++) {
          const g = r.moves[k], cost = Math.max(...g.map((i) => times[i]));
          forward = side === 0; t += cost;
          if (k === st.s - 1) {
            moving = g;
            const verb = forward ? (g.length > 1 ? "חוצים קדימה" : "חוצה קדימה") : (g.length > 1 ? "חוזרים עם הלפיד" : "חוזר עם הלפיד");
            caption = `חצייה ${k + 1}${NB}: ${names(g)} ${verb}, ${mins(cost)}. ${passed(t)}.`;
          } else { across ^= g.reduce((m, i) => m | (1 << i), 0); side = 1 - side; }
        }
        const line = $(".bridge-line");
        line.innerHTML = r.moves.length ? `<span class="bl-lab">החציות${NB}:</span> ${ltr(planLine(r.moves, st.s - 1))}` : `<span class="bl-lab">החציות${NB}:</span> עוד אין.`;
        const now = line.querySelector(".is-now");       // keep the marked crossing in view inside the line's own scroll
        if (now) line.scrollTop = Math.max(0, now.offsetTop - line.offsetTop - 4);
        $(".bridge-frame").innerHTML = frameSvg(times, across, side, moving, forward, t);
        $(".bridge-caption").innerHTML = caption + (st.s === r.moves.length && st.s > 0 && acrossOf(r.moves) === (1 << times.length) - 1 ? " כולם בצד הרחוק." : "");
        $(".ex-pos").textContent = `חצייה ${st.s} מתוך ${r.moves.length}`;
        $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = st.s >= r.moves.length;
      };
      // the reader's plan: the people on the torch's bank as toggles, a crossing takes the
      // picked ones (one to cap forward, one to cap back), and the total runs against the best
      const mineDraw = (plans) => {
        const times = st.times, n = times.length, side = st.mine.length % 2;
        const across = acrossOf(st.mine);
        const done = across === (1 << n) - 1, bank = times.map((_, i) => i).filter((i) => ((across >> i) & 1) === side);
        st.pick = st.pick.filter((i) => bank.includes(i));
        $(".br-mine").hidden = false;
        $(".br-who").innerHTML = done ? "" : bank.map((i) => `<button type="button" class="md-button br-p" data-i="${i}" aria-pressed="${st.pick.includes(i)}">${NAMES[i]} (${fm(times[i])})</button>`).join("");
        $(".br-go").disabled = done || !st.pick.length || st.pick.length > st.cap;
        $(".br-go").hidden = done;
        $(".br-mine .ex-title").textContent = done ? "התוכנית הושלמה" : "מי חוצה עכשיו?";
        $(".br-go").textContent = side === 0 ? "חצייה קדימה" : "חזרה עם הלפיד";
        $(".br-undo").disabled = !st.mine.length;
        const t = plans.mine.time, best = plans.best.time, cap = st.cap === 2 ? "שניים" : "שלושה";
        const say = (cls, html) => { const m = $(".br-msg"); m.className = `br-msg ${cls}`; m.innerHTML = html; };
        if (!done) say("", st.mine.length ? `עד עכשיו ${mins(t)} ב-${ltr(st.mine.length)} חציות. ${side === 0 ? `בחרו עד ${cap} שחוצים קדימה.` : "בחרו מי מחזיר את הלפיד."}`
          : `בחרו עד ${cap} מהגדה הקרובה ולחצו "חצייה קדימה". הזמן של חצייה הוא הזמן של האיטי שבה.`);
        else if (t === best) say("wv-ok", `✓ כולם בצד השני אחרי ${mins(t)}${NB}: הזמן הקצר ביותר.`);
        else {
          // the first miss says only by how much; the hint waits for the second, and names the plan that is the best here
          const hint = st.fails < 2 || st.cap !== 2 ? "" : plans.pair.time === best ? ` רמז${NB}: נסו לשלוח את שני האיטיים יחד, כך שמשלמים על האיטי מביניהם פעם אחת.`
            : plans.escort.time === best ? ` רמז${NB}: כאן משתלם שהמהיר ביותר ילווה כל אחד ויחזיר את הלפיד.` : "";
          say("wv-bad", `כולם בצד השני אחרי ${mins(t)}, ${ltr(fm(t - best))} יותר מהקצר ביותר. אפשר לבטל חציות ולנסות שוב.${hint}`);
          $(".br-show").hidden = false;
        }
      };
      const fresh = () => { st.s = 0; st.mine = []; st.pick = []; st.fails = 0; $(".br-show").hidden = true; };
      $(".br-who").addEventListener("click", (e) => {
        const b = e.target.closest(".br-p");
        if (!b) return;
        const i = Number(b.dataset.i);
        st.pick = st.pick.includes(i) ? st.pick.filter((j) => j !== i) : st.pick.length < st.cap ? [...st.pick, i] : st.pick;
        draw();
      });
      $(".br-go").addEventListener("click", () => {
        if (!st.pick.length || st.pick.length > st.cap) return;
        st.mine.push([...st.pick].sort((u, v) => u - v)); st.pick = []; st.s = st.mine.length;
        if (acrossOf(st.mine) === (1 << st.times.length) - 1 && bridgeTime(st.times, st.mine) > bridgeSolve(st.times, st.cap).time) st.fails += 1;
        draw();
      });
      $(".br-undo").addEventListener("click", () => { st.mine.pop(); st.pick = []; st.s = st.mine.length; $(".br-show").hidden = true; draw(); });
      $(".br-show").addEventListener("click", () => { $(".br-show").hidden = true; st.plan = "best"; $(".ex-plan").value = "best"; st.s = 0; draw(); });
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => (st.times.length ? plansOf()[st.plan].moves.length : 0);
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (!total()) return;
        if (st.s >= total()) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= total()) { stop(); return; } st.s += 1; draw(); }, Number($(".ex-speed").value));
        st.s += 1; draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      input.addEventListener("change", () => { stop(); st.times = parse(); fresh(); draw(); });
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      $(".ex-greedy").addEventListener("change", draw);
      $(".ex-cap").addEventListener("change", () => { stop(); st.cap = Number($(".ex-cap").value); fresh(); draw(); });
      $(".ex-plan").addEventListener("change", () => { stop(); st.plan = $(".ex-plan").value; st.s = st.plan === "mine" ? st.mine.length : 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); input.value = defaults; st.times = parse(); st.cap = 2; st.plan = "best"; $(".ex-cap").value = "2"; $(".ex-plan").value = "best"; fresh(); draw(); });
      st.times = parse();
      draw();
    },
  });

  dvqExplorers.register({
    views: { bridge: bridgeView },
    cols: { bridge: { main: ".bridge-frame", side: ".bridge-caption, .br-msg", w: "minmax(0, 2.2fr)" } },   // the tables and the legend stay wide; the bridge beside its caption and the own plan's message
    help: {
      bridge: "זמני החצייה בשדה, קיבולת הגשר ובורר התוכנית : ״החצייה הבאה״ ו״הפעלה״ מעבירים חצייה אחרי חצייה, והטבלה משווה את שלוש התוכניות. המתג ״הכלל החמדני״ מראה בכל סיבוב את שתי הדרכים להעביר את שני האיטיים ואת הזולה מביניהן. ״התוכנית שלי״ בבורר התוכנית : בוחרים מי חוצה בכל פעם, והזמן נבדק מול הקצר ביותר בסוף.",
    },
    models: { bridgeSolve, bridgeEscort, bridgeTime, bridgeEscortMoves, bridgePairMoves, bridgeGreedy },
  });
})();
