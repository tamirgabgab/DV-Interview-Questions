// kinds: strip
//   strip                  0030        drag the spider and the fly on their walls: the periodic strip and the path
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { EPS, W, f, ltr } = dvqExplorers.lib;

  // Strip (0030): the four lateral faces of the box [0, a] x [0, b] x [0, h] unrolled along
  // x, with the perimeter coordinate p running bottom -> sideB -> top -> side0 (period
  // 2(b + h)). An end face folded flat on one of its edges puts its point at x = -gap (or
  // a + gap); the shortest valid straight line between an image of S and an image of F is
  // the path. The same math as tools/figures/q0030.py and the page code.
  const STRIP_FACES = ["bottom", "sideB", "top", "side0"];
  const stripPeriod = (b, h) => 2 * (b + h);
  const stripBands = (b, h) => ({ bottom: [0, b], sideB: [b, b + h], top: [b + h, 2 * b + h], side0: [2 * b + h, 2 * (b + h)] });
  // The four images of the point (y, z) of an end face: the edge it leaves through, its
  // distance to that edge, the p of the foot on the edge and the p-range of the edge.
  const stripImages = (y, z, b, h) => [
    { edge: "bottom", gap: z, p: y, lo: 0, hi: b },
    { edge: "sideB", gap: b - y, p: b + z, lo: b, hi: b + h },
    { edge: "top", gap: h - z, p: b + h + (b - y), lo: b + h, hi: 2 * b + h },
    { edge: "side0", gap: y, p: 2 * b + h + (h - z), lo: 2 * b + h, hi: 2 * (b + h) },
  ];
  const stripMod = (p, b, h) => { const P = stripPeriod(b, h); return ((p % P) + P) % P; };
  // The (y, z) of an end face at perimeter coordinate p on the given edge.
  const stripEdgePoint = (edge, p, b, h) => {
    p = stripMod(p, b, h);
    if (edge === "bottom") return [p, 0];
    if (edge === "sideB") return [b, p - b];
    if (edge === "top") return [2 * b + h - p, h];
    return [0, 2 * b + 2 * h - p];
  };
  // The 3D point of (x, p) on the lateral faces.
  const stripPoint3 = (x, p, b, h) => {
    const q = stripMod(p, b, h);
    if (q < b) return [x, q, 0];
    if (q < b + h) return [x, b, q - b];
    if (q < 2 * b + h) return [x, 2 * b + h - q, h];
    return [x, 0, 2 * b + 2 * h - q];
  };
  const stripBandOf = (p, b, h) => {
    const q = stripMod(p, b, h), bands = stripBands(b, h);
    return STRIP_FACES.find((n) => bands[n][0] <= q && q < bands[n][1]) || "side0";
  };
  // The lateral faces a straight strip line crosses from pFrom to pTo, in order.
  const stripFacesBetween = (pFrom, pTo, b, h) => {
    const P = stripPeriod(b, h), step = pTo >= pFrom ? 1 : -1;
    const cuts = [];
    for (let k = -2; k <= 2; k++) [0, b, b + h, 2 * b + h].forEach((lo) => cuts.push(lo + k * P));
    cuts.sort((u, v) => u - v);
    const at = (p) => stripBandOf(p + step * 1e-7, b, h);          // just past the cut, in the direction of travel
    const out = [at(pFrom)];
    let p = pFrom;
    for (;;) {
      const next = step > 0 ? cuts.find((c) => c > p + EPS) : [...cuts].reverse().find((c) => c < p - EPS);
      if (next === undefined || (step > 0 ? next >= pTo - EPS : next <= pTo + EPS)) return out;
      p = next;
      out.push(at(p));
    }
  };
  // Every straight line of the strip method (4 x 4 x 3), shortest first.
  const stripLines = (a, b, h, y0, z0, y1, z1) => {
    const P = stripPeriod(b, h), out = [];
    stripImages(y0, z0, b, h).forEach((s) => stripImages(y1, z1, b, h).forEach((f) => [-1, 0, 1].forEach((k) => {
      const dx = a + f.gap + s.gap, dp = f.p + k * P - s.p;
      const pExit = s.p + (dp * s.gap) / dx, pEnter = s.p + (dp * (s.gap + a)) / dx;
      const valid = s.lo - EPS <= pExit && pExit <= s.hi + EPS &&
        f.lo + k * P - EPS <= pEnter && pEnter <= f.hi + k * P + EPS;
      out.push({ length: Math.hypot(dx, dp), sEdge: s.edge, fEdge: f.edge, k, xs: -s.gap, ps: s.p,
                 xf: a + f.gap, pf: f.p + k * P, dx, dp, pExit, pEnter, valid });
    })));
    return out.sort((u, v) => u.length - v.length || u.k - v.k);
  };
  // The best line with the path point by point: faces, 3D points and segment lengths.
  const stripBest = (a, b, h, y0, z0, y1, z1) => {
    const lines = stripLines(a, b, h, y0, z0, y1, z1);
    const c = lines.find((l) => l.valid);
    const faces = ["end0", ...stripFacesBetween(c.pExit, c.pEnter, b, h), "enda"];
    const P = stripPeriod(b, h);
    const ts = [-c.xs / c.dx];                                    // where the line crosses x = 0
    const cuts = [];
    for (let k = -2; k <= 2; k++) [0, b, b + h, 2 * b + h].forEach((lo) => cuts.push(lo + k * P));
    cuts.filter((q) => (q - c.pExit) * (q - c.pEnter) < -EPS).sort((u, v) => u - v)
      .forEach((q) => ts.push((q - c.ps) / c.dp));
    ts.sort((u, v) => u - v);
    ts.push((a - c.xs) / c.dx);                                   // where it crosses x = a
    const pts = [[0, y0, z0], ...ts.map((t) => stripPoint3(c.xs + t * c.dx, c.ps + t * c.dp, b, h)), [a, y1, z1]];
    pts[1][0] = 0; pts[pts.length - 2][0] = a;                    // exact on the two walls
    const segs = [ts[0], ...ts.slice(1).map((t, i) => t - ts[i]), 1 - ts[ts.length - 1]].map((t) => t * c.length);
    const exit = stripEdgePoint(c.sEdge, c.pExit, b, h), enter = stripEdgePoint(c.fEdge, c.pEnter, b, h);
    return { line: c, lines, faces, pts, segs, exit: [0, ...exit], enter: [a, ...enter],
             valid: lines.filter((l) => l.valid).length };
  };

  // The strip box (0030): two wall panels where S and F can be dragged, sliders for the box,
  // and the periodic strip redrawn on every change with the eight images, the 48 lines and
  // the shortest valid one; the summary lists the path face by face.
  const stripView = () => ({
    mount(box) {
      const d = box.dataset;
      const defaults = { a: Number(d.a || 30), b: Number(d.b || 12), h: Number(d.h || 12),
                         y0: Number(d.y0 || 6), z0: Number(d.z0 || 11), y1: Number(d.y1 || 6), z1: Number(d.z1 || 1) };
      const st = { ...defaults };
      const HEB = { bottom: "הרצפה", sideB: "הקיר הרחוק", top: "התקרה", side0: "הקיר הקרוב", end0: "הקיר של העכביש", enda: "הקיר של הזבוב" };
      const num = (v) => { const s = Number(v).toFixed(2); return s.replace(/\.?0+$/, ""); };
      const p3 = (p) => `(${p.map(num).join(", ")})`;
      box.innerHTML =
        `<div class="ex-controls">` +
        [["a", "האורך a", 1, 60, 1], ["b", "הרוחב b", 1, 30, 1], ["h", "הגובה h", 1, 30, 1]].map(([k, label, min, max, step]) =>
          `<label><span>${label}</span><input type="range" class="ex-${k}" min="${min}" max="${max}" step="${step}" value="${st[k]}" dir="ltr"><output class="out-${k}"></output></label>`).join("") +
        `<label>הקווים <select class="ex-show"><option value="valid" selected>החוקיים</option><option value="all">כל 48</option><option value="best">הקצר בלבד</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="strip-walls">` +
        `<div class="strip-wall"><p>הקיר של העכביש, ‏<bdi dir="ltr">x = 0</bdi> : גררו את S</p><svg class="figure wall-s" role="img" aria-label="הקיר של העכביש"></svg>` +
        `<p class="strip-coords" dir="ltr"><label>y<sub>0</sub> <input type="number" class="ex-y0" step="0.25" min="0"></label> ` +
        `<label>z<sub>0</sub> <input type="number" class="ex-z0" step="0.25" min="0"></label></p></div>` +
        `<div class="strip-wall"><p>הקיר של הזבוב, ‏<bdi dir="ltr">x = a</bdi> : גררו את F</p><svg class="figure wall-f" role="img" aria-label="הקיר של הזבוב"></svg>` +
        `<p class="strip-coords" dir="ltr"><label>y<sub>1</sub> <input type="number" class="ex-y1" step="0.25" min="0"></label> ` +
        `<label>z<sub>1</sub> <input type="number" class="ex-z1" step="0.25" min="0"></label></p></div></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">הרצועה המחזורית : הדמויות של S משמאל, של F מימין, והקווים ביניהן</p>` +
        `<div class="strip-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>S והדמות הנבחרת שלו</span><span><i class="s2"></i>F והדמות הנבחרת שלו</span>` +
        `<span><i class="ink"></i>שאר הדמויות</span><span><i class="box-path"></i>המסלול הקצר ביותר</span>` +
        `<span><i class="strip-valid"></i>קו חוקי אחר</span><span><i class="strip-faint"></i>קו שנפסל</span>` +
        `<span><i class="s3"></i>צלעות היציאה והכניסה, והנקודות עליהן</span></span>` +
        `<p class="ex-title">המסלול, פאה אחרי פאה</p><div class="strip-segments"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const show = $(".ex-show"), summary = $(".ex-summary"), chart = $(".strip-chart"), segsBox = $(".strip-segments");
      const walls = { s: $(".wall-s"), f: $(".wall-f") };
      const inputs = {};
      ["a", "b", "h", "y0", "z0", "y1", "z1"].forEach((k) => { inputs[k] = $(`.ex-${k}`); });

      const clamp = () => {
        st.y0 = Math.min(Math.max(st.y0, 0), st.b); st.y1 = Math.min(Math.max(st.y1, 0), st.b);
        st.z0 = Math.min(Math.max(st.z0, 0), st.h); st.z1 = Math.min(Math.max(st.z1, 0), st.h);
      };
      // A wall panel: y to the right, z up; the hinge edge of the best line and its point.
      const wallSvg = (svg, who, res) => {
        const { b, h } = st, S = 11, pad = 26, W = b * S + 2 * pad, Hh = h * S + 2 * pad;
        const X = (y) => pad + y * S, Y = (z) => pad + (h - z) * S;
        const l = res.line, edge = who === "s" ? l.sEdge : l.fEdge, pt = who === "s" ? res.exit : res.enter;
        const me = who === "s" ? [st.y0, st.z0] : [st.y1, st.z1];
        const edges = { bottom: [[0, 0], [b, 0]], sideB: [[b, 0], [b, h]], top: [[0, h], [b, h]], side0: [[0, 0], [0, h]] };
        const [[ey0, ez0], [ey1, ez1]] = edges[edge];
        svg.setAttribute("viewBox", `0 0 ${W} ${Hh}`);
        svg.innerHTML =
          `<rect class="box-end" x="${X(0)}" y="${Y(h)}" width="${f(b * S)}" height="${f(h * S)}"/>` +
          `<line class="s3-line" x1="${f(X(ey0))}" y1="${f(Y(ez0))}" x2="${f(X(ey1))}" y2="${f(Y(ez1))}" stroke-width="5"><title>צלע ${who === "s" ? "היציאה" : "הכניסה"} : ${HEB[edge]}</title></line>` +
          `<line class="box-path" x1="${f(X(me[0]))}" y1="${f(Y(me[1]))}" x2="${f(X(pt[1]))}" y2="${f(Y(pt[2]))}" stroke-width="2.5"/>` +
          `<circle class="s3-dot" cx="${f(X(pt[1]))}" cy="${f(Y(pt[2]))}" r="4"><title>${who === "s" ? "נקודת היציאה" : "נקודת הכניסה"} ${p3(pt)}</title></circle>` +
          `<circle class="${who === "s" ? "s1" : "s2"}-dot wall-pt" cx="${f(X(me[0]))}" cy="${f(Y(me[1]))}" r="8"><title>${who.toUpperCase()} = ${p3(who === "s" ? [0, ...me] : [st.a, ...me])}</title></circle>` +
          `<text class="legend" x="${f(X(b / 2))}" y="${Hh - 6}" text-anchor="middle">y</text>` +
          `<text class="legend" x="${pad - 12}" y="${f(Y(h / 2) + 4)}" text-anchor="middle">z</text>` +
          `<text class="legend" x="${f(X(0))}" y="${Hh - 6}" text-anchor="middle" style="font-size:10px">0</text>` +
          `<text class="legend" x="${f(X(b))}" y="${Hh - 6}" text-anchor="middle" style="font-size:10px">${b}</text>` +
          `<text class="legend" x="${pad - 12}" y="${f(Y(h) + 4)}" text-anchor="middle" style="font-size:10px">${h}</text>`;
        svg.dataset.pad = pad; svg.dataset.s = S; svg.dataset.w = W; svg.dataset.h = Hh;
      };
      // The strip: p up, x to the right, one period of the lateral faces with a band of b
      // above and below for the shifted images.
      const stripSvg = (res) => {
        const { a, b, h } = st, P = stripPeriod(b, h);
        const bands = stripBands(b, h);
        const xmin = -h - 2, xmax = a + h + 2, pmin = -b, pmax = P + b;
        const S = Math.min(640 / (xmax - xmin), 420 / (pmax - pmin));
        const padL = 30, padT = 14, padR = 48, padB = 22;
        const W = (xmax - xmin) * S + padL + padR, Hh = (pmax - pmin) * S + padT + padB;
        const X = (x) => padL + (x - xmin) * S, Y = (p) => padT + (pmax - p) * S;
        let s = `<svg class="figure strip-live" viewBox="0 0 ${f(W)} ${f(Hh)}" role="img" aria-label="הרצועה המחזורית עם הדמויות של העכביש ושל הזבוב והקווים ביניהן">`;
        [-1, 0, 1].forEach((k) => STRIP_FACES.forEach((name) => {
          const lo = Math.max(bands[name][0] + k * P, pmin), hi = Math.min(bands[name][1] + k * P, pmax);
          if (hi <= lo) return;
          s += `<rect class="${k === 0 ? "box-face" : "box-copy"}" x="${f(X(0))}" y="${f(Y(hi))}" width="${f(a * S)}" height="${f((hi - lo) * S)}"><title>${HEB[name]}${k === 0 ? "" : " (עותק מחזורי)"}</title></rect>`;
          if (k === 0 && (hi - lo) * S > 14) s += `<text class="legend" x="${f(X(0) + 6)}" y="${f(Y(hi) + 14)}" style="font-size:12px">${name}</text>`;
        }));
        s += `<line class="axis-c" x1="${f(X(0))}" x2="${f(X(0))}" y1="${f(Y(pmin))}" y2="${f(Y(pmax))}" stroke-width="1.5"/>` +
             `<line class="axis-c" x1="${f(X(a))}" x2="${f(X(a))}" y1="${f(Y(pmin))}" y2="${f(Y(pmax))}" stroke-width="1.5"/>` +
             `<line class="ink-line" x1="${f(X(xmin))}" x2="${f(X(xmax))}" y1="${f(Y(0))}" y2="${f(Y(0))}" stroke-width="1" stroke-dasharray="4 3"/>` +
             `<line class="ink-line" x1="${f(X(xmin))}" x2="${f(X(xmax))}" y1="${f(Y(P))}" y2="${f(Y(P))}" stroke-width="1" stroke-dasharray="4 3"/>` +
             `<text class="legend" x="${f(X(0))}" y="${f(Hh - 6)}" text-anchor="middle" style="font-size:12px">x = 0</text>` +
             `<text class="legend" x="${f(X(a))}" y="${f(Hh - 6)}" text-anchor="middle" style="font-size:12px">x = ${a}</text>` +
             `<text class="legend" x="${f(X(xmax) + 4)}" y="${f(Y(0) - 3)}" style="font-size:10px">p = 0</text>` +
             `<text class="legend" x="${f(X(xmax) + 4)}" y="${f(Y(P) - 3)}" style="font-size:10px">p = ${P}</text>`;
        const mode = show.value, best = res.line;
        const seg = (l, cls, w) =>
          `<line class="${cls}" x1="${f(X(l.xs))}" y1="${f(Y(l.ps))}" x2="${f(X(l.xf))}" y2="${f(Y(l.pf))}" stroke-width="${w}">` +
          `<title>S דרך ${HEB[l.sEdge]}, F דרך ${HEB[l.fEdge]}${l.k ? `, k = ${l.k}` : ""} : ${num(l.length)}${l.valid ? "" : ", נפסל"}</title></line>`;
        if (mode === "all") res.lines.filter((l) => !l.valid).forEach((l) => { s += seg(l, "strip-faint", 1); });
        if (mode !== "best") res.lines.filter((l) => l.valid && l !== best).forEach((l) => { s += seg(l, "strip-valid", 1.3); });
        const sImg = stripImages(st.y0, st.z0, b, h), fImg = stripImages(st.y1, st.z1, b, h);
        const sEdge = sImg.find((i) => i.edge === best.sEdge), fEdge = fImg.find((i) => i.edge === best.fEdge);
        s += `<line class="s3-line" x1="${f(X(0))}" x2="${f(X(0))}" y1="${f(Y(sEdge.lo))}" y2="${f(Y(sEdge.hi))}" stroke-width="5"/>` +
             `<line class="s3-line" x1="${f(X(a))}" x2="${f(X(a))}" y1="${f(Y(fEdge.lo + best.k * P))}" y2="${f(Y(fEdge.hi + best.k * P))}" stroke-width="5"/>` +
             seg(best, "box-path", 3);
        sImg.forEach((i) => {
          const chosen = i.edge === best.sEdge;
          s += `<circle class="${chosen ? "s1" : "ink"}-dot" cx="${f(X(-i.gap))}" cy="${f(Y(i.p))}" r="${chosen ? 5 : 3.5}"><title>S דרך ${HEB[i.edge]} : x = −${num(i.gap)}, p = ${num(i.p)}</title></circle>`;
        });
        fImg.forEach((i) => [-1, 0, 1].forEach((k) => {
          const p = i.p + k * P;
          if (p < pmin || p > pmax) return;
          const chosen = i.edge === best.fEdge && k === best.k;
          s += `<circle class="${chosen ? "s2" : "ink"}-dot" cx="${f(X(a + i.gap))}" cy="${f(Y(p))}" r="${chosen ? 5 : 3.5}"><title>F דרך ${HEB[i.edge]}${k ? `, k = ${k}` : ""} : x = ${num(a + i.gap)}, p = ${num(p)}</title></circle>`;
        }));
        s += `<circle class="s3-dot" cx="${f(X(0))}" cy="${f(Y(best.pExit))}" r="4"><title>נקודת היציאה : p = ${num(best.pExit)}</title></circle>` +
             `<circle class="s3-dot" cx="${f(X(a))}" cy="${f(Y(best.pEnter))}" r="4"><title>נקודת הכניסה : p = ${num(best.pEnter)}</title></circle>` +
             `<text class="legend" x="${f(X((best.xs + best.xf) / 2) - 8)}" y="${f(Y((best.ps + best.pf) / 2) + 20)}" text-anchor="end" style="font-size:15px">d = ${num(best.length)}</text>`;
        return s + "</svg>";
      };
      const draw = () => {
        clamp();
        ["a", "b", "h"].forEach((k) => { $(`.out-${k}`).textContent = String(st[k]); inputs[k].value = st[k]; });
        ["y0", "z0", "y1", "z1"].forEach((k) => { if (document.activeElement !== inputs[k]) inputs[k].value = num(st[k]); });
        inputs.y0.max = inputs.y1.max = st.b; inputs.z0.max = inputs.z1.max = st.h;
        const res = stripBest(st.a, st.b, st.h, st.y0, st.z0, st.y1, st.z1);
        const air = Math.hypot(st.a, st.y1 - st.y0, st.z1 - st.z0);
        wallSvg(walls.s, "s", res);
        wallSvg(walls.f, "f", res);
        chart.innerHTML = stripSvg(res);
        summary.innerHTML = `המרחק הקצר ביותר הוא ${ltr(num(res.line.length))}, דרך ${res.faces.length} פאות : ${ltr(res.faces.join(" → "))}. ` +
          `העכביש עוזב את הקיר שלו ב-${ltr(p3(res.exit))} ונכנס לקיר של הזבוב ב-${ltr(p3(res.enter))}. ` +
          `מתוך 48 הקווים ${ltr(res.valid)} חוקיים; דרך האוויר המרחק הוא ${ltr(num(air))}.`;
        segsBox.innerHTML = `<table><thead><tr><th>הפאה</th><th>אורך הקטע</th><th>הנקודה בסוף הקטע</th></tr></thead><tbody>` +
          res.faces.map((name, i) => `<tr><td>${HEB[name]} <bdi dir="ltr">(${name})</bdi></td><td>${ltr(num(res.segs[i]))}</td><td>${ltr(p3(res.pts[i + 1]))}</td></tr>`).join("") +
          `</tbody></table>`;

      };
      ["a", "b", "h"].forEach((k) => inputs[k].addEventListener("input", () => { st[k] = Number(inputs[k].value); draw(); }));
      ["y0", "z0", "y1", "z1"].forEach((k) => inputs[k].addEventListener("change", () => {
        const v = Number(inputs[k].value);
        if (Number.isFinite(v)) st[k] = v;
        draw();
      }));
      show.addEventListener("change", draw);
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, defaults); show.value = "valid"; draw(); });
      // drag S or F inside its wall
      Object.entries(walls).forEach(([who, svg]) => {
        let drag = false;
        const at = (e) => {
          const r = svg.getBoundingClientRect();
          const x = (e.clientX - r.left) / r.width * Number(svg.dataset.w), y = (e.clientY - r.top) / r.height * Number(svg.dataset.h);
          const pad = Number(svg.dataset.pad), S = Number(svg.dataset.s);
          const yy = Math.round(((x - pad) / S) * 4) / 4, zz = Math.round((st.h - (y - pad) / S) * 4) / 4;
          return [Math.min(Math.max(yy, 0), st.b), Math.min(Math.max(zz, 0), st.h)];
        };
        const move = (e) => {
          const [y, z] = at(e);
          if (who === "s") { st.y0 = y; st.z0 = z; } else { st.y1 = y; st.z1 = z; }
          draw();
        };
        svg.addEventListener("pointerdown", (e) => { drag = true; svg.setPointerCapture(e.pointerId); svg.classList.add("is-dragging"); move(e); e.preventDefault(); });
        svg.addEventListener("pointermove", (e) => { if (drag) move(e); });
        const end = () => { drag = false; svg.classList.remove("is-dragging"); };
        svg.addEventListener("pointerup", end);
        svg.addEventListener("pointercancel", end);
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { strip: stripView },
    help: {
      strip: "גוררים את העכביש ואת הזבוב על הקירות : הרצועה המחזורית מראה את התמונות, את 48 הקווים ואת הקצר שבהם, והמסלול נפרש פנים אחרי פנים.",
    },
    models: { stripImages, stripEdgePoint, stripPoint3, stripFacesBetween, stripLines, stripBest },
  });
})();
