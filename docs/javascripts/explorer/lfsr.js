// kinds: lfsr
//   lfsr                   0036        a width of 3 to 8 bits: tick the taps, step or play from 0…01; one picture of every cycle in the order of the step (up to 6 bits), the seed's lit as it goes; the register; a strip of clk, state, s[0] and fb; the polynomials and their periods, the primitive ones counted
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, bitsOf, code, f, ltr, waveStrip } = dvqExplorers.lib;

  // LFSR (0036): the page's step and period on the mask of the taps (bit i of the mask is
  // s[i]; x^k is s[width - k]); the walk from a seed until a state repeats; the eight
  // polynomials x^4 + ... + 1 with their periods.
  const lfsrNext = (state, mask, width) => {
    let fb = 0;
    for (let v = state & mask; v; v >>= 1) fb ^= v & 1;
    return (state >> 1) | (fb << (width - 1));
  };
  const lfsrWalk = (mask, width, seed = 1) => {
    const seen = new Map(), states = [];
    let s = seed;
    while (!seen.has(s)) { seen.set(s, states.length); states.push(s); s = lfsrNext(s, mask, width); }
    return { states, period: states.length - seen.get(s), back: seen.get(s) };
  };
  const lfsrPeriod = (mask, width, seed = 1) => lfsrWalk(mask, width, seed).period;
  const lfsrPoly = (mask, width) => {
    const terms = [`x^${width}`];
    for (let k = width - 1; k >= 1; k--) if ((mask >> (width - k)) & 1) terms.push(k === 1 ? "x" : `x^${k}`);
    return terms.concat("1").join(" + ");
  };
  // The LFSR strip: one slot per state visited so far (step 0 .. k), its value, the bit
  // that leaves (s[0]) and the feedback bit that enters the next state.
  const lfsrStrip = (mask, width, k, seed = 1) => {
    const walk = lfsrWalk(mask, width, seed), total = walk.period;
    const states = walk.states.concat(walk.states[walk.back]).slice(0, Math.min(k, total) + 1);
    const fb = states.map((s) => { let v = 0; for (let x = s & mask; x; x >>= 1) v ^= x & 1; return v; });
    return { states, out: states.map((s) => s & 1), fb, total };
  };
  // Every cycle of the step: x^n is always a tap (bit 0 of the mask, s[0], the bit that
  // leaves), so the next state gives s[0] back and the step can be undone; the non-zero
  // states then split into disjoint cycles. The first one is the cycle of the seed 0…01,
  // in the order of the step; the rest follow in order of their smallest state.
  const lfsrCycles = (mask, width) => {
    const n = 1 << width, done = new Uint8Array(n), cycles = [];
    for (let s0 = 1; s0 < n; s0++) {
      if (done[s0]) continue;
      const c = [];
      for (let v = s0; !done[v]; v = lfsrNext(v, mask, width)) { done[v] = 1; c.push(v); }
      cycles.push(c);
    }
    return cycles;
  };
  // φ(2^n − 1) / n: the number of primitive polynomials of degree n (Euler's totient by trial division)
  const lfsrPrimitiveCount = (width) => {
    let n = (1 << width) - 1, phi = n;
    for (let p = 2; p * p <= n; p++) if (n % p === 0) { while (n % p === 0) n /= p; phi -= phi / p; }
    if (n > 1) phi -= phi / n;
    return phi / width;
  };
  const lfsrTable = (width) => {
    const rows = [];
    for (let m = 0; m < 1 << (width - 1); m++) {
      const mask = 1 | (m << 1);
      rows.push({ mask, poly: lfsrPoly(mask, width), period: lfsrPeriod(mask, width) });
    }
    return rows;
  };

  // The LFSR box (0036): a width of 3 to 8 bits, tick the taps (x^n and 1 are fixed), step
  // or play from 0…01. Up to 6 bits one picture holds every state in the order of the step:
  // the seed's cycle as a ring that lights up as the steps go round it, the other cycles as
  // smaller rings beside it, and 0 with its loop (in the middle of the seed's ring when
  // there is room). Under it the register and the step in words; beside them (the side
  // column) a timing strip of clk, the state, s[0] and the feedback bit for every step so
  // far, and the table of the polynomials with their periods: every one up to 5 bits, the
  // primitive ones from 6 bits on, with the count φ(2^n − 1) / n, about eight rows in view.
  const lfsrView = () => ({
    mount(box) {
      const SEED = 1, RING_MAX = 6, FULL_TABLE = 5, NB = " ";
      const st = { width: 4, mask: 0b0011, k: 0 };
      const bits = (v) => bitsOf(v, st.width);
      const states = () => (1 << st.width) - 1;
      const sup = (k) => (k === 1 ? "x" : `x<sup>${k}</sup>`);
      const polyHtml = (mask, width = st.width) => {
        const t = [`x<sup>${width}</sup>`];
        for (let k = width - 1; k >= 1; k--) if ((mask >> (width - k)) & 1) t.push(sup(k));
        return ltr(t.concat("1").join(" + "));
      };
      box.innerHTML =
        `<div class="ex-controls"><label>רוחב <select class="ex-width" aria-label="מספר הביטים">${[3, 4, 5, 6, 7, 8].map((w) => `<option value="${w}"${w === 4 ? " selected" : ""}>${w} ביטים</option>`).join("")}</select></label>` +
        `<span class="lf-taps" dir="ltr" role="group" aria-label="בחירת ה-taps"></span>` +
        `<span class="lf-presets">מהשאלה${NB}: <button type="button" class="md-button ex-preset" data-mask="3">${ltr("x<sup>4</sup> + x<sup>3</sup> + 1")}</button> ` +
        `<button type="button" class="md-button ex-preset" data-mask="5">${ltr("x<sup>4</sup> + x<sup>2</sup> + 1")}</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">צעד</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1000">איטי</option><option value="500" selected>בינוני</option><option value="180">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד שהמצב חוזר</button><span class="ex-pos"></span></div>` +
        `<div class="lf-ring"></div>` +
        `<p class="ex-title lf-reg-title">הרגיסטר${NB}: ${code("s[0]")} יוצא, וה-XOR של ה-taps נכנס משמאל</p><div class="lf-reg"></div>` +
        `<div class="lf-panel"><p class="lf-state"></p><p class="lf-fb"></p>` +
        `<p class="ex-summary lf-sum" aria-live="polite"></p></div><p class="lf-cycles-text"></p>` +
        `<p class="ex-title lf-strip-title">רצועת התזמון${NB}: המצב, ${code("s[0]")} שיוצא ו-${code("fb")} שנכנס</p>` +
        `<div class="wv-wrap lf-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-LFSR, גלילה אופקית"></div>` +
        `<p class="ex-title lf-table-title"></p><div class="lf-table" tabindex="0" role="group" aria-label="טבלת הפולינומים, גלילה"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null, tableKey = "";
      // the tap boxes follow the width: x^width and 1 fixed, a box per middle power
      const tapsHtml = () => {
        const ks = []; for (let k = st.width - 1; k >= 1; k--) ks.push(k);
        $(".lf-taps").innerHTML = `<span class="lf-fixed">${ltr(`x<sup>${st.width}</sup>`)} +</span> ` +
          ks.map((k) => `<label><input type="checkbox" class="ex-tap" data-k="${k}"> <span>${ltr(sup(k))} +</span></label>`).join(" ") + `<span class="lf-fixed">1</span>`;
        box.querySelectorAll(".ex-tap").forEach((c) => c.addEventListener("change", () => {
          const bit = 1 << (st.width - Number(c.dataset.k));
          st.mask = c.checked ? st.mask | bit : st.mask & ~bit;
          stop(); st.k = 0; draw();
        }));
      };
      // The picture of every cycle (up to 6 bits): the seed's cycle first, its states round a
      // ring in the order of the step, the k steps taken so far lit and the current state
      // marked; the other cycles as smaller rings, a colour each in turn, packed in rows; 0
      // with its loop in the middle of the seed's ring when it fits there, else beside it.
      // The states are written in their circles up to 4 bits; from 5 bits 31 labels would be
      // too small to read at this size, and a state's value is its tooltip.
      const cyclesSvg = (cycles, k) => {
        const w = st.width, rr = w <= 4 ? 14 : w === 5 ? 7 : 5, label = w <= 4, gap = 12;
        const zr = label ? rr : 10, space = 2 * rr + (rr > 8 ? 8 : 4);
        const loop = (x, y, r) => `<path class="lf-loop" d="M${f(x + r * 0.7)},${f(y - r * 0.7)} a ${f(r * 0.8)} ${f(r * 0.8)} 0 1 0 ${f(-r * 1.4)} 0" marker-end="url(#lf-arrow)"/>`;
        const rings = cycles.map((c) => ({ c, R: c.length === 1 ? 0 : Math.max(rr * 1.8, (c.length * space) / (2 * Math.PI)) }));
        const inner = rings[0].R - rr - 4 >= 1.9 * zr + 18;   // room for 0, its loop and the length
        if (!inner) rings.push({ c: [0], R: 0 });
        // a ring's box: its circle of states, or one state with its loop above it
        rings.forEach((g) => { g.D = g.R ? 2 * (g.R + rr) + 4 : 3.8 * (g.c[0] ? rr : zr) + 4; });
        // the rows about 1.3 times wider than the rings' area is tall, as the column is wide
        const area = Math.sqrt(rings.reduce((a, g) => a + (g.D + gap) ** 2, 0));
        const Wd = Math.max(rings[0].D, 1.3 * area, rings.length === 2 ? rings[0].D + gap + rings[1].D : 0);
        const rows = [[]];
        let x = 0;
        rings.forEach((g) => { if (x && x + g.D > Wd) { rows.push([]); x = 0; } rows[rows.length - 1].push(g); x += g.D + gap; });
        const rowW = (r) => r.reduce((a, g) => a + g.D, 0) + gap * (r.length - 1);
        const W = Math.max(...rows.map(rowW)) + 2 * gap;
        let y = gap;
        rows.forEach((r) => {
          const h = Math.max(...r.map((g) => g.D));
          let x0 = (W - rowW(r)) / 2;
          r.forEach((g) => { g.cx = x0 + g.D / 2; g.cy = y + h / 2; x0 += g.D + gap; });
          y += h + gap;
        });
        const H = y, L0 = cycles[0].length, at = k % L0;
        // as large as one screen allows: at most 19rem wide and 11rem tall
        const disp = Math.min(19, (11 * W) / H);
        let s = `<svg class="lf-live lf-cyc" viewBox="0 0 ${f(W)} ${f(H)}" style="max-width:${f(disp)}rem" role="img" ` +
          `aria-label="המצבים בסדר הצעד${NB}: ${cycles.length === 1 ? "מחזור אחד" : `${cycles.length} מחזורים`} ונקודת השבת 0, ${k} צעדים מ-${bits(SEED)}">` +
          `<defs><marker id="lf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 6 : 4}" markerHeight="${rr > 8 ? 6 : 4}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker></defs>`;
        const node = (v, px, py, r, cls) => `<g class="lf-node${cls}"><circle cx="${f(px)}" cy="${f(py)}" r="${r}"><title>${bits(v)}</title></circle>` +
          (label || !v ? `<text x="${f(px)}" y="${f(py + 3.5)}" text-anchor="middle">${label ? bits(v) : "0"}</text>` : "") + `</g>`;
        rings.forEach((g, j) => {
          const L = g.c.length, tint = j === 0 ? "" : g.c[0] ? ` lf-c${1 + ((j - 1) % 2)}` : " lf-zero";
          const pos = (i) => { const ang = -Math.PI / 2 + (i / L) * 2 * Math.PI; return [g.cx + g.R * Math.cos(ang), g.cy + g.R * Math.sin(ang)]; };
          if (L === 1) {
            const r = g.c[0] ? rr : zr;
            s += loop(g.cx, g.cy, r) + node(g.c[0], g.cx, g.cy, r, tint);
            return;
          }
          for (let i = 0; i < L; i++) {
            // a chord bent outward a little, so a cycle of two shows two arrows
            const [x1, y1] = pos(i), [x2, y2] = pos((i + 1) % L), mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
            const ox = mx - g.cx, oy = my - g.cy, od = Math.hypot(ox, oy) || 1, bend = L === 2 ? g.R * 0.6 : rr * 0.6;
            const qx = mx + (ox / od) * bend + (L === 2 ? (i ? -1 : 1) * g.R * 0.6 : 0), qy = my + (oy / od) * bend;
            const u1 = Math.hypot(qx - x1, qy - y1) || 1, u2 = Math.hypot(x2 - qx, y2 - qy) || 1;
            const cls = j ? tint : `${i < k ? " is-seen" : ""}${i === k - 1 ? " is-cur" : ""}`;
            s += `<path class="lf-edge${cls}" d="M${f(x1 + ((qx - x1) / u1) * rr)},${f(y1 + ((qy - y1) / u1) * rr)} Q${f(qx)},${f(qy)} ${f(x2 - ((x2 - qx) / u2) * (rr + 2))},${f(y2 - ((y2 - qy) / u2) * (rr + 2))}" marker-end="url(#lf-arrow)"/>`;
          }
          g.c.forEach((v, i) => {
            const [px, py] = pos(i);
            s += node(v, px, py, rr, j ? tint : `${i <= k ? " is-seen" : ""}${i === at ? " is-cur" : ""}${v === SEED ? " is-seed" : ""}`);
          });
          if (j === 0 && inner) {
            s += loop(g.cx, g.cy, zr) + node(0, g.cx, g.cy, zr, " lf-zero") +
                 `<text class="tick" x="${f(g.cx)}" y="${f(g.cy + zr + 16)}" text-anchor="middle">${L}</text>`;
          } else s += `<text class="tick" x="${f(g.cx)}" y="${f(g.cy + 4)}" text-anchor="middle">${L}</text>`;
        });
        return s + "</svg>";
      };
      // from 7 bits there is no picture: the strip lists the states
      const noRing = () => `<p class="ex-note">‏${ltr(states())} מצבים שאינם אפס${NB}: יותר מדי לציור. רצועת התזמון מראה את המצבים שבוקרו, בהקסה.</p>`;
      // the cycles in words: why they are disjoint, their lengths, the seed's one
      const cyclesText = (cycles) => {
        const n = states(), lens = cycles.map((c) => c.length);
        const byLen = new Map(); lens.forEach((l) => byLen.set(l, (byLen.get(l) || 0) + 1));
        const sum = lens.length <= 8 ? lens.join(" + ") : [...byLen].sort((u, v) => v[0] - u[0]).map(([l, k]) => `${k} × ${l}`).join(" + ");
        return `הצעד הפיך (${code("s[0]")} הוא תמיד tap, האיבר ${ltr(`x<sup>${st.width}</sup>`)}), ולכן המצבים מתחלקים למחזורים זרים והאפס חוזר לעצמו. ` + (lens.length === 1
            ? `<span class="lf-ok">כאן מחזור אחד של כל ${ltr(n)} המצבים${NB}: הפולינום פרימיטיבי.</span>`
            : `כאן ${ltr(lens.length)} מחזורים, ${ltr(`${sum} = ${n}`)}, ואף התחלה לא מגיעה ליותר מ-${ltr(Math.max(...lens))} מצבים.`);
      };
      // The register (V4): s[width − 1] .. s[0] left to right, the taps outlined and wired to
      // one XOR under the row, its output fb back into the left end, s[0] out at the right.
      const regSvg = (cur, fb) => {
        const n = st.width, CW = 40, X0 = 64, Y = 22, CH = 40, BUS = Y + CH + 30, W = X0 + n * (CW + 4) + 70, H = BUS + 34;
        const cx = (b) => X0 + (n - 1 - b) * (CW + 4) + CW / 2;
        let s = `<svg class="figure lf-regsvg" viewBox="0 0 ${W} ${H}" style="max-width:${(W / 25).toFixed(1)}rem" role="img" aria-label="הרגיסטר במצב ${bits(cur)}, היזון חוזר ${fb}">` +
          `<defs><marker id="lf-arrow3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-head"/></marker></defs>`;
        const taps = [];
        for (let b = 0; b < n; b++) if ((st.mask >> b) & 1) taps.push(b);
        // the wires: down from every tap to the bus, along it to the XOR, up and into the left end
        taps.forEach((b) => { s += `<line class="lf-wire" x1="${cx(b)}" y1="${Y + CH}" x2="${cx(b)}" y2="${BUS}"/><circle class="lf-dot" cx="${cx(b)}" cy="${BUS}" r="3"/>`; });
        const xorX = 26;
        s += `<line class="lf-wire" x1="${xorX + 12}" y1="${BUS}" x2="${Math.max(...taps.map(cx))}" y2="${BUS}"/>` +
             `<circle class="lf-xor" cx="${xorX}" cy="${BUS}" r="12"/><path class="lf-wire" d="M${xorX - 8},${BUS} H${xorX + 8} M${xorX},${BUS - 8} V${BUS + 8}"/>` +
             `<path class="lf-wire" d="M${xorX},${BUS - 12} V${Y + CH / 2} H${X0 - 2}" fill="none" marker-end="url(#lf-arrow3)"/>` +
             `<text class="lf-regfb" x="${xorX + 4}" y="${BUS + 28}" text-anchor="middle">fb = ${fb}</text>`;
        for (let b = 0; b < n; b++) {
          const x = cx(b) - CW / 2, v = (cur >> b) & 1, tap = taps.includes(b);
          s += `<rect class="lf-cell${v ? " is-one" : ""}${tap ? " is-tap" : ""}" x="${x}" y="${Y}" width="${CW}" height="${CH}" rx="4"/>` +
               `<text class="lf-cellv" x="${cx(b)}" y="${Y + CH / 2 + 7}" text-anchor="middle">${v}</text>` +
               `<text class="lf-celli" x="${cx(b)}" y="${Y - 6}" text-anchor="middle">s[${b}]</text>`;
        }
        const ox = cx(0) + CW / 2;
        s += `<path class="lf-wire" d="M${ox + 2},${Y + CH / 2} H${ox + 34}" marker-end="url(#lf-arrow3)"/><text class="lf-regfb" x="${ox + 48}" y="${Y + CH / 2 + 5}" text-anchor="middle">${cur & 1}</text>`;
        return s + "</svg>";
      };
      // the strip: every step so far, the bus in binary up to 6 bits and in hex beyond
      const stripHtml = () => {
        const sp = lfsrStrip(st.mask, st.width, st.k, SEED), hex = st.width > 6;
        const label = (v) => (hex ? `0x${v.toString(16).toUpperCase().padStart(2, "0")}` : bits(v));
        const SW = hex ? 40 : Math.max(36, Math.round(14 + 7.6 * st.width)), n = sp.states.length;
        return waveStrip([
          { name: "clk", kind: "clock" },
          { name: "state", kind: "bus", values: sp.states.map(label) },
          { name: "s[0]", kind: "bit", values: sp.out, cls: "wv-s2" },
          { name: "fb", kind: "bit", values: sp.fb, cls: "wv-s1" },
        ], n, { slotW: SW, cursor: n - 1, ticks: (k) => k, label: `רצועת התזמון של ה-LFSR${NB}: ${n} מצבים` });
      };
      // the table: every polynomial up to 5 bits, only the primitive ones from 6; drawn again
      // only for a new width or polynomial, and scrolled to show the current row
      const drawTable = () => {
        const n = states(), all = lfsrTable(st.width), prim = lfsrPrimitiveCount(st.width), full = st.width <= FULL_TABLE;
        const rows = full ? all : all.filter((r) => r.period === n);
        // the title on one line; from 6 bits every row has the same period, so the title gives it
        $(".lf-table-title").innerHTML = (full
          ? `כל ${ltr(all.length)} הפולינומים, הפרימיטיביים`
          : `הפרימיטיביים בלבד, מחזור ${ltr(n)}`) + `${NB}: ${ltr(`φ(${n}) / ${st.width} = ${prim}`)}`;
        const t = $(".lf-table");
        t.innerHTML = `<table><thead><tr><th>הפולינום</th><th>המסכה</th>${full ? "<th>המחזור</th>" : ""}</tr></thead><tbody>` +
          rows.map((r) => `<tr class="${r.mask === st.mask ? "is-cur" : ""}${r.period === n ? " is-max" : ""}"><td>${polyHtml(r.mask)}</td><td>${code(bits(r.mask))}</td>` +
            (full ? `<td>${ltr(r.period)}${r.period === n ? " ✓" : ""}</td>` : "") + `</tr>`).join("") +
          `</tbody></table>`;
        const tr = t.querySelector("tr.is-cur"), head = t.querySelector("thead");
        t.scrollTop = 0;
        if (tr && tr.offsetTop + tr.offsetHeight > t.clientHeight) t.scrollTop = tr.offsetTop - head.offsetHeight - (t.clientHeight - head.offsetHeight - tr.offsetHeight) / 2;
      };
      const draw = () => {
        const walk = lfsrWalk(st.mask, st.width, SEED), total = walk.period, n = states();
        st.k = Math.min(st.k, total);
        box.querySelectorAll(".ex-tap").forEach((c) => { c.checked = ((st.mask >> (st.width - Number(c.dataset.k))) & 1) === 1; });
        const cycles = lfsrCycles(st.mask, st.width);
        $(".lf-ring").innerHTML = st.width <= RING_MAX ? cyclesSvg(cycles, st.k) : noRing();
        $(".lf-cycles-text").innerHTML = cyclesText(cycles);
        const cur = st.k < total ? walk.states[st.k] : walk.states[walk.back];
        const tapsIdx = [];
        for (let i = 0; i < st.width; i++) if ((st.mask >> i) & 1) tapsIdx.push(i);
        let fb = 0; tapsIdx.forEach((i) => { fb ^= (cur >> i) & 1; });
        const next = lfsrNext(cur, st.mask, st.width);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${total}`;
        $(".ex-prev").disabled = st.k === 0;
        $(".lf-state").innerHTML = `המצב אחרי ${ltr(st.k)} צעדים${NB}: ${code(bits(cur))}` + (st.k === total ? ` — חזר למצב ההתחלה.` : ".");
        $(".lf-fb").innerHTML = `הצעד הבא${NB}: ${ltr(`${code("fb")} = ${code(tapsIdx.map((i) => `s[${i}]`).join(" ^ "))} = ${tapsIdx.map((i) => (cur >> i) & 1).join(" ^ ")} = ${fb}`)}, ` +
          `ואז ${ltr(`${code(`(${bits(cur)} >> 1) | (${fb} << ${st.width - 1})`)} = ${code(bits(next))}`)}.`;
        $(".lf-reg").innerHTML = regSvg(cur, fb);
        const wrap = $(".lf-strip");
        wrap.innerHTML = stripHtml();
        wrap.scrollLeft = wrap.scrollWidth;                // the current step in view
        const maximal = total === n;
        $(".lf-sum").innerHTML = st.k < total
          ? `בוקרו ${ltr(st.k + 1)} מצבים מתוך ${ltr(n)}. ` + (maximal ? `הפולינום פרימיטיבי${NB}: המחזור יהיה ${ltr(n)}.` : `המחזור של הפולינום הזה הוא ${ltr(total)}, ולכן ${ltr(n - total)} מצבים לא יבוקרו לעולם.`)
          : maximal ? `<span class="lf-ok">מחזור מקסימלי${NB}: ${ltr(n)} צעדים, כל מצב שאינו אפס פעם אחת ✓</span>`
          : `<span class="lf-bad">מחזור של ${ltr(total)} צעדים בלבד${NB}: ${ltr(n - total)} מצבים לא בוקרו.</span>`;
        const key = `${st.width}:${st.mask}`;
        if (key !== tableKey) { tableKey = key; drawTable(); }
        answer(box, st.k >= total ? (maximal ? `הפולינום ${polyHtml(st.mask)} פרימיטיבי${NB}: מחזור מקסימלי של ${ltr(n)} צעדים.`
          : `הפולינום ${polyHtml(st.mask)} אינו פרימיטיבי${NB}: מחזור של ${ltr(total)} צעדים בלבד מתוך ${ltr(n)}.`) : null, ".lf-table tr.is-cur");
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => lfsrWalk(st.mask, st.width, SEED).period;
      // a new width: the first primitive polynomial of the table, the question's one at 4
      const setWidth = (w) => {
        stop(); st.width = w; st.k = 0;
        st.mask = w === 4 ? 0b0011 : (lfsrTable(w).find((r) => r.period === states()) || lfsrTable(w)[0]).mask;
        $(".ex-width").value = String(w); tapsHtml(); draw();
      };
      $(".ex-width").addEventListener("change", () => setWidth(Number($(".ex-width").value)));
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => { if (st.width !== 4) setWidth(4); stop(); st.mask = Number(b.dataset.mask); st.k = 0; draw(); }));
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, total()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      play.addEventListener("click", () => {
        if (timer) { stop(); return; }
        if (st.k >= total()) st.k = 0;
        play.textContent = "עצירה";
        timer = setInterval(() => { st.k++; draw(); if (st.k >= total()) stop(); }, Number(speed.value));
      });
      speed.addEventListener("change", () => { if (timer) { stop(); play.click(); } });
      tapsHtml();
      draw();
    },
  });

  dvqExplorers.register({
    views: { lfsr: lfsrView },
    // the picture of the cycles, the register and the step on one side; the strip and the table on the other
    cols: { lfsr: { side: ".lf-strip-title, .lf-strip, .wv-export, .lf-table-title, .lf-table" } },
    help: {
      lfsr: "מסמנים taps ובוחרים רוחב\u00a0: ״צעד״ ו״הפעלה״ מריצים את המצב מ-0…01. הציור (עד 6 ביטים) מראה את כל המצבים בסדר הצעד\u00a0: המחזור של 0…01 הוא הטבעת הראשונה, והיא נצבעת צעד אחרי צעד; המחזורים האחרים הם טבעות קטנות לידה, והאפס חוזר לעצמו. מתחת לציור הרגיסטר עצמו (הביטים, ה-taps וה-XOR שמחזיר את fb), ובצד רצועת התזמון (המצב, הביט שיוצא וביט ההיזון בכל צעד) וטבלת הפולינומים עם אורך המחזור של כל אחד.",
    },
    models: { lfsrNext, lfsrWalk, lfsrPeriod, lfsrPoly, lfsrTable, lfsrPrimitiveCount, lfsrStrip, lfsrCycles },
  });
})();
