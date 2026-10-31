// kinds: farm
//   farm                   0048        the farmer, the food line and the water line: the shortest path by reflection
//                                      (modes a and b: parallel lines; mode c: the food line tilted by theta)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every file and merges the models.
(() => {
  const { f, ltr } = dvqExplorers.lib;

  // The water line is y = 0 and the food line y = H; the farmer A stands at (0, a) and the
  // cow B at (L, b). Reflecting B through the water line and then through the food line puts
  // it at (L, 2H + b), so the shortest path is a straight line with the vertical rise
  // D = 2H + b - a, cut by the two lines in the ratio (H - a) : H : b. The same math as
  // tools/figures/q0048.py.
  const farmShortest = (L, H, a, b) => {
    const D = 2 * H + b - a, x = (L * (H - a)) / D, y = (L * H) / D, w = (L * b) / D;
    return { D, x, y, w, z1: Math.hypot(x, H - a), z2: Math.hypot(y, H), z3: Math.hypot(w, b), z: Math.hypot(L, D) };
  };
  // Part b: the heights whose shortest path stops after x and x + y, or null (valid when
  // 0 <= x <= y and 0 <= w <= y).
  const FARM_EPS = 1e-9;
  const farmHeights = (L, H, x, y) => {
    const w = L - x - y;
    if (!(y > 0) || x < -FARM_EPS || w < -FARM_EPS || x > y + FARM_EPS || w > y + FARM_EPS) return null;
    return [Math.min(H, Math.max(0, H * (1 - x / y))), Math.min(H, Math.max(0, (H * w) / y))];
  };
  // The range a stop can be dragged in while the other one stays: the food stop p1 in
  // [0, min(p2 / 2, 2 p2 - L)] (x <= y and w <= y), the water stop p2 in
  // [max(2 p1, (L + p1) / 2), L].
  const farmStopRange = (L, p1, p2, which) =>
    which === "food" ? [0, Math.max(0, Math.min(p2 / 2, 2 * p2 - L))] : [Math.max(2 * p1, (L + p1) / 2), L];

  // Part c: the food line passes through (0, H) at theta degrees above the water line y = 0,
  // and the two lines meet at O = (-H / tan theta, 0). The two reflections are a rotation by
  // 2 theta about O: B2 = (0, H) + R(2 theta)(L, H + b). The food stop P is at distance sf from
  // (0, H) along the food line, the water stop Q where P -> B1 crosses y = 0, and Qs is Q
  // reflected through the food line. Seen from O, the straight line A -> B2 turns by
  // 2 theta + beta - alpha <= 3 theta, at most 180 degrees for theta <= 60: the reflection is
  // always valid. The same math as tilted() in tools/figures/q0048.py.
  const farmTilt = (L, H, a, b, theta) => {
    const t = (theta * Math.PI) / 180, c = Math.cos(t), s = Math.sin(t);
    const c2 = c * c - s * s, s2 = 2 * c * s, u = H + b, v = H - a;
    const B1 = [L, -b], B2 = [L * c2 - u * s2, H + L * s2 + u * c2];
    const zSq = B2[0] ** 2 + (B2[1] - a) ** 2;
    const sf = (v * (L * c2 - u * s2)) / (L * s + (2 * H + b - a) * c);
    const P = [sf * c, H + sf * s];
    const Q = [P[0] + ((L - P[0]) * P[1]) / (P[1] + b), 0];
    const Qs = [c2 * Q[0] - s2 * H, H + s2 * Q[0] + c2 * H];
    const dist = (p, q) => Math.hypot(p[0] - q[0], p[1] - q[1]);
    const r = { B1, B2, z_sq: zSq, z: Math.sqrt(zSq), sf, P, Q, Qs, z1: dist([0, a], P), z2: dist(P, Q), z3: dist(Q, [L, b]) };
    if (theta === 0) return { ...r, O: null, alpha: 0, beta: 0, turn: 0 };
    const ox = -H / Math.tan(t), deg = (x) => (x * 180) / Math.PI;
    const alpha = deg(Math.atan2(a, -ox)), beta = deg(Math.atan2(b, L - ox));
    return { ...r, O: [ox, 0], alpha, beta, turn: 2 * theta + beta - alpha };
  };
  const TMAX = 60;
  const bMax = (L, H, theta) => H + L * Math.tan((theta * Math.PI) / 180);

  const LIM = { L: [0.5, 20], H: [0.5, 10] };
  const num = (v) => { const s = Number(v).toFixed(2); return s.replace(/\.?0+$/, "").replace(/^-0$/, "0"); };
  const snap = (v, q) => Math.round(v / q) * q;

  const farmView = () => ({
    mount(box) {
      const d = box.dataset;
      const st = { mode: ["b", "c"].includes(d.mode) ? d.mode : "a", L: Number(d.l || 7), H: Number(d.h || 3), a: Number(d.a || 1), b: Number(d.b || 2), t: Number(d.t || 15), refl: false };
      // in part c st.b is the height asked for; the cow stays under the food line, at bEff()
      const bEff = () => (st.mode === "c" ? Math.min(st.b, bMax(st.L, st.H, st.t)) : st.b);
      const field = (k, label, title) =>
        `<label class="farm-f farm-f-${k}"><span>${label}</span> <input type="number" class="ex-${k}" step="0.1" dir="ltr" inputmode="decimal" aria-label="${title}"></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>סעיף <select class="ex-mode" aria-label="מה בוחרים">` +
        `<option value="a"${st.mode === "a" ? " selected" : ""}>א : בוחרים את a ואת b</option>` +
        `<option value="b"${st.mode === "b" ? " selected" : ""}>ב : בוחרים את נקודות העצירה</option>` +
        `<option value="c"${st.mode === "c" ? " selected" : ""}>ג : קו האוכל נוטה בזווית θ</option></select></label>` +
        `<label><input type="checkbox" class="ex-refl"> הצגת השיקוף</label>` +
        `<button type="button" class="md-button ex-random">ערכים אקראיים</button></div>` +
        `<div class="ex-controls farm-fields">` +
        field("L", "L", "האורך L, המרחק האופקי בין החוואי לפרה") + field("H", "H", "הגובה H, המרחק בין הקווים") +
        `<label class="farm-f farm-th"><span>θ</span> <input type="range" class="ex-trange" min="0" max="${TMAX}" step="1" dir="ltr" data-nolink aria-label="הזווית θ של קו האוכל, במעלות">` +
        `<input type="number" class="ex-t" step="0.1" dir="ltr" inputmode="decimal" aria-label="הזווית θ של קו האוכל, במעלות, בין 0 ל-${TMAX}"><span>°</span></label>` +
        field("a", "a", "הגובה a של החוואי מעל קו המים") + field("b", "b", "הגובה b של הפרה מעל קו המים") +
        field("x", "x", "המרחק האופקי x מהחוואי לנקודת האוכל") + field("y", "y", "המרחק האופקי y מנקודת האוכל לנקודת המים") +
        `</div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-note farm-note" aria-live="polite"></p>` +
        `<p class="ex-title farm-drag"></p>` +
        `<svg class="figure farm-live" role="img" aria-label="השטח בין קו האוכל לקו המים, החוואי, הפרה והמסלול הקצר ביותר"></svg>` +
        `<span class="viz-legend"><span><i class="s3"></i>קו האוכל</span><span><i class="s1"></i>קו המים</span>` +
        `<span><i class="ink"></i>החוואי A</span><span><i class="s2"></i>הפרה B</span>` +
        `<span><i class="box-path"></i>המסלול הקצר ביותר</span><span class="farm-lg-copy"><i class="box-copy"></i>השיקופים</span><span class="farm-lg-arc"><i class="farm-arc"></i>הסיבוב של B סביב O</span></span>` +
        `<div class="farm-table"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $(".farm-live"), summary = $(".ex-summary"), note = $(".farm-note"), table = $(".farm-table");
      const mode = $(".ex-mode"), refl = $(".ex-refl"), trange = $(".ex-trange");
      const inputs = {};
      ["L", "H", "t", "a", "b", "x", "y"].forEach((k) => { inputs[k] = $(`.ex-${k}`); });
      const clipId = `farm-clip-${(farmView.n = (farmView.n || 0) + 1)}`;
      let layout = null, frozen = null, message = "";

      // The drawing: the strip [0, H] (with the reflections [-H, 0], [H, 2H] and [2H, 3H] when
      // shown), centred on (cx, cy) at S px per unit. A drag freezes the layout, so the corner
      // under the pointer stays put; it is laid out again when the drag ends.
      const fit = () => {
        if (st.mode === "c") return fitC(layout);
        const narrow = box.clientWidth > 0 && box.clientWidth < 560;
        const W = narrow ? 400 : 640, left = 64, right = st.refl ? 96 : 40, top = 30, bottom = 64;
        const lo = st.refl ? -st.H : 0, hi = st.refl ? 3 * st.H : st.H;
        const S = Math.min((W - left - right) / st.L, (st.refl ? (narrow ? 520 : 560) : (narrow ? 240 : 280)) / (hi - lo));
        const Hh = top + (hi - lo) * S + bottom;
        return { W, Hh, S, cx: left + (W - left - right) / 2, cy: top + (hi - st.H / 2) * S, narrow };
      };
      const X = (u) => (layout.c ? layout.ox + u * layout.S : layout.cx + (u - st.L / 2) * layout.S);
      const Y = (v) => (layout.c ? layout.oy - v * layout.S : layout.cy - (v - st.H / 2) * layout.S);

      // Part c's drawing: a window in the plane that holds A, B, the stops (and B1, B2, the
      // image of the water stop with the reflection) for every theta from 0 to 60, with the
      // cow at bEff() of each theta. It is kept while it still holds them, so changing theta
      // or dragging moves nothing but the lines and the points.
      const needC = () => {
        let x0 = -0.3, x1 = st.L, y0 = 0, y1 = st.H;
        const add = ([x, y]) => { x0 = Math.min(x0, x); x1 = Math.max(x1, x); y0 = Math.min(y0, y); y1 = Math.max(y1, y); };
        for (let th = 0; th <= TMAX; th += 2) {
          const b = Math.min(st.b, bMax(st.L, st.H, th)), r = farmTilt(st.L, st.H, st.a, b, th);
          [[0, st.a], [st.L, b], r.P, r.Q].forEach(add);
          if (st.refl) [r.B1, r.B2, r.Qs].forEach(add);
        }
        return [x0, x1, y0, y1];
      };
      const fitC = (old) => {
        const narrow = box.clientWidth > 0 && box.clientWidth < 560;
        let [x0, x1, y0, y1] = needC();
        const key = `${st.L} ${st.H} ${st.refl} ${narrow}`;
        if (old && old.c && old.key === key) {
          const [ox0, ox1, oy0, oy1] = old.win, inside = x0 >= ox0 && x1 <= ox1 && y0 >= oy0 && y1 <= oy1;
          if (inside && (ox1 - ox0) * (oy1 - oy0) < 2.5 * (x1 - x0) * (y1 - y0)) return old;
        }
        const span = Math.max(x1 - x0, y1 - y0);
        x0 -= 0.06 * span; x1 += 0.06 * span; y0 -= (st.refl ? 0.06 : 0.03) * span; y1 += 0.08 * span;
        if (y1 - y0 < 0.42 * (x1 - x0)) y1 = y0 + 0.42 * (x1 - x0);       // room above the food line
        const W = narrow ? 400 : 640, left = 30, right = 30, top = 20, bottom = 30;
        const maxH = st.refl ? (narrow ? 460 : 540) : (narrow ? 280 : 320);
        const S = Math.min((W - left - right) / (x1 - x0), maxH / (y1 - y0));
        const pad = (W - left - right - (x1 - x0) * S) / 2;
        return { c: true, key, win: [x0, x1, y0, y1], W, Hh: top + (y1 - y0) * S + bottom, S, narrow,
                 ox: left + pad - x0 * S, oy: top + y1 * S };
      };
      const line = (x1, y1, x2, y2, cls, w, dash, extra = "") =>
        `<line class="${cls}" x1="${f(X(x1))}" y1="${f(Y(y1))}" x2="${f(X(x2))}" y2="${f(Y(y2))}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ""}${extra}/>`;
      const text = (u, v, s, dx = 0, dy = 0, anchor = "middle", size = 15) =>
        `<text class="legend" x="${f(X(u) + dx)}" y="${f(Y(v) + dy)}" text-anchor="${anchor}" style="font-size:${size}px">${s}</text>`;
      const dot = (u, v, cls, r, title, drag) =>
        (drag ? `<circle class="farm-hit" data-drag="${drag}" cx="${f(X(u))}" cy="${f(Y(v))}" r="16"/>` : "") +
        `<circle class="${cls}-dot${drag ? " farm-handle-pt" : ""}"${drag ? ` data-drag="${drag}"` : ""} cx="${f(X(u))}" cy="${f(Y(v))}" r="${r}"><title>${title}</title></circle>`;

      const picture = (s) => {
        const { L, H, a, b } = st, p1 = s.x, p2 = s.x + s.y;
        const fs = layout.narrow ? 16 : 15;
        let out = "";
        const strip = (lo, hi, cls) => `<rect class="${cls}" x="${f(X(0))}" y="${f(Y(hi))}" width="${f(L * layout.S)}" height="${f((hi - lo) * layout.S)}"/>`;
        const ext = 18 / layout.S;
        if (st.refl) {
          out += strip(-H, 0, "box-copy") + strip(H, 2 * H, "box-copy") + strip(2 * H, 3 * H, "box-copy");
          [[-H, "s3-line"], [2 * H, "s1-line"], [3 * H, "s3-line"]].forEach(([v, cls]) => { out += line(-ext, v, L + ext, v, cls, 2.5, "9 6"); });
          [[-H, "−H"], [0, "0"], [H, "H"], [2 * H, "2H"], [3 * H, "3H"]].forEach(([v, t]) => { out += text(0, v, t, -24, 5, "end", fs - 2); });
        }
        out += strip(0, H, "box-face");
        out += line(-ext, 0, L + ext, 0, "s1-line", 3, "9 6") + line(-ext, H, L + ext, H, "s3-line", 3, "9 6");
        // the path, dashed
        out += line(0, a, p1, H, "box-path", 3.5, "10 6") + line(p1, H, p2, 0, "box-path", 3.5, "10 6") + line(p2, 0, L, b, "box-path", 3.5, "10 6");
        if (st.refl) {
          const top = 2 * H + b;
          out += line(p2, 0, L, -b, "ink-line", 1.5, "4 3") + line(L, b, L, -b, "ink-line", 1, "2 3") +
                 line(0, a, L, top, "box-path", 2.5, "10 6") +
                 line(0, a, L, a, "ink-line", 1.2) + line(L, a, L, top, "ink-line", 1.2);
          [[0, a, p1, H], [p1, H, p2, 2 * H], [p2, 2 * H, L, top]].forEach(([x0, y0, x1, y1], i) => {
            out += line(x0, y0, x1, y0, "ink-line", 1, "3 3") + line(x1, y0, x1, y1, "ink-line", 1, "3 3");
            if (Math.abs(Y(y0) - Y(y1)) > 14 && Math.abs(X(x0) - X(x1)) > 14) out += text((x0 + x1) / 2, (y0 + y1) / 2, `z${i + 1}`, -6, -4, "end", fs);
          });
          const dd = L + 32 / layout.S;
          const tk = 6 / layout.S;
          out += line(dd, a, dd, top, "ink-line", 1.2) + line(dd - tk, a, dd + tk, a, "ink-line", 1.2) + line(dd - tk, top, dd + tk, top, "ink-line", 1.2) + text(dd, (a + top) / 2, `D = ${num(s.D)}`, 6, 5, "start", fs) +
                 text(L / 2, a, `L = ${num(L)}`, 0, 18, "middle", fs) +
                 dot(p2, 2 * H, "s1", 4, "נקודת המים אחרי השיקוף") +
                 dot(L, -b, "ink", 4, `B′ = (${num(L)}, −${num(b)}) : השיקוף של B דרך קו המים`) + text(L, -b, "B′", 14, 16, "start", fs) +
                 dot(L, top, "s2", 6, `B″ = (${num(L)}, ${num(top)}) : השיקוף של B′ דרך קו האוכל`) + text(L, top, "B″", 0, -12, "middle", fs + 1);
        } else {
          // horizontal parts under the water line and the heights at the sides
          const yb = -22 / layout.S, yl = -48 / layout.S, tk = 6 / layout.S;
          [[0, p1, "x"], [p1, p2, "y"], [p2, L, "w"]].forEach(([lo, hi, t]) => {
            out += line(lo, yb, hi, yb, "ink-line", 1.2) + line(lo, yb + tk, lo, yb - tk, "ink-line", 1.2) + line(hi, yb + tk, hi, yb - tk, "ink-line", 1.2);
            if ((hi - lo) * layout.S > 22) out += text((lo + hi) / 2, yb, t, 0, -5, "middle", fs);
          });
          out += line(0, yl, L, yl, "ink-line", 1.2) + line(0, yl + tk, 0, yl - tk, "ink-line", 1.2) + line(L, yl + tk, L, yl - tk, "ink-line", 1.2) +
                 text(L / 2, yl, `L = ${num(L)}`, 0, -5, "middle", fs);
          const da = -14 / layout.S, db = L + 14 / layout.S;
          if (a * layout.S > 16) out += line(da, 0, da, a, "ink-line", 1.2) + text(da, a / 2, "a", -6, 5, "end", fs);
          if (b * layout.S > 16) out += line(db, 0, db, b, "ink-line", 1.2) + text(db, b / 2, "b", 6, 5, "start", fs);
          const dh = -40 / layout.S;
          out += line(dh, 0, dh, H, "ink-line", 1.2) + text(dh, H / 2, "H", -6, 5, "end", fs);
          [[p1, a, H, "z1"], [p2, H, 0, "z2"], [L, 0, b, "z3"]].forEach(([u, v0, v1, t], i) => {
            const u0 = [0, p1, p2][i];
            if (Math.hypot(X(u) - X(u0), Y(v1) - Y(v0)) > 40) out += text((u0 + u) / 2, (v0 + v1) / 2, t, i === 1 ? 12 : -8, -4, i === 1 ? "start" : "end", fs);
          });
        }
        // the stops, the farmer and the cow, and the corners
        const dragStops = st.mode === "b";
        out += dot(p1, H, "s3", 6, `נקודת האוכל, x = ${num(p1)}`, dragStops ? "food" : null) +
               dot(p2, 0, "s1", 6, `נקודת המים, x + y = ${num(p2)}`, dragStops ? "water" : null) +
               dot(0, a, "ink", 7, `החוואי A, a = ${num(a)}`, dragStops ? null : "A") + text(0, a, "A", 14, -8, "start", fs + 2) +
               dot(L, b, "s2", 7, `הפרה B, b = ${num(b)}`, dragStops ? null : "B") + text(L, b, "B", -14, -8, "end", fs + 2);
        [[0, 0], [L, 0], [0, H], [L, H]].forEach(([u, v]) => {
          out += `<rect class="farm-corner" data-drag="corner" x="${f(X(u) - 7)}" y="${f(Y(v) - 7)}" width="14" height="14" rx="3"><title>גוררים את הפינה כדי לשנות את L ואת H</title></rect>`;
        });
        return out;
      };

      // part c: the field between the rays from O at angles k0 theta and k1 theta, inside the
      // window (Sutherland-Hodgman against the two lines); at theta = 0 the rays are the lines
      // y = k H
      const lineK = (k) => {
        const tr = (k * st.t * Math.PI) / 180;
        return st.t > 0 ? { p: [-st.H / Math.tan((st.t * Math.PI) / 180), 0], d: [Math.cos(tr), Math.sin(tr)], ray: true }
                        : { p: [0, k * st.H], d: [1, 0], ray: false };
      };
      const clipHalf = (poly, { p, d }, keepLeft) => {
        const side = (q) => (d[0] * (q[1] - p[1]) - d[1] * (q[0] - p[0])) * (keepLeft ? 1 : -1);
        const out = [];
        poly.forEach((q, i) => {
          const r = poly[(i + poly.length - 1) % poly.length], sq = side(q), sr = side(r);
          if ((sq >= 0) !== (sr >= 0)) { const k = sr / (sr - sq); out.push([r[0] + k * (q[0] - r[0]), r[1] + k * (q[1] - r[1])]); }
          if (sq >= 0) out.push(q);
        });
        return out;
      };
      const wedgeC = (k, cls) => {
        const [x0, x1, y0, y1] = layout.win;
        let poly = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]];
        poly = clipHalf(clipHalf(poly, lineK(k), true), lineK(k + 1), false);
        return poly.length < 3 ? "" : `<polygon class="${cls}" points="${poly.map(([u, v]) => `${f(X(u))},${f(Y(v))}`).join(" ")}"/>`;
      };
      // the part of line k inside the window (from O on, when the lines meet)
      const rayC = (k, cls, w) => {
        const { p, d, ray } = lineK(k), [x0, x1, y0, y1] = layout.win;
        let lo = ray ? 0 : -Infinity, hi = Infinity;
        [[d[0], x0 - p[0], x1 - p[0]], [d[1], y0 - p[1], y1 - p[1]]].forEach(([dd, a0, a1]) => {
          if (Math.abs(dd) < 1e-12) { if (a0 > 0 || a1 < 0) hi = -Infinity; return; }
          const t0 = a0 / dd, t1 = a1 / dd;
          lo = Math.max(lo, Math.min(t0, t1)); hi = Math.min(hi, Math.max(t0, t1));
        });
        return hi > lo ? line(p[0] + lo * d[0], p[1] + lo * d[1], p[0] + hi * d[0], p[1] + hi * d[1], cls, w, "9 6") : "";
      };
      const inWin = ([u, v]) => { const [x0, x1, y0, y1] = layout.win; return u >= x0 && u <= x1 && v >= y0 && v <= y1; };
      const arcC = (o, rad, a0, a1, cls, w, dash) => {
        const pt = (deg) => [o[0] + rad * Math.cos((deg * Math.PI) / 180), o[1] + rad * Math.sin((deg * Math.PI) / 180)];
        const [p0, p1] = [pt(a0), pt(a1)], R = f(rad * layout.S);
        return `<path class="${cls}" d="M ${f(X(p0[0]))} ${f(Y(p0[1]))} A ${R} ${R} 0 0 0 ${f(X(p1[0]))} ${f(Y(p1[1]))}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ""}/>`;
      };
      const pictureC = (r) => {
        const { L, H, a, t } = st, b = bEff(), fs = layout.narrow ? 16 : 15;
        const [x0, x1, y0, y1] = layout.win;
        let out = `<defs><clipPath id="${clipId}"><rect x="${f(X(x0))}" y="${f(Y(y1))}" width="${f((x1 - x0) * layout.S)}" height="${f((y1 - y0) * layout.S)}"/></clipPath></defs>` +
                  `<g clip-path="url(#${clipId})">`;
        if (st.refl) out += wedgeC(-1, "box-copy") + wedgeC(1, "box-copy") + wedgeC(2, "box-copy");
        out += wedgeC(0, "box-face");
        if (st.refl) out += rayC(-1, "s3-line", 2) + rayC(2, "s1-line", 2) + rayC(3, "s3-line", 2);
        out += rayC(0, "s1-line", 3) + rayC(1, "s3-line", 3);
        // the two sides the farmer and the cow move on
        out += line(0, 0, 0, H, "ink-line", 1, "2 3") + line(L, 0, L, bMax(L, H, t), "ink-line", 1, "2 3");
        out += line(0, a, ...r.P, "box-path", 3.5, "10 6") + line(...r.P, ...r.Q, "box-path", 3.5, "10 6") + line(...r.Q, L, b, "box-path", 3.5, "10 6");
        if (st.refl) {
          out += line(...r.Q, ...r.B1, "ink-line", 1.5, "4 3") + line(L, b, ...r.B1, "ink-line", 1, "2 3") + line(...r.B1, ...r.B2, "ink-line", 1, "2 3") +
                 line(0, a, ...r.B2, "box-path", 2.5, "10 6");
          if (r.O) {
            const rad = Math.hypot(L - r.O[0], b);
            out += arcC(r.O, rad, r.beta, r.beta + 2 * t, "farm-arc", 1.8, "5 4");
            const mid = ((r.beta + t) * Math.PI) / 180, m = [r.O[0] + rad * Math.cos(mid), rad * Math.sin(mid)];
            if (inWin(m) && t >= 3) out += text(...m, "2θ", 8, 0, "start", fs);
          }
        }
        if (r.O && inWin(r.O)) {
          out += arcC(r.O, Math.min(2.2, (x1 - x0) / 8), 0, t, "farm-arc", 1.5) + dot(...r.O, "ink", 5, `O = (${num(r.O[0])}, 0) : הקווים נפגשים כאן`) + text(...r.O, "O", 0, 20, "middle", fs);
        }
        out += `</g>`;
        if (st.refl) {
          out += dot(...r.Qs, "s1", 4, `Q* = (${num(r.Qs[0])}, ${num(r.Qs[1])}) : התמונה של נקודת המים דרך קו האוכל`) +
                 dot(...r.B1, "ink", 4, `B1 = (${num(L)}, ${num(-b)}) : השיקוף של B דרך קו המים`) + text(...r.B1, "B1", 12, 16, "start", fs) +
                 dot(...r.B2, "s2", 6, `B2 = (${num(r.B2[0])}, ${num(r.B2[1])}) : השיקוף של B1 דרך קו האוכל, B מסובב ב-2θ סביב O`) + text(...r.B2, "B2", 0, -12, "middle", fs + 1);
        }
        out += dot(...r.P, "s3", 6, `נקודת האוכל P = (${num(r.P[0])}, ${num(r.P[1])})`) +
               dot(...r.Q, "s1", 6, `נקודת המים Q = (${num(r.Q[0])}, 0)`) +
               dot(0, a, "ink", 7, `החוואי A, a = ${num(a)}`, "A") + text(0, a, "A", -12, -8, "end", fs + 2) +
               dot(L, b, "s2", 7, `הפרה B, b = ${num(b)}`, "B") + text(L, b, "B", 12, -8, "start", fs + 2);
        return out;
      };
      const drawC = () => {
        const r = farmTilt(st.L, st.H, st.a, bEff(), st.t);
        if (!frozen) layout = fit();
        svg.setAttribute("viewBox", `0 0 ${layout.W} ${f(layout.Hh)}`);
        svg.innerHTML = pictureC(r);
        $(".farm-lg-copy").style.display = st.refl ? "" : "none";
        $(".farm-lg-arc").style.display = st.refl ? "" : "none";
        $(".farm-drag").textContent = "שנו את הזווית θ במחוון, וגררו את החוואי A ואת הפרה B לאורך הדפנות.";
        sync({ x: 0, y: 0 });
        const pt = (p) => `(${num(p[0])}, ${num(p[1])})`, b = bEff();
        const par = farmShortest(st.L, st.H, st.a, Math.min(b, st.H)).z;
        summary.innerHTML = (r.O ? `${ltr(`B2 = ${pt(r.B2)}`)}, הפרה מסובבת ב-${ltr(`2θ = ${num(2 * st.t)}°`)} סביב ${ltr(`O = (${num(r.O[0])}, 0)`)}. `
          : `${ltr(`B2 = ${pt(r.B2)}`)}, כי כש-θ = 0 שני השיקופים הם הזזה ב-2H כלפי מעלה. `) +
          `המסלול הקצר ביותר : ${ltr(`z = |AB2| ≈ ${num(r.z)}`)}, עם עצירה באוכל ב-${ltr(pt(r.P))} ובמים ב-${ltr(pt(r.Q))}. ` +
          (r.O ? `הקו הישר מסתובב סביב O ב-${ltr(`2θ + β − α ≈ ${num(r.turn)}° ≤ 180°`)}, ולכן השיקוף תקף.` : "בקווים מקבילים השיקוף תקף תמיד.");
        const iso = (x) => `\u2066${x}\u2069`;          // an LTR island in the plain-text note
        let auto = "";
        if (st.b > b + 1e-9) auto = `הפרה ירדה ל-${iso(`b = ${num(b)}`)} כדי להישאר מתחת לקו האוכל, ${iso("b ≤ H + L·tanθ")}. כשהזווית תגדל היא תחזור ל-${num(st.b)}.`;
        else if (r.O && Math.abs(r.turn - 180) < 1e-6) auto = `כאן ${iso("2θ + β − α = 180°")} בדיוק : המסלול עובר דרך O ונוגע בה בשני הקווים.`;
        else if (r.P[0] < -1e-9) auto = `נקודת האוכל משמאל לחוואי, ב-${iso(`x = ${num(r.P[0])}`)} : הקווים ממשיכים שמאלה עד O, ולכן מותר לעצור שם.`;
        else if (st.t === 0) auto = `כש-θ = 0 הקווים מקבילים וזה סעיף א : ${iso("B2 = (L, 2H + b)")}, ${iso(`z ≈ ${num(par)}`)}.`;
        note.textContent = message || auto;
        const d = (p, q) => `${num(q[0] - p[0])}`, e = (p, q) => `${num(q[1] - p[1])}`;
        const A = [0, st.a], B = [st.L, b];
        const row = (name, p, q, z, cls = "") => `<tr${cls}><td>${name}</td><td>${ltr(d(p, q))}</td><td>${ltr(e(p, q))}</td><td>${ltr(z)}</td></tr>`;
        table.innerHTML = `<table><thead><tr><th>הקטע</th><th>אופקי</th><th>אנכי</th><th>האורך, לפי פיתגורס</th></tr></thead><tbody>` +
          row("מהחוואי לאוכל", A, r.P, `z1 = ${num(r.z1)}`) +
          row("מהאוכל למים", r.P, r.Q, `z2 = ${num(r.z2)}`) +
          row("מהמים לפרה", r.Q, B, `z3 = ${num(r.z3)}`) +
          row("הקו הישר מ-A ל-B2", A, r.B2, `z = ${num(r.z)}`, ` class="farm-total"`) +
          `</tbody></table>`;
      };

      const sync = (s) => {
        const vals = { L: st.L, H: st.H, t: st.t, a: st.a, b: bEff(), x: s.x, y: s.y };
        Object.entries(inputs).forEach(([k, el]) => { if (document.activeElement !== el) el.value = num(vals[k]); });
        const editAB = st.mode !== "b", isC = st.mode === "c";
        ["a", "b"].forEach((k) => { inputs[k].disabled = !editAB; inputs[k].closest("label").hidden = !editAB; });
        ["x", "y"].forEach((k) => { inputs[k].disabled = editAB; inputs[k].closest("label").hidden = editAB; });
        inputs.t.disabled = trange.disabled = !isC; inputs.t.closest("label").hidden = !isC;
        if (document.activeElement !== trange) trange.value = String(st.t);
        inputs.L.min = LIM.L[0]; inputs.L.max = LIM.L[1]; inputs.H.min = LIM.H[0]; inputs.H.max = LIM.H[1];
        inputs.t.min = 0; inputs.t.max = TMAX;
        inputs.a.min = inputs.b.min = 0; inputs.a.max = num(st.H); inputs.b.max = num(isC ? bMax(st.L, st.H, st.t) : st.H);
      };
      const draw = () => {
        if (st.mode === "c") { drawC(); return; }
        const s = farmShortest(st.L, st.H, st.a, st.b);
        if (!frozen) layout = fit();
        svg.setAttribute("viewBox", `0 0 ${layout.W} ${f(layout.Hh)}`);
        svg.innerHTML = picture(s);
        $(".farm-lg-copy").style.display = st.refl ? "" : "none";
        $(".farm-lg-arc").style.display = "none";
        $(".farm-drag").textContent = st.mode === "a"
          ? "גררו את החוואי A ואת הפרה B לאורך הדפנות, ואת הפינות כדי לשנות את L ואת H."
          : "גררו את נקודת האוכל ואת נקודת המים לאורך הקווים, ואת הפינות כדי לשנות את L ואת H.";
        sync(s);
        const sq = (v) => `${num(v)}²`;
        summary.innerHTML = (st.mode === "b"
          ? `העצירות ${ltr(`x = ${num(s.x)}, y = ${num(s.y)}, w = ${num(s.w)}`)} הן הקצרות ביותר כש-${ltr(`a = ${num(st.a)}, b = ${num(st.b)}`)}. `
          : `העצירות הטובות ביותר : ${ltr(`x = ${num(s.x)}, y = ${num(s.y)}, w = ${num(s.w)}`)}. `) +
          `המסלול הקצר ביותר : ${ltr(`z = √(L² + (2H + b − a)²) = √(${sq(st.L)} + ${sq(s.D)}) ≈ ${num(s.z)}`)}.`;
        note.textContent = message;
        const row = (name, h, v, z, cls = "") => `<tr${cls}><td>${name}</td><td>${ltr(h)}</td><td>${ltr(v)}</td><td>${ltr(z)}</td></tr>`;
        table.innerHTML = `<table><thead><tr><th>הקטע</th><th>אופקי</th><th>אנכי</th><th>האורך, לפי פיתגורס</th></tr></thead><tbody>` +
          row("מהחוואי לאוכל", `x = ${num(s.x)}`, `H − a = ${num(st.H - st.a)}`, `z1 = ${num(s.z1)}`) +
          row("מהאוכל למים", `y = ${num(s.y)}`, `H = ${num(st.H)}`, `z2 = ${num(s.z2)}`) +
          row("מהמים לפרה", `w = ${num(s.w)}`, `b = ${num(st.b)}`, `z3 = ${num(s.z3)}`) +
          row("כל המסלול", `L = ${num(st.L)}`, `2H + b − a = ${num(s.D)}`, `z = ${num(s.z)}`, ` class="farm-total"`) +
          `</tbody></table>`;
      };
      const say = (m) => { message = m; };

      // the heights follow H in proportion, so the picture keeps its shape
      const setSize = (L, H) => {
        const ra = st.a / st.H, rb = st.b / st.H;
        st.L = L; st.H = H; st.a = ra * H; st.b = rb * H;
      };
      const setStops = (p1, p2) => {
        const hb = farmHeights(st.L, st.H, p1, p2 - p1);
        if (hb) [st.a, st.b] = hb;
      };
      const stopsMessage = (p1, p2) => {
        const x = p1, y = p2 - p1, w = st.L - p2;
        if (Math.abs(x - y) < 1e-6 && Math.abs(w - y) < 1e-6) return "כאן x = y = w : החוואי על קו המים והפרה על קו האוכל, כמו בסעיף ב.";
        if (Math.abs(x - y) < 1e-6) return "כאן x = y : החוואי הגיע לקו המים (a = 0), ונקודת האוכל לא יכולה לזוז ימינה יותר.";
        if (Math.abs(w - y) < 1e-6) return "כאן w = y : הפרה הגיעה לקו האוכל (b = H), והקטע האחרון לא יכול להיות ארוך מהאמצעי.";
        return "";
      };

      // typed values: a value out of range is refused with a line that says why
      const typed = (k) => {
        const v = Number(inputs[k].value);
        say("");
        if (inputs[k].value.trim() === "" || !Number.isFinite(v)) { say(`הערך של ${k} צריך להיות מספר.`); draw(); return; }
        if (k === "L" || k === "H") {
          const [lo, hi] = LIM[k];
          if (v < lo || v > hi) { say(`הערך של ${k} צריך להיות בין ${lo} ל-${hi}.`); draw(); return; }
          setSize(k === "L" ? v : st.L, k === "H" ? v : st.H);
        } else if (k === "t") {
          if (v < 0 || v > TMAX) { say(`הזווית θ צריכה להיות בין 0 ל-${TMAX} מעלות : עד 60 מעלות השיקוף תקף תמיד.`); draw(); return; }
          st.t = v;
        } else if (k === "b" && st.mode === "c") {
          const hi = bMax(st.L, st.H, st.t);
          if (v < 0 || v > hi + 1e-9) { say(`הערך של b צריך להיות בין 0 ל-H + L·tanθ = ${num(hi)} : הפרה בין הקווים או עליהם.`); draw(); return; }
          st.b = v;
        } else if (k === "a" || k === "b") {
          if (v < 0 || v > st.H) { say(`הערך של ${k} צריך להיות בין 0 ל-H = ${num(st.H)} : הנקודה בין הקווים או עליהם.`); draw(); return; }
          st[k] = v;
        } else {
          const s = farmShortest(st.L, st.H, st.a, st.b);
          const x = k === "x" ? v : s.x, y = k === "y" ? v : s.y, w = st.L - x - y;
          let why = "";
          if (x < 0 || y <= 0 || w < -1e-9) why = "צריך x ≥ 0, y > 0 ו-x + y ≤ L.";
          else if (x > y + 1e-9) why = "צריך x ≤ y : אחרת a יוצא שלילי, והחוואי מתחת לקו המים.";
          else if (w > y + 1e-9) why = "צריך w ≤ y : אחרת b יוצא גדול מ-H, והפרה מעל קו האוכל.";
          if (why) { say(`אין a ו-b שבהם זה המסלול הקצר ביותר : ${why}`); draw(); return; }
          setStops(x, x + y);
          say(stopsMessage(x, x + y));
        }
        draw();
      };
      Object.keys(inputs).forEach((k) => {
        inputs[k].addEventListener("change", () => typed(k));
        inputs[k].addEventListener("keydown", (e) => { if (e.key === "Enter") inputs[k].blur(); });
      });
      mode.addEventListener("change", () => { st.mode = mode.value; if (st.mode !== "c") st.b = Math.min(st.b, st.H); say(""); draw(); });
      trange.addEventListener("input", () => { st.t = Number(trange.value); say(""); draw(); });
      refl.addEventListener("change", () => { st.refl = refl.checked; draw(); });

      // a random example: L and H in halves, then the heights (part a) or two valid stops (part b)
      const random = (rng) => {
        st.L = 2 + snap(rng() * 18, 0.5); st.H = 1 + snap(rng() * 9, 0.5);
        if (st.mode === "a") {
          st.a = Math.min(st.H, snap(rng() * st.H, 0.1)); st.b = Math.min(st.H, snap(rng() * st.H, 0.1));
        } else if (st.mode === "c") {
          st.t = Math.round(rng() * TMAX);
          st.a = Math.min(st.H, snap(rng() * st.H, 0.1));
          const hi = bMax(st.L, st.H, st.t);
          st.b = Math.min(hi, snap(rng() * hi, 0.1));
        } else {
          let p1 = st.L / 3, p2 = (2 * st.L) / 3;
          for (let i = 0; i < 400; i++) {
            const u = snap(rng() * st.L, 0.1), v = snap(rng() * st.L, 0.1);
            if (farmHeights(st.L, st.H, Math.min(u, v), Math.abs(v - u))) { p1 = Math.min(u, v); p2 = Math.max(u, v); break; }
          }
          setStops(p1, p2);
        }
        say("");
        draw();
      };
      const seed = dvqExplorers.lib.seedControls(box, $(".ex-random"), random);
      $(".ex-random").addEventListener("click", () => seed.draw());

      // dragging: a corner sets L and H around the centre, A and B their heights (part a),
      // the food and water stops their places on the lines (part b)
      const at = (e) => {
        const p = svg.createSVGPoint();
        p.x = e.clientX; p.y = e.clientY;
        const m = svg.getScreenCTM();
        return m ? p.matrixTransform(m.inverse()) : { x: 0, y: 0 };
      };
      let drag = null;
      const move = (e) => {
        const { x: px, y: py } = at(e), S = layout.S;
        const u = st.L / 2 + (px - layout.cx) / S, vUp = st.H / 2 + (layout.cy - py) / S;
        if (drag === "corner") {
          const maxL = Math.min(LIM.L[1], (2 * Math.min(layout.cx - 30, layout.W - layout.cx - 30)) / S);
          const maxH = Math.min(LIM.H[1], (2 * Math.min(layout.cy - 12, layout.Hh - layout.cy - 12)) / S);
          const L = Math.min(maxL, Math.max(LIM.L[0], snap((2 * Math.abs(px - layout.cx)) / S, 0.1)));
          const H = Math.min(maxH, Math.max(LIM.H[0], snap((2 * Math.abs(py - layout.cy)) / S, 0.1)));
          setSize(L, H);
          say("");
        } else if (st.mode === "c") {
          const v = (layout.oy - py) / S, hi = drag === "A" ? st.H : bMax(st.L, st.H, st.t);
          st[drag === "A" ? "a" : "b"] = Math.min(hi, Math.max(0, snap(v, 0.05)));
          say("");
        } else if (drag === "A" || drag === "B") {
          st[drag === "A" ? "a" : "b"] = Math.min(st.H, Math.max(0, snap(vUp, 0.05)));
          say("");
        } else {
          const s = farmShortest(st.L, st.H, st.a, st.b);
          let p1 = s.x, p2 = s.x + s.y;
          const [lo, hi] = farmStopRange(st.L, p1, p2, drag);
          const want = snap(u, 0.05), got = Math.min(hi, Math.max(lo, want));
          if (drag === "food") p1 = got; else p2 = got;
          setStops(p1, p2);
          say(want > hi + 1e-9 || want < lo - 1e-9 ? stopsMessage(p1, p2) || "הגרירה נעצרת כאן : מעבר לנקודה הזו אין a ו-b חוקיים." : stopsMessage(p1, p2));
        }
        draw();
      };
      svg.addEventListener("pointerdown", (e) => {
        const t = e.target.closest("[data-drag]");
        if (!t) return;
        drag = t.dataset.drag;
        frozen = true;
        svg.setPointerCapture(e.pointerId);
        svg.classList.add("is-dragging");
        e.preventDefault();
        move(e);
      });
      svg.addEventListener("pointermove", (e) => { if (drag) move(e); });
      const end = () => {
        if (!drag) return;
        drag = null; frozen = null;
        svg.classList.remove("is-dragging");
        draw();
        // a drag is an edit of the fields: the link and the remembered state read them
        inputs.L.dispatchEvent(new Event("input", { bubbles: true }));
      };
      svg.addEventListener("pointerup", end);
      svg.addEventListener("pointercancel", end);
      if (typeof ResizeObserver !== "undefined") {
        let wasNarrow = box.clientWidth > 0 && box.clientWidth < 560;
        new ResizeObserver(() => { const nw = box.clientWidth > 0 && box.clientWidth < 560; if (nw !== wasNarrow && !drag) { wasNarrow = nw; draw(); } }).observe(box);
      }
      draw();
    },
  });

  dvqExplorers.register({
    views: { farm: farmView },
    help: {
      farm: "בסעיף א גוררים את החוואי ואת הפרה לאורך הדפנות, ובסעיף ב את נקודות העצירה לאורך הקווים; הפינות משנות את L ואת H, והשיקוף מראה את הקו הישר שמוצאים בו את המסלול. בסעיף ג המחוון משנה את הזווית θ של קו האוכל, והשיקוף מראה את הסיבוב של הפרה סביב O.",
    },
    models: { farmShortest, farmHeights, farmStopRange, farmTilt },
  });
})();
