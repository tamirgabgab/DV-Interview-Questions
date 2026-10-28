// kinds: josephus
//   josephus               0016        sliders N and L (2 to 6), and the circle played step by step; the survivor chart with the zero points; a seat lookup, N up to a million; the proof panel: the new labels after every step and a full round
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, f, frame, ltr } = dvqExplorers.lib;

  const josephusZero = (n, L) => {
    let m = 1 + ((n - 1) % (L - 1));
    while (m * L <= n) m *= L;
    return m;
  };
  const josephusFormula = (n, L) => (L * (n - josephusZero(n, L))) / (L - 1);
  // The elimination step by step: [who stays, [who leave]] per step, and the survivor.
  const josephusSteps = (n, L) => {
    const circle = Array.from({ length: n }, (_, i) => i), steps = [];
    let i = 0;
    while (circle.length > 1) {
      const stays = circle[i], leave = [];
      const count = Math.min(L - 1, circle.length - 1);
      for (let s = 0; s < count; s++) {
        const j = (i + 1) % circle.length;
        leave.push(circle.splice(j, 1)[0]);
        if (j < i) i -= 1;
      }
      steps.push([stays, leave]);
      i = (i + 1) % circle.length;
    }
    return { steps, survivor: circle[0] };
  };

  // The renumbering of the proof: after `s` steps, the people left in counting order from
  // the next one who stays. The new label is the position in that order, so the survivor's
  // new label is the survivor of the smaller circle.
  const josephusRenumber = (n, L, s) => {
    const circle = Array.from({ length: n }, (_, i) => i);
    let i = 0;
    for (let k = 0; k < s && circle.length > 1; k++) {
      const count = Math.min(L - 1, circle.length - 1);
      for (let c = 0; c < count; c++) {
        const j = (i + 1) % circle.length;
        circle.splice(j, 1);
        if (j < i) i -= 1;
      }
      i = (i + 1) % circle.length;
    }
    return circle.slice(i).concat(circle.slice(0, i));
  };

  // The survivor alone, in O(n) with a circular linked list (N up to a million).
  const josephusSurvivor = (n, L) => {
    if (n === 1) return 0;
    const next = new Int32Array(n);
    for (let i = 0; i < n; i++) next[i] = (i + 1) % n;
    let cur = 0, left = n;                          // cur stays in this step
    while (left > 1) {
      const count = Math.min(L - 1, left - 1);
      for (let s = 0; s < count; s++) { next[cur] = next[next[cur]]; left -= 1; }   // the one after cur leaves
      cur = next[cur];
    }
    return cur;
  };
  // The reverse lookup: the first `count` circle sizes N (up to `limit`) in which seat s
  // survives, by the closed form.
  const josephusSeats = (s, L, count = 5, limit = 1000000) => {
    const out = [];
    if (s % L !== 0) return out;                    // F_L is always a multiple of L
    for (let n = 1; n <= limit && out.length < count; n++) if (josephusFormula(n, L) === s) out.push(n);
    return out;
  };

  // The Josephus box (0016): sliders for N and L (one stays, L - 1 leave), and a circle
  // that plays the elimination step by step or at a chosen speed; the survivor can be
  // highlighted from the start, the people who left are listed in order, and the survivor
  // chart stays, with the zero points and the seat lookup's circles ringed.
  const josephusView = (box) => ({
    mount(box2) {
      const nmax = Number(box.dataset.nmax || 64), lmax = Number(box.dataset.lmax || 6), NBIG = 1000000, NCIRCLE = 128;
      const defaults = { n: Number(box.dataset.n || 20), l: Number(box.dataset.l || 2) };
      const st = { ...defaults, s: 0, seat: null };
      const runFast = (n) => josephusSurvivor(n, st.l);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מספר האנשים N</span><input type="range" class="ex-n" min="1" max="${nmax}" step="1" value="${st.n}" dir="ltr"><output class="out-n"></output>` +
        `<input type="number" class="ex-num ex-nbig" min="1" max="${NBIG}" step="1" value="${st.n}" dir="ltr" aria-label="מספר האנשים, עד מיליון"></label>` +
        `<label><span>הכלל ${ltr("L")} : אחד נשאר, ${ltr("L − 1")} יוצאים</span><input type="range" class="ex-l" min="2" max="${lmax}" step="1" value="${st.l}" dir="ltr"><output class="out-l"></output></label>` +
        `<label><input type="checkbox" class="ex-mark" checked> להדגיש את השורד מההתחלה</label>` +
        `<label>המושב <input type="number" class="ex-num ex-seat" min="0" step="1" dir="ltr" placeholder="s" aria-label="מושב לחיפוש הפוך : לאילו N הוא שורד"></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1200">איטי</option><option value="500" selected>בינוני</option><option value="150">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<span class="ex-pos"></span></div>` +
        `<div class="jos-box"><div class="jos-circle" data-steady></div><div class="jos-panel"><p class="jos-now"></p><p class="jos-order"></p></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p><p class="ex-note jos-seat"></p><p class="ex-title">השורד לכל N, עם N הנבחר מודגש; נקודות שחורות הן נקודות אפס</p><div class="jos-chart"></div>` +
        `<section class="ex-proof jos-proof"><p class="ex-proof-title">שלב ההוכחה : מספור מחדש</p>` +
        `<div class="ex-controls"><label><input type="checkbox" class="ex-renum" checked> המספר החדש ליד כל מי שנשאר</label>` +
        `<button type="button" class="md-button ex-round">עד סוף הסיבוב</button></div><p class="jos-renum"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), mark = $(".ex-mark");
      let timer = null, chartFor = "";
      const circleSvg = (n, out, stays, leave, winner, renum) => {   // stays: the people who stay in this step; renum: old -> new label
        let w, R, r, small;
        if (n <= 12) [w, R, r, small] = [300, renum ? 96 : 105, 17, ""];
        else if (n <= 20) [w, R, r, small] = [300, renum ? 106 : 118, 15, ""];
        else if (n <= 40) [w, R, r, small] = [340, renum ? 130 : 140, 11, " st-sm"];
        else [w, R, r, small] = [340, 150, 7, " st-none"];
        const cx = w / 2, cy = w / 2, h = renum ? w : w - 20;   // room below for the new labels
        let s = `<svg class="figure jos-live" viewBox="0 0 ${w} ${h}" style="max-width:${(w / 16).toFixed(0)}rem" role="img" aria-label="${n} אנשים במעגל">` +
                `<circle cx="${cx}" cy="${cy}" r="${R}" fill="none" class="ink-line" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/>`;
        for (let i = 0; i < n; i++) {
          const a = -Math.PI / 2 + (2 * Math.PI * i) / n;
          const x = cx + R * Math.cos(a), y = cy + R * Math.sin(a);
          const cls = i === winner ? "st-ok" : leave.includes(i) ? "st-bad" : stays.includes(i) ? "st-stack" : out.has(i) ? "st-done" : "st-cell";
          const faded = out.has(i) && !leave.includes(i) ? ' class="st-faded"' : "";
          s += `<g${faded}><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${r}"><title>אדם ${i}</title></circle>`;
          if (small !== " st-none") s += `<text class="st-text${small}" x="${f(x)}" y="${f(y + (small ? 4 : 5))}" text-anchor="middle">${i}</text>`;
          if (out.has(i)) { const dd = Math.max(r - 3, 3); s += `<line class="pg-strike" x1="${f(x - dd)}" y1="${f(y + dd)}" x2="${f(x + dd)}" y2="${f(y - dd)}"/>`; }
          if (renum && renum.has(i)) {                       // the new label just outside the circle
            const xo = cx + (R + r + 9) * Math.cos(a), yo = cy + (R + r + 9) * Math.sin(a);
            s += `<text class="jos-new${i === winner ? " is-win" : ""}" x="${f(xo)}" y="${f(yo + 4)}" text-anchor="middle">${renum.get(i)}</text>`;
          }
          s += "</g>";
        }
        s += `<text class="st-text" x="${cx}" y="${cy + 6}" text-anchor="middle">${n - out.size}</text></svg>`;
        return s;
      };
      const chartSvg = (n, seat) => {
        const vals = Array.from({ length: nmax }, (_, i) => runFast(i + 1));
        const ymax = Math.max(nmax, 1), step = ymax > 40 ? 16 : 8, ticks = [];
        for (let v = 0; v <= ymax; v += step) ticks.push(v);
        const fr = frame("השורד לכל גודל מעגל", nmax, ymax, ticks);
        let s = fr.s;
        vals.forEach((v, i) => {
          const k = i + 1, cls = k === n ? "s2-dot" : v === 0 ? "ink-dot" : "s1-dot";
          if (seat !== null && v === seat) s += `<circle class="jos-seat-ring" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="8"/>`;
          s += `<circle class="${cls}" cx="${f(fr.cx(k))}" cy="${f(fr.Y(v))}" r="${k === n ? 6 : Math.min(4, fr.slot * 0.4).toFixed(1)}"><title>N = ${k}: ${v}</title></circle>`;
          const nearN = k !== n && Math.abs(k - n) < fr.every;   // a tick that would overlap the chosen N's
          if (k === n || (!nearN && (k % fr.every === 0 || k === 1))) s += fr.xtick(k);
        });
        return s + fr.close();
      };
      const digitsIn = (v, base) => v.toString(base);
      const people = (nums) => nums.length === 1 ? String(nums[0]) : `${nums.slice(0, -1).join(", ")} ו-${nums[nums.length - 1]}`;
      const draw = () => {
        const n = st.n, L = st.l, big = n > NCIRCLE;
        $(".out-n").textContent = String(n); $(".ex-nbig").value = n; $(".ex-n").value = Math.min(n, nmax);
        $(".out-l").textContent = String(L);
        // the circle and the steps up to NCIRCLE people; above that only the numbers
        const { steps, survivor } = big ? { steps: [], survivor: runFast(n) } : josephusSteps(n, L);
        st.s = Math.min(Math.max(st.s, 0), steps.length);
        const out = new Set();
        steps.slice(0, st.s).forEach(([, leave]) => leave.forEach((p) => out.add(p)));
        const cur = st.s > 0 ? steps[st.s - 1] : null;
        const done = st.s >= steps.length;
        const winner = done || mark.checked ? survivor : null;
        $(".jos-box").hidden = big;
        $(".jos-proof").hidden = big;
        const left = big ? [] : josephusRenumber(n, L, st.s), renum = new Map(left.map((p, k) => [p, k]));
        const showNew = $(".ex-renum").checked && st.s > 0 && n <= 40 && left.length > 1;
        $(".ex-play-row").hidden = big;
        if (!big) {
          const stays = cur ? [cur[0]] : [];
          $(".jos-circle").innerHTML = circleSvg(n, out, stays, cur ? cur[1] : [], winner, showNew ? renum : null);
          const rule = L === 2 ? "נשאר, והבא אחריו יוצא" : `נשאר, ו-${L - 1} הבאים אחריו יוצאים`;
          let round = 0, prev = null;
          steps.slice(0, Math.max(st.s, 1)).forEach(([st0]) => { if (prev === null || st0 <= prev) round += 1; prev = st0; });
          const stayText = stays.length === 1 ? `אדם ${stays[0]} נשאר` : `אנשים ${people(stays)} נשארים`;
          const leaveText = cur ? (cur[1].length === 1 ? `ואדם ${cur[1][0]} יוצא` : `ואנשים ${people(cur[1])} יוצאים`) : "";
          $(".jos-now").innerHTML = st.s === 0 ? `${n} אנשים במעגל. מתחילים מאדם 0 : הוא ${rule}. המספר במרכז הוא כמה אנשים נשארו.`
            : done && steps.length === st.s ? `צעד ${st.s} : ${stayText}, ${leaveText}. נשאר אדם ${survivor}, והוא השורד.`
            : `צעד ${st.s}, סיבוב ${round} : ${stayText}, ${leaveText}.`;
          const order = steps.slice(0, st.s).flatMap(([, leave]) => leave);
          $(".jos-order").innerHTML = order.length ? `סדר היציאה (${ltr(order.length)} מתוך ${ltr(n - 1)}) : ` +
            order.map((p, i) => `<span class="jos-chip${i >= order.length - (cur ? cur[1].length : 0) ? " is-now" : ""}">${p}</span>`).join(" ") : "עוד אף אחד לא יצא.";
          $(".ex-pos").textContent = `צעד ${st.s} מתוך ${steps.length}`;
          $(".ex-prev").disabled = st.s <= 0; $(".ex-next").disabled = done;
        } else {
          // no circle, no steps: an empty counter hides the scrubber, which would keep the
          // number of steps of the last small circle (and differ after a reload)
          $(".ex-pos").textContent = "";
        }
        answer(box, done ? `השורד הוא אדם ${ltr(survivor)}${big ? "" : `, אחרי ${ltr(steps.length)} צעדים`}.` : null, ".jos-circle circle.st-ok");
        const sim = survivor, how = big ? "בסימולציה ברשימה מקושרת" : "בסימולציה";
        const form = josephusFormula(n, L), M = josephusZero(n, L);
        const text = `עם ${ltr(`N = ${n}`)} ו-${ltr(`L = ${L}`)} השורד הוא ${sim} ${how}, והנוסחה ` +
          `${ltr(`${L}(N − M) / ${L - 1}`)} עם נקודת האפס ${ltr(`M = ${M}`)} נותנת ${form}` +
          `${sim === form ? ", אותו דבר." : ", שלא כמו בסימולציה."}` +
          (L === 2 ? ` בבינארי : ${ltr(`N = ${digitsIn(n, 2)}`)}, והשורד ${ltr(digitsIn(sim, 2))}.`
            : L === 3 ? ` בבסיס 3 : ${ltr(`N = ${digitsIn(n, 3)}`)}, ‏${ltr(`⌊N/2⌋ = ${digitsIn(Math.floor(n / 2), 3)}`)}, ‏${ltr(`⌊M/2⌋ = ${digitsIn(Math.floor(M / 2), 3)}`)}, והשורד ${ltr(digitsIn(sim, 3))}.` : "");
        $(".ex-summary").innerHTML = text + (big ? ` המעגל והצעדים מצוירים עד ${ltr(NCIRCLE)} אנשים.` : "");
        // the reverse lookup: in which circles does seat s survive
        let seatText = "";
        if (st.seat !== null) {
          const ns = josephusSeats(st.seat, L, 5);
          seatText = ns.length === 0
            ? `המושב ${ltr(st.seat)} לא שורד באף מעגל${L === 2 ? " : השורד תמיד זוגי" : ` : השורד תמיד כפולה של ${ltr(L)}`}.`
            : `המושב ${ltr(st.seat)} שורד כש-${ltr("N")} הוא ${ltr(ns.join(", "))}${ns.length === 5 ? ", …" : ""}` +
              (L === 2 ? ` (כל ${ltr("N = 2^k + s/2")} עם ${ltr("2^k > s/2")}).` : ` (כל ${ltr("N = M + s(L − 1)/L")} עם נקודת אפס ${ltr("M")} מתאימה).`) +
              (ns.some((v) => v <= nmax) ? " בגרף הם מוקפים." : "");
        }
        $(".jos-seat").innerHTML = seatText;
        // the proof panel: the circle left after st.s steps, numbered again from the next one
        // who stays, is the same game with fewer people
        if (!big) {
          const n2 = left.length, F2 = josephusSurvivor(n2, L), FN = survivor;
          let t;
          if (st.s === 0) t = `לפני הצעד הראשון המספור החדש הוא הישן. אחרי כל צעד ממספרים מחדש את מי שנשאר, מ-0 אצל הבא שנשאר, ומקבלים את אותו משחק עם פחות אנשים.`;
          else if (n2 === 1) t = `נשאר רק אדם ${ltr(FN)}, והוא השורד.`;
          else {
            t = `אחרי ${st.s === 1 ? "צעד אחד" : `${ltr(st.s)} צעדים`} נשארו ${ltr(n2)} אנשים, והספירה ממשיכה מאדם ${ltr(left[0])}. במספור החדש, מ-0 אצלו, זה המשחק של ${ltr(n2)} אנשים : ` +
              `השורד שלו הוא ${ltr(`F(${n2}) = ${F2}`)}, ובמספור הישן זה אדם ${ltr(FN)}${showNew ? ", המודגש בשני המספרים" : ""}. `;
            const step = left[1] - left[0], affine = left.every((p, k) => p === left[0] + step * k);
            if (st.s === 1 && n > L - 1) {
              t += `זה הצעד של הנסיגה : כל מספר ישן גדול מהחדש ב-${ltr(L)} (מודולו ${ltr(n)}), ולכן ` +
                `${ltr(`F(${n}) = (F(${n2}) + ${L}) mod ${n} = (${F2} + ${L}) mod ${n} = ${(F2 + L) % n}`)}.`;
            } else if (affine && step > 1) {
              t += `סיבוב שלם : נשארו רק ${ltr(`${left[0]}, ${left[0] + step}, ${left[0] + 2 * step}, …`)}, וכל מספר ישן הוא ${ltr(step)} כפול החדש${left[0] ? ` ועוד ${ltr(left[0])}` : ""}. ` +
                `לכן ${ltr(`F(${n}) = ${step} · F(${n2})${left[0] ? ` + ${left[0]}` : ""} = ${step} · ${F2}${left[0] ? ` + ${left[0]}` : ""} = ${step * F2 + left[0]}`)}.`;
            }
          }
          $(".jos-renum").innerHTML = t;
          // the end of the current round: the stayer of the next step wraps past the previous one
          $(".ex-round").disabled = st.s >= steps.length;
        }
        const key = `${n}/${L}/${st.seat}`;
        if (chartFor !== key) { chartFor = key; $(".jos-chart").innerHTML = chartSvg(n, st.seat); }
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => (st.n > NCIRCLE ? 0 : josephusSteps(st.n, st.l).steps.length);
      $(".ex-next").addEventListener("click", () => { stop(); st.s += 1; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s -= 1; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.s >= total()) st.s = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { if (st.s >= total()) { stop(); return; } st.s += 1; draw(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      mark.addEventListener("change", draw);
      $(".ex-renum").addEventListener("change", draw);
      $(".ex-round").addEventListener("click", () => {
        stop();
        const { steps } = josephusSteps(st.n, st.l);
        let k = st.s;                                    // the next step; the round goes on while the stayers rise
        while (k + 1 < steps.length && steps[k + 1][0] > steps[k][0]) k += 1;
        st.s = Math.min(k + 1, steps.length);
        draw();
      });
      $(".ex-n").addEventListener("input", () => { stop(); st.n = Number($(".ex-n").value); st.s = 0; draw(); });
      $(".ex-nbig").addEventListener("change", () => { const v = Math.round(Number($(".ex-nbig").value)); if (!Number.isFinite(v) || v < 1) { $(".ex-nbig").value = st.n; return; } stop(); st.n = Math.min(NBIG, v); st.s = 0; draw(); });
      $(".ex-seat").addEventListener("change", () => { const v = Math.round(Number($(".ex-seat").value)); stop(); st.seat = $(".ex-seat").value === "" || !Number.isFinite(v) || v < 0 ? null : v; draw(); });
      [$(".ex-nbig"), $(".ex-seat")].forEach((el) => el.addEventListener("keydown", (e) => { if (e.key === "Enter") el.blur(); }));
      $(".ex-l").addEventListener("input", () => { stop(); st.l = Number($(".ex-l").value); st.s = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, defaults, { s: 0, seat: null }); $(".ex-n").value = st.n; $(".ex-seat").value = ""; $(".ex-l").value = st.l; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { josephus: josephusView },
    help: {
      josephus: "המעגל מראה את המשחק : N ו-L (אחד נשאר, L − 1 יוצאים) בסליידרים, ״הצעד הבא״ או ״הפעלה״ מוציאים אדם אחרי אדם, השורד מודגש מהתחלה, והגרף מראה את השורד לכל N עם נקודות האפס. שדה המושב מחפש באילו מעגלים מושב שורד. בשלב ההוכחה כל מי שנשאר מקבל מספר חדש, מ-0 אצל הבא שנשאר, ו״עד סוף הסיבוב״ מראה איך סיבוב שלם מקטין את המעגל.",
    },
    models: { josephusSteps, josephusZero, josephusFormula, josephusSurvivor, josephusSeats, josephusRenumber },
  });
})();
