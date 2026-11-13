// kinds: gasring
//   gasring                0104        gas stations on a circle (data-gas "1.2.3.4.5", data-cost "3.4.5.1.2", data-start "3"): the ring with the gas of every station and the cost of every leg, edited in two fields or picked from ready rings (the page's example, no start, sum 0 with four starts, sum 3 with more starts than the lowest level); a start picked in a select or by clicking a station, and the lap from it driven leg by leg (the tank in the middle of the ring and in a row of cells, the leg where it goes below zero in red); beside it the levels P over two laps with the window of the lap from the start, its floor, the lowest level and the good starts in green
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";
  const MINUS = "\u2212";
  const NMAX = 10, VMAX = 99;

  // --- the model, as tools/figures/q0104.py ------------------------------------------------
  // levels: P_0 = 0 and P_(k+1) = P_k + gas[k] - cost[k], the tank on arriving at station k
  // from station 0 if it could go below zero
  const gsLevels = (gas, cost) => {
    const p = [0];
    gas.forEach((g, i) => p.push(p[i] + g - cost[i]));
    return p;
  };
  // walk: the tank after every leg of the lap from s, up to and with the first below zero
  const gsWalk = (gas, cost, s) => {
    const n = gas.length, out = [];
    let tank = 0;
    for (let k = 0; k < n; k++) {
      const i = (s + k) % n;
      tank += gas[i] - cost[i];
      out.push(tank);
      if (tank < 0) break;
    }
    return out;
  };
  // good: every start whose lap never runs dry, by driving it
  const gsGood = (gas, cost) => gas.map((_, s) => s).filter((s) => {
    const w = gsWalk(gas, cost, s);
    return w.length === gas.length && w[w.length - 1] >= 0;
  });
  // part b's one pass: restart after the station where the tank went below zero
  const gsOnePass = (gas, cost) => {
    let start = 0, tank = 0, total = 0;
    gas.forEach((g, i) => {
      const d = g - cost[i];
      tank += d;
      total += d;
      if (tank < 0) { start = i + 1; tank = 0; }
    });
    return total >= 0 ? start : -1;
  };
  // "1, 2, 3", "1.2.3" or "1 2 3": 1 to NMAX whole numbers from 0 to VMAX, else null
  const gsParse = (text) => {
    const p = String(text || "").trim().split(/[\s,.;]+/).filter(Boolean);
    if (!p.length || p.length > NMAX || p.some((x) => !/^\d+$/.test(x) || Number(x) > VMAX)) return null;
    return p.map(Number);
  };
  const gsPresets = [
    ["הדוגמה", [1, 2, 3, 4, 5], [3, 4, 5, 1, 2]],
    ["אין פתרון", [2, 3, 4], [3, 4, 3]],
    ["סכום 0, ארבע תחנות", [3, 1, 2, 1, 2, 2, 1], [1, 3, 1, 2, 2, 1, 2]],
    ["סכום 3, שלוש תחנות", [1, 3, 2, 3, 4], [2, 1, 3, 2, 2]],
  ];
  const presetOf = (gas, cost) => gsPresets.findIndex(([, g, c]) => g.join() === gas.join() && c.join() === cost.join());

  // --- drawing -------------------------------------------------------------------------
  const num = (v) => (v < 0 ? `${MINUS}${-v}` : String(v));
  const f1 = (x) => x.toFixed(1);
  const list = (xs) => xs.join(", ");
  const leg = (a, b) => ltr(`${a} → ${b}`);

  // the ring: the stations clockwise from the top, the gas outside (+), the cost of the leg
  // to the next station on its arrow (−), the tank in the middle
  const RW = 360, RH = 316, CX = 180, CY = 158, R = 104;
  const ringSvg = (st, k, w, goods) => {
    const { gas, cost, start: s } = st, n = gas.length, T = w.length;
    const ang = (i) => -Math.PI / 2 + (2 * Math.PI * i) / n;
    const pt = (a, rad) => [CX + rad * Math.cos(a), CY + rad * Math.sin(a)];
    const bad = k === T && w[T - 1] < 0;
    const now = bad ? (s + k - 1) % n : (s + k) % n;
    const tank = k ? w[k - 1] : 0;
    const SR = n > 7 ? 14 : 17;                   // smaller stations leave the legs of a ring of 8 to 10 visible
    let o = `<svg class="figure gs-fig gs-live" viewBox="0 0 ${RW} ${RH}" style="max-width:320px" direction="ltr" role="group" ` +
      `aria-label="${n} תחנות על מעגל, עם כיוון השעון מלמעלה${NB}: הדלק של כל תחנה מחוץ למעגל והמחיר של כל קטע עליו. לחיצה על תחנה בוחרת אותה כתחנת ההתחלה">`;
    const gap = (SR + 5) / R;
    for (let i = 0; i < n; i++) {
      const j = (i - s + n) % n;                  // the leg's place in the lap from s
      const cls = j < k - (bad ? 1 : 0) ? " is-done" : bad && j === k - 1 ? " is-bad" : j === k - 1 ? " is-now" : "";
      const a0 = ang(i) + gap, a1 = ang(i + 1) - gap - 0.06, ae = ang(i + 1) - gap;
      const [x0, y0] = pt(a0, R), [x1, y1] = pt(a1, R), [tx0, ty0] = pt(ae, R);
      const tx = -Math.sin(ae), ty = Math.cos(ae), nx = Math.cos(ae), ny = Math.sin(ae);
      const bx = tx0 - 8 * tx, by = ty0 - 8 * ty;
      const [mx, my] = pt((ang(i) + ang(i + 1)) / 2, R - 26);
      const large = n === 1 ? 1 : 0;
      o += `<g class="gs-leg${cls}"><title>leg ${i} → ${(i + 1) % n}: costs ${cost[i]}</title>` +
        `<path d="M${f1(x0)},${f1(y0)} A${R},${R} 0 ${large} 1 ${f1(x1)},${f1(y1)}" fill="none"/>` +
        `<path class="gs-head" d="M${f1(tx0)},${f1(ty0)} L${f1(bx + 4.5 * nx)},${f1(by + 4.5 * ny)} L${f1(bx - 4.5 * nx)},${f1(by - 4.5 * ny)} Z"/>` +
        `<text class="gs-cost" x="${f1(mx)}" y="${f1(my + 4.5)}" text-anchor="middle">${num(-cost[i])}</text></g>`;
    }
    for (let i = 0; i < n; i++) {
      const [x, y] = pt(ang(i), R), [gx, gy] = pt(ang(i), R + 34);
      const cls = (goods.includes(i) ? " is-good" : "") + (i === s ? " is-start" : "") + (i === now ? " is-now" : "");
      const label = `תחנה ${i}, דלק ${gas[i]}, ומחיר ${cost[i]} לקטע הבא${goods.includes(i) ? ", תחנה טובה" : ""}${i === s ? ", תחנת ההתחלה" : ""}${NB}: בחירה כתחנת ההתחלה`;
      o += `<g class="gs-st${cls}" data-s="${i}" tabindex="0" role="button" aria-label="${label}"><title>station ${i}: gas ${gas[i]}</title>` +
        (i === s ? `<circle class="gs-ring" cx="${f1(x)}" cy="${f1(y)}" r="${SR + 5}"/>` : "") +
        `<circle cx="${f1(x)}" cy="${f1(y)}" r="${SR}"/>` +
        `<text class="gs-num" x="${f1(x)}" y="${f1(y + 5)}" text-anchor="middle">${i}</text></g>` +
        `<text class="gs-gas" x="${f1(gx)}" y="${f1(gy + 5)}" text-anchor="middle" aria-hidden="true">+${gas[i]}</text>`;   // outside the button: its name holds the gas
    }
    o += `<text class="gs-tanklab" x="${CX}" y="${CY - 10}" text-anchor="middle" direction="rtl">המכל</text>` +
      `<text class="gs-tankval${tank < 0 ? " is-neg" : ""}" x="${CX}" y="${CY + 18}" text-anchor="middle">${num(tank)}</text>`;
    return o + "</svg>";
  };

  // the levels over two laps (the second lap is the first plus S), the lap from s shaded,
  // its floor P_s dashed, the lowest level of the first lap dotted, the good starts green and
  // the point of the step ringed. One scale for every step of a ring.
  const CW = 420, CH = 226, X0 = 40, XR = 12, TOP = 24, BASE = 194;
  const chartSvg = (st, k, w, p, goods) => {
    const { start: s } = st, n = st.gas.length, S = p[n];
    const q = Array.from({ length: 2 * n + 1 }, (_, i) => p[i % n] + Math.floor(i / n) * S);
    const low = Math.min(...p.slice(0, n));
    let lo = Math.min(...q), hi = Math.max(...q);
    const span = Math.max(1, hi - lo), stepY = [1, 2, 5, 10, 20, 50, 100, 200, 500].find((t) => span / t <= 6) || 1000;
    lo = Math.floor(lo / stepY) * stepY - (lo % stepY === 0 ? stepY / 2 : 0);
    hi = Math.ceil(hi / stepY) * stepY + (hi % stepY === 0 ? stepY / 2 : 0);
    const X = (i) => X0 + 8 + (i / (2 * n)) * (CW - X0 - XR - 16);
    const Y = (v) => BASE - ((v - lo) / (hi - lo)) * (BASE - TOP);
    const bad = k === w.length && w[w.length - 1] < 0;
    let o = `<svg class="perf-chart gs-chart gs-live" viewBox="0 0 ${CW} ${CH}" role="img" ` +
      `aria-label="הרמות לאורך שני סיבובים, מתחנה 0${NB}: הרמה של תחנה ${s} היא ${num(p[s])}, והנמוכה בסיבוב הראשון ${num(low)}">`;
    o += `<rect class="gs-win" x="${f1(X(s) - 7)}" y="${TOP - 6}" width="${f1(X(s + n) - X(s) + 14)}" height="${BASE - TOP + 6}" rx="4"/>`;
    for (let v = Math.ceil(lo / stepY) * stepY; v <= hi; v += stepY) {
      o += `<line class="grid" x1="${X0}" x2="${CW - XR}" y1="${f1(Y(v))}" y2="${f1(Y(v))}"/>` +
        `<text class="tick" x="${X0 - 6}" y="${f1(Y(v) + 4)}" text-anchor="end">${num(v)}</text>`;
    }
    o += `<line class="gs-lap" x1="${f1(X(n))}" x2="${f1(X(n))}" y1="${TOP - 8}" y2="${BASE}"/>`;
    o += `<line class="gs-low" x1="${X0}" x2="${CW - XR}" y1="${f1(Y(low))}" y2="${f1(Y(low))}"/>`;
    o += `<line class="gs-floor" x1="${f1(X(s))}" x2="${f1(X(s + n))}" y1="${f1(Y(p[s]))}" y2="${f1(Y(p[s]))}"/>`;
    o += `<path class="gs-line" d="${q.map((v, i) => `${i ? "L" : "M"}${f1(X(i))},${f1(Y(v))}`).join(" ")}" fill="none"/>`;
    if (k) o += `<path class="gs-drive${bad ? " is-bad" : ""}" d="${q.slice(s, s + k + 1).map((v, i) => `${i ? "L" : "M"}${f1(X(s + i))},${f1(Y(v))}`).join(" ")}" fill="none"/>`;
    q.forEach((v, i) => {
      const t = i % n, first = i < n;
      let cls = "gs-pt";
      if (first && goods.includes(t)) cls += " is-good";
      if (first && p[t] === low) cls += " is-min";
      const inLap = i >= s && i <= s + k;
      if (inLap && v < p[s]) cls += " is-bad";
      if (i === s + k) cls += " is-now";
      o += `<circle class="${cls}" cx="${f1(X(i))}" cy="${f1(Y(v))}" r="${cls.includes("is-now") ? 6.5 : cls.includes("is-good") ? 5.5 : 4}"><title>level ${num(v)} before station ${t}${first ? "" : ", second lap"}</title></circle>`;
      if (inLap) o += `<text class="gs-val" x="${f1(X(i))}" y="${f1(Y(v) - 10)}" text-anchor="middle">${num(v - p[s])}</text>`;
      if (n <= 6 || i % 2 === 0) o += `<text class="tick" x="${f1(X(i))}" y="${BASE + 18}" text-anchor="middle">${t}</text>`;
    });
    return o + `<line class="axis" x1="${X0}" x2="${CW - XR}" y1="${BASE}" y2="${BASE}"/></svg>`;
  };

  // the tank after every leg, in the order of the lap, read from the left
  const tankRow = (st, k, w) => {
    const { start: s } = st, n = st.gas.length;
    let o = `<div class="gs-tank" dir="ltr" style="grid-template-columns:repeat(${n}, minmax(0, 1fr))" role="group" aria-label="המכל אחרי כל קטע, לפי סדר הנסיעה">`;
    for (let j = 0; j < n; j++) {
      const a = (s + j) % n, b = (s + j + 1) % n, seen = j < k;
      const cls = seen ? (w[j] < 0 ? " is-neg" : j === k - 1 ? " is-now" : " is-done") : j >= w.length ? " is-off" : "";
      o += `<span class="gs-cell${cls}"><small>${a}→${b}</small><b>${seen ? num(w[j]) : "\u00b7"}</b></span>`;
    }
    return o + "</div>";
  };

  const ringView = () => ({
    mount(box) {
      const read = (v) => gsParse(String(v || "").split(".").join(", "));
      const g0 = read(box.dataset.gas), c0 = read(box.dataset.cost);
      const ok0 = g0 && c0 && g0.length === c0.length;
      const init = { gas: ok0 ? g0 : gsPresets[0][1].slice(), cost: ok0 ? c0 : gsPresets[0][2].slice() };
      const s0 = Number(box.dataset.start);
      init.start = Number.isInteger(s0) && s0 >= 0 && s0 < init.gas.length ? s0 : 0;
      const st = { gas: init.gas.slice(), cost: init.cost.slice(), start: init.start, k: 0, msg: "", err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הטבעת <select class="gs-preset" aria-label="איזו טבעת">${gsPresets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        `<label>הדלק <input type="text" class="gs-gasf" dir="ltr" spellcheck="false" autocomplete="off" aria-label="הדלק בכל תחנה, מתחנה 0, למשל 1, 2, 3"></label>` +
        `<label>המחיר <input type="text" class="gs-costf" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המחיר של כל קטע, מתחנה 0 לתחנה 1 וכן הלאה"></label>` +
        `<label>ההתחלה <select class="gs-start" aria-label="תחנת ההתחלה"></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary gs-sum" aria-live="polite"></p>` +
        `<div class="gs-wrap gs-ringwrap" data-edits></div>` +
        `<div class="gs-wrap gs-chartwrap"></div>` +
        `<div class="gs-tankwrap"><p class="gs-tankhead">המכל אחרי כל קטע, לפי סדר הנסיעה משמאל לימין${NB}:</p><div class="gs-tankrow"></div></div>` +
        `<p class="gs-note"></p>` +
        `<span class="viz-legend"><span><i class="gs-key-good"></i>תחנה טובה</span><span><i class="gs-key-start"></i>ההתחלה</span>` +
        `<span><i class="gs-key-now"></i>המכונית</span><span><i class="gs-key-done"></i>קטע שנסעו בו</span>` +
        `<span><i class="gs-key-bad"></i>המכל מתחת ל-0</span><span><i class="gs-key-line"></i>הרמה P</span>` +
        `<span><i class="gs-key-win"></i>הסיבוב מההתחלה</span><span><i class="gs-key-floor"></i>הרמה של ההתחלה</span>` +
        `<span><i class="gs-key-low"></i>הרמה הנמוכה</span></span>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), wrap = $(".gs-ringwrap");
      const syncFields = () => {
        const i = presetOf(st.gas, st.cost);
        $(".gs-preset").value = i < 0 ? "custom" : String(i);
        $(".gs-gasf").value = list(st.gas);
        $(".gs-costf").value = list(st.cost);
        const sel = $(".gs-start");
        if (sel.options.length !== st.gas.length) sel.innerHTML = st.gas.map((_, s) => `<option value="${s}">${s}</option>`).join("");
        sel.value = String(st.start);
      };
      const draw = () => {
        const { gas, cost, start: s } = st, n = gas.length;
        const w = gsWalk(gas, cost, s), T = w.length, p = gsLevels(gas, cost), S = p[n], goods = gsGood(gas, cost);
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, done = k === T, bad = w[T - 1] < 0;
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const had = wrap.contains(document.activeElement) ? Number(document.activeElement.dataset && document.activeElement.dataset.s) : null;
        wrap.innerHTML = ringSvg(st, k, w, goods);
        if (had !== null && Number.isInteger(had)) { const g = wrap.querySelector(`[data-s="${had}"]`); if (g) g.focus(); }
        $(".gs-chartwrap").innerHTML = chartSvg(st, k, w, p, goods);
        $(".gs-tankrow").innerHTML = tankRow(st, k, w);
        const goodTxt = goods.length ? `${goods.length === 1 ? "התחנה הטובה" : "התחנות הטובות"}${NB}: ${list(goods)}` : "אין תחנה טובה";
        let sum, note, ans = null, marks = [];
        if (!k) {
          sum = `יוצאים מתחנה ${s} עם מכל ריק. ${n} תחנות, הסכום ${ltr(`S = ${num(S)}`)}. ${goodTxt}.`;
          note = st.err ? `<span class="gs-err">${st.err}</span>` : st.msg ||
            `כל צעד הוא קטע אחד${NB}: מקבלים את הדלק של התחנה ומשלמים את המחיר של הקטע לתחנה הבאה. בגרף המכל הוא הגובה מעל הרמה של תחנה ${s}, ${ltr(`P<sub>${s}</sub> = ${num(p[s])}`)}.`;
        } else {
          const a = (s + k - 1) % n, b = (s + k) % n, before = k > 1 ? w[k - 2] : 0, t = w[k - 1];
          sum = `קטע ${k}, ${leg(a, b)}${NB}: ${ltr(`${num(before)} + ${gas[a]} − ${cost[a]} = ${num(t)}`)}.`;
          if (t < 0) {
            sum += " המכל מתחת ל-0.";
            note = `נתקעים בקטע ${leg(a, b)}. לפי סעיף ב גם אף תחנה מ-${s} עד ${a} לא טובה${NB}: מגיעים אליה מ-${s} עם מכל לא שלילי, וממנה נתקעים לכל המאוחר כאן. ` +
              (S < 0 ? `הסכום ${ltr(num(S))} שלילי, ולכן אין תחנה טובה בכלל.` : `ממשיכים לחפש מ-${(a + 1) % n}.`);
            ans = `מתחנה ${s} נתקעים בקטע ${leg(a, b)}. ${goodTxt}.`;
            marks = goods.length ? ".gs-ringwrap .gs-st.is-good > circle:not(.gs-ring)" : ".gs-ringwrap .gs-leg.is-bad path:not(.gs-head)";
          } else if (k === n) {
            note = `השלמתם סיבוב, והמכל לא ירד מתחת ל-0. בסוף נשאר הסכום ${ltr(`S = ${num(S)}`)}, ובגרף אף נקודה של הסיבוב לא מתחת לרמה של ${s}.`;
            ans = `מתחנה ${s} משלימים סיבוב. ${goodTxt}.`;
            marks = ".gs-ringwrap .gs-st.is-good > circle:not(.gs-ring)";
          } else {
            note = `בגרף${NB}: הנקודה ${ltr(`${num(p[(s + k) % n] + (s + k >= n ? S : 0))} − ${num(p[s])} = ${num(t)}`)} מעל הרמה של תחנה ${s}. ` +
              (t === 0 ? "המכל ריק, אבל לא שלילי." : `נשארו ${n - k} ${n - k === 1 ? "קטע" : "קטעים"}.`);
          }
        }
        $(".gs-sum").innerHTML = sum;
        $(".gs-note").innerHTML = note;
        answer(box, done ? ans : null, marks);
      };
      const total = () => gsWalk(st.gas, st.cost, st.start).length;
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= total(), restart: () => { st.k = 0; draw(); } });
      const restart = () => { stop(); st.k = 0; draw(); };
      const setRing = (gas, cost, msg = "") => {
        st.gas = gas; st.cost = cost; st.err = ""; st.msg = msg;
        if (st.start >= gas.length) st.start = 0;
        syncFields(); restart();
      };
      $(".gs-preset").addEventListener("change", () => {
        const pr = gsPresets[Number($(".gs-preset").value)];
        if (!pr || $(".gs-preset").value === "custom") { syncFields(); return; }
        st.start = 0;
        setRing(pr[1].slice(), pr[2].slice());
      });
      // a field with another number of values changes the number of stations: the other
      // field is cut, or padded with zeros (said in the note)
      const field = (which) => () => {
        const v = gsParse($(which === "gas" ? ".gs-gasf" : ".gs-costf").value);
        if (!v) {
          st.err = `צריך בין 1 ל-${NMAX} מספרים שלמים מ-0 עד ${VMAX}, מופרדים בפסיקים, אחד לכל תחנה מתחנה 0.`;
          st.msg = ""; stop(); st.k = 0; draw(); return;
        }
        const other = (which === "gas" ? st.cost : st.gas).slice(0, v.length);
        const pad = v.length - other.length;
        while (other.length < v.length) other.push(0);
        const msg = pad > 0 ? `נוספו ${pad === 1 ? "תחנה" : `${pad} תחנות`}, ${which === "gas" ? "המחיר" : "הדלק"} שלהן 0${NB}: אפשר לשנות אותו בשדה השני.` : "";
        if (which === "gas") setRing(v, other, msg); else setRing(other, v, msg);
      };
      $(".gs-gasf").addEventListener("change", field("gas"));
      $(".gs-costf").addEventListener("change", field("cost"));
      $(".gs-start").addEventListener("change", () => {
        const s = Number($(".gs-start").value);
        if (Number.isInteger(s) && s >= 0 && s < st.gas.length) st.start = s;
        st.msg = ""; st.err = ""; restart();
      });
      const pick = (s) => { st.start = s; st.msg = ""; st.err = ""; $(".gs-start").value = String(s); restart(); };
      wrap.addEventListener("click", (ev) => { const g = ev.target.closest(".gs-st[data-s]"); if (g) pick(Number(g.dataset.s)); });
      wrap.addEventListener("keydown", (ev) => {
        const g = ev.target.closest(".gs-st[data-s]");
        if (g && (ev.key === "Enter" || ev.key === " ")) { ev.preventDefault(); pick(Number(g.dataset.s)); }
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { gas: init.gas.slice(), cost: init.cost.slice(), start: init.start, msg: "", err: "" });
        syncFields(); restart();
      });
      syncFields();
      draw();
    },
  });

  dvqExplorers.register({
    views: { gasring: ringView },
    help: {
      gasring: "בוחרים טבעת או כותבים בשדות את הדלק של כל תחנה ואת המחיר של כל קטע, מתחנה 0 (עד 10 תחנות). את ההתחלה בוחרים בשדה או בלחיצה על תחנה. כל צעד הוא קטע אחד : המכל באמצע הטבעת ובשורה שמתחת לגרף, וקטע שבו הוא יורד מתחת ל-0 באדום. בגרף המכל הוא הגובה של הנקודה מעל הרמה של ההתחלה, והתחנות הטובות ירוקות.",
    },
    cols: { gasring: { main: ".gs-ringwrap, .viz-legend", side: ".gs-chartwrap, .gs-tankwrap, .gs-note", w: "minmax(0, 1fr)" } },   // the ring and the legend beside the levels, the tank and the step's note
    models: { gsLevels, gsWalk, gsGood, gsOnePass, gsParse, gsPresets },
  });
})();
