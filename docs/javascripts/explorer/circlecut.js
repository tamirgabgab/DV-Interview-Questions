// kinds: circlecut
//   circlecut              0092        points on a circle, every pair joined by a chord (n from 1 to 10, the points dragged on the circle or a regular polygon): every region of the disc in its own colour, the counts live (points, chords, crossing points, regions, against C(n, 4) + C(n, 2) + 1), and the chords added one at a time, each adding 1 + the number of points where it meets the earlier chords; points where three chords meet are ringed
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for the
// question tests.
(() => {
  const { answer, arrowStep, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const NMIN = 1, NMAX = 10, MERGE = 1e-7, GAP = 2;

  // --- the model (tests/0092 compares it with the generator's reference) ---------------------

  const comb = (n, k) => { if (k < 0 || k > n) return 0; let r = 1; for (let i = 0; i < k; i++) r = (r * (n - i)) / (i + 1); return Math.round(r); };
  const mcMoser = (n) => comb(n, 4) + comb(n, 2) + 1;
  const rad = (t) => (t * Math.PI) / 180;
  const pointsOf = (angles) => angles.map((t) => [Math.cos(rad(t)), Math.sin(rad(t))]);
  // every pair of points, in the order (1, 2), (1, 3), ..., (2, 3), ...
  const mcChords = (n) => { const c = []; for (let a = 0; a < n; a++) for (let b = a + 1; b < n; b++) c.push([a, b]); return c; };
  const cut = (p, q, r, s) => {
    const den = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0]);
    if (Math.abs(den) < 1e-14) return null;
    const t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / den;
    const u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / den;
    return t > 1e-9 && t < 1 - 1e-9 && u > 1e-9 && u < 1 - 1e-9 ? [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]), t] : null;
  };
  // the arrangement of the given chords: the distinct crossing points (closer than MERGE is one
  // point) and, for every chord, the crossing points on it with their place t along it
  const arrangement = (angles, chords) => {
    const P = pointsOf(angles), inner = [], on = chords.map(() => new Map());
    const index = (x, y) => {
      const k = inner.findIndex(([a, b]) => Math.abs(a - x) < MERGE && Math.abs(b - y) < MERGE);
      if (k >= 0) return k;
      inner.push([x, y]);
      return inner.length - 1;
    };
    for (let i = 0; i < chords.length; i++) for (let j = i + 1; j < chords.length; j++) {
      const [a, b] = chords[i], [c, d] = chords[j];
      if (new Set([a, b, c, d]).size < 4) continue;
      const h = cut(P[a], P[b], P[c], P[d]);
      if (!h) continue;
      const k = index(h[0], h[1]);
      on[i].set(k, h[2]);
      on[j].set(k, cut(P[c], P[d], P[a], P[b])[2]);
    }
    return { P, inner, on };
  };
  // { V, E, regions, crossings, triples }: Euler's formula on the planar graph of the points, the
  // crossings, the chord pieces and the n arcs (regions inside the disc = E - V + 1)
  const mcCount = (angles, chords = mcChords(angles.length)) => {
    const n = angles.length;
    if (!n) return { V: 0, E: 0, regions: 1, crossings: 0, triples: [] };
    const { inner, on } = arrangement(angles, chords);
    const V = n + inner.length, E = n + on.reduce((s, m) => s + m.size + 1, 0);
    const through = inner.map((_, k) => on.filter((m) => m.has(k)).length);
    return { V, E, regions: E - V + 1, crossings: inner.length, triples: inner.filter((_, k) => through[k] >= 3) };
  };
  // the chords added one at a time: each adds 1 + the number of distinct points where it meets
  // the chords drawn before it
  const mcIncrements = (angles) => {
    const chords = mcChords(angles.length), out = [];
    let total = 1;
    chords.forEach((c, i) => {
      const before = mcCount(angles, chords.slice(0, i + 1)).regions;
      const k = before - total - 1;
      total = before;
      out.push({ chord: c, meets: k, added: k + 1, total });
    });
    return out;
  };
  // the regions as closed walks, kept on their left (the outside of the disc dropped)
  const mcFaces = (angles, chords = mcChords(angles.length)) => {
    const n = angles.length;
    if (!n) return [];
    const { P, inner, on } = arrangement(angles, chords);
    const pos = P.concat(inner), edges = [];
    const order = angles.map((_, i) => i).sort((a, b) => (((angles[a] % 360) + 360) % 360) - (((angles[b] % 360) + 360) % 360));
    for (let k = 0; k < n; k++) edges.push(["arc", order[k], order[(k + 1) % n]]);
    chords.forEach(([a, b], i) => {
      const seq = [a, ...[...on[i].entries()].sort((x, y) => x[1] - y[1]).map(([k]) => n + k), b];
      for (let j = 0; j + 1 < seq.length; j++) edges.push(["chord", seq[j], seq[j + 1]]);
    });
    const outAngle = (e, fwd) => {
      const [kind, u, v] = edges[e], s = fwd ? u : v, t = fwd ? v : u;
      if (kind === "arc") return rad(angles[s]) + (fwd ? Math.PI / 2 : -Math.PI / 2);
      return Math.atan2(pos[t][1] - pos[s][1], pos[t][0] - pos[s][0]);
    };
    const norm = (a) => ((a % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
    const ring = new Map();
    edges.forEach(([, u, v], e) => {
      if (!ring.has(u)) ring.set(u, []);
      if (!ring.has(v)) ring.set(v, []);
      ring.get(u).push([e, true]);
      ring.get(v).push([e, false]);
    });
    ring.forEach((hs) => hs.sort((x, y) => norm(outAngle(...x)) - norm(outAngle(...y))));
    const seen = new Set(), found = [];
    edges.forEach((_, e0) => [true, false].forEach((f0) => {
      if (seen.has(`${e0}${f0}`)) return;
      const walk = [];
      let e = e0, f = f0;
      while (!seen.has(`${e}${f}`)) {
        seen.add(`${e}${f}`);
        const [kind, u, v] = edges[e], a = f ? u : v, b = f ? v : u;
        walk.push([kind, a, b, f]);
        const hs = ring.get(b), i = hs.findIndex(([x, y]) => x === e && y === !f);
        [e, f] = hs[(i - 1 + hs.length) % hs.length];
      }
      found.push(walk);
    }));
    const sample = (walk) => {
      const out = [];
      walk.forEach(([kind, a, b, f]) => {
        if (kind === "chord") { out.push(pos[a]); return; }
        const t0 = rad(angles[a]), t1 = rad(angles[b]);
        let span = f ? norm(t1 - t0) : -norm(t0 - t1);
        if (Math.abs(span) < 1e-12) span = f ? 2 * Math.PI : -2 * Math.PI;
        const steps = Math.max(2, Math.floor(Math.abs(span) / 0.08));
        for (let s = 0; s < steps; s++) out.push([Math.cos(t0 + (span * s) / steps), Math.sin(t0 + (span * s) / steps)]);
      });
      return out;
    };
    const area = (pts) => pts.reduce((s, p, i) => { const q = pts[(i + 1) % pts.length]; return s + p[0] * q[1] - q[0] * p[1]; }, 0) / 2;
    return found.map((w) => ({ walk: w, pts: sample(w) })).filter((x) => area(x.pts) > 1e-12).map((x) => ({ ...x, pos }));
  };
  // the starting points of the box for n points: spread around the circle, nudged off the
  // regular polygon so no three chords meet
  const NUDGE = [0, 9, -6, 11, -8, 5, -10, 7, -4, 8];
  const mcDefault = (n) => Array.from({ length: n }, (_, k) => (Math.round((90 + (360 * k) / n + (NUDGE[k] * 6) / Math.max(n, 6)) * 2) / 2) % 360);
  const mcRegular = (n) => Array.from({ length: n }, (_, k) => 90 + (360 * k) / n);

  // --- the drawing -----------------------------------------------------------------------------

  const R = 120, PAD = 30, SIZE = 2 * (R + PAD), C = R + PAD;
  const xy = (p) => [C + R * p[0], C - R * p[1]];
  const COLS = 6;
  const colours = (faces) => {
    const side = new Map();
    faces.forEach((f, i) => f.walk.forEach(([kind, a, b]) => {
      if (kind !== "chord") return;
      const k = `${Math.min(a, b)}.${Math.max(a, b)}`;
      if (!side.has(k)) side.set(k, []);
      side.get(k).push(i);
    }));
    const nb = faces.map(() => new Set());
    side.forEach((o) => { for (const i of o) for (const j of o) if (i !== j) nb[i].add(j); });
    const col = [];
    faces.forEach((_, v) => {
      const used = new Set([...nb[v]].filter((u) => u < v).map((u) => col[u]));
      for (let j = 0; j < COLS; j++) if (!used.has((v + j) % COLS)) { col[v] = (v + j) % COLS; break; }
    });
    return col;
  };
  const facePath = (f, angles) => {
    let d = "";
    f.walk.forEach(([kind, a, b, fwd]) => {
      const [x0, y0] = xy(f.pos[a]), [x1, y1] = xy(f.pos[b]);
      if (!d) d = `M${x0.toFixed(1)},${y0.toFixed(1)}`;
      if (kind === "chord") { d += `L${x1.toFixed(1)},${y1.toFixed(1)}`; return; }
      const t0 = ((angles[a] % 360) + 360) % 360, t1 = ((angles[b] % 360) + 360) % 360;
      let span = fwd ? (((t1 - t0) % 360) + 360) % 360 : (((t0 - t1) % 360) + 360) % 360;
      if (span === 0) span = 360;
      const sweep = fwd ? 0 : 1;
      if (span === 360) d += `A${R},${R} 0 0 ${sweep} ${(2 * C - x0).toFixed(1)},${(2 * C - y0).toFixed(1)}A${R},${R} 0 0 ${sweep} ${x1.toFixed(1)},${y1.toFixed(1)}`;
      else d += `A${R},${R} 0 ${span > 180 ? 1 : 0} ${sweep} ${x1.toFixed(1)},${y1.toFixed(1)}`;
    });
    return `${d}Z`;
  };
  const discSvg = (angles, shown, { newChord = null, later = [], hits = [], triples = [], handles }) => {
    const faces = mcFaces(angles, shown), col = colours(faces), P = pointsOf(angles), n = angles.length;
    const label = `${n} נקודות על מעגל, ${shown.length} קווים, ${faces.length} חלקים`;
    let s = "";
    faces.forEach((f, i) => { s += `<path class="mc-reg mc-c${col[i]}" d="${facePath(f, angles)}"/>`; });
    s += `<circle class="mc-ring" cx="${C}" cy="${C}" r="${R}"/>`;
    const line = ([a, b], cls) => { const [x1, y1] = xy(P[a]), [x2, y2] = xy(P[b]); return `<line class="${cls}" x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}"/>`; };
    later.forEach((c) => { s += line(c, "mc-chord is-later"); });
    shown.forEach((c) => { if (!newChord || c[0] !== newChord[0] || c[1] !== newChord[1]) s += line(c, "mc-chord"); });
    if (newChord) s += line(newChord, "mc-chord is-new");
    hits.forEach((p) => { const [x, y] = xy(p); s += `<circle class="mc-hit" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4.5"/>`; });
    triples.forEach((p) => { const [x, y] = xy(p); s += `<circle class="mc-triple" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="8"/>`; });
    P.forEach((p, k) => {
      const [x, y] = xy(p), [lx, ly] = [C + (R + 18) * p[0], C - (R + 18) * p[1]];
      const deg = Math.round((((angles[k] % 360) + 360) % 360) * 2) / 2;
      s += handles
        ? `<g class="mc-h" data-k="${k}" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="359.5" aria-valuenow="${deg}" aria-label="נקודה ${k + 1}, ב-${deg} מעלות${NB}: גוררים על המעגל, או מזיזים בחיצים (עם Shift בקפיצות של 10)">` +
          `<circle class="mc-hring" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="13"/><circle class="mc-pt" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="7"/></g>`
        : `<circle class="mc-pt" cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="6"/>`;
      s += `<text class="mc-plab" x="${lx.toFixed(1)}" y="${(ly + 4.5).toFixed(1)}" text-anchor="middle">${k + 1}</text>`;
    });
    return { svg: `<svg class="figure mc-fig mc-live" viewBox="0 0 ${SIZE} ${SIZE}" role="group" aria-label="${label}">${s}</svg>`, inner: s, label, regions: faces.length };
  };

  // --- the box ---------------------------------------------------------------------------------

  const view = () => ({
    mount(box) {
      const n0 = Math.min(NMAX, Math.max(NMIN, Number(box.dataset.n) || 5));
      const where0 = box.dataset.where === "regular" ? "regular" : "free";
      const show0 = box.dataset.show === "steps" ? "steps" : "all";
      const parsed = (box.dataset.angles || "").split(/[\s,]+/).filter(Boolean).map(Number);
      const a0 = parsed.length === n0 && parsed.every((x) => Number.isFinite(x)) ? parsed : mcDefault(n0);
      const st = { angles: where0 === "regular" ? mcRegular(n0) : a0.slice(), k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>נקודות</span><select class="mc-n" aria-label="כמה נקודות על המעגל">${Array.from({ length: NMAX - NMIN + 1 }, (_, i) => `<option value="${i + NMIN}">${i + NMIN}</option>`).join("")}</select></label>` +
        `<label><span>המיקום</span><select class="mc-where" aria-label="איפה הנקודות"><option value="free">חופשי, גוררים</option><option value="regular">מצולע משוכלל</option></select></label>` +
        `<label><span>הקווים</span><select class="mc-show" aria-label="כל הקווים, או קו אחר קו"><option value="all">כולם</option><option value="steps">קו אחר קו</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row mc-play">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הקו הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הקו הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הקווים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<div class="mc-stage"></div>` +
        `<span class="viz-legend mc-legend"><span><i class="mc-key-reg"></i>חלק של העיגול</span><span class="mc-stepkey"><i class="mc-key-new"></i>הקו החדש</span><span class="mc-stepkey"><i class="mc-key-hit"></i>איפה הוא פוגש קווים קודמים</span><span class="mc-stepkey"><i class="mc-key-later"></i>קו שעוד לא צויר</span><span><i class="mc-key-triple"></i>שלושה קווים או יותר באותה נקודה</span></span>` +
        `<p class="mc-counts" aria-live="polite"></p>` +
        `<p class="ex-summary mc-sum"></p>` +
        `<p class="mc-note"></p>`;
      const $ = (q) => box.querySelector(q);
      $(".mc-n").value = String(n0);
      $(".mc-where").value = where0;
      $(".mc-show").value = show0;
      const chordsAll = () => mcChords(st.angles.length);
      const steps = () => $(".mc-show").value === "steps";
      const draw = () => {
        const n = st.angles.length, all = chordsAll(), T = all.length, free = $(".mc-where").value === "free";
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = steps() ? st.k : T, shown = all.slice(0, k);
        $(".mc-play").hidden = !steps();
        box.querySelectorAll(".mc-stepkey").forEach((el) => { el.hidden = !steps(); });
        $(".ex-pos").textContent = steps() ? `קו ${k} מתוך ${T}` : "";   // no counter: the scrubber hides too
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        const cnt = mcCount(st.angles, shown);
        const nc = steps() && k > 0 ? all[k - 1] : null;
        let hits = [];
        if (nc) {   // the points where the new chord meets the earlier ones
          const { inner, on } = arrangement(st.angles, shown);
          hits = [...on[k - 1].keys()].map((i) => inner[i]);
        }
        const d = discSvg(st.angles, shown, { newChord: nc, later: steps() ? all.slice(k) : [], hits, triples: cnt.triples, handles: free });
        const had = document.activeElement && document.activeElement.closest && document.activeElement.closest(".mc-h");
        const keep = had && box.contains(had) ? had.dataset.k : null;   // a redraw keeps the focused point focused
        // the svg itself stays (the page wraps a new figure with its enlarge button, which
        // would move it and drop the focus); only its content is redrawn
        const live = $(".mc-stage svg.mc-live");
        if (live) { live.innerHTML = d.inner; live.setAttribute("aria-label", d.label); } else $(".mc-stage").innerHTML = d.svg;
        if (keep !== null) { const h = $(`.mc-h[data-k="${keep}"]`); if (h) h.focus({ preventScroll: true }); }
        const full = mcCount(st.angles), formula = mcMoser(n);
        $(".mc-counts").innerHTML = `<span>נקודות <b>${n}</b></span><span>קווים <b>${shown.length}</b></span><span>נקודות חיתוך <b>${cnt.crossings}</b></span><span>חלקים <b>${d.regions}</b></span>` +
          `<span>הנוסחה <b>${formula}</b></span>`;
        let sum, note;
        if (steps() && k === 0) sum = `עוד אין קווים${NB}: העיגול הוא חלק אחד.`;
        else if (steps()) {
          const m = hits.length;
          sum = `הקו בין ${ltr(nc[0] + 1)} ל-${ltr(nc[1] + 1)} פוגש ${m === 0 ? "אף קו קודם לא" : m === 1 ? "קו קודם בנקודה אחת" : `קווים קודמים ב-${ltr(m)} נקודות`}, ולכן נחתך ל-${ltr(m + 1)} ${m ? "קטעים" : "קטע אחד"} ומוסיף ${ltr(m + 1)} ${m ? "חלקים" : "חלק"}. עכשיו ${ltr(d.regions)} חלקים.`;
        } else sum = `${ltr(n)} נקודות ו-${ltr(T)} קווים${NB}: העיגול מתחלק ל-${ltr(d.regions)} חלקים.`;
        if (full.triples.length) note = `${full.triples.length === 1 ? "בנקודה אחת" : `ב-${ltr(full.triples.length)} נקודות`} נפגשים שלושה קווים או יותר (מסומן בעיגול), ולכן יש ${ltr(full.regions)} חלקים ולא ${ltr(formula)}, כמו בנוסחה למצב כללי.`;
        else note = `אין שלושה קווים שנפגשים באותה נקודה, ולכן מספר החלקים הוא בדיוק הנוסחה${NB}: ${ltr(`C(${n}, 4) + C(${n}, 2) + 1`)}, כלומר ${ltr(`${comb(n, 4)} + ${comb(n, 2)} + 1 = ${formula}`)}.`;
        $(".mc-sum").innerHTML = sum;
        $(".mc-note").innerHTML = note;
        answer(box, !steps() || k === T ? `${ltr(full.regions)} חלקים${full.regions === formula ? ", כמו בנוסחה." : `, הנוסחה למצב כללי נותנת ${ltr(formula)}.`}` : null, ".mc-sum");
      };
      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= chordsAll().length, restart: () => { st.k = 0; draw(); } });
      const setN = () => {
        stop();
        const n = Number($(".mc-n").value);
        st.angles = $(".mc-where").value === "regular" ? mcRegular(n) : n === n0 && where0 === "free" ? a0.slice() : mcDefault(n);
        st.k = 0;
        draw();
      };
      $(".mc-n").addEventListener("change", setN);
      $(".mc-where").addEventListener("change", setN);
      $(".mc-show").addEventListener("change", () => { stop(); st.k = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = chordsAll().length; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop();
        $(".mc-n").value = String(n0); $(".mc-where").value = where0; $(".mc-show").value = show0;
        st.angles = where0 === "regular" ? mcRegular(n0) : a0.slice();
        st.k = 0;
        draw();
      });

      // dragging a point along the circle (half degrees; at least GAP degrees from the others)
      const stage = $(".mc-stage");
      const place = (k, deg) => {
        let t = ((Math.round(deg * 2) / 2) % 360 + 360) % 360;
        const clash = st.angles.some((u, j) => j !== k && Math.abs(((t - u + 540) % 360) - 180) < GAP);
        if (clash) return false;
        st.angles[k] = t;
        return true;
      };
      let drag = null;
      const at = (e) => {
        const svg = stage.querySelector("svg"), p = svg.createSVGPoint();
        p.x = e.clientX; p.y = e.clientY;
        const m = svg.getScreenCTM(), q = m ? p.matrixTransform(m.inverse()) : { x: C, y: C };
        return (Math.atan2(C - q.y, q.x - C) * 180) / Math.PI;
      };
      const changed = () => { draw(); box.dispatchEvent(new Event("input", { bubbles: true })); };
      stage.addEventListener("pointerdown", (e) => {
        const h = e.target.closest(".mc-h");
        if (!h) return;
        stop();
        drag = Number(h.dataset.k);
        stage.setPointerCapture(e.pointerId);
        stage.querySelector("svg").classList.add("is-dragging");
        e.preventDefault();
      });
      stage.addEventListener("pointermove", (e) => { if (drag !== null && place(drag, at(e))) { draw(); stage.querySelector("svg").classList.add("is-dragging"); } });
      const end = () => {
        if (drag === null) return;
        const k = drag;
        drag = null;
        changed();
        const h = stage.querySelector(`.mc-h[data-k="${k}"]`);
        if (h) h.focus({ preventScroll: true });
      };
      stage.addEventListener("pointerup", end);
      stage.addEventListener("pointercancel", end);
      stage.addEventListener("keydown", (e) => {
        const h = e.target.closest(".mc-h");
        if (!h) return;
        const d = arrowStep(e);
        if (!d) return;
        e.preventDefault(); e.stopPropagation();
        const k = Number(h.dataset.k);
        let t = st.angles[k] + d;                           // past a neighbour that is too close
        for (let i = 0; i < 360 && !place(k, t); i++) t += Math.sign(d);
        changed();
        const again = stage.querySelector(`.mc-h[data-k="${k}"]`);
        if (again) again.focus({ preventScroll: true });
      });
      // the dragged points and the step ride in the link after the controls
      box.dvqExtra = {
        get: () => {
          const moved = $(".mc-where").value === "free" && st.angles.join(",") !== (Number($(".mc-n").value) === n0 && where0 === "free" ? a0 : mcDefault(Number($(".mc-n").value))).join(",");
          const parts = [];
          if (moved) parts.push(`a${st.angles.map((x) => Math.round(x * 2)).join("_")}`);   // half degrees
          if (steps() && st.k) parts.push(`k${st.k}`);
          return parts.join(".");
        },
        set: (text) => {
          for (const part of text.split(".")) {
            if (/^k\d+$/.test(part)) { st.k = Number(part.slice(1)); continue; }
            if (/^a\d+(_\d+)*$/.test(part)) {
              const v = part.slice(1).split("_").map((x) => Number(x) / 2);
              if (v.length !== st.angles.length || v.some((x) => !Number.isFinite(x) || x < 0 || x >= 360)) return false;
              st.angles = v;
              continue;
            }
            if (part) return false;
          }
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { circlecut: view },
    help: {
      circlecut: "בוחרים כמה נקודות, ואם הן חופשיות או קודקודים של מצולע משוכלל. נקודה חופשית גוררים לאורך המעגל, או מזיזים בחיצים אחרי לחיצה עליה (Shift מזיז ב-10 מעלות). כל חלק של העיגול צבוע בצבע משלו, ומתחת סופרים נקודות, קווים, נקודות חיתוך וחלקים, מול הנוסחה. ב\"קו אחר קו\" הקווים נוספים אחד אחד : הקו החדש מודגש, הנקודות שבהן הוא פוגש קווים קודמים מסומנות, והוא מוסיף חלק אחד ועוד חלק לכל נקודה כזו. נקודה שבה נפגשים שלושה קווים מסומנת בעיגול : שם יש פחות חלקים מהנוסחה.",
    },
    models: { mcMoser, mcChords, mcCount, mcIncrements, mcFaces: (a) => mcFaces(a).length, mcDefault, mcRegular },
  });
})();
