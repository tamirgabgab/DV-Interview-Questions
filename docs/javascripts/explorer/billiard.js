// kinds: billiard
//   billiard               0080        a 360 x 180 table with six pockets of width w (corners and middles, or a separate width for the middles), the ball dragged anywhere and the aim arrow turned to any direction; a shot runs the ball along its real path, bouncing, into its pocket, and the unfolded table under it shows the same shot as a straight line with the gap at every line of pockets; the calculation of parts c and d (s, c, eps, K, m) beside it; an optional real ball of radius 2.625 cm (the centre on the table shrunk by it)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { arrowStep, ltr } = dvqExplorers.lib;
  const NB = " ";

  // --- the model -------------------------------------------------------------------------------
  // The table is a x b with its corner (0, 0) at the origin; a ball of radius rho moves its
  // centre on the table shrunk by rho on every side, A = a - 2 rho by B = b - 2 rho, with the
  // pockets at that table's corners and middles (rho = 0: the point ball of the page). The
  // direction is mirrored so the ball moves right and up (x -> A - x when it moves left, y ->
  // B - y when it moves down); unfolded, the path is the ray (X + t dx, Y + t dy), t >= 0,
  // and the pockets are the grid points (k A/2, m B), corners for even k and middles for odd
  // k, each a disc of radius wc/2 or wm/2. The ball enters the first disc the ray reaches
  // (a disc it starts in counts only when it moves towards the centre, so the pocket it
  // leaves from its centre is ignored): the discs of different k lie in disjoint strips
  // k A/2 ± w/2 when w < A/2, so the first k with such a disc is the first in time, and
  // within one k the earliest entry wins. The same rule as find_pocket on the page.
  const BIL_A = 360, BIL_B = 180, BIL_RHO = 2.625, BIL_KMAX = 20000, BIL_CROSS = 400;
  const mod = (v, n) => ((v % n) + n) % n;
  const fold = (v, L) => { const u = mod(v, 2 * L); return u > L ? 2 * L - u : u; };
  // the grid lines j L with p < j L < q (the cushions crossed between two points of the ray)
  const lines = (p, q, L) => Math.max(0, Math.ceil(q / L) - 1 - Math.floor(p / L));
  const bilPocketAt = (k, m) => [[0, 1, 2, 1][mod(k, 4)], mod(m, 2)];      // x index 0 / 1 / 2 (0, A/2, A), y index 0 / 1
  const BIL_NAMES = [["הפינה השמאלית התחתונה", "הפינה השמאלית העליונה"], ["הכיס האמצעי התחתון", "הכיס האמצעי העליון"],
    ["הפינה הימנית התחתונה", "הפינה הימנית העליונה"]];

  const bilShot = ({ a = BIL_A, b = BIL_B, rho = 0, x0, y0, deg, wc, wm = wc, kmax = BIL_KMAX, cap = 0 }) => {
    const A = a - 2 * rho, B = b - 2 * rho;
    const th = (deg * Math.PI) / 180;
    let c = Math.cos(th), sn = Math.sin(th);
    if (Math.abs(c) < 1e-12) c = 0;
    if (Math.abs(sn) < 1e-12) sn = 0;
    const mx = c < 0, my = sn < 0;
    const X = mx ? A - (x0 - rho) : x0 - rho, Y = my ? B - (y0 - rho) : y0 - rho;
    const dx = Math.abs(c), dy = Math.abs(sn);
    const rOf = (k) => (mod(k, 2) ? wm : wc) / 2, wmax = Math.max(wc, wm);
    const enter = (k, m) => {
      const r = rOf(k), ux = (k * A) / 2 - X, uy = m * B - Y;
      const ahead = ux * dx + uy * dy, off = Math.abs(ux * dy - uy * dx);
      return ahead > 0 && off < r ? { k, m, t: Math.max(0, ahead - Math.sqrt(r * r - off * off)), off, ahead } : null;
    };
    const checks = [];
    let hit = null;
    if (dx === 0) {
      // straight up: only the column the ball stands in, if it is within a pocket's reach
      for (let k = Math.floor((2 * (X - wmax / 2)) / A); k <= Math.ceil((2 * (X + wmax / 2)) / A) && !hit; k++) {
        const row = Math.floor(Y / B);
        const got = [enter(k, row), enter(k, row + 1)].filter(Boolean).sort((u, v) => u.t - v.t);
        if (got.length) hit = got[0];
      }
    } else {
      const slope = dy / dx;
      for (let k = Math.floor((2 * X - wmax) / A); k <= kmax; k++) {
        const px = (k * A) / 2, yk = Y + (px - X) * slope, reach = rOf(k) / dx;
        const got = [];
        for (let m = Math.floor((yk - reach) / B); m <= Math.ceil((yk + reach) / B); m++) {
          const e = enter(k, m);
          if (e) got.push(e);
        }
        got.sort((u, v) => u.t - v.t);
        if (checks.length < 400) {
          const m = got.length ? got[0].m : Math.round(yk / B);
          checks.push({ k, yk, m, gap: Math.abs(yk - m * B), d: Math.abs(yk - m * B) * dx, ok: got.length > 0, back: px < X });
        }
        if (got.length) { hit = got[0]; break; }
      }
    }
    // the path: to the pocket, or `cap` cm when there is none (a periodic path)
    const T = hit ? hit.t : cap || 12 * (A + B);
    const real = (u, v) => {
      let x = fold(u, A), y = fold(v, B);
      if (mx) x = A - x;
      if (my) y = B - y;
      return [x + rho, y + rho];
    };
    const at = (t) => real(X + t * dx, Y + t * dy);
    // the cushions: the grid lines x = j A and y = i B the ray crosses before T
    const cross = [];
    if (dx > 0) for (let j = Math.floor(X / A) + 1; j * A < X + T * dx && cross.length < BIL_CROSS; j++) cross.push({ t: (j * A - X) / dx, v: true, j });
    if (dy > 0) for (let i = Math.floor(Y / B) + 1; i * B < Y + T * dy && cross.length < 2 * BIL_CROSS; i++) cross.push({ t: (i * B - Y) / dy, v: false, j: i });
    cross.sort((u, v) => u.t - v.t);
    cross.forEach((e) => {
      e.at = at(e.t);
      const side = mod(e.j, 2);                       // the odd lines are the far cushion
      e.wall = e.v ? ((side === 1) !== mx ? "right" : "left") : ((side === 1) !== my ? "top" : "bottom");
    });
    let pocket = null;
    if (hit) {
      let [i, j] = bilPocketAt(hit.k, hit.m);
      if (mx) i = 2 - i;
      if (my) j = 1 - j;
      pocket = { i, j, x: (i * a) / 2, y: j * b, name: BIL_NAMES[i][j] };      // the table's pocket (its centre on the shrunk table is rho closer)
    }
    const tan = dx > 0 ? dy / dx : null;
    return {
      A, B, rho, X, Y, dx, dy, mx, my, hit, pocket, T, cross: cross.slice(0, BIL_CROSS), checks,
      cushions: (dx > 0 ? lines(X, X + T * dx, A) : 0) + (dy > 0 ? lines(Y, Y + T * dy, B) : 0), end: at(T),
      s: tan === null ? null : (A * tan) / (2 * B), c: tan === null ? null : (Y - X * tan) / B,
      epsC: dx > 0 ? wc / (2 * B * dx) : null, epsM: dx > 0 ? wm / (2 * B * dx) : null,
    };
  };
  // the real point of the path at distance t (for the animation and the tests)
  const bilAt = (shot, t) => {
    const { A, B, rho, X, Y, dx, dy, mx, my } = shot;
    let x = fold(X + t * dx, A), y = fold(Y + t * dy, B);
    if (mx) x = A - x;
    if (my) y = B - y;
    return [x + rho, y + rho];
  };

  // --- the view --------------------------------------------------------------------------------
  const W = 640, PAD = 18, S = (W - 2 * PAD) / BIL_A, HT = Math.round(2 * PAD + BIL_B * S);
  const PX = (x) => PAD + x * S, PY = (y) => PAD + (BIL_B - y) * S;
  const nf = (v, n = 2) => { const s = Number(v).toFixed(n).replace(/\.?0+$/, ""); return (s === "-0" ? "0" : s).replace("-", "−"); };
  const PRESETS = [
    { label: "סעיף א", x: 0, y: 0, deg: 36.87, w: 9 },
    { label: "‏37°", x: 0, y: 0, deg: 37, w: 9 },
    { label: "‏37°, כיסים של 1 ס״מ", x: 0, y: 0, deg: 37, w: 1 },
    { label: "‏45° לאמצע", x: 0, y: 0, deg: 45, w: 9 },
    { label: "מהמרכז ל-(0, 0)", x: 180, y: 90, deg: 49.4, w: 9 },
    { label: "לא נכנס לעולם", x: 180, y: 45, deg: 45, w: 9 },
  ];

  const billiardView = () => ({
    mount(box) {
      const D = { x: Number(box.dataset.x0 ?? 180), y: Number(box.dataset.y0 ?? 90), deg: Number(box.dataset.deg ?? 49.4), w: Number(box.dataset.w ?? 9) };
      const field = (cls, label, aria, max) => `<label class="bil-f">${label} <input type="number" class="${cls}" min="0" max="${max}" step="any" dir="ltr" inputmode="decimal" aria-label="${aria}"></label>`;
      const slider = (cls, label, aria, min, max, step) => `<label><span>${label}</span><input type="range" class="${cls}" min="${min}" max="${max}" step="${step}" dir="ltr" aria-label="${aria}"><output class="${cls}-o"></output></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        field("bil-x", "‏x₀", "מיקום הכדור לאורך השולחן, בסנטימטרים, 0 עד 360", BIL_A) +
        field("bil-y", "‏y₀", "מיקום הכדור לרוחב השולחן, בסנטימטרים, 0 עד 180", BIL_B) +
        slider("bil-dr", "כיוון", "כיוון המכה במעלות, 0 ימינה ו-90 למעלה", 0, 359, 1) +
        field("bil-deg", "מעלות", "כיוון המכה במעלות, גם עם שבר", 360) +
        `</div><div class="ex-controls">` +
        slider("bil-w", "רוחב הכיסים", "רוחב הכיסים w בסנטימטרים", 1, 20, 0.5) +
        `<label class="bil-chk"><input type="checkbox" class="bil-sep"> רוחב אחר לאמצעיים</label>` +
        `<span class="bil-wm-row" hidden>${slider("bil-wm", "האמצעיים", "רוחב הכיסים האמצעיים בסנטימטרים", 1, 20, 0.5)}</span>` +
        `<label class="bil-chk"><input type="checkbox" class="bil-rho"> כדור אמיתי, רדיוס 2.625 ס״מ</label>` +
        `</div><div class="ex-controls">` +
        PRESETS.map((p, i) => `<button type="button" class="md-button bil-pre" data-i="${i}">${p.label}</button>`).join("") +
        `</div><div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary bil-shoot">מכה</button>` +
        `<button type="button" class="md-button bil-back">חזרה לנקודת היציאה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button></div>` +
        `<svg class="figure bil-live" viewBox="0 0 ${W} ${HT}" role="group" aria-label="שולחן הביליארד, ששת הכיסים, הכדור, חץ הכיוון והמסלול"></svg>` +
        `<p class="bil-count" data-steady></p>` +
        `<p class="ex-summary bil-sum" aria-live="polite"></p>` +
        `<p class="ex-title">אותה מכה על השולחן הפתוח : קו ישר, וליד כל קו של כיסים הפער מנקודת הרשת הקרובה</p>` +
        `<svg class="figure bil-unf" role="img" aria-label="השולחן הפתוח : עותקי השולחן, נקודות הרשת של הכיסים והמסלול כקו ישר"></svg>` +
        `<span class="viz-legend"><span><i class="bil-key-felt"></i>השולחן עצמו</span><span><i class="box-copy"></i>העותקים</span>` +
        `<span><i class="bil-key-hole"></i>כיס</span><span><i class="bil-key-path"></i>המסלול</span><span><i class="s1"></i>פגיעה בדופן</span>` +
        `<span><i class="bil-key-gap"></i>הפער בקו של כיסים</span><span><i class="bil-key-in"></i>הכיס שהכדור נכנס אליו</span></span>` +
        `<p class="bil-unf-note"></p>` +
        `<section class="ex-proof bil-calc"><p class="ex-proof-title">החישוב של סעיפים ג ו-ד</p><div class="bil-calc-body"></div></section>`;
      const $ = (s) => box.querySelector(s);
      const ix = $(".bil-x"), iy = $(".bil-y"), idr = $(".bil-dr"), ideg = $(".bil-deg"), iw = $(".bil-w"), isep = $(".bil-sep"), iwm = $(".bil-wm"), irho = $(".bil-rho");
      const live = $(".bil-live"), unf = $(".bil-unf");
      const st = { x: D.x, y: D.y, deg: D.deg, w: D.w, wm: D.w, sep: false, rho: false, phase: "idle", d: 0, shot: null, raf: 0 };
      const rho = () => (st.rho ? BIL_RHO : 0);
      const clampPos = () => {
        const r = rho();
        st.x = Math.min(BIL_A - r, Math.max(r, st.x));
        st.y = Math.min(BIL_B - r, Math.max(r, st.y));
      };
      const syncFields = () => {
        ix.value = nf(st.x); iy.value = nf(st.y);
        ideg.value = nf(st.deg); idr.value = String(Math.round(st.deg) % 360);
        $(".bil-dr-o").textContent = `${nf(st.deg, 1)}°`;
        iw.value = String(st.w); $(".bil-w-o").textContent = `${nf(st.w, 1)} ס״מ`;
        iwm.value = String(st.wm); $(".bil-wm-o").textContent = `${nf(st.wm, 1)} ס״מ`;
        isep.checked = st.sep; irho.checked = st.rho;
        $(".bil-wm-row").hidden = !st.sep;
      };
      const still = () => navigator.webdriver === true || (typeof matchMedia === "function" && matchMedia("(prefers-reduced-motion: reduce)").matches);
      const compute = () => {
        st.shot = bilShot({ rho: rho(), x0: st.x, y0: st.y, deg: st.deg, wc: st.w, wm: st.sep ? st.wm : st.w });
      };

      // --- the real table ---
      const drawLive = () => {
        const sh = st.shot, r = rho(), wm = st.sep ? st.wm : st.w;
        let s = `<rect class="bil-rail" x="${PAD - 9}" y="${PAD - 9}" width="${BIL_A * S + 18}" height="${BIL_B * S + 18}" rx="10"/>` +
          `<rect class="bil-felt" x="${PAD}" y="${PAD}" width="${BIL_A * S}" height="${BIL_B * S}"/>`;
        for (let i = 0; i < 3; i++) for (let j = 0; j < 2; j++) {
          const px = r + (i * (BIL_A - 2 * r)) / 2, py = r + j * (BIL_B - 2 * r), rad = ((i === 1 ? wm : st.w) / 2) * S;
          const isIn = st.phase === "done" && sh.pocket && sh.pocket.i === i && sh.pocket.j === j;
          s += `<circle class="bil-hole${isIn ? " is-in" : ""}" cx="${PX(px).toFixed(1)}" cy="${PY(py).toFixed(1)}" r="${Math.max(2.5, rad).toFixed(1)}"><title>${BIL_NAMES[i][j]}</title></circle>`;
        }
        const ballR = Math.max(5, (r || 2.625) * S);
        if (st.phase === "idle") {
          // the aim: the first leg of the path, dashed, and the arrow to drag
          const first = sh.cross.find((e) => e.t > 1e-9);
          const t1 = Math.min(sh.T, first ? first.t : sh.T);
          const [ex, ey] = bilAt(sh, t1);
          s += `<line class="bil-aim" x1="${PX(st.x).toFixed(1)}" y1="${PY(st.y).toFixed(1)}" x2="${PX(ex).toFixed(1)}" y2="${PY(ey).toFixed(1)}"/>`;
        } else {
          const pts = [[st.x, st.y], ...sh.cross.filter((e) => e.t < st.d).map((e) => e.at), bilAt(sh, st.d)];
          s += `<polyline class="bil-trail" points="${pts.map(([x, y]) => `${PX(x).toFixed(1)},${PY(y).toFixed(1)}`).join(" ")}"/>`;
          sh.cross.filter((e) => e.t < st.d).slice(0, 60).forEach((e, n) => {
            s += `<circle class="s1-dot" cx="${PX(e.at[0]).toFixed(1)}" cy="${PY(e.at[1]).toFixed(1)}" r="4"><title>פגיעה ${n + 1}</title></circle>`;
          });
        }
        const [bx, by] = st.phase === "idle" ? [st.x, st.y] : bilAt(sh, st.d);
        const sunk = st.phase === "done" && sh.pocket;
        if (!sunk) s += `<circle class="bil-ball" cx="${PX(bx).toFixed(1)}" cy="${PY(by).toFixed(1)}" r="${ballR.toFixed(1)}"/>`;
        // the handles: the ball at its start, and the tip of the aim arrow
        const th = (st.deg * Math.PI) / 180, L = 48;
        const tx = st.x + L * Math.cos(th), ty = st.y + L * Math.sin(th);
        s += `<g class="bil-h bil-start" data-drag="ball" tabindex="0" role="button" aria-label="הכדור ב-(${nf(st.x, 1)}, ${nf(st.y, 1)}) : גוררים, או מזיזים בחיצים (עם Shift בקפיצות)">` +
          `<circle class="bil-hit" cx="${PX(st.x).toFixed(1)}" cy="${PY(st.y).toFixed(1)}" r="18"/>` +
          (st.phase === "idle" ? "" : `<circle class="bil-ghost" cx="${PX(st.x).toFixed(1)}" cy="${PY(st.y).toFixed(1)}" r="${ballR.toFixed(1)}"/>`) + `</g>`;
        s += `<line class="bil-arrow" x1="${PX(st.x).toFixed(1)}" y1="${PY(st.y).toFixed(1)}" x2="${PX(tx).toFixed(1)}" y2="${PY(ty).toFixed(1)}"/>` +
          `<g class="bil-h bil-tip" data-drag="aim" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="360" aria-valuenow="${nf(st.deg, 1)}" aria-label="כיוון המכה : ${nf(st.deg, 1)} מעלות. גוררים, או מסובבים בחיצים">` +
          `<circle class="bil-hit" cx="${PX(tx).toFixed(1)}" cy="${PY(ty).toFixed(1)}" r="18"/><circle class="bil-tipdot" cx="${PX(tx).toFixed(1)}" cy="${PY(ty).toFixed(1)}" r="7"/></g>`;
        live.innerHTML = s;
      };

      // --- the unfolded table (the mirrored frame: right and up) ---
      const drawUnf = () => {
        const sh = st.shot, { A, B, X, Y, dx, dy } = sh, wc = st.w, wm = st.sep ? st.wm : st.w;
        const tw = Math.min(sh.T, dx > 0 ? (6 * A - X) / dx : Infinity, dy > 0 ? (5 * B - Y) / dy : Infinity);
        const X1 = X + tw * dx, Y1 = Y + tw * dy;
        const xb = Math.max(A, (Math.ceil((X1 + 1e-9) / (A / 2)) + (sh.hit ? 0 : 0)) * (A / 2)), yb = Math.max(B, Math.ceil((Y1 + 1e-9) / B) * B);
        const sc = Math.min((W - 2 * PAD) / xb, 380 / yb), w = Math.round(xb * sc + 2 * PAD), h = Math.round(yb * sc + 2 * PAD);
        const ux = (x) => PAD + x * sc, uy = (y) => PAD + (yb - y) * sc;
        let s = "";
        for (let i = 0; i * A < xb - 1e-9; i++) for (let j = 0; j * B < yb - 1e-9; j++) {
          s += `<rect class="${i || j ? "box-copy" : "bil-felt"}" x="${ux(i * A).toFixed(1)}" y="${uy(Math.min(yb, (j + 1) * B)).toFixed(1)}" width="${(Math.min(A, xb - i * A) * sc).toFixed(1)}" height="${(B * sc).toFixed(1)}"/>`;
        }
        for (let k = 1; k * (A / 2) < xb; k += 2) s += `<line class="bil-mid" x1="${ux((k * A) / 2).toFixed(1)}" y1="${uy(0).toFixed(1)}" x2="${ux((k * A) / 2).toFixed(1)}" y2="${uy(yb).toFixed(1)}"/>`;
        const passed = X + st.d * dx;
        // the gaps at the lines of pockets the ball has passed (all of them once it is done)
        sh.checks.forEach((c) => {
          const px = (c.k * A) / 2;
          if (px < 0 || px > xb + 1e-9 || c.back) return;
          if (st.phase === "idle" || (st.phase === "run" && passed < px)) return;
          if (c.yk > yb + B || c.yk < -B) return;
          s += `<line class="bil-gap${c.ok ? " is-in" : ""}" x1="${ux(px).toFixed(1)}" y1="${uy(c.yk).toFixed(1)}" x2="${ux(px).toFixed(1)}" y2="${uy(c.m * B).toFixed(1)}"><title>k = ${c.k} : פער של ${nf(c.gap, 1)} ס״מ</title></line>`;
        });
        for (let k = 0; k * (A / 2) <= xb + 1e-9; k++) for (let m = 0; m * B <= yb + 1e-9; m++) {
          const isIn = st.phase === "done" && sh.hit && sh.hit.k === k && sh.hit.m === m;
          const rad = ((k % 2 ? wm : wc) / 2) * sc;
          s += `<circle class="bil-hole${isIn ? " is-in" : ""}" cx="${ux((k * A) / 2).toFixed(1)}" cy="${uy(m * B).toFixed(1)}" r="${Math.max(2.5, rad).toFixed(1)}"/>`;
        }
        s += `<line class="bil-ghost-line" x1="${ux(X).toFixed(1)}" y1="${uy(Y).toFixed(1)}" x2="${ux(X1).toFixed(1)}" y2="${uy(Y1).toFixed(1)}"/>`;
        if (st.phase !== "idle") {
          const t = Math.min(st.d, tw), cx = X + t * dx, cy = Y + t * dy;
          s += `<line class="bil-path" x1="${ux(X).toFixed(1)}" y1="${uy(Y).toFixed(1)}" x2="${ux(cx).toFixed(1)}" y2="${uy(cy).toFixed(1)}" stroke-width="2.5"/>`;
          sh.cross.filter((e) => e.t < t).slice(0, 80).forEach((e) => {
            s += `<circle class="s1-dot" cx="${ux(X + e.t * dx).toFixed(1)}" cy="${uy(Y + e.t * dy).toFixed(1)}" r="3.5"/>`;
          });
          if (!(st.phase === "done" && sh.pocket) && st.d <= tw) s += `<circle class="bil-ball" cx="${ux(cx).toFixed(1)}" cy="${uy(cy).toFixed(1)}" r="5"/>`;
        }
        s += `<circle class="ink-dot" cx="${ux(X).toFixed(1)}" cy="${uy(Y).toFixed(1)}" r="4"/>`;
        unf.setAttribute("viewBox", `0 0 ${w} ${h}`);
        unf.innerHTML = s;
        const notes = [];
        if (sh.mx || sh.my) notes.push(`הכדור נע ${sh.mx && sh.my ? "שמאלה ולמטה" : sh.mx ? "שמאלה" : "למטה"}, ולכן השולחן הפתוח משוקף כך שהמסלול עולה ימינה.`);
        if (tw < sh.T - 1e-6) notes.push(`השרטוט מראה רק את תחילת הדרך, ${ltr(nf(tw, 0))} מתוך ${ltr(nf(sh.T, 0))} ס״מ.`);
        $(".bil-unf-note").innerHTML = notes.join(" ");
      };

      // --- the texts ---
      const wallName = { top: "העליונה", bottom: "התחתונה", left: "השמאלית", right: "הימנית" };
      const drawTexts = () => {
        const sh = st.shot;
        const n = st.phase === "idle" ? 0 : sh.cross.filter((e) => e.t < st.d).length;
        $(".bil-count").innerHTML = `פגיעות בדפנות${NB}: ${ltr(n)} · דרך${NB}: ${ltr(nf(st.phase === "idle" ? 0 : st.d, 0))} ס״מ`;
        let sum;
        if (st.phase !== "done") sum = st.phase === "run" ? "הכדור בדרך…" : `לוחצים "מכה", או Enter על הכדור או על החץ.`;
        else if (sh.pocket) {
          const walls = sh.cross.filter((e) => e.t < sh.T).slice(0, 6).map((e) => wallName[e.wall]);
          const hits = sh.cushions === 0 ? "בלי לפגוע בדופן" : sh.cushions === 1 ? `אחרי פגיעה אחת, בדופן ${walls[0]}` :
            `אחרי ${ltr(sh.cushions)} פגיעות` + (sh.cushions <= 6 ? ` (בדופן ${walls.join(", ")})` : "");
          sum = `הכדור נכנס ל${sh.pocket.name.slice(1)} ${ltr(`(${nf(sh.pocket.x)}, ${nf(sh.pocket.y)})`)} ${hits}, מסלול של ${ltr(nf(sh.T, 1))} ס״מ.`;
        } else sum = `הכדור לא נכנס לשום כיס. אחרי ${ltr(sh.cushions)} פגיעות הוא עוד על השולחן, והחישוב לא מצא כיס ב-${ltr(BIL_KMAX)} קווים של הרשת${NB}: המסלול מחזורי ומפספס את כל הכיסים.`;
        $(".bil-sum").innerHTML = sum;
        // the calculation
        const body = $(".bil-calc-body");
        if (sh.dx === 0) {
          body.innerHTML = `<p>התנועה אנכית לגמרי${NB}: הכדור עולה ויורד על אותו קו, ונכנס רק אם הקו עובר בכיס.</p>`;
          return;
        }
        const corner = Math.abs(sh.X) < 1e-9 && Math.abs(sh.Y) < 1e-9;
        const tanP = sh.dy / sh.dx;
        const sep = st.sep && st.wm !== st.w;
        let p = `<p>${st.rho ? `כדור ברדיוס 2.625${NB}: המרכז נע על שולחן של ${ltr(`${nf(sh.A)} × ${nf(sh.B)}`)}. ` : ""}` +
          `הערכים${NB}: ${ltr(`s = a·tan α / (2b) = ${nf(sh.s, 4)}`)}` + (corner ? "" : `, ${ltr(`c = (y₀ − x₀ tan α)/b = ${nf(sh.c, 4)}`)}`) +
          `, ${ltr(`ε = w/(2b cos α) = ${nf(sh.epsC, 4)}`)}` + (sep ? ` לפינות ו-${ltr(nf(sh.epsM, 4))} לאמצעיים` : "") +
          (sh.mx || sh.my ? ` (אחרי השיקוף${NB}: ${ltr(`tan α = ${nf(tanP, 4)}`)})` : "") + `.</p>`;
        const shown = sh.checks.filter((c) => !c.back || c.ok);
        const rows = shown.length > 8 ? [...shown.slice(0, 6), null, ...shown.slice(-1)] : shown;
        p += `<table class="bil-checks"><thead><tr><th>‏k</th><th>‏ks + c</th><th>‏m</th><th>המרחק</th><th>נכנס?</th></tr></thead><tbody>` +
          rows.map((c) => (c === null ? `<tr><td colspan="5">…</td></tr>` :
            `<tr${c.ok ? ' class="is-in"' : ""}><td>${c.k}</td><td>${ltr(nf(c.yk / sh.B, 4))}</td><td>${c.m}</td><td>${ltr(`${nf(c.d, 2)} ס״מ`)}</td><td>${c.ok ? "כן" : c.d < 1e-9 ? "כיס היציאה" : "לא"}</td></tr>`)).join("") +
          `</tbody></table>`;
        if (sh.hit) {
          const K = sh.hit.k, m = sh.hit.m, k4 = mod(K, 4);
          const rule = k4 % 2 ? `${ltr("K")} אי־זוגי` : `${ltr(`K ≡ ${k4} (mod 4)`)}`;
          p += `<p>התוצאה${NB}: ${ltr(`K = ${K}`)}, ${ltr(`m = ${m}`)}${NB}: ${rule}, ו-${ltr("m")} ${mod(m, 2) ? "אי־זוגי" : "זוגי"}${NB}: ${sh.mx || sh.my ? "בשולחן המשוקף זה " + BIL_NAMES[bilPocketAt(K, m)[0]][bilPocketAt(K, m)[1]] + ", ובשולחן האמיתי " : ""}${sh.pocket.name}.` +
            (corner ? ` מהפינה זו השורה של סעיף ג.` : ` זו הטבלה של סעיף ד.`) + `</p>`;
        } else p += `<p>אין ${ltr("k")} עד ${ltr(BIL_KMAX)} עם מרחק קטן מחצי רוחב הכיס.</p>`;
        body.innerHTML = p;
      };

      const draw = () => { drawLive(); drawUnf(); drawTexts(); };
      const stopAnim = () => { if (st.raf) cancelAnimationFrame(st.raf); st.raf = 0; };
      const reset = () => { stopAnim(); st.phase = "idle"; st.d = 0; };
      const changed = () => { clampPos(); syncFields(); reset(); compute(); draw(); };
      const shoot = () => {
        stopAnim();
        compute();
        const L = st.shot.T;
        if (still() || L <= 0) { st.phase = "done"; st.d = L; draw(); return; }
        st.phase = "run"; st.d = 0;
        const dur = Math.min(9000, Math.max(1200, (L / 500) * 1000)), t0 = performance.now();
        const tick = (now) => {
          st.d = Math.min(L, ((now - t0) / dur) * L);
          if (st.d >= L) { st.phase = "done"; st.raf = 0; draw(); return; }
          draw();
          st.raf = requestAnimationFrame(tick);
        };
        draw();
        st.raf = requestAnimationFrame(tick);
      };

      // --- the controls ---
      const num = (el, lo, hi) => { const v = Number(el.value); return el.value.trim() === "" || !Number.isFinite(v) ? null : Math.min(hi, Math.max(lo, v)); };
      ix.addEventListener("change", () => { const v = num(ix, 0, BIL_A); if (v !== null) st.x = v; changed(); });
      iy.addEventListener("change", () => { const v = num(iy, 0, BIL_B); if (v !== null) st.y = v; changed(); });
      idr.addEventListener("input", () => { st.deg = Number(idr.value); changed(); });
      ideg.addEventListener("change", () => { const v = Number(ideg.value); if (ideg.value.trim() !== "" && Number.isFinite(v)) st.deg = mod(v, 360); changed(); });
      iw.addEventListener("input", () => { st.w = Number(iw.value); if (!st.sep) st.wm = st.w; changed(); });
      isep.addEventListener("change", () => { st.sep = isep.checked; if (!st.sep) st.wm = st.w; changed(); });
      iwm.addEventListener("input", () => { st.wm = Number(iwm.value); changed(); });
      irho.addEventListener("change", () => { st.rho = irho.checked; changed(); });
      $(".bil-shoot").addEventListener("click", shoot);
      $(".bil-back").addEventListener("click", () => { reset(); draw(); });
      box.querySelectorAll(".bil-pre").forEach((btn) => btn.addEventListener("click", () => {
        const p = PRESETS[Number(btn.dataset.i)];
        Object.assign(st, { x: p.x, y: p.y, deg: p.deg, w: p.w, wm: p.w, sep: false, rho: false });
        changed();
        ix.dispatchEvent(new Event("input", { bubbles: true }));    // the link and the remembered state read the fields
        shoot();
      }));
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { x: D.x, y: D.y, deg: D.deg, w: D.w, wm: D.w, sep: false, rho: false });
        changed();
      });

      // dragging the ball (its start) or the tip of the arrow
      const at = (e) => {
        const p = live.createSVGPoint();
        p.x = e.clientX; p.y = e.clientY;
        const m = live.getScreenCTM();
        const q = m ? p.matrixTransform(m.inverse()) : { x: 0, y: 0 };
        return [(q.x - PAD) / S, BIL_B - (q.y - PAD) / S];
      };
      let drag = null;
      const move = (e) => {
        const [x, y] = at(e);
        if (drag === "ball") { st.x = Math.round(x); st.y = Math.round(y); } else {
          const d = (Math.atan2(y - st.y, x - st.x) * 180) / Math.PI;
          st.deg = mod(Math.round(d * 2) / 2, 360);
        }
        changed();
      };
      live.addEventListener("pointerdown", (e) => {
        const t = e.target.closest("[data-drag]");
        if (!t) return;
        drag = t.dataset.drag;
        live.setPointerCapture(e.pointerId);
        live.classList.add("is-dragging");
        e.preventDefault();
        if (drag === "aim") move(e); else { reset(); draw(); }
      });
      live.addEventListener("pointermove", (e) => { if (drag) move(e); });
      const end = () => {
        if (!drag) return;
        const was = drag;
        drag = null;
        live.classList.remove("is-dragging");
        (was === "ball" ? ix : ideg).dispatchEvent(new Event("input", { bubbles: true }));
        const el = live.querySelector(was === "ball" ? ".bil-start" : ".bil-tip");
        if (el) el.focus({ preventScroll: true });
      };
      live.addEventListener("pointerup", end);
      live.addEventListener("pointercancel", end);
      // keyboard: arrows move the ball (1 cm, 10 with Shift) or turn the arrow (1°, 10 with Shift); Enter shoots
      live.addEventListener("keydown", (e) => {
        const t = e.target.closest("[data-drag]");
        if (!t) return;
        if (e.key === "Enter") { e.preventDefault(); shoot(); return; }
        const d = arrowStep(e);
        if (!d) return;
        e.preventDefault(); e.stopPropagation();
        if (t.dataset.drag === "ball") {
          if (e.key === "ArrowLeft" || e.key === "ArrowRight") st.x += d; else st.y += d;
        } else st.deg = mod(st.deg + d, 360);
        const which = t.dataset.drag;
        changed();
        const el = live.querySelector(which === "ball" ? ".bil-start" : ".bil-tip");
        if (el) el.focus({ preventScroll: true });
        (which === "ball" ? ix : ideg).dispatchEvent(new Event("input", { bubbles: true }));
      });

      syncFields();
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { billiard: billiardView },
    help: {
      billiard: "גוררים את הכדור לכל מקום על השולחן ואת קצה החץ לכל כיוון, או מקלידים x₀, y₀ ומעלות. מחוון קובע את רוחב הכיסים, ואפשר רוחב אחר לכיסים האמצעיים וכדור ברדיוס אמיתי. \"מכה\" מריצה את הכדור עד הכיס, ומתחת אותה מכה על השולחן הפתוח עם הפער בכל קו של כיסים; החישוב של סעיפים ג ו-ד מראה את s, ε, K ו-m. הכפתורים טוענים את המכות של הדף.",
    },
    models: { bilShot, bilAt, bilFold: fold, bilPocketAt, BIL_RHO },
  });
})();
