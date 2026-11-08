// kinds: ducci
//   ducci                  0088        differences in a circle (the numbers typed, drawn at random or taken from the presets): the circle round by round, the difference of each pair of neighbours on the edge between them (the next round's numbers), the round where the cycle starts marked, and a chart of the maximum of every round (it never rises; the rounds where every number becomes divisible by one more 2 marked)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for the
// question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 3, NMAX = 12, VMAX = 99999, CAP = 600;
  const PRESETS = [
    ["2, 6, 11, 4", "2 6 11 4"],
    ["טריבונאצ'י", "0 7 20 44"],
    ["טריבונאצ'י גדול", "0 1705 4841 10609"],
    ["שמונה מספרים", "3 1 4 1 5 9 2 6"],
    ["0, 0, 1", "0 0 1"],
    ["1 עד 5", "1 2 3 4 5"],
    ["1 בין 5 אפסים", "1 0 0 0 0 0"],
  ];

  // --- the model (tests/0088 compares it with the page's code and the generator) ------------

  const duStep = (v) => v.map((x, i) => Math.abs(x - v[(i + 1) % v.length]));
  // { tail, period, states }: the rounds before the cycle, its length, the states until it closes
  const duOrbit = (v0) => {
    const seen = new Map(), states = [];
    let v = v0.slice();
    while (!seen.has(v.join(",")) && states.length < CAP) {
      seen.set(v.join(","), states.length);
      states.push(v);
      v = duStep(v);
    }
    const k = v.join(",");
    return seen.has(k) ? { tail: seen.get(k), period: states.length - seen.get(k), states } : { tail: null, period: null, states };
  };
  // one round mod 2 on the parities kept as the bits of an n-bit number, and the power-of-2 test
  const duParityStep = (b, n) => (b ^ ((b >>> 1) | ((b & 1) << (n - 1)))) >>> 0;
  const duAlwaysZero = (n) => { let b = 1; for (let t = 0; t < n; t++) b = duParityStep(b, n); return b === 0; };
  const duParse = (text) => {
    const parts = String(text).trim().split(/[\s,]+/).filter(Boolean);
    if (parts.length < NMIN || parts.length > NMAX || !parts.every((p) => /^\d{1,5}$/.test(p))) return null;
    return parts.map(Number);
  };

  // --- the drawings --------------------------------------------------------------------------

  const CW = 300, CH = 270, CX = 150, CY = 135, CR = 98;
  const circleSvg = (v, inCycle) => {
    const n = v.length, nxt = duStep(v), big = v.some((x) => x > 999);
    const pts = v.map((_, i) => {
      const a = -Math.PI / 2 + (2 * Math.PI * i) / n;          // clockwise from the top
      return [CX + CR * Math.cos(a), CY + CR * Math.sin(a)];
    });
    const rNode = n > 8 ? 17 : 21, fs = big ? (n > 6 ? 10 : 12) : n > 8 ? 13 : 15, dfs = big ? 10 : 12;
    let s = `<svg class="figure du-fig du-live" viewBox="0 0 ${CW} ${CH}" role="img" aria-label="${n} מספרים על מעגל, בכיוון השעון מלמעלה : ${v.join(", ")}. על כל צלע ההפרש של שני השכנים, המספרים של הסיבוב הבא : ${nxt.join(", ")}">`;
    s += `<circle class="du-ring" cx="${CX}" cy="${CY}" r="${CR}"/>`;
    pts.forEach(([x1, y1], i) => {
      const [x2, y2] = pts[(i + 1) % n], mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
      const w = Math.max(24, String(nxt[i]).length * (dfs * 0.62) + 10);
      s += `<line class="du-chord" x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>`;
      s += `<rect class="du-diff-bg" x="${(mx - w / 2).toFixed(1)}" y="${(my - 10).toFixed(1)}" width="${w.toFixed(1)}" height="20" rx="5"/>`;
      s += `<text class="du-diff" x="${mx.toFixed(1)}" y="${(my + 4.5).toFixed(1)}" text-anchor="middle" style="font-size:${dfs}px">${nxt[i]}</text>`;
    });
    pts.forEach(([x, y], i) => {
      s += `<circle class="du-node${inCycle ? " is-cyc" : ""}" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="${rNode}"/>`;
      s += `<text class="du-val" x="${x.toFixed(1)}" y="${(y + fs * 0.36).toFixed(1)}" text-anchor="middle" style="font-size:${fs}px">${v[i]}</text>`;
    });
    return s + `</svg>`;
  };

  const GW = 560, GH = 170, GX0 = 58, GX1 = 548, GY0 = 14, GY1 = 140;
  const chartSvg = (orb, k) => {
    const S = orb.states, T = S.length, maxes = S.map((v) => Math.max(...v)), top = Math.max(1, maxes[0]);
    const bw = (GX1 - GX0) / T, y = (m) => GY1 - ((GY1 - GY0) * m) / top;
    let s = `<svg class="figure du-chart" viewBox="0 0 ${GW} ${GH}" role="img" aria-label="המקסימום בכל סיבוב, מ-${maxes[0]} בהתחלה. הוא אף פעם לא עולה">`;
    s += `<line class="du-axis" x1="${GX0}" y1="${GY1}" x2="${GX1}" y2="${GY1}"/>`;
    s += `<text class="du-lab" x="${GX0 - 6}" y="${GY0 + 8}" text-anchor="end">${top}</text><text class="du-lab" x="${GX0 - 6}" y="${GY1}" text-anchor="end">0</text>`;
    // the power of 2 that divides every number: a round where it grows is a halving of the game
    const twos = (v) => { const g = v.reduce((a, x) => (x ? (a ? Math.min(a, x & -x) : x & -x) : a), 0); return g; };
    S.forEach((v, t) => {
      const m = maxes[t], even = m > 0 && t > 0 && twos(v) > twos(S[t - 1]);
      const cyc = orb.tail !== null && orb.period > 1 && t >= orb.tail;
      const cls = `du-bar${cyc ? " is-cyc" : even ? " is-half" : ""}${t === k ? " is-now" : ""}`;
      const h = Math.max(m ? 1.5 : 0, GY1 - y(m));
      s += `<rect class="${cls}" x="${(GX0 + t * bw + bw * 0.12).toFixed(2)}" y="${(GY1 - h).toFixed(2)}" width="${Math.max(0.6, bw * 0.76).toFixed(2)}" height="${h.toFixed(2)}"/>`;
    });
    if (orb.tail !== null && orb.period > 1) {
      const x = GX0 + orb.tail * bw;
      s += `<line class="du-cycline" x1="${x.toFixed(1)}" y1="${GY0 - 4}" x2="${x.toFixed(1)}" y2="${GY1}"/>`;
    }
    s += `<text class="du-lab" x="${GX0}" y="${GY1 + 18}" text-anchor="start">0</text><text class="du-lab" x="${GX1}" y="${GY1 + 18}" text-anchor="end">${T - 1}</text>`;
    return s + `</svg>`;
  };

  // --- the box -------------------------------------------------------------------------------

  const view = () => ({
    mount(box) {
      const v0 = duParse((box.dataset.v || "").replace(/,/g, " ")) || [2, 6, 11, 4];
      const st = { v: v0.slice(), k: 0 };
      let orb = duOrbit(st.v);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>המספרים</span><input type="text" class="ex-num du-field du-nums-in" dir="ltr" spellcheck="false" aria-label="המספרים על המעגל${NB}: ${NMIN} עד ${NMAX} מספרים שלמים בין 0 ל-${VMAX}, מופרדים ברווח"></label>` +
        `<label><span>כמה</span><select class="du-n" data-nolink aria-label="כמה מספרים להגריל בכפתור ההגרלה">${Array.from({ length: NMAX - NMIN + 1 }, (_, i) => `<option value="${i + NMIN}">${i + NMIN}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button du-rand">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err du-err" role="status"></span></div>` +
        `<div class="ex-controls du-presets"><span>התחלות${NB}:</span>` +
        PRESETS.map(([t, v]) => `<button type="button" class="md-button ex-preset" data-v="${v}">${/^\d/.test(t) ? `<span dir="ltr">${t}</span>` : t}</button>`).join("") + `</div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הסיבוב הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הסיבוב הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1000, 500, 180) +
        `<span class="ex-pos"></span></div>` +
        `<div class="du-stage"></div>` +
        `<span class="viz-legend"><span><i class="du-key-node"></i>מספר על המעגל</span><span><i class="du-key-diff"></i>ההפרש של שני שכנים : המספר של הסיבוב הבא</span></span>` +
        `<div class="du-chartbox"></div>` +
        `<span class="viz-legend"><span><i class="du-key-bar"></i>המקסימום בכל סיבוב</span><span><i class="du-key-half"></i>סיבוב שבו כל המספרים מתחלקים בעוד 2 : המשחק נחצה</span><span><i class="du-key-cyc"></i>בתוך המחזור</span></span>` +
        `<p class="ex-summary du-sum" aria-live="polite"></p>` +
        `<p class="du-note"></p>`;
      const $ = (q) => box.querySelector(q);
      const total = () => orb.states.length - 1 + (orb.tail !== null && orb.period > 1 ? 1 : 0);
      const stateAt = (k) => (k < orb.states.length ? orb.states[k] : duStep(orb.states[orb.states.length - 1]));
      const draw = () => {
        const T = total();
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, v = stateAt(k), n = v.length, zero = orb.tail !== null && orb.period === 1 && v.every((x) => !x);
        const inCyc = orb.tail !== null && orb.period > 1 && k >= orb.tail;
        if (document.activeElement !== $(".du-nums-in")) $(".du-nums-in").value = st.v.join(" ");
        $(".du-n").value = String(st.v.length);
        $(".ex-pos").textContent = `סיבוב ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        $(".du-stage").innerHTML = circleSvg(v, inCyc);
        $(".du-chartbox").innerHTML = chartSvg(orb, Math.min(k, orb.states.length - 1));
        const even = v.some((x) => x) && v.every((x) => x % 2 === 0);
        $(".du-sum").innerHTML = (k ? `סיבוב ${ltr(k)}${NB}: ` : "ההתחלה. ") + `על המעגל <span class="du-nums" dir="ltr">${v.join(", ")}</span>, והמקסימום ${ltr(Math.max(...v))}.` +
          (inCyc ? ` <span class="du-tag">בתוך המחזור</span>` : "");
        let note = "";
        if (orb.tail === null) note = `אחרי ${ltr(CAP)} סיבובים עוד לא חזר אף מצב. נסו מספרים קטנים יותר.`;
        else if (zero) note = `כל המספרים 0, ומכאן הם נשארים 0.`;
        else if (even) note = `כל המספרים זוגיים${NB}: מכאן המשחק הוא פעמיים המשחק על החצאים, ${ltr(v.map((x) => x / 2).join(", "))}.`;
        else if (k === orb.tail && orb.period > 1) note = `המצב הזה חוזר אחרי ${ltr(orb.period)} סיבובים${NB}: כאן מתחיל המחזור.`;
        else if (orb.period === 1) note = `${n} מספרים${NB}: ${duAlwaysZero(n) ? "חזקה של 2, ולכן מגיעים בסוף לאפסים." : "לא חזקה של 2, אבל ההתחלה הזו מגיעה לאפסים."}`;
        else note = `${n} מספרים, לא חזקה של 2${NB}: ההתחלה הזו נכנסת למחזור אחרי ${ltr(orb.tail)} סיבובים.`;
        $(".du-note").innerHTML = note;
        if (k === T && orb.tail !== null) {
          answer(box, orb.period === 1
            ? `כל המספרים 0 אחרי ${ltr(orb.tail)} סיבובים.`
            : `נכנסים למחזור באורך ${ltr(orb.period)} אחרי ${ltr(orb.tail)} סיבובים, ולא מגיעים לאפסים לעולם.`, ".du-sum");
        } else answer(box, null);
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= total(), restart: () => { st.k = 0; draw(); } });
      const setV = (v) => { stop(); st.v = v; st.k = 0; orb = duOrbit(v); $(".du-err").textContent = ""; $(".du-nums-in").value = v.join(" "); draw(); };
      $(".du-nums-in").addEventListener("change", () => {
        const v = duParse($(".du-nums-in").value);
        if (!v) { $(".du-err").textContent = `המספרים${NB}: ${NMIN} עד ${NMAX} מספרים שלמים בין 0 ל-${VMAX}`; return; }
        setV(v);
      });
      const rand = () => Array.from({ length: Number($(".du-n").value) || 4 }, () => Math.floor(Math.random() * 21));
      $(".du-rand").addEventListener("click", () => setV(rand()));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => setV(duParse(b.dataset.v))));
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => setV(v0.slice()));
      draw();
    },
  });

  dvqExplorers.register({
    views: { ducci: view },
    help: {
      ducci: "מקלידים מספרים מופרדים ברווח, בוחרים התחלה מוכנה, או בוחרים כמה מספרים ומגרילים. על המעגל המספרים של הסיבוב הנוכחי, ועל כל צלע ההפרש של שני השכנים שבקצותיה : אלה המספרים של הסיבוב הבא. החיצים עוברים סיבוב אחרי סיבוב. בגרף, עמודה לכל סיבוב בגובה המקסימום שלו : הוא אף פעם לא עולה. עמודה ירוקה היא סיבוב שבו כל המספרים מתחלקים בעוד 2 (בפעם הראשונה הם כולם זוגיים, אחר כך כולם מתחלקים ב-4, וכן הלאה), ועמודות סגולות הן המחזור.",
    },
    models: { duStep, duOrbit, duParityStep, duAlwaysZero, duParse },
    cols: { ducci: { main: ".du-stage, .du-stage + .viz-legend", side: ".du-chartbox, .du-chartbox + .viz-legend", w: "minmax(0, 1fr)" } },   // the circle beside the chart of the maxima
  });
})();
