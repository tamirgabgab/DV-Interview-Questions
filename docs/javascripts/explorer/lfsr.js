// kinds: lfsr
//   lfsr                   0036        a width of 3 to 8 bits: tick the taps, pick the seed (a field, or a click on a state) and XOR or XNOR, step or play; every cycle of the polynomial as its own ring (up to 6 bits), the visited states filled; the register; a strip of clk, state, s[0] and fb; the polynomials and their periods, the primitive ones counted
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, bitsOf, code, f, ltr, waveStrip } = dvqExplorers.lib;

  // LFSR (0036): the page's step and period on the mask of the taps (bit i of the mask is
  // s[i]; x^k is s[width - k]); the walk from a seed until a state repeats; the eight
  // polynomials x^4 + ... + 1 with their periods. xnor inverts the feedback bit (the trap
  // of the page: the stuck state is then all ones, when the number of taps is even).
  const lfsrNext = (state, mask, width, xnor = false) => {
    let fb = xnor ? 1 : 0;
    for (let v = state & mask; v; v >>= 1) fb ^= v & 1;
    return (state >> 1) | (fb << (width - 1));
  };
  const lfsrWalk = (mask, width, seed = 1, xnor = false) => {
    const seen = new Map(), states = [];
    let s = seed;
    while (!seen.has(s)) { seen.set(s, states.length); states.push(s); s = lfsrNext(s, mask, width, xnor); }
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
  const lfsrStrip = (mask, width, k, seed = 1, xnor = false) => {
    const walk = lfsrWalk(mask, width, seed, xnor), total = walk.period;
    const states = walk.states.concat(walk.states[walk.back]).slice(0, Math.min(k, total) + 1);
    const fb = states.map((s) => lfsrNext(s, mask, width, xnor) >> (width - 1));
    return { states, out: states.map((s) => s & 1), fb, total };
  };
  // Every cycle of the step: s[0] (the x^n of the polynomial, bit 0 of the mask) is always
  // a tap, so the step can be undone and the states split into disjoint cycles. lfsrCycles:
  // the non-zero states, the cycle of the seed 0…01 first, the rest in order of their
  // smallest state. lfsrAllCycles: every state, the stuck ones (cycles of one state)
  // included, in order of the smallest state, with XOR or XNOR.
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
  const lfsrAllCycles = (mask, width, xnor = false) => {
    const n = 1 << width, done = new Uint8Array(n), cycles = [];
    for (let s0 = 0; s0 < n; s0++) {
      if (done[s0]) continue;
      const c = [];
      for (let v = s0; !done[v]; v = lfsrNext(v, mask, width, xnor)) { done[v] = 1; c.push(v); }
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

  // The LFSR box (0036): a width of 3 to 8 bits, tick the taps (x^n and 1 are fixed), a
  // seed (a field of bits, or a click on a state of the picture) and XOR or XNOR; step or
  // play from the seed. The picture is every cycle of the step as its own ring (up to 6
  // bits), the stuck states with a loop, the visited states filled and the current one lit;
  // under it the register, and beside them the table of the polynomials with their periods
  // from 0…01 (every one up to 5 bits, the primitive ones from 6 bits on, with the count
  // φ(2^n − 1) / n), the timing strip and the lengths of the cycles.
  const lfsrView = () => ({
    mount(box) {
      const RING_MAX = 6, FULL_TABLE = 5;
      const st = { width: 4, mask: 0b0011, k: 0, seed: 1, xnor: false, note: "" };
      const bits = (v) => bitsOf(v, st.width);
      const sup = (k) => (k === 1 ? "x" : `x<sup>${k}</sup>`);
      const polyHtml = (mask, width = st.width) => {
        const t = [`x<sup>${width}</sup>`];
        for (let k = width - 1; k >= 1; k--) if ((mask >> (width - k)) & 1) t.push(sup(k));
        return ltr(t.concat("1").join(" + "));
      };
      box.innerHTML =
        `<div class="ex-controls"><label>רוחב <select class="ex-width" aria-label="מספר הביטים">${[3, 4, 5, 6, 7, 8].map((w) => `<option value="${w}"${w === 4 ? " selected" : ""}>${w} ביטים</option>`).join("")}</select></label>` +
        `<span class="lf-taps" dir="ltr" role="group" aria-label="בחירת ה-taps"></span>` +
        `<label>מצב התחלה <input type="text" class="lf-seed" dir="ltr" inputmode="numeric" size="8" maxlength="8" autocomplete="off" spellcheck="false" aria-label="מצב ההתחלה, בביטים" value="0001"></label>` +
        `<label class="lf-xnor-l"><input type="checkbox" class="lf-xnor"> ‏XNOR במקום XOR</label>` +
        `<span class="lf-presets">הפולינומים של השאלה : <button type="button" class="md-button ex-preset" data-mask="3">${ltr("x<sup>4</sup> + x<sup>3</sup> + 1")}</button> ` +
        `<button type="button" class="md-button ex-preset" data-mask="5">${ltr("x<sup>4</sup> + x<sup>2</sup> + 1")}</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">צעד</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1000">איטי</option><option value="500" selected>בינוני</option><option value="180">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד שהמצב חוזר</button><span class="ex-pos"></span></div>` +
        `<div class="lf-stage"><div class="lf-ring"></div>` +
        `<p class="ex-summary lf-sum" aria-live="polite"></p><p class="lf-fb"></p></div>` +
        `<p class="ex-title lf-reg-title">הרגיסטר : ${code("s[0]")} יוצא מימין, וביט ההיזון החוזר נכנס משמאל</p><div class="lf-reg"></div>` +
        `<p class="ex-title lf-table-title"></p><div class="lf-table" tabindex="0" role="group" aria-label="טבלת הפולינומים ואורכי המחזור, נגללת"></div>` +
        `<p class="ex-title lf-strip-title">רצועת התזמון : המצב, ${code("s[0]")} שיוצא ו-${code("fb")} שנכנס</p>` +
        `<div class="wv-wrap lf-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-LFSR, גלילה אופקית"></div>` +
        `<p class="lf-cycles-text"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed"), seedIn = $(".lf-seed"), xnorIn = $(".lf-xnor");
      let timer = null, tableKey = "";
      const walkNow = () => lfsrWalk(st.mask, st.width, st.seed, st.xnor);
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
      // The picture: one ring per cycle, the stuck states (a cycle of one) with a loop,
      // packed in rows, left to right. A state is a node with data-v: a click makes it the
      // seed. The visited states are filled, the last step's arrow and the current state lit.
      const ringsSvg = (cycles, shown) => {
        const w = st.width, rr = w <= 4 ? 14 : w === 5 ? 10 : 5, label = w <= 5, gap = w <= 4 ? 14 : 10, Wd = 420;
        const pitch = 2 * rr + (w <= 4 ? 8 : w === 5 ? 3 : 2);
        const rings = cycles.map((c) => ({ c, R: Math.max(rr * 1.8, (c.length * pitch) / (2 * Math.PI)) }));
        let x = gap, y = gap, rowH = 0, used = 0;
        rings.forEach((g) => {
          const D = 2 * (g.R + rr) + 4;
          if (x + D > Wd - gap && x > gap) { x = gap; y += rowH + gap; rowH = 0; }
          g.cx = x + D / 2; g.cy = y + D / 2; x += D + gap; rowH = Math.max(rowH, D); used = Math.max(used, x);
        });
        const Hd = y + rowH + gap, visited = new Set(shown), cur = shown[shown.length - 1];
        const prev = shown.length > 1 ? shown[shown.length - 2] : -1;
        let s = `<svg class="lf-live lf-rings" viewBox="0 0 ${f(used)} ${f(Hd)}" width="${f(used)}" height="${f(Hd)}" role="img" aria-label="המחזורים של ${1 << w} המצבים, טבעת לכל מחזור : ${cycles.map((c) => c.length).join(", ")}. המצב הנוכחי ${bits(cur)}">` +
          `<defs><marker id="lf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 6 : 4}" markerHeight="${rr > 8 ? 6 : 4}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker>` +
          `<marker id="lf-arrow-todo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 6 : 4}" markerHeight="${rr > 8 ? 6 : 4}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead is-todo"/></marker></defs>`;
        rings.forEach((g) => {
          const L = g.c.length;
          const pos = (i) => { const ang = -Math.PI / 2 + (i / L) * 2 * Math.PI; return [g.cx + g.R * Math.cos(ang), g.cy + g.R * Math.sin(ang)]; };
          if (L === 1) {
            s += `<path class="lf-loop" d="M${f(g.cx + rr * 0.7)},${f(g.cy - rr * 0.7)} a ${f(rr * 0.8)} ${f(rr * 0.8)} 0 1 0 ${f(-rr * 1.4)} 0" marker-end="url(#lf-arrow)"/>`;
          } else {
            for (let i = 0; i < L; i++) {
              // a chord bent outward a little, so a cycle of two shows two arrows
              const a = g.c[i], b = g.c[(i + 1) % L];
              const [x1, y1] = pos(i), [x2, y2] = pos((i + 1) % L), mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
              const ox = mx - g.cx, oy = my - g.cy, od = Math.hypot(ox, oy) || 1, bend = L === 2 ? g.R * 0.6 : rr * 0.6;
              const qx = mx + (ox / od) * bend + (L === 2 ? (i ? -1 : 1) * g.R * 0.6 : 0), qy = my + (oy / od) * bend;
              const u1 = Math.hypot(qx - x1, qy - y1) || 1, u2 = Math.hypot(x2 - qx, y2 - qy) || 1;
              const taken = visited.has(a) && visited.has(b) && (st.k > shown.indexOf(a) || a === prev);
              s += `<path class="lf-edge${taken ? "" : " is-todo"}${a === prev && b === cur ? " is-cur" : ""}" d="M${f(x1 + ((qx - x1) / u1) * rr)},${f(y1 + ((qy - y1) / u1) * rr)} Q${f(qx)},${f(qy)} ${f(x2 - ((x2 - qx) / u2) * (rr + 2))},${f(y2 - ((y2 - qy) / u2) * (rr + 2))}" fill="none" marker-end="url(#lf-arrow${taken ? "" : "-todo"})"/>`;
            }
          }
          g.c.forEach((v, i) => {
            const [px, py] = L === 1 ? [g.cx, g.cy] : pos(i);
            s += `<g class="lf-node${L === 1 ? " lf-zero" : ""}${visited.has(v) ? " is-seen" : ""}${v === cur ? " is-cur" : ""}${v === st.seed ? " is-seed" : ""}" data-v="${v}"><circle cx="${f(px)}" cy="${f(py)}" r="${rr}"><title>${bits(v)}</title></circle>` +
                 (label ? `<text x="${f(px)}" y="${f(py + (rr > 12 ? 4 : 3))}" text-anchor="middle"${rr > 12 ? "" : ' font-size="7"'}>${bits(v)}</text>` : "") + `</g>`;
          });
          if (L > 1) s += `<text class="tick" x="${f(g.cx)}" y="${f(g.cy + 4)}" text-anchor="middle">${L}</text>`;
        });
        return s + "</svg>";
      };
      // from 7 bits there is no picture: the strip lists the states
      const noRing = () => `<p class="ex-note">‏${ltr(1 << st.width)} מצבים : יותר מדי לציור. רצועת התזמון מראה את המצבים שבוקרו, בהקסה.</p>`;
      // the strip: every step so far, the bus in binary up to 6 bits and in hex beyond
      const stripHtml = () => {
        const sp = lfsrStrip(st.mask, st.width, st.k, st.seed, st.xnor), hex = st.width > 6;
        const label = (v) => (hex ? `0x${v.toString(16).toUpperCase().padStart(2, "0")}` : bits(v));
        const SW = hex ? 40 : Math.max(36, Math.round(14 + 7.6 * st.width)), n = sp.states.length;
        return waveStrip([
          { name: "clk", kind: "clock" },
          { name: "state", kind: "bus", values: sp.states.map(label) },
          { name: "s[0]", kind: "bit", values: sp.out, cls: "wv-s2" },
          { name: "fb", kind: "bit", values: sp.fb, cls: "wv-s1" },
        ], n, { slotW: SW, cursor: n - 1, ticks: (k) => k, label: `רצועת התזמון של ה-LFSR : ${n} מצבים` });
      };
      // the lengths of the cycles in words: a sum when they are few, counts per length otherwise
      const cyclesText = (cycles) => {
        const N = 1 << st.width, stuck = cycles.filter((c) => c.length === 1).map((c) => c[0]);
        const lens = cycles.filter((c) => c.length > 1).map((c) => c.length);
        const byLen = new Map(); lens.forEach((l) => byLen.set(l, (byLen.get(l) || 0) + 1));
        const sum = lens.length <= 8 ? lens.join(" + ") : [...byLen].sort((u, v) => v[0] - u[0]).map(([l, k]) => `${k} × ${l}`).join(" + ");
        const whole = lens.length === 1 && lens[0] === N - 1;
        return `כל המחזורים : ${ltr(lens.length > 1 ? `${sum} = ${N - stuck.length}` : sum)}` +
          (stuck.length ? `, ו-${stuck.map((v) => code(bits(v))).join(" ו-")} ${stuck.length > 1 ? "חוזרים לעצמם" : "חוזר לעצמו"}. ` : `, ואין מצב תקוע. `) +
          `הצעד הפיך, כי ${code("s[0]")} (האיבר ${ltr(`x<sup>${st.width}</sup>`)}) הוא תמיד tap : לכל מצב יש קודם אחד, ולכן המחזורים זרים. ` +
          (whole ? `<span class="lf-ok">מחזור אחד דרך כל שאר המצבים : הפולינום פרימיטיבי.</span>`
            : `אף מצב התחלה לא נותן יותר מ-${ltr(Math.max(1, ...lens))} צעדים.`);
      };
      // The register: s[width − 1] .. s[0] left to right, the taps outlined and wired to
      // one XOR (with a bubble for XNOR) under the row, its output fb back into the left
      // end, s[0] out at the right.
      const regSvg = (cur, fb) => {
        const n = st.width, CW = 40, X0 = 64, Y = 22, CH = 40, BUS = Y + CH + 34, W = X0 + n * (CW + 4) + 70, H = BUS + 38;
        const cx = (b) => X0 + (n - 1 - b) * (CW + 4) + CW / 2;
        let s = `<svg class="figure lf-regsvg" viewBox="0 0 ${W} ${H}" style="max-width:${(W / 16).toFixed(1)}rem" role="img" aria-label="הרגיסטר במצב ${bits(cur)}, היזון חוזר ${fb}">` +
          `<defs><marker id="lf-arrow3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-head"/></marker></defs>`;
        const taps = [];
        for (let b = 0; b < n; b++) if ((st.mask >> b) & 1) taps.push(b);
        // the wires: down from every tap to the bus, along it to the XOR, up and into the left end
        taps.forEach((b) => { s += `<line class="lf-wire" x1="${cx(b)}" y1="${Y + CH}" x2="${cx(b)}" y2="${BUS}"/><circle class="lf-dot" cx="${cx(b)}" cy="${BUS}" r="3"/>`; });
        const xorX = 26, top = BUS - 12 - (st.xnor ? 7 : 0);
        s += `<line class="lf-wire" x1="${xorX + 12}" y1="${BUS}" x2="${Math.max(...taps.map(cx))}" y2="${BUS}"/>` +
             `<circle class="lf-xor" cx="${xorX}" cy="${BUS}" r="12"/><path class="lf-wire" d="M${xorX - 8},${BUS} H${xorX + 8} M${xorX},${BUS - 8} V${BUS + 8}"/>` +
             (st.xnor ? `<circle class="lf-xor" cx="${xorX}" cy="${BUS - 15.5}" r="3.5"/>` : "") +
             `<path class="lf-wire" d="M${xorX},${top} V${Y + CH / 2} H${X0 - 2}" fill="none" marker-end="url(#lf-arrow3)"/>` +
             `<text class="lf-regfb" x="${xorX + 4}" y="${BUS + 30}" text-anchor="middle">fb = ${fb}</text>`;
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
      const draw = () => {
        const walk = walkNow(), total = walk.period, N = 1 << st.width, n = N - 1;
        st.k = Math.min(st.k, total);
        box.querySelectorAll(".ex-tap").forEach((c) => { c.checked = ((st.mask >> (st.width - Number(c.dataset.k))) & 1) === 1; });
        if (document.activeElement !== seedIn || seedIn.value !== bits(st.seed)) seedIn.value = bits(st.seed);
        seedIn.size = seedIn.maxLength = st.width;
        xnorIn.checked = st.xnor;
        box.classList.toggle("lf-wide", st.width > 4);
        const shown = walk.states.concat(walk.states[0]).slice(0, st.k + 1);
        const cycles = lfsrAllCycles(st.mask, st.width, st.xnor);
        const ringBox = $(".lf-ring");
        ringBox.classList.toggle("is-none", st.width > RING_MAX);
        ringBox.innerHTML = st.width <= RING_MAX ? ringsSvg(cycles, shown) : noRing();
        const cur = walk.states[st.k % total];
        const tapsIdx = [];
        for (let i = 0; i < st.width; i++) if ((st.mask >> i) & 1) tapsIdx.push(i);
        const next = lfsrNext(cur, st.mask, st.width, st.xnor), fb = next >> (st.width - 1);
        const stuck = total === 1, maximal = total === n, back = st.k === total;
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${total}`;
        $(".ex-prev").disabled = st.k === 0;
        const seen = Math.min(st.k + 1, total);
        const count = st.xnor || st.seed === 0 ? `בוקרו ${ltr(seen)} מתוך ${ltr(N)} המצבים` : `בוקרו ${ltr(seen)} מתוך ${ltr(n)} המצבים שאינם אפס`;
        $(".lf-sum").innerHTML = (st.note ? `<span class="lf-bad">${st.note}</span> ` : "") +
          `אחרי ${ltr(st.k)} צעדים : המצב ${code(bits(cur))}` + (back ? (stuck ? `, אותו מצב : ה-LFSR תקוע. ` : `, חזרה למצב ההתחלה. `) : `. `) + `${count}.`;
        st.note = "";
        const xs = tapsIdx.map((i) => `s[${i}]`).join(" ^ "), vs = tapsIdx.map((i) => (cur >> i) & 1).join(" ^ ");
        const wrapX = (t) => (st.xnor ? `~(${t})` : t);
        $(".lf-fb").innerHTML = `הצעד הבא : ${ltr(`${code("fb")} = ${code(wrapX(xs))} = ${tapsIdx.length > 1 || st.xnor ? `${wrapX(vs)} = ` : ""}${fb}`)}, ` +
          `ואז ${ltr(`${code(`(${bits(cur)} >> 1) | (${fb} << ${st.width - 1})`)} = ${code(bits(next))}`)}.`;
        $(".lf-reg").innerHTML = regSvg(cur, fb);
        const wrap = $(".lf-strip");
        wrap.innerHTML = stripHtml();
        wrap.scrollLeft = wrap.scrollWidth;                // the current step in view
        $(".lf-cycles-text").innerHTML = cyclesText(cycles);
        // the table (from 0…01, with XOR): every polynomial up to 5 bits, only the primitive
        // ones from 6; rebuilt when the width or the taps change, the current row in view
        const key = `${st.width}.${st.mask}`;
        if (key !== tableKey) {
          tableKey = key;
          const all = lfsrTable(st.width), prim = lfsrPrimitiveCount(st.width), full = st.width <= FULL_TABLE;
          const rows = full ? all : all.filter((r) => r.period === n);
          $(".lf-table-title").innerHTML = (full
            ? `כל ${ltr(all.length)} הפולינומים ואורך המחזור מ-${code(bits(1))}`
            : `${ltr(rows.length)} הפולינומים הפרימיטיביים מתוך ${ltr(all.length)}`) +
            `; פרימיטיביים (✓) : ${ltr(`φ(${n}) / ${st.width} = ${prim}`)}`;
          const tab = $(".lf-table");
          tab.innerHTML = `<table><thead><tr><th>הפולינום</th><th>המסכה</th><th>אורך המחזור</th></tr></thead><tbody>` +
            rows.map((r) => `<tr class="${r.mask === st.mask ? "is-cur" : ""}${r.period === n ? " is-max" : ""}"><td>${polyHtml(r.mask)}</td><td>${code(bits(r.mask))}</td><td>${ltr(r.period)}${r.period === n ? " ✓" : ""}</td></tr>`).join("") +
            `</tbody></table>`;
          const row = tab.querySelector("tr.is-cur");
          tab.scrollTop = row ? Math.max(0, row.offsetTop - tab.clientHeight / 2) : 0;
        }
        const from = st.seed === 1 ? "" : ` מהמצב ${code(bits(st.seed))}`;
        answer(box, !back ? null
          : stuck ? `המצב ${code(bits(st.seed))} תקוע${st.xnor ? " עם XNOR" : ""} : ${st.xnor ? "ה-XNOR של ה-taps שלו הוא 1" : "ה-XOR של אפסים הוא אפס"}, בכל פולינום${st.xnor ? " עם מספר זוגי של taps" : ""}.`
          : maximal ? `הפולינום ${polyHtml(st.mask)} פרימיטיבי : מחזור מקסימלי של ${ltr(n)} צעדים${st.xnor ? ", גם עם XNOR" : ""}.`
          : st.xnor && tapsIdx.length % 2 ? `עם XNOR ומספר אי-זוגי של taps המחזור${from} הוא ${ltr(total)} צעדים, ואין מצב תקוע.`
          : `הפולינום ${polyHtml(st.mask)} אינו פרימיטיבי : המחזור${from} הוא ${ltr(total)} צעדים בלבד מתוך ${ltr(n)}.`, ".lf-table tr.is-cur");
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; play.textContent = "הפעלה"; };
      const total = () => walkNow().period;
      // a new width: the first primitive polynomial of the table, the question's one at 4
      const setWidth = (w) => {
        stop(); st.width = w; st.k = 0; st.seed = 1;
        st.mask = w === 4 ? 0b0011 : (lfsrTable(w).find((r) => r.period === (1 << w) - 1) || lfsrTable(w)[0]).mask;
        $(".ex-width").value = String(w); tapsHtml(); draw();
      };
      const setSeed = (v) => { stop(); st.seed = v; st.k = 0; draw(); };
      $(".ex-width").addEventListener("change", () => setWidth(Number($(".ex-width").value)));
      // the seed field: up to `width` bits of 0 and 1 (a shorter text is padded with zeros)
      seedIn.addEventListener("change", () => {
        const t = seedIn.value.trim();
        if (/^[01]+$/.test(t) && t.length <= st.width) { setSeed(parseInt(t, 2)); return; }
        st.note = `מצב התחלה הוא ${st.width} ביטים של 0 ו-1.`;
        seedIn.value = bits(st.seed); draw();
      });
      xnorIn.addEventListener("change", () => { stop(); st.xnor = xnorIn.checked; st.k = 0; draw(); });
      $(".lf-ring").addEventListener("click", (e) => {
        const g = e.target.closest && e.target.closest("g[data-v]");
        if (g) setSeed(Number(g.dataset.v));
      });
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => {
        if (st.width !== 4) setWidth(4);
        stop(); st.mask = Number(b.dataset.mask); st.seed = 1; st.xnor = false; st.k = 0; draw();
      }));
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
    cols: { lfsr: { side: ".lf-table-title, .lf-table, .lf-strip-title, .lf-strip, .wv-export, .lf-cycles-text" } },   // the rings, the step and the register beside the table, the strip and the cycle lengths
    help: {
      lfsr: "מסמנים taps ובוחרים רוחב, מצב התחלה ו-XOR או XNOR; ״צעד״ ו״הפעלה״ מריצים את המצב. כל מחזור של הפולינום מצויר כטבעת משלו (עד 6 ביטים), מצב תקוע מצויר עם לולאה, והמצבים שבוקרו מתמלאים; לחיצה על מצב בציור קובעת אותו כמצב ההתחלה. הטבלה נותנת את אורך המחזור של כל פולינום מ-0…01 עם XOR.",
    },
    models: { lfsrNext, lfsrWalk, lfsrPeriod, lfsrPoly, lfsrTable, lfsrPrimitiveCount, lfsrStrip, lfsrCycles, lfsrAllCycles },
  });
})();
