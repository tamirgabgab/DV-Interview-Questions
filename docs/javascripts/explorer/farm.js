// kinds: farm
//   farm                   0048        the farmer, the food line and the water line: the shortest path by reflection
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

  const LIM = { L: [0.5, 20], H: [0.5, 10] };
  const num = (v) => { const s = Number(v).toFixed(2); return s.replace(/\.?0+$/, "").replace(/^-0$/, "0"); };
  const snap = (v, q) => Math.round(v / q) * q;

  const farmView = () => ({
    mount(box) {
      const d = box.dataset;
      const st = { mode: d.mode === "b" ? "b" : "a", L: Number(d.l || 7), H: Number(d.h || 3), a: Number(d.a || 1), b: Number(d.b || 2), refl: false };
      const field = (k, label, title) =>
        `<label class="farm-f farm-f-${k}"><span>${label}</span> <input type="number" class="ex-${k}" step="0.1" dir="ltr" inputmode="decimal" aria-label="${title}"></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>סעיף <select class="ex-mode" aria-label="מה בוחרים">` +
        `<option value="a"${st.mode === "a" ? " selected" : ""}>א : בוחרים את a ואת b</option>` +
        `<option value="b"${st.mode === "b" ? " selected" : ""}>ב : בוחרים את נקודות העצירה</option></select></label>` +
        `<label><input type="checkbox" class="ex-refl"> הצגת השיקוף</label>` +
        `<button type="button" class="md-button ex-random">ערכים אקראיים</button></div>` +
        `<div class="ex-controls farm-fields">` +
        field("L", "L", "האורך L, המרחק האופקי בין החוואי לפרה") + field("H", "H", "הגובה H, המרחק בין הקווים") +
        field("a", "a", "הגובה a של החוואי מעל קו המים") + field("b", "b", "הגובה b של הפרה מעל קו המים") +
        field("x", "x", "המרחק האופקי x מהחוואי לנקודת האוכל") + field("y", "y", "המרחק האופקי y מנקודת האוכל לנקודת המים") +
        `</div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-note farm-note" aria-live="polite"></p>` +
        `<svg class="figure farm-live" role="img" aria-label="השטח בין קו האוכל לקו המים, החוואי, הפרה והמסלול הקצר ביותר"></svg>` +
        `<span class="viz-legend"><span><i class="s3"></i>קו האוכל</span><span><i class="s1"></i>קו המים</span>` +
        `<span><i class="ink"></i>החוואי A</span><span><i class="s2"></i>הפרה B</span>` +
        `<span><i class="box-path"></i>המסלול הקצר ביותר</span><span class="farm-lg-copy"><i class="box-copy"></i>השיקופים</span></span>` +
        `<div class="farm-table"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const svg = $(".farm-live"), summary = $(".ex-summary"), note = $(".farm-note"), table = $(".farm-table");
      const mode = $(".ex-mode"), refl = $(".ex-refl");
      const inputs = {};
      ["L", "H", "a", "b", "x", "y"].forEach((k) => { inputs[k] = $(`.ex-${k}`); });
      let layout = null, frozen = null, message = "";

      // The drawing: the strip [0, H] (with the reflections [-H, 0], [H, 2H] and [2H, 3H] when
      // shown), centred on (cx, cy) at S px per unit. A drag freezes the layout, so the corner
      // under the pointer stays put; it is laid out again when the drag ends.
      const fit = () => {
        const narrow = box.clientWidth > 0 && box.clientWidth < 560;
        const W = narrow ? 400 : 640, left = 64, right = st.refl ? 96 : 40, top = 30, bottom = 64;
        const lo = st.refl ? -st.H : 0, hi = st.refl ? 3 * st.H : st.H;
        const S = Math.min((W - left - right) / st.L, (st.refl ? (narrow ? 520 : 560) : (narrow ? 240 : 280)) / (hi - lo));
        const Hh = top + (hi - lo) * S + bottom;
        return { W, Hh, S, cx: left + (W - left - right) / 2, cy: top + (hi - st.H / 2) * S, narrow };
      };
      const X = (u) => layout.cx + (u - st.L / 2) * layout.S;
      const Y = (v) => layout.cy - (v - st.H / 2) * layout.S;
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

      const sync = (s) => {
        const vals = { L: st.L, H: st.H, a: st.a, b: st.b, x: s.x, y: s.y };
        Object.entries(inputs).forEach(([k, el]) => { if (document.activeElement !== el) el.value = num(vals[k]); });
        const editAB = st.mode === "a";
        ["a", "b"].forEach((k) => { inputs[k].disabled = !editAB; inputs[k].closest("label").hidden = !editAB; });
        ["x", "y"].forEach((k) => { inputs[k].disabled = editAB; inputs[k].closest("label").hidden = editAB; });
        inputs.L.min = LIM.L[0]; inputs.L.max = LIM.L[1]; inputs.H.min = LIM.H[0]; inputs.H.max = LIM.H[1];
        inputs.a.min = inputs.b.min = 0; inputs.a.max = inputs.b.max = num(st.H);
      };
      const draw = () => {
        const s = farmShortest(st.L, st.H, st.a, st.b);
        if (!frozen) layout = fit();
        svg.setAttribute("viewBox", `0 0 ${layout.W} ${f(layout.Hh)}`);
        svg.innerHTML = picture(s);
        $(".farm-lg-copy").style.display = st.refl ? "" : "none";
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
      mode.addEventListener("change", () => { st.mode = mode.value; say(""); draw(); });
      refl.addEventListener("change", () => { st.refl = refl.checked; draw(); });

      // a random example: L and H in halves, then the heights (part a) or two valid stops (part b)
      const random = (rng) => {
        st.L = 2 + snap(rng() * 18, 0.5); st.H = 1 + snap(rng() * 9, 0.5);
        if (st.mode === "a") {
          st.a = Math.min(st.H, snap(rng() * st.H, 0.1)); st.b = Math.min(st.H, snap(rng() * st.H, 0.1));
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
      farm: "בסעיף א גוררים את החוואי ואת הפרה לאורך הדפנות, ובסעיף ב את נקודות העצירה לאורך הקווים; הפינות משנות את L ואת H, והשיקוף מראה את הקו הישר שמוצאים בו את המסלול.",
    },
    models: { farmShortest, farmHeights, farmStopRange },
  });
})();
