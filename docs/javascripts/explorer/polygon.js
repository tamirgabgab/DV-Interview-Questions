// kinds: polygon
//   polygon                0007        the same for n vertices (3 to 10): drag, type, arrow keys or draw; random draws against 1 - n / 2^(n-1)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { TRI_M, arrowStep, bigComb, f, fmt, ltr, seedControls, triNorm } = dvqExplorers.lib;

  // Polygon on the unit circle (0007, part b): n whole angles; the n arcs between the
  // sorted vertices decide exactly as for the triangle. The continuous probability
  // 1 - n / 2^(n-1), and a random draw of n different angles.
  const polyArcs = (angles) => {
    const a = angles.map(triNorm).sort((u, v) => u - v), n = a.length;
    const arcs = [];
    for (let i = 0; i + 1 < n; i++) arcs.push(a[i + 1] - a[i]);
    arcs.push(TRI_M - (a[n - 1] - a[0]));
    return arcs;
  };
  const polyClass = (angles) => {
    const arcs = polyArcs(angles);
    if (arcs.includes(0) || arcs.includes(TRI_M)) return "degenerate";
    const top = Math.max(...arcs);
    return top < 180 ? "in" : top === 180 ? "edge" : "out";
  };
  const polyProb = (n) => 1 - n / Math.pow(2, n - 1);
  // The discrete count of part d for n vertices at whole degrees (M points): the bad sets
  // by the first vertex of the half circle, M * C(floor(M / 2), n - 1) of the C(M, n).
  // Exact in BigInt: { num, den } reduced, and the value.
  const bigGcd = (a, b) => (b ? bigGcd(b, a % b) : a);
  const polyProbDiscrete = (n, M = TRI_M) => {
    const all = bigComb(M, n), bad = BigInt(M) * bigComb(Math.floor(M / 2), n - 1), good = all - bad;
    const g = bigGcd(good, all);
    return { num: (good / g).toString(), den: (all / g).toString(), value: Number(good) / Number(all) };
  };
  const polyRandom = (n, rnd = Math.random) => {
    const used = new Set(), out = [];
    while (out.length < n) { const v = Math.floor(rnd() * TRI_M); if (!used.has(v)) { used.add(v); out.push(v); } }
    return out;
  };

  // The polygon box (0007, part b): the triangle box generalised to n vertices, n from
  // the slider; the same colours, arcs and inputs, a random draw, and a counter of random
  // polygons that contain the centre against 1 - n / 2^(n-1).
  const polygonView = () => ({
    mount(box) {
      const C = 160, R = 104, R_ARC = 116, R_LBL = 137, NMAX = Number(box.dataset.nmax || 10);
      const KIND = { in: "המצולע מכיל את המרכז", edge: "המרכז על צלע", out: "המצולע לא מכיל את המרכז", degenerate: "אין מצולע" };
      const num = (v) => Number(v).toLocaleString("en-US");
      const rad = (d) => (d * Math.PI) / 180;
      const at = (d, r) => [C + r * Math.cos(rad(d)), C - r * Math.sin(rad(d))];
      const st = { n: Math.min(NMAX, Math.max(3, Number(box.dataset.n || 5))), angles: [], runs: 0, hits: 0 };
      const regular = (n) => Array.from({ length: n }, (_, i) => Math.round((20 + (360 * i) / n) % 360));
      st.angles = regular(st.n);
      box.innerHTML =
        `<div class="ex-controls"><label><span>מספר הקודקודים n</span><input type="range" class="ex-n" min="3" max="${NMAX}" step="1" value="${st.n}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-random">הגרלה</button>` +
        `<button type="button" class="md-button ex-regular">מצולע משוכלל</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="tri-box"><svg class="figure tri-live" viewBox="0 0 320 320" role="group" aria-label="קודקודים על מעגל היחידה">` +
        `<circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/><g class="tri-arcs"></g><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text><g class="poly-pts"></g></svg>` +
        `<div class="tri-panel"><p class="tri-angles"></p><p class="tri-status" aria-live="polite"></p><p class="tri-arcs-text"></p></div></div>` +
        `<div class="ex-controls tri-run"><button type="button" class="md-button ex-rounds">1,000 הגרלות</button>` +
        `<button type="button" class="md-button ex-rounds-reset">איפוס המונה</button></div>` +
        `<p class="ex-summary tri-compare"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), shape = $(".tri-shape"), arcsG = $(".tri-arcs"), ptsG = $(".poly-pts");
      let running = false;
      const arcPath = (from, len) => {
        const [x0, y0] = at(from, R_ARC), [x1, y1] = at(from + len, R_ARC);
        return `M${f(x0)},${f(y0)} A${R_ARC},${R_ARC} 0 ${len > 180 ? 1 : 0} 0 ${f(x1)},${f(y1)}`;
      };
      const render = () => {
        const n = st.n, angles = st.angles;
        $(".out-n").textContent = String(n);
        const kind = polyClass(angles);
        const order = angles.map((_, i) => i).sort((i, j) => angles[i] - angles[j] || i - j);
        const arcs = polyArcs(angles), top = Math.max(...arcs);
        svg.setAttribute("class", `figure tri-live is-${kind}`);
        shape.setAttribute("points", order.map((i) => at(angles[i], R).map((v) => f(v)).join(",")).join(" "));
        let g = "";
        arcs.forEach((len, k) => {
          if (len <= 0 || len >= 360) return;
          const from = angles[order[k]], [lx, ly] = at(from + len / 2, R_LBL), max = len === top;
          g += `<path class="tri-arc${max ? " is-max" : ""}" d="${arcPath(from, len)}" fill="none"/>` +
               (n <= 8 || max ? `<text class="legend${max ? " tri-max-label" : ""}" x="${f(lx)}" y="${f(ly + 5)}" text-anchor="middle" font-size="${n > 6 ? 10 : 12}">${len}°</text>` : "");
        });
        arcsG.innerHTML = g;
        ptsG.innerHTML = angles.map((d, i) => {
          const [x, y] = at(d, R), [nx, ny] = at(d, R - 22);
          return `<circle class="tri-pt" data-i="${i}" cx="${f(x)}" cy="${f(y)}" r="${n > 7 ? 7 : 9}" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359" aria-valuenow="${d}" aria-label="P${i + 1} : ${d} מעלות, חיצים מזיזים"><title>P${i + 1}</title></circle>` +
                 `<text class="legend tri-name" x="${f(nx)}" y="${f(ny + 4)}" text-anchor="middle" font-size="${n > 6 ? 10 : 12}">P${i + 1}</text>`;
        }).join("");
        // the inputs follow n
        const panel = $(".tri-angles");
        if (panel.children.length !== n) {
          panel.innerHTML = angles.map((_, i) => `<label>${ltr(`P${i + 1}`)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של P${i + 1} במעלות">°</label>`).join(" ");
          panel.querySelectorAll(".ex-deg").forEach((inp, i) => {
            inp.addEventListener("change", () => {
              const v = Number(inp.value);
              if (inp.value.trim() !== "" && Number.isFinite(v)) { const next = [...st.angles]; next[i] = ((Math.round(v) % 360) + 360) % 360; st.angles = next; }
              render();
            });
            inp.addEventListener("keydown", (e) => { if (e.key === "Enter") inp.blur(); });
          });
        }
        panel.querySelectorAll(".ex-deg").forEach((inp, i) => { if (document.activeElement !== inp) inp.value = angles[i]; });
        svg.setAttribute("aria-label", `${n} קודקודים על מעגל היחידה בזוויות ${angles.join(", ")} מעלות : ${KIND[kind]}`);
        const why = {
          in: `כל ${ltr(n)} הקשתות קטנות מ-180°, הגדולה היא ${ltr(top + "°")}.`,
          edge: `יש קשת של בדיוק 180°, והצלע שמולה היא קוטר שעובר דרך המרכז.`,
          out: `יש קשת של ${ltr(top + "°")}, יותר מ-180° : כל הקודקודים בחצי מעגל אחד.`,
          degenerate: `שני קודקודים או יותר באותה זווית.`,
        }[kind];
        const mark = { in: "✓", edge: "●", out: "✗", degenerate: "●" }[kind];
        $(".tri-status").innerHTML = `<span class="tri-kind is-${kind}">${mark} ${KIND[kind]}.</span> ${why}`;
        $(".tri-arcs-text").innerHTML = kind === "degenerate" ? "" : `הקשתות לפי הסדר על המעגל : ${ltr(arcs.map((v) => `${v}°`).join(", "))}.`;
        const p = polyProb(n), d = polyProbDiscrete(n);
        $(".tri-compare").innerHTML = `הנוסחה של סעיף ג לזוויות רציפות : ${ltr(`1 − ${n}/2^${n - 1} = ${fmt(p, 4)}`)}. ` +
          `בזוויות שלמות, כמו בספירה של סעיף ד : ${ltr(`1 − 360·C(180, ${n - 1}) / C(360, ${n}) = ${d.num}/${d.den} ≈ ${fmt(d.value, 4)}`)}, ` +
          `${ltr(fmt(Math.abs(d.value - p), 4))} ${d.value < p ? "פחות" : "יותר"} מהרציף. ` +
          (st.runs ? `מתוך ${ltr(num(st.runs))} מצולעים אקראיים (זוויות שלמות שונות), ${ltr(num(st.hits))} הכילו את המרכז : ${ltr(fmt(st.hits / st.runs, 4))}, מול ${ltr(fmt(d.value, 4))} הבדיד.` : `לחצו "1,000 הגרלות" כדי להשוות.`);
      };
      const setN = (n) => { st.n = n; st.angles = regular(n); st.runs = st.hits = 0; render(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      const seed = seedControls(box, $(".ex-random"), (rng) => { st.angles = polyRandom(st.n, rng); render(); });
      $(".ex-random").addEventListener("click", seed.draw);
      $(".ex-regular").addEventListener("click", () => { st.angles = regular(st.n); render(); });
      const N0 = st.n;
      $(".ex-reset").addEventListener("click", () => { $(".ex-n").value = N0; setN(N0); });
      $(".ex-rounds").addEventListener("click", () => {
        for (let r = 0; r < 1000; r++) if (polyClass(polyRandom(st.n)) === "in") st.hits++;
        st.runs += 1000; render();
      });
      $(".ex-rounds-reset").addEventListener("click", () => { st.runs = st.hits = 0; render(); });
      // drag: the vertex nearest to the finger follows it around the circle
      let drag = null;
      const degAt = (e) => {
        const r = svg.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 320 - C, y = C - ((e.clientY - r.top) / r.height) * 320;
        return ((Math.round((Math.atan2(y, x) * 180) / Math.PI) % 360) + 360) % 360;
      };
      svg.addEventListener("pointerdown", (e) => {
        const d = degAt(e);
        const dist = (i) => { const u = Math.abs(st.angles[i] - d); return Math.min(u, 360 - u); };
        const target = e.target.closest(".tri-pt");
        drag = target ? Number(target.dataset.i) : st.angles.reduce((b, _, i) => (dist(i) < dist(b) ? i : b), 0);
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        const next = [...st.angles]; next[drag] = d; st.angles = next; render();
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const d = degAt(e);
        if (d === st.angles[drag]) return;
        const next = [...st.angles]; next[drag] = d; st.angles = next; render();
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      // keyboard: a focused vertex moves one degree per arrow, ten with Shift; the
      // vertices are redrawn, so the focus is put back on the same one
      svg.addEventListener("keydown", (e) => {
        const t = e.target.closest(".tri-pt"), d = arrowStep(e);
        if (!t || !d) return;
        e.preventDefault(); e.stopPropagation();
        const i = Number(t.dataset.i), next = [...st.angles];
        next[i] = ((next[i] + d) % 360 + 360) % 360; st.angles = next; render();
        const g = svg.querySelector(`.tri-pt[data-i="${i}"]`); if (g) g.focus({ preventScroll: true });
      });
      void running;
      render();
    },
  });

  dvqExplorers.register({
    views: { polygon: polygonView },
    help: {
      polygon: "n קודקודים על המעגל : גוררים, מקלידים או מגרילים, וירוק אומר שהמרכז בפנים. ״1,000 הגרלות״ משווה לנוסחה הרציפה ולשבר הבדיד.",
    },
    models: { polyArcs, polyClass, polyProb, polyProbDiscrete, polyRandom },
  });
})();
