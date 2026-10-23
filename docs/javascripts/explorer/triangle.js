// kinds: triangle
//   triangle               0007        three points to drag, type or nudge with arrow keys, inside / edge / outside; play counts every triangle; a largest-arc histogram of 1,000 draws
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, TOP, TRI_M, arrowStep, f, fmt, frame, ltr, mulberry32, seedControls, triNorm } = dvqExplorers.lib;

  // Random triangle (0007): three whole angles in degrees on the unit circle. The three arcs
  // between the sorted points decide: every arc below 180 puts the centre inside, an arc of
  // exactly 180 puts it on an edge (that edge is a diameter), and a point on top of another
  // leaves no triangle at all.
  const triArcs = (angles) => {
    const a = angles.map(triNorm).sort((u, v) => u - v);
    return [a[1] - a[0], a[2] - a[1], TRI_M - (a[2] - a[0])];
  };
  const triClass = (angles) => {
    const arcs = triArcs(angles);
    if (arcs.includes(0) || arcs.includes(TRI_M)) return "degenerate";
    const top = Math.max(...arcs);
    return top < 180 ? "in" : top === 180 ? "edge" : "out";
  };
  // The enumeration of the play button: every set of three different angles a < b < c, in
  // increasing order (a first, then b, then c): C(360, 3) frames. For a fixed pair a < b,
  // how many c in (b, t] put the centre inside and how many on an edge (the rest outside).
  const TRI_TOTAL = (TRI_M * (TRI_M - 1) * (TRI_M - 2)) / 6;
  const triCountC = (a, b, t) => {
    if (t <= b) return { in: 0, edge: 0 };
    if (b - a === 180) return { in: 0, edge: t - b };      // a-b is a diameter for every c
    if (b - a > 180) return { in: 0, edge: 0 };             // arc a-b too long for every c
    const lo = Math.max(b + 1, a + 181), hi = Math.min(t, b + 179);   // arcs b-c and c-a below 180
    let edge = 0;
    if (a + 180 <= t) edge++;                               // c = a + 180: arc c-a is 180
    if (b + 180 <= t) edge++;                               // c = b + 180: arc b-c is 180
    return { in: Math.max(0, hi - lo + 1), edge };
  };
  // Running totals per pair (a, b), built once: the frame where the pair starts and the
  // counts of every frame before it.
  let triTables = null;
  const triTable = () => {
    if (triTables) return triTables;
    const P = ((TRI_M - 1) * (TRI_M - 2)) / 2;              // pairs a < b <= 358 (b = 359 has no c)
    const start = new Float64Array(P + 1), cin = new Int32Array(P + 1), cedge = new Int32Array(P + 1);
    const pa = new Uint16Array(P), pb = new Uint16Array(P);
    let p = 0;
    for (let a = 0; a < TRI_M - 2; a++) {
      for (let b = a + 1; b < TRI_M - 1; b++) {
        const n = triCountC(a, b, TRI_M - 1);
        pa[p] = a; pb[p] = b;
        start[p + 1] = start[p] + (TRI_M - 1 - b);
        cin[p + 1] = cin[p] + n.in;
        cedge[p + 1] = cedge[p] + n.edge;
        p++;
      }
    }
    triTables = { P, start, cin, cedge, pa, pb };
    return triTables;
  };
  const triPairIndex = (a, b) => a * (TRI_M - 2) - (a * (a - 1)) / 2 + (b - a - 1);
  // frame k (0-based) -> the angles [a, b, c]
  const triFrame = (k) => {
    const T = triTable();
    k = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
    let lo = 0, hi = T.P - 1;                               // last pair whose start <= k
    while (lo < hi) {
      const mid = (lo + hi + 1) >> 1;
      if (T.start[mid] <= k) lo = mid; else hi = mid - 1;
    }
    const a = T.pa[lo], b = T.pb[lo];
    return [a, b, b + 1 + (k - T.start[lo])];
  };
  // three different angles -> their frame
  const triIndex = (angles) => {
    const [a, b, c] = angles.map(triNorm).sort((u, v) => u - v);
    return triTable().start[triPairIndex(a, b)] + (c - b - 1);
  };
  // the counts of frames 0..k
  const triCounts = (k) => {
    const T = triTable();
    k = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
    const [a, b, c] = triFrame(k);
    const p = triPairIndex(a, b), n = triCountC(a, b, c);
    const seen = k + 1, inside = T.cin[p] + n.in, edge = T.cedge[p] + n.edge;
    return { seen, in: inside, edge, out: seen - inside - edge };
  };

  // The largest arc of three random points: the continuous distribution function (the
  // arcs are Dirichlet(1, 1, 1)), and a histogram of `draws` random whole-degree
  // triangles in bins of `bin` degrees from 120 to 360, split inside / outside (a
  // largest arc below 180 is inside; exactly 180 is the centre on an edge, counted
  // outside; a degenerate triangle is skipped and counted).
  const triArcCdf = (x) => {
    const u = x / 360;
    if (x <= 120) return 0;
    if (x >= 360) return 1;
    return x < 180 ? 1 - 3 * (1 - u) * (1 - u) + 3 * (1 - 2 * u) * (1 - 2 * u) : 1 - 3 * (1 - u) * (1 - u);
  };
  const triHistogram = (rnd = Math.random, draws = 1000, bin = 10) => {
    const bins = [];
    for (let lo = 120; lo < 360; lo += bin) bins.push({ lo, hi: lo + bin, in: 0, out: 0, expected: draws * (triArcCdf(lo + bin) - triArcCdf(lo)) });
    let degenerate = 0;
    for (let k = 0; k < draws; k++) {
      const angles = [0, 1, 2].map(() => Math.floor(rnd() * TRI_M));
      const kind = triClass(angles);
      if (kind === "degenerate") { degenerate += 1; continue; }
      const top = Math.max(...triArcs(angles));
      const b = bins[Math.min(bins.length - 1, Math.floor((top - 120) / bin))];
      if (kind === "in") b.in += 1; else b.out += 1;
    }
    return { bins, draws, degenerate };
  };
  const chartFrame = frame;   // for views whose own `frame` is a number (the triangle enumeration)

  // The triangle box (0007): three points on the unit circle, dragged or typed in whole
  // degrees; the triangle is green with the centre inside, amber with the centre on an edge
  // (or no triangle), red without it; the arcs carry their size and the longest one stands
  // out. Play walks through every set of three different angles in increasing order and
  // counts the three kinds; the slider jumps to any frame, and a hand-made triangle shows
  // where it sits in that order.
  const triangleView = () => ({
    mount(box) {
      const C = 160, R = 104, R_ARC = 116, R_LBL = 137, NAMES = ["P1", "P2", "P3"];
      const KIND = {
        in: "המשולש מכיל את המרכז",
        edge: "המרכז על צלע",
        out: "המשולש לא מכיל את המרכז",
        degenerate: "אין משולש",
      };
      const num = (v) => Number(v).toLocaleString("en-US");
      const rad = (d) => (d * Math.PI) / 180;
      const at = (d, r) => [C + r * Math.cos(rad(d)), C - r * Math.sin(rad(d))];
      box.innerHTML =
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="group" aria-label="שלוש נקודות על מעגל היחידה">` +
        `<circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/>` +
        `<g class="tri-arcs"></g><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text>` +
        NAMES.map((n, i) => `<circle class="tri-pt" data-i="${i}" r="9" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359"><title>${n}</title></circle>` +
          `<text class="legend tri-name" data-i="${i}" text-anchor="middle">${n}</text>`).join("") +
        `</svg><div class="tri-panel">` +
        `<p class="tri-angles">` + NAMES.map((n, i) =>
          `<label>${ltr(n)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של ${n} במעלות">°</label>`).join(" ") + `</p>` +
        `<div class="ex-controls"><button type="button" class="md-button ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="tri-status" aria-live="polite"></p><p class="tri-arcs-text"></p></div></div>` +
        `<div class="ex-controls tri-run">` +
        `<button type="button" class="md-button md-button--primary ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed">` +
        [[2, "2 משולשים בשנייה"], [30, "30 בשנייה"], [1000, "1,000 בשנייה"], [100000, "100,000 בשנייה"], [1000000, "מיליון בשנייה"]]
          .map(([v, n]) => `<option value="${v}"${v === 30 ? " selected" : ""}>${n}</option>`).join("") +
        `</select></label>` +
        `<button type="button" class="md-button ex-prev" aria-label="המשולש הקודם בספירה">‹ הקודם</button>` +
        `<button type="button" class="md-button ex-next" aria-label="המשולש הבא בספירה">הבא ›</button>` +
        `<button type="button" class="md-button ex-first">להתחלה</button>` +
        `<button type="button" class="md-button ex-last">לסוף</button></div>` +
        `<label class="tri-frames">הספירה <input type="range" class="ex-frame" min="0" max="${TRI_TOTAL - 1}" step="1" dir="ltr" aria-label="מספר המשולש בספירה"></label>` +
        `<p class="tri-frame-text"></p><ul class="tri-counts"></ul>` +
        `<p class="ex-summary tri-compare"></p>` +
        `<div class="ex-controls tri-hist-row"><button type="button" class="md-button ex-hist">1,000 הגרלות : הקשת הגדולה</button><span class="tri-hist-text"></span></div><div class="tri-hist"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), shape = $(".tri-shape"), arcsG = $(".tri-arcs");
      // the histogram of the largest arc over 1,000 random triangles, stacked inside / outside
      const histSvg = (h) => {
        const n = h.bins.length, vmax = Math.max(...h.bins.map((b) => Math.max(b.in + b.out, b.expected)));
        const ymax = Math.ceil(vmax / 20) * 20 || 20, ticks = [];
        for (let v = 0; v <= ymax; v += ymax / 4) ticks.push(v);
        const fr = chartFrame("הקשת הגדולה ביותר ב-1,000 משולשים אקראיים", n, ymax, ticks);
        let s = fr.s;
        h.bins.forEach((b, i) => {
          const x = fr.cx(i + 1), bw = Math.max(fr.slot * 0.72, 1);
          const yOut = fr.Y(b.out), yIn = fr.Y(b.in + b.out);
          const title = `${b.lo}° עד ${b.hi}° : ${b.in} בפנים, ${b.out} בחוץ; צפוי ${fmt(b.expected, 1)}`;
          if (b.lo === 170) s += `<rect class="hist-near" x="${f(x - fr.slot / 2)}" y="${TOP}" width="${f(fr.slot)}" height="${f(BASE - TOP)}"/>`;
          if (b.out) s += `<rect class="bar hist-out" x="${f(x - bw / 2)}" y="${f(yOut)}" width="${f(bw)}" height="${f(BASE - yOut)}"><title>${title}</title></rect>`;
          if (b.in) s += `<rect class="bar hist-in${b.lo === 120 ? " is-fat" : ""}" x="${f(x - bw / 2)}" y="${f(yIn)}" width="${f(bw)}" height="${f(yOut - yIn)}"><title>${title}</title></rect>`;
          s += `<line class="ink-line" x1="${f(x - bw / 2)}" x2="${f(x + bw / 2)}" y1="${f(fr.Y(b.expected))}" y2="${f(fr.Y(b.expected))}" stroke-width="2" stroke-dasharray="3 2"/>`;
          if (b.lo % 30 === 0) s += fr.xtick(i + 1, `${b.lo}°`);
        });
        return s + fr.close();
      };
      const drawHist = (rng) => {
        const h = triHistogram(rng, 1000, 10);
        const fat = h.bins[0], near = h.bins.find((b) => b.lo === 170), inside = h.bins.reduce((t, b) => t + b.in, 0);
        $(".tri-hist").innerHTML = histSvg(h);
        $(".tri-hist-text").innerHTML = `${ltr(num(inside))} מתוך ${ltr(num(h.draws - h.degenerate))} בפנים${h.degenerate ? ` (${ltr(h.degenerate)} מנוונים הושמטו)` : ""}; ` +
          `"שמנים", קשת מתחת ל-130° : ${ltr(fat.in)} (צפוי ${ltr(fmt(fat.expected, 1))}); כמעט מנוונים, 170° עד 180° : ${ltr(near.in)} (צפוי ${ltr(fmt(near.expected, 1))}). הקו המקווקו בכל עמודה הוא הצפי מההתפלגות הרציפה.`;
      };
      const pts = [...box.querySelectorAll(".tri-pt")], names = [...box.querySelectorAll(".tri-name")];
      const inputs = [...box.querySelectorAll(".ex-deg")];
      const play = $(".ex-play"), speed = $(".ex-speed"), slider = $(".ex-frame");
      let angles = (box.dataset.angles || "20,140,250").split(",").map(Number).map((v) => ((v % 360) + 360) % 360);
      const PAGE = angles.slice();
      let frame = 0, running = false, last = 0, pos = 0;

      const arcPath = (from, len) => {
        const [x0, y0] = at(from, R_ARC), [x1, y1] = at(from + len, R_ARC);
        return `M${f(x0)},${f(y0)} A${R_ARC},${R_ARC} 0 ${len > 180 ? 1 : 0} 0 ${f(x1)},${f(y1)}`;
      };
      const render = () => {
        const kind = triClass(angles);
        const order = [0, 1, 2].sort((i, j) => angles[i] - angles[j] || i - j);
        const arcs = triArcs(angles), top = Math.max(...arcs);
        svg.setAttribute("class", `figure tri-live is-${kind}`);
        shape.setAttribute("points", angles.map((d) => at(d, R).map((v) => f(v)).join(",")).join(" "));
        let g = "";
        arcs.forEach((len, n) => {
          if (len <= 0 || len >= 360) return;
          const from = angles[order[n]];
          const [lx, ly] = at(from + len / 2, R_LBL);
          const max = len === top;
          g += `<path class="tri-arc${max ? " is-max" : ""}" d="${arcPath(from, len)}" fill="none"/>` +
               `<text class="legend${max ? " tri-max-label" : ""}" x="${f(lx)}" y="${f(ly + 5)}" text-anchor="middle">${len}°</text>`;
        });
        arcsG.innerHTML = g;
        angles.forEach((d, i) => {
          const [x, y] = at(d, R), [nx, ny] = at(d, R - 24);
          pts[i].setAttribute("cx", f(x)); pts[i].setAttribute("cy", f(y));
          pts[i].setAttribute("aria-valuenow", d); pts[i].setAttribute("aria-label", `${NAMES[i]} : ${d} מעלות, חיצים מזיזים`);
          names[i].setAttribute("x", f(nx)); names[i].setAttribute("y", f(ny + 5));
          if (document.activeElement !== inputs[i] || running) inputs[i].value = d;
        });
        svg.setAttribute("aria-label", `שלוש נקודות על מעגל היחידה בזוויות ${angles.join(", ")} מעלות : ${KIND[kind]}`);
        const sorted = order.map((i) => angles[i]);
        const why = {
          in: `כל שלוש הקשתות קטנות מ-180°, הגדולה היא ${ltr(top + "°")}.`,
          edge: `יש קשת של בדיוק 180°, והצלע שמולה היא קוטר שעובר דרך המרכז.`,
          out: `יש קשת של ${ltr(top + "°")}, יותר מ-180° : שלוש הנקודות בחצי מעגל אחד.`,
          degenerate: `שתי נקודות או יותר באותה זווית.`,
        }[kind];
        const mark = { in: "✓", edge: "●", out: "✗", degenerate: "●" }[kind];
        $(".tri-status").innerHTML = `<span class="tri-kind is-${kind}">${mark} ${KIND[kind]}.</span> ${why}`;
        $(".tri-arcs-text").innerHTML = kind === "degenerate" ? "" :
          `הקשתות : ${ltr(`${sorted[1]} − ${sorted[0]} = ${arcs[0]}°`)}, ${ltr(`${sorted[2]} − ${sorted[1]} = ${arcs[1]}°`)}, ` +
          `${ltr(`360 − (${sorted[2]} − ${sorted[0]}) = ${arcs[2]}°`)}.`;
        // the place of this triangle in the enumeration, and the counts up to it
        const distinct = kind !== "degenerate";
        if (distinct) frame = triIndex(angles);
        slider.value = frame;
        const c = triCounts(frame);
        $(".tri-frame-text").innerHTML = distinct
          ? `משולש ${ltr(num(frame + 1))} מתוך ${ltr(num(TRI_TOTAL))} בספירה : כל שלוש זוויות שונות מ-0° עד 359°, בסדר עולה.`
          : `לשתי נקודות באותה זווית אין מקום בספירה; המונים נשארו במשולש ${ltr(num(frame + 1))}.`;
        const pct = (v) => ltr(`${f((100 * v) / c.seen, 2)}%`);
        $(".tri-counts").innerHTML =
          `<li class="is-in">מכילים את המרכז : ${ltr(num(c.in))} (${pct(c.in)})</li>` +
          `<li class="is-edge">המרכז על צלע : ${ltr(num(c.edge))} (${pct(c.edge)})</li>` +
          `<li class="is-out">לא מכילים : ${ltr(num(c.out))} (${pct(c.out)})</li>`;
        const p = c.in / c.seen, exact = 89 / 359;
        const diff = p - exact;
        $(".tri-compare").innerHTML =
          `החלק שמכיל עד כאן : ${ltr(fmt(p, 5))}. בסוף הספירה : ${ltr("1,911,720 / 7,711,320 = 89/359 ≈ 0.24791")} (סעיף ד), ` +
          `ובזוויות רציפות ${ltr("1/4")} (סעיף ג). ההפרש מ-${ltr("89/359")} : ${ltr((diff >= 0 ? "+" : "−") + fmt(Math.abs(diff), 5))}` +
          (c.seen === TRI_TOTAL ? ", והספירה הושלמה." : ". הסדר עולה, ולכן החלק נודד בדרך ומגיע לערך המדויק רק בסוף.");
      };
      const setAngles = (next) => { angles = next.map((v) => ((Math.round(v) % 360) + 360) % 360); render(); };
      const setFrame = (k) => {
        frame = Math.min(Math.max(Math.floor(k), 0), TRI_TOTAL - 1);
        angles = triFrame(frame);
        render();
      };
      const stop = () => {
        running = false;
        play.textContent = "הפעלה";
        $(".tri-status").setAttribute("aria-live", "polite");
      };
      const tick = (now) => {
        if (!running) return;
        pos = Math.min(pos + ((now - last) / 1000) * Number(speed.value), TRI_TOTAL - 1);
        last = now;
        if (Math.floor(pos) !== frame) setFrame(pos);
        if (frame >= TRI_TOTAL - 1) stop(); else requestAnimationFrame(tick);
      };
      play.addEventListener("click", () => {
        if (running) { stop(); return; }
        if (triClass(angles) === "degenerate" || frame >= TRI_TOTAL - 1) setFrame(frame >= TRI_TOTAL - 1 ? 0 : frame);
        pos = frame;
        running = true;
        play.textContent = "עצירה";
        $(".tri-status").setAttribute("aria-live", "off");
        last = performance.now();
        requestAnimationFrame(tick);
      });
      $(".ex-prev").addEventListener("click", () => { stop(); setFrame(frame - 1); });
      $(".ex-next").addEventListener("click", () => { stop(); setFrame(frame + 1); });
      $(".ex-first").addEventListener("click", () => { stop(); setFrame(0); });
      $(".ex-last").addEventListener("click", () => { stop(); setFrame(TRI_TOTAL - 1); });
      slider.addEventListener("input", () => { stop(); setFrame(Number(slider.value)); });
      const seed = seedControls(box, $(".ex-random"), (rng) => { stop(); setAngles([0, 1, 2].map(() => Math.floor(rng() * 360))); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-hist").addEventListener("click", () => { drawHist(mulberry32(Number($(".ex-seed").value) || 1)); });
      $(".ex-reset").addEventListener("click", () => { stop(); setAngles(PAGE); $(".tri-hist").innerHTML = ""; $(".tri-hist-text").textContent = ""; });
      inputs.forEach((inp, i) => {
        inp.addEventListener("change", () => {
          const v = Number(inp.value);
          if (inp.value.trim() !== "" && Number.isFinite(v)) {
            stop();
            const next = [...angles]; next[i] = v; setAngles(next);
          } else render();                              // a bad entry falls back to the angle shown
        });
        inp.addEventListener("keydown", (e) => { if (e.key === "Enter") inp.blur(); });
      });

      // drag: the point nearest to the finger follows it around the circle, in whole degrees
      let drag = null;
      const degAt = (e) => {
        const r = svg.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 320 - C, y = C - ((e.clientY - r.top) / r.height) * 320;
        return ((Math.round((Math.atan2(y, x) * 180) / Math.PI) % 360) + 360) % 360;
      };
      svg.addEventListener("pointerdown", (e) => {
        stop();
        const d = degAt(e);
        const dist = (i) => { const u = Math.abs(angles[i] - d); return Math.min(u, 360 - u); };
        const target = e.target.closest(".tri-pt");
        drag = target ? Number(target.dataset.i) : [0, 1, 2].reduce((b, i) => (dist(i) < dist(b) ? i : b), 0);
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        const next = [...angles]; next[drag] = d; setAngles(next);
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const d = degAt(e);
        if (d === angles[drag]) return;
        const next = [...angles]; next[drag] = d; setAngles(next);
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      // keyboard: a focused point moves one degree per arrow, ten with Shift
      svg.addEventListener("keydown", (e) => {
        const t = e.target.closest(".tri-pt"), d = arrowStep(e);
        if (!t || !d) return;
        e.preventDefault(); e.stopPropagation(); stop();
        const i = Number(t.dataset.i), next = [...angles]; next[i] += d; setAngles(next);
      });
      render();
    },
  });

  dvqExplorers.register({
    views: { triangle: triangleView },
    help: {
      triangle: "שלוש נקודות על המעגל : גוררים, מקלידים זוויות או מזיזים בחיצים, וירוק אומר שהמרכז בפנים. ״הפעלה״ עובר על כל השלשות וסופר, ו״1,000 הגרלות״ מצייר היסטוגרמה של הקשת הגדולה.",
    },
    models: { TRI_TOTAL, triArcs, triClass, triCountC, triFrame, triIndex, triCounts, triArcCdf, triHistogram },
  });
})();
