// kinds: clock
//   clock                  0029        a clock face to drag, play or type: meetings of the hands so far
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { EPS, f, ltr } = dvqExplorers.lib;

  // Clock (0029), time in seconds from 00:00:00. Hands i and j meet at k * P / q: the second
  // and minute hands every 3600/59 s, second and hour every 43200/719 s, minute and hour every
  // 43200/11 s. A "second" is the window [sec, sec + 1), so integer arithmetic stays exact.
  const CLOCK_PERIOD = { s: 60, m: 3600, h: 43200 };
  const CLOCK_PAIRS = [["s", "m", 3600, 59], ["s", "h", 43200, 719], ["m", "h", 43200, 11]];
  const CLOCK_DAY = 86400, CLOCK_HALF = 43200;
  // Meetings from 00:00:00 to the end of second sec: per pair, all three, and distinct moments.
  const clockCounts = (sec) => {
    const pairs = CLOCK_PAIRS.map(([, , P, q]) => Math.floor(((sec + 1) * q - 1) / P) + 1);
    const triple = Math.floor(sec / CLOCK_HALF) + 1;
    return { pairs, triple, total: pairs[0] + pairs[1] + pairs[2] - 2 * triple };
  };
  // The meetings inside second sec, as [pair index, time].
  const clockMeetsIn = (sec) => {
    const out = [];
    CLOCK_PAIRS.forEach(([, , P, q], n) => {
      const k = Math.floor((sec * q + P - 1) / P);           // the first k with k P >= sec q
      if (k * P < (sec + 1) * q) out.push([n, (k * P) / q]);
    });
    return out;
  };
  // The first meeting after t, or the last one before it (null outside the day).
  // `mask` limits the search to some pairs (indices into CLOCK_PAIRS).
  const clockNext = (t, mask = [0, 1, 2]) => {
    let best = null;
    mask.forEach((n) => {
      const [, , P, q] = CLOCK_PAIRS[n];
      const v = ((Math.floor((t * q) / P + EPS) + 1) * P) / q;
      if (v < CLOCK_DAY && (best === null || v < best)) best = v;
    });
    return best;
  };
  const clockPrev = (t, mask = [0, 1, 2]) => {
    let best = null;
    mask.forEach((n) => {
      const [, , P, q] = CLOCK_PAIRS[n];
      const k = Math.ceil((t * q) / P - EPS) - 1;
      if (k >= 0 && (best === null || (k * P) / q > best)) best = (k * P) / q;
    });
    return best;
  };
  // "H:MM:SS.ss" as tools/figures/q0029.py writes it: hundredths rounded, but at most .99.
  const clockLabel = (t) => {
    const sec = Math.floor(t);
    const two = (v) => String(v).padStart(2, "0");
    const base = `${Math.floor(sec / 3600)}:${two(Math.floor(sec / 60) % 60)}:${two(sec % 60)}`;
    if (Math.abs(t - sec) < 1e-9) return base;
    return `${base}.${two(Math.min(Math.floor((t - sec) * 100 + 0.5), 99))}`;
  };

  // The clock box: a face whose hands can be dragged, a play button with a speed, a day
  // slider, a time field and jumps to the next or previous meeting. The counters cover
  // 00:00:00 to the end of the second shown; hands that meet inside that second turn orange.
  const clockView = () => ({
    mount(box) {
      const C = 140, R = 124, LAST = CLOCK_DAY - 1e-6;
      const HAND = { h: ["ink", 62, 7], m: ["s1", 96, 4.5], s: ["s3", 108, 2] };
      const NAMES = { s: "השניות", m: "הדקות", h: "השעות" };
      const PAIR_NAME = CLOCK_PAIRS.map(([i, j]) => `${NAMES[i]} ו${NAMES[j]}`);
      const pt = (turn, r) => [C + r * Math.sin(2 * Math.PI * turn), C - r * Math.cos(2 * Math.PI * turn)];
      let face = `<svg class="figure clock-live" viewBox="0 0 280 280" role="img" aria-label="שעון">` +
        `<circle class="clock-face" cx="${C}" cy="${C}" r="${R}"/>`;
      for (let n = 0; n < 60; n++) {
        const [x0, y0] = pt(n / 60, R - (n % 5 ? 5 : 11)), [x1, y1] = pt(n / 60, R);
        face += `<line class="${n % 5 ? "clock-tick" : "clock-tick5"}" x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1)}"/>`;
      }
      for (let n = 1; n <= 12; n++) {
        const [x, y] = pt(n / 12, R - 26);
        face += `<text class="legend" x="${f(x)}" y="${f(y + 5)}" text-anchor="middle">${n}</text>`;
      }
      ["h", "m", "s"].forEach((k) => {
        const [cls, len, w] = HAND[k];
        face += `<line class="${cls}-line hand hand-${k}" x1="${C}" y1="${C}" x2="${C}" y2="${C - len}" ` +
                `stroke-width="${w}" stroke-linecap="round"/>`;
      });
      face += `<circle class="ink-dot" cx="${C}" cy="${C}" r="5"/></svg>`;

      box.innerHTML =
        `<div class="ex-controls">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed">` +
        [[1, "זמן אמת"], [10, "פי 10"], [60, "דקה בשנייה"], [600, "10 דקות בשנייה"], [3600, "שעה בשנייה"]]
          .map(([v, n]) => `<option value="${v}"${v === 60 ? " selected" : ""}>${n}</option>`).join("") +
        `</select></label>` +
        `<button type="button" class="md-button ex-prev">לפגישה הקודמת</button>` +
        `<button type="button" class="md-button ex-next">לפגישה הבאה</button>` +
        `<button type="button" class="md-button ex-triple">למשולשת הבאה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה ל-00:00</button></div>` +
        `<div class="ex-controls clock-filter"><span>הקפיצות ופס הזמן :</span>` +
        PAIR_NAME.map((name, n) => `<label><input type="checkbox" class="ex-pair" value="${n}" checked> ${name}</label>`).join("") + `</div>` +
        `<div class="clock-box">${face}<div class="clock-panel">` +
        `<p class="clock-time" dir="ltr"></p>` +
        `<label>שעה <input type="text" class="ex-time" inputmode="numeric" maxlength="8" size="8" ` +
        `placeholder="HH:MM:SS" aria-label="שעה, שעות : דקות : שניות" dir="ltr"></label>` +
        `<p class="clock-total"></p><ul class="clock-counts"></ul></div></div>` +
        `<label class="clock-day">היממה <input type="range" class="ex-day" min="0" max="${CLOCK_DAY - 1}" step="1" dir="ltr"></label>` +
        `<div class="clock-timeline" dir="ltr"></div>` +
        `<p class="ex-summary" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), hands = {}, play = $(".ex-play"), speed = $(".ex-speed");
      const timeIn = $(".ex-time"), day = $(".ex-day"), summary = $(".ex-summary");
      ["h", "m", "s"].forEach((k) => { hands[k] = $(`.hand-${k}`); });
      let t = Number(box.dataset.t || 0), shown = -1, running = false, last = 0;
      const mask = () => {
        const on = [...box.querySelectorAll(".ex-pair")].filter((c) => c.checked).map((c) => Number(c.value));
        return on.length ? on : [0, 1, 2];
      };
      // the timeline: one row per pair with a tick at every meeting; dense bands show where
      // the meetings of a pair cluster. A click jumps to the nearest meeting of that row.
      const TL_W = 600, TL_CLS = ["s1-line", "s3-line", "s2-line"];
      const tlX = (sec) => (sec / CLOCK_DAY) * TL_W;
      const timeline = $(".clock-timeline");
      timeline.innerHTML = CLOCK_PAIRS.map(([, , P, q], n) => {
        let ticks = "";
        for (let k = 0; k * P < CLOCK_DAY * q; k++) {
          const x = tlX((k * P) / q).toFixed(1);
          ticks += `<line class="${TL_CLS[n]}" x1="${x}" x2="${x}" y1="1" y2="13" stroke-width="${n === 2 ? 2 : 1}" stroke-opacity="${n === 2 ? 0.9 : 0.55}"/>`;
        }
        return `<div class="tl-row" data-pair="${n}"><span class="tl-name">${PAIR_NAME[n]}</span>` +
          `<svg viewBox="0 0 ${TL_W} 14" preserveAspectRatio="none" role="img" aria-label="הפגישות של ${PAIR_NAME[n]} לאורך היממה">${ticks}` +
          `<line class="tl-cursor" x1="0" x2="0" y1="0" y2="14"/></svg></div>`;
      }).join("") + `<div class="tl-axis"><span>00:00</span><span class="tl-mid">06:00</span><span>12:00</span><span class="tl-mid">18:00</span><span>24:00</span></div>`;
      timeline.querySelectorAll(".tl-row").forEach((row) => {
        const n = Number(row.dataset.pair), svg = row.querySelector("svg");
        svg.addEventListener("click", (e) => {
          const r = svg.getBoundingClientRect();
          const at = ((e.clientX - r.left) / r.width) * CLOCK_DAY;
          const [, , P, q] = CLOCK_PAIRS[n];
          const k = Math.round((at * q) / P);
          stop();
          setTime(Math.min(Math.max((k * P) / q, 0), LAST));
        });
      });

      const two = (v) => String(v).padStart(2, "0");
      const hms = (sec) => `${two(Math.floor(sec / 3600))}:${two(Math.floor(sec / 60) % 60)}:${two(sec % 60)}`;
      const render = (force) => {
        ["h", "m", "s"].forEach((k) => {
          const turn = (t / CLOCK_PERIOD[k]) % 1;
          hands[k].setAttribute("transform", `rotate(${(turn * 360).toFixed(3)} ${C} ${C})`);
        });
        const sec = Math.floor(t);
        if (sec === shown && !force) return;
        shown = sec;
        const meets = clockMeetsIn(sec), cnt = clockCounts(sec);
        const on = new Set();
        meets.forEach(([n]) => { on.add(CLOCK_PAIRS[n][0]); on.add(CLOCK_PAIRS[n][1]); });
        ["h", "m", "s"].forEach((k) => hands[k].classList.toggle("is-meet", on.has(k)));
        $(".clock-time").textContent = hms(sec);
        svg.setAttribute("aria-label", `שעון בשעה ${hms(sec)}`);
        if (document.activeElement !== timeIn || running) timeIn.value = hms(sec);
        day.value = sec;
        const enabled = mask();
        timeline.querySelectorAll(".tl-row").forEach((row) => {
          row.classList.toggle("is-off", !enabled.includes(Number(row.dataset.pair)));
          const x = tlX(t).toFixed(1);
          const c = row.querySelector(".tl-cursor");
          c.setAttribute("x1", x); c.setAttribute("x2", x);
        });
        $(".clock-total").innerHTML = `מתחילת היממה : ${cnt.total === 1 ? "פגישה אחת" : `${ltr(cnt.total)} פגישות`}`;
        const hit = new Set(meets.map(([n]) => n));
        $(".clock-counts").innerHTML = PAIR_NAME.map((name, n) =>
          `<li${hit.has(n) ? ' class="is-meet"' : ""}>${name}: ${ltr(cnt.pairs[n])}</li>`).join("") +
          `<li${sec % CLOCK_HALF === 0 ? ' class="is-meet"' : ""}>שלושתם יחד : ${ltr(cnt.triple)}, ` +
          `ולכן ${ltr(`${cnt.pairs.join(" + ")} − 2 · ${cnt.triple} = ${cnt.total}`)}</li>`;
        let text;
        const triple = sec % CLOCK_HALF === 0;               // all three meet only at 00:00 and 12:00
        if (triple) {
          text = `בשנייה הזו שלושת המחוגים נפגשים, ב-${ltr(clockLabel(meets[0][1]))}.`;
        } else if (meets.length) {
          text = "בשנייה הזו : " + meets.map(([n, v]) => `${PAIR_NAME[n]} נפגשים ב-${ltr(clockLabel(v))}`).join(", ") + ".";
        } else {
          const nx = clockNext(sec + 1 - 1e-9, mask());
          text = "בשנייה הזו אין פגישה." + (nx === null ? " אין עוד פגישות עד סוף היממה."
            : ` הבאה : ב-${ltr(clockLabel(nx))}, ${clockMeetsIn(Math.floor(nx)).map(([n]) => PAIR_NAME[n]).join(" וגם ")}.`);
        }
        summary.innerHTML = text;                    // built from numbers and fixed names only
      };
      const setTime = (v) => { t = Math.min(Math.max(v, 0), LAST); render(); };
      const stop = () => {
        running = false;
        play.textContent = "הפעלה";
        summary.setAttribute("aria-live", "polite");
      };
      const tick = (now) => {
        if (!running) return;
        t = Math.min(t + ((now - last) / 1000) * Number(speed.value), LAST);
        last = now;
        render();
        if (t >= LAST) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (t >= LAST) t = 0;
        running = true;
        play.textContent = "עצירה";
        summary.setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      $(".ex-next").addEventListener("click", () => { stop(); const v = clockNext(t, mask()); if (v !== null) setTime(v); });
      $(".ex-prev").addEventListener("click", () => { stop(); const v = clockPrev(t, mask()); if (v !== null) setTime(v); });
      $(".ex-triple").addEventListener("click", () => { stop(); setTime(t < CLOCK_HALF - 1e-9 ? CLOCK_HALF : 0); });
      box.querySelectorAll(".ex-pair").forEach((c) => c.addEventListener("change", () => render(true)));
      $(".ex-reset").addEventListener("click", () => { stop(); setTime(0); });
      day.addEventListener("input", () => { stop(); setTime(Number(day.value)); });
      timeIn.addEventListener("change", () => {
        const m = /^\s*(\d{1,2})(?::(\d{1,2}))?(?::(\d{1,2}))?\s*$/.exec(timeIn.value);
        const [h, mi, se] = m ? [1, 2, 3].map((n) => Number(m[n] || 0)) : [];
        if (m && h < 24 && mi < 60 && se < 60) { stop(); setTime(h * 3600 + mi * 60 + se); }
        render(true);                                   // a bad entry falls back to the time shown
      });
      timeIn.addEventListener("keydown", (e) => { if (e.key === "Enter") timeIn.blur(); });

      // drag: the hand nearest to the finger follows it; a full turn of that hand moves the
      // time by its period (60 s, an hour or 12 hours)
      let drag = null;
      const where = (e) => {
        const r = svg.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width * 280 - C, y = (e.clientY - r.top) / r.height * 280 - C;
        return [((Math.atan2(x, -y) / (2 * Math.PI)) + 1) % 1, Math.hypot(x, y)];
      };
      const turnAt = (e) => where(e)[0];
      svg.addEventListener("pointerdown", (e) => {
        stop();
        const [at, rad] = where(e);
        const dist = (k) => { const d = Math.abs(((t / CLOCK_PERIOD[k]) % 1) - at); return Math.min(d, 1 - d); };
        const best = Math.min(...["s", "m", "h"].map(dist));
        const near = ["s", "m", "h"].filter((k) => dist(k) < best + 0.02);
        // hands on top of each other: the length of the hand under the finger decides
        const byLength = rad > 100 ? "s" : rad > 66 ? "m" : "h";
        const k = near.includes(byLength) ? byLength : near[0];
        drag = { k, at };
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (!drag) return;
        const at = turnAt(e);
        let d = at - drag.at;
        if (d > 0.5) d -= 1;
        if (d < -0.5) d += 1;
        drag.at = at;
        setTime(t + d * CLOCK_PERIOD[drag.k]);
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      render(true);
    },
  });

  dvqExplorers.register({
    views: { clock: clockView },
    help: {
      clock: "השעון מראה את מפגשי המחוגים : גוררים מחוג, מקלידים שעה או מפעילים, והקפיצות עוברות למפגש הבא או הקודם. המונים וציר הזמן סופרים את המפגשים מההתחלה.",
    },
    models: { clockCounts, clockMeetsIn, clockNext, clockPrev, clockLabel },
  });
})();
