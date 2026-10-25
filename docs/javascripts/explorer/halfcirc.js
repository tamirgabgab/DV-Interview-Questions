// kinds: halfcirc
//   halfcirc               0007        part c's proof: three points to drag, the half-circle that starts at each one counterclockwise, which of A1, A2, A3 holds (at most one), and batches of continuous random draws counting each event against 1/4
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { arrowStep, f, ltr, seedControls } = dvqExplorers.lib;
  const NB = " ";

  // The events of 0007 part c for three angles in degrees: A_i holds when the other two
  // points lie in the half-circle [θ_i, θ_i + 180] that starts at P_i counterclockwise.
  // The centre is inside when none holds; on an edge when an arc is exactly 180.
  const halfOffset = (from, to) => (((to - from) % 360) + 360) % 360;
  const halfEvents = (angles) => {
    const events = angles.map((a, i) => angles.every((b, j) => j === i || halfOffset(a, b) <= 180));
    const sorted = [...angles].sort((u, v) => u - v);
    const arcs = sorted.map((a, i) => (i < 2 ? sorted[i + 1] - a : 360 - a + sorted[0]));
    return { events, inside: !events.some(Boolean), edge: arcs.some((a) => a === 180), arcs };
  };
  // n triangles with continuous uniform angles: how often each A_i holds, how often none
  // does (the centre inside) and how often two hold at once (never, but for ties)
  const halfCount = (n, rnd) => {
    const a = [0, 0, 0];
    let inside = 0, both = 0, last = null;
    for (let t = 0; t < n; t++) {
      last = [rnd() * 360, rnd() * 360, rnd() * 360];
      const e = halfEvents(last).events, k = e.filter(Boolean).length;
      e.forEach((v, i) => { if (v) a[i]++; });
      if (!k) inside++;
      if (k > 1) both++;
    }
    return { a, inside, both, n, last };
  };

  // The half-circles box (0007 part c): the circle with P1, P2, P3 (drag, arrows on a
  // focused point, or typed degrees), each half-circle A_i shaded in its own colour (a
  // checkbox per half), which one holds the other two points, and buttons that add 100 or
  // 1,000 continuous random triangles to the counts of A1, A2, A3 and of "inside".
  const halfcircView = () => ({
    mount(box) {
      const C = 160, R = 100, R_LBL = 146, NAMES = ["P1", "P2", "P3"], CLS = ["s1", "s2", "s3"];
      const rad = (d) => (d * Math.PI) / 180;
      const at = (d, r) => [C + r * Math.cos(rad(d)), C - r * Math.sin(rad(d))];
      const PAGE = (box.dataset.angles || "40,110,170").split(",").map(Number).map((v) => ((v % 360) + 360) % 360);
      let angles = PAGE.slice();
      const counts = { a: [0, 0, 0], inside: 0, both: 0, n: 0 };
      box.innerHTML =
        `<div class="tri-box"><svg class="figure tri-live hc-live" viewBox="0 0 320 320" role="group" aria-label="שלוש נקודות על המעגל וחצאי המעגל שמתחילים בהן">` +
        `<g class="hc-halves"></g><circle class="axis-c" cx="${C}" cy="${C}" r="${R}" fill="none"/><polygon class="tri-shape"/>` +
        `<circle class="center-dot" cx="${C}" cy="${C}" r="4"/><text class="tick" x="${C + 7}" y="${C + 15}">O</text>` +
        NAMES.map((n, i) => `<circle class="tri-pt hc-pt-${CLS[i]}" data-i="${i}" r="9" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359"><title>${n}</title></circle>` +
          `<text class="legend tri-name" data-i="${i}" text-anchor="middle">${n}</text>`).join("") +
        `</svg><div class="tri-panel">` +
        `<p class="tri-angles">` + NAMES.map((n, i) =>
          `<label>${ltr(n)} <input type="number" class="ex-deg" data-i="${i}" min="0" max="359" step="1" dir="ltr" aria-label="הזווית של ${n} במעלות">°</label>`).join(" ") + `</p>` +
        `<p class="tri-angles">` + NAMES.map((n, i) => `<label><input type="checkbox" class="hc-show" data-i="${i}" checked> <span class="hc-key hc-key-${CLS[i]}"></span>‏A${i + 1}</label>`).join(" ") + `</p>` +
        `<ul class="hc-events"></ul><p class="tri-status hc-status" aria-live="polite"></p>` +
        `<div class="ex-controls"><button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div></div></div>` +
        `<div class="ex-controls hc-run"><button type="button" class="md-button md-button--primary ex-draw100">100 הגרלות</button>` +
        `<button type="button" class="md-button ex-draw1000">1,000 הגרלות</button>` +
        `<button type="button" class="md-button ex-clear">איפוס הספירה</button></div>` +
        `<div class="hc-counts"></div><p class="ex-summary hc-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $("svg"), pts = [...box.querySelectorAll(".tri-pt")], names = [...box.querySelectorAll(".tri-name")], inputs = [...box.querySelectorAll(".ex-deg")];
      const show = () => [...box.querySelectorAll(".hc-show")].map((c) => c.checked);
      // a half as an arc outside the circle (one radius per half), and its half-disc when it holds
      const halfArc = (from, r) => {
        const [x0, y0] = at(from, r), [x1, y1] = at(from + 180, r);
        return `M${f(x0)},${f(y0)} A${r},${r} 0 0 0 ${f(x1)},${f(y1)}`;
      };
      const halfDisc = (from) => {
        const [x0, y0] = at(from, R), [x1, y1] = at(from + 180, R);
        return `M${C},${C} L${f(x0)},${f(y0)} A${R},${R} 0 0 0 ${f(x1)},${f(y1)} Z`;
      };
      const render = () => {
        const ev = halfEvents(angles), on = show();
        angles.forEach((d, i) => {
          const [x, y] = at(d, R), [lx, ly] = at(d, R_LBL);
          pts[i].setAttribute("cx", f(x)); pts[i].setAttribute("cy", f(y)); pts[i].setAttribute("aria-valuenow", d);
          pts[i].setAttribute("aria-valuetext", `${NAMES[i]} : ${d}°`);
          names[i].setAttribute("x", f(lx)); names[i].setAttribute("y", f(ly + 5));
          if (document.activeElement !== inputs[i]) inputs[i].value = d;
        });
        $(".hc-halves").innerHTML = angles.map((d, i) => (on[i] && ev.events[i] ? `<path class="hc-disc hc-${CLS[i]}" d="${halfDisc(d)}"/>` : "")).join("") +
          angles.map((d, i) => (on[i] ? `<path class="hc-arc hc-${CLS[i]}${ev.events[i] ? " is-holds" : ""}" d="${halfArc(d, R + 10 + 9 * i)}"/>` : "")).join("");
        $(".tri-shape").setAttribute("points", angles.map((d) => at(d, R).map((v) => f(v)).join(",")).join(" "));
        svg.classList.toggle("is-in", ev.inside); svg.classList.toggle("is-out", !ev.inside && !ev.edge); svg.classList.toggle("is-edge", !ev.inside && ev.edge);
        $(".hc-events").innerHTML = angles.map((d, i) => {
          const others = [0, 1, 2].filter((j) => j !== i).map((j) => `${NAMES[j]} ב-${ltr(`${halfOffset(d, angles[j])}°`)}`).join(", ");
          return `<li class="${ev.events[i] ? "is-holds" : ""}"><span class="hc-key hc-key-${CLS[i]}"></span>‏A${i + 1}, חצי המעגל מ-${ltr(`${d}°`)}${NB}: ${others} ${ev.events[i] ? "✓ שתיהן בפנים" : "✗"}</li>`;
        }).join("");
        const k = ev.events.filter(Boolean).length;
        $(".hc-status").innerHTML = !k ? `<span class="tri-kind is-in">אף מאורע לא מתקיים, ולכן המרכז בתוך המשולש.</span>`
          : k === 1 ? `<span class="tri-kind ${ev.edge ? "is-edge" : "is-out"}">רק ${ltr(`A${ev.events.indexOf(true) + 1}`)} מתקיים${ev.edge ? ", עם קשת של 180° בדיוק, והמרכז על צלע" : ", והמרכז מחוץ למשולש"}.</span>`
          : `<span class="tri-kind is-edge">שני מאורעות יחד${NB}: זה קורה רק כששתי נקודות מתלכדות או עומדות זו מול זו, בהסתברות 0.</span>`;
      };
      const setAngles = (next) => { angles = next.map((v) => ((Math.round(v) % 360) + 360) % 360); render(); };
      const pct = (v) => (counts.n ? `${(100 * v / counts.n).toFixed(1)}%` : "–");
      const renderCounts = () => {
        if (!counts.n) { $(".hc-counts").innerHTML = ""; $(".hc-sum").textContent = ""; return; }
        const rows = counts.a.map((v, i) => `<tr><td><span class="hc-key hc-key-${CLS[i]}"></span>‏A${i + 1}</td><td>${v.toLocaleString("en-US")}</td><td>${pct(v)}</td><td>25%</td></tr>`).join("") +
          `<tr class="is-in"><td>אף אחד, המרכז בפנים</td><td>${counts.inside.toLocaleString("en-US")}</td><td>${pct(counts.inside)}</td><td>25%</td></tr>` +
          `<tr><td>שניים יחד</td><td>${counts.both}</td><td>${pct(counts.both)}</td><td>0</td></tr>`;
        $(".hc-counts").innerHTML = `<table class="bridge-table hc-table"><thead><tr><th>המאורע</th><th>פעמים</th><th>שכיחות</th><th>צפוי</th></tr></thead><tbody>${rows}</tbody></table>`;
        const out = counts.a.reduce((t, v) => t + v, 0);
        $(".hc-sum").innerHTML = `ב-${ltr(counts.n.toLocaleString("en-US"))} משולשים אקראיים, המרכז בחוץ ${ltr(out.toLocaleString("en-US"))} פעמים, וכל פעם בדיוק אחד מ-${ltr("A1, A2, A3")} מתקיים${NB}: ` +
          `${ltr(`${pct(counts.a[0])} + ${pct(counts.a[1])} + ${pct(counts.a[2])}`)} מול ${ltr("3 · 1/4")}. המרכז בפנים ${ltr(pct(counts.inside))} מהפעמים, מול ${ltr("1/4")}. המשולש האחרון מוצג על המעגל.`;
      };
      let batch = 100;
      const seed = seedControls(box, $(".ex-clear"), (rng) => {
        const r = halfCount(batch, rng);
        r.a.forEach((v, i) => { counts.a[i] += v; });
        counts.inside += r.inside; counts.both += r.both; counts.n += r.n;
        setAngles(r.last); renderCounts();
      }, { fresh: false });
      $(".ex-draw100").addEventListener("click", () => { batch = 100; seed.draw(); });
      $(".ex-draw1000").addEventListener("click", () => { batch = 1000; seed.draw(); });
      $(".ex-clear").addEventListener("click", () => { counts.a = [0, 0, 0]; counts.inside = counts.both = counts.n = 0; renderCounts(); });
      $(".ex-reset").addEventListener("click", () => setAngles(PAGE));
      inputs.forEach((inp, i) => inp.addEventListener("change", () => { const v = Math.round(Number(inp.value)); if (Number.isFinite(v)) { const next = [...angles]; next[i] = v; setAngles(next); } else inp.value = angles[i]; }));
      box.querySelectorAll(".hc-show").forEach((c) => c.addEventListener("change", render));
      // drag: the point nearest to the finger follows it around the circle, in whole degrees
      let drag = null;
      const degAt = (e) => {
        const r = svg.getBoundingClientRect();
        const x = ((e.clientX - r.left) / r.width) * 320 - C, y = C - ((e.clientY - r.top) / r.height) * 320;
        return ((Math.round((Math.atan2(y, x) * 180) / Math.PI) % 360) + 360) % 360;
      };
      svg.addEventListener("pointerdown", (e) => {
        const d = degAt(e), dist = (i) => { const u = Math.abs(angles[i] - d); return Math.min(u, 360 - u); };
        const target = e.target.closest(".tri-pt");
        drag = target ? Number(target.dataset.i) : [0, 1, 2].reduce((b, i) => (dist(i) < dist(b) ? i : b), 0);
        svg.setPointerCapture(e.pointerId); svg.classList.add("is-dragging");
        const next = [...angles]; next[drag] = d; setAngles(next);
        e.preventDefault();
      });
      svg.addEventListener("pointermove", (e) => {
        if (drag === null) return;
        const d = degAt(e);
        if (d !== angles[drag]) { const next = [...angles]; next[drag] = d; setAngles(next); }
      });
      const end = () => { drag = null; svg.classList.remove("is-dragging"); };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      svg.addEventListener("keydown", (e) => {
        const t = e.target.closest(".tri-pt"), d = arrowStep(e);
        if (!t || !d) return;
        e.preventDefault(); e.stopPropagation();
        const i = Number(t.dataset.i), next = [...angles]; next[i] += d; setAngles(next);
      });
      render();
    },
  });

  dvqExplorers.register({
    views: { halfcirc: halfcircView },
    help: {
      halfcirc: "גוררים את P1, P2, P3 (או מקלידים זוויות) : כל חצי מעגל צבוע מתחיל בנקודה שלו נגד כיוון השעון, והרשימה אומרת אם הוא מכיל את שתי הנקודות האחרות. לכל היותר אחד מתקיים. ״100 הגרלות״ ו״1,000 הגרלות״ מוסיפים משולשים אקראיים לספירה.",
    },
    models: { halfEvents, halfCount },
  });
})();
