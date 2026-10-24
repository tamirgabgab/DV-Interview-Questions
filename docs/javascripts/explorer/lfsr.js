// kinds: lfsr
//   lfsr                   0036        a width of 3 to 8 bits: tick the taps, step or play from 0…01 on a ring of the states (up to 6 bits); a strip of clk, state, s[0] and fb; the polynomials and their periods, the primitive ones counted; the proof panel: every cycle of the polynomial as its own ring
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
  // Every cycle of the step: with the 1 of the polynomial always a tap (bit 0 of the mask)
  // the step can be undone, so the non-zero states split into disjoint cycles; the first
  // one is the cycle of the seed 0…01, the rest in order of their smallest state.
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
  // or play from 0…01 on a ring of the 2^n − 1 non-zero states (0 sits in the middle as the
  // fixed point; up to 6 bits), a timing strip of clk, the state, s[0] and the feedback bit
  // for every step so far, and the table of the polynomials with their periods: every one
  // up to 5 bits, the primitive ones from 6 bits on, with the count φ(2^n − 1) / n.
  const lfsrView = () => ({
    mount(box) {
      const SEED = 1, RING_MAX = 6, FULL_TABLE = 5;
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
        `<span class="lf-presets">הפולינומים של השאלה : <button type="button" class="md-button ex-preset" data-mask="3">${ltr("x<sup>4</sup> + x<sup>3</sup> + 1")}</button> ` +
        `<button type="button" class="md-button ex-preset" data-mask="5">${ltr("x<sup>4</sup> + x<sup>2</sup> + 1")}</button></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">צעד</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` +
        `<label>הקצב <select class="ex-speed"><option value="1000">איטי</option><option value="500" selected>בינוני</option><option value="180">מהיר</option></select></label>` +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד שהמצב חוזר</button><span class="ex-pos"></span></div>` +
        `<div class="lf-box"><div class="lf-ring"></div><div class="lf-panel">` +
        `<p class="lf-poly"></p><p class="lf-state"></p><p class="lf-fb"></p>` +
        `<p class="ex-summary lf-sum" aria-live="polite"></p></div></div>` +
        `<p class="ex-title">רצועת התזמון : המצב, הביט שיוצא (${code("s[0]")}) וביט ההיזון החוזר שנכנס, צעד אחרי צעד</p>` +
        `<div class="wv-wrap lf-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-LFSR, גלילה אופקית"></div>` +
        `<p class="ex-title lf-table-title"></p><div class="lf-table" tabindex="0"></div>` +
        `<section class="ex-proof lf-proof"><p class="ex-proof-title">שלב ההוכחה : כל המחזורים של הפולינום</p>` +
        `<div class="lf-cycles"></div><p class="lf-cycles-text"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      let timer = null;
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
      const ring = (walk, shown) => {
        const n = states(), C = 150, R = st.width <= 4 ? 118 : 128;
        const rr = st.width <= 4 ? 17 : st.width === 5 ? 11 : 6, label = st.width <= 5;
        const pos = (v) => { const ang = -Math.PI / 2 + ((v - 1) / n) * 2 * Math.PI; return [C + R * Math.cos(ang), C + R * Math.sin(ang)]; };
        const visited = new Set(shown), cur = shown[shown.length - 1];
        let s = `<svg class="lf-live" viewBox="0 0 300 300" role="img" aria-label="טבעת של ${n} המצבים שאינם אפס, המצבים שבוקרו וחיצים ביניהם">` +
          `<defs><marker id="lf-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 7 : 5}" markerHeight="${rr > 8 ? 7 : 5}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker></defs>`;
        for (let i = 1; i < shown.length; i++) {
          const [x1, y1] = pos(shown[i - 1]), [x2, y2] = pos(shown[i]);
          const dx = x2 - x1, dy = y2 - y1, d = Math.hypot(dx, dy) || 1;
          s += `<line class="lf-edge${i === shown.length - 1 ? " is-cur" : ""}" x1="${f(x1 + (dx / d) * rr)}" y1="${f(y1 + (dy / d) * rr)}" x2="${f(x2 - (dx / d) * (rr + 2))}" y2="${f(y2 - (dy / d) * (rr + 2))}" marker-end="url(#lf-arrow)"/>`;
        }
        for (let v = 1; v <= n; v++) {
          const [x, y] = pos(v);
          s += `<g class="lf-node${visited.has(v) ? " is-seen" : ""}${v === cur ? " is-cur" : ""}${v === SEED ? " is-seed" : ""}"><circle cx="${f(x)}" cy="${f(y)}" r="${rr}"><title>${bits(v)}</title></circle>` +
               (label ? `<text x="${f(x)}" y="${f(y + (rr > 12 ? 4 : 3))}" text-anchor="middle"${rr > 12 ? "" : ' font-size="7"'}>${bits(v)}</text>` : "") + `</g>`;
        }
        const zr = Math.max(rr, 14);
        s += `<g class="lf-node lf-zero"><circle cx="${C}" cy="${C}" r="${zr}"/><text x="${C}" y="${C + 4}" text-anchor="middle"${st.width > 4 ? ' font-size="8"' : ""}>${bits(0)}</text></g>` +
             `<path class="lf-loop" d="M${C + 12},${C - zr + 4} a 11 11 0 1 1 -24 0" marker-end="url(#lf-arrow)"/></svg>`;
        return s;
      };
      // from 7 bits there is no ring: the strip below lists the states
      const noRing = () => `<p class="ex-note">‏${ltr(states())} מצבים שאינם אפס : יותר מדי לטבעת. רצועת התזמון שמתחת מראה את המצבים שבוקרו, בהקסה.</p>`;
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
        ], n, { slotW: SW, cursor: n - 1, ticks: (k) => k, label: `רצועת התזמון של ה-LFSR : ${n} מצבים` });
      };
      // the proof panel: every state with its arrow, one small ring per cycle (up to 6 bits),
      // the seed's cycle first and the current state lit, and the cycle lengths in words
      const cyclesSvg = (cycles, cur) => {
        const rr = st.width <= 4 ? 14 : st.width === 5 ? 10 : 5, label = st.width <= 5, gap = 14, Wd = 640;
        // the fixed point 0 first, then the cycles; packed in rows, left to right
        const rings = [{ c: [0], R: rr * 1.8 }].concat(cycles.map((c) => ({ c, R: Math.max(rr * 1.8, (c.length * (2 * rr + (rr > 8 ? 8 : 4))) / (2 * Math.PI)) })));
        let x = gap, y = gap, rowH = 0, used = 0;
        rings.forEach((g) => {
          const D = 2 * (g.R + rr) + 4;
          if (x + D > Wd - gap && x > gap) { x = gap; y += rowH + gap; rowH = 0; }
          g.cx = x + D / 2; g.cy = y + D / 2; x += D + gap; rowH = Math.max(rowH, D); used = Math.max(used, x);
        });
        // the picture is as wide as its rings, so a few small rings fill a phone
        const Hd = y + rowH + gap;
        let s = `<svg class="figure lf-all" viewBox="0 0 ${f(used)} ${f(Hd)}" style="max-width:${f(used / 14)}rem" role="img" aria-label="כל ${cycles.length} המחזורים של המצבים שאינם אפס, ונקודת השבת 0">` +
          `<defs><marker id="lf-arrow2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="${rr > 8 ? 6 : 4}" markerHeight="${rr > 8 ? 6 : 4}" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="lf-arrowhead"/></marker></defs>`;
        rings.forEach((g, j) => {
          const L = g.c.length, cls = j === 0 ? "lf-zero" : `lf-c${(j - 1) % 3}`;
          const pos = (i) => { const ang = -Math.PI / 2 + (i / L) * 2 * Math.PI; return [g.cx + g.R * Math.cos(ang), g.cy + g.R * Math.sin(ang)]; };
          if (L === 1) {
            const [px, py] = [g.cx, g.cy];
            s += `<path class="lf-loop" d="M${f(px + rr * 0.7)},${f(py - rr * 0.7)} a ${f(rr * 0.8)} ${f(rr * 0.8)} 0 1 0 ${f(-rr * 1.4)} 0" marker-end="url(#lf-arrow2)"/>`;
          } else {
            for (let i = 0; i < L; i++) {
              // a chord bent outward a little, so a cycle of two shows two arrows
              const [x1, y1] = pos(i), [x2, y2] = pos((i + 1) % L), mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
              const ox = mx - g.cx, oy = my - g.cy, od = Math.hypot(ox, oy) || 1, bend = L === 2 ? g.R * 0.6 : rr * 0.6;
              const qx = mx + (ox / od) * bend + (L === 2 ? (i ? -1 : 1) * g.R * 0.6 : 0), qy = my + (oy / od) * bend;
              const u1 = Math.hypot(qx - x1, qy - y1) || 1, u2 = Math.hypot(x2 - qx, y2 - qy) || 1;
              s += `<path class="lf-edge ${cls}" d="M${f(x1 + ((qx - x1) / u1) * rr)},${f(y1 + ((qy - y1) / u1) * rr)} Q${f(qx)},${f(qy)} ${f(x2 - ((x2 - qx) / u2) * (rr + 2))},${f(y2 - ((y2 - qy) / u2) * (rr + 2))}" fill="none" marker-end="url(#lf-arrow2)"/>`;
            }
          }
          g.c.forEach((v, i) => {
            const [px, py] = L === 1 ? [g.cx, g.cy] : pos(i);
            s += `<g class="lf-node ${cls}${v === cur ? " is-cur" : ""}${v === SEED ? " is-seed" : ""}"><circle cx="${f(px)}" cy="${f(py)}" r="${rr}"><title>${bits(v)}</title></circle>` +
                 (label ? `<text x="${f(px)}" y="${f(py + (rr > 12 ? 4 : 3))}" text-anchor="middle"${rr > 12 ? "" : ' font-size="7"'}>${bits(v)}</text>` : "") + `</g>`;
          });
          if (L > 1) s += `<text class="tick" x="${f(g.cx)}" y="${f(g.cy + 4)}" text-anchor="middle">${L}</text>`;
        });
        return s + "</svg>";
      };
      const drawCycles = (cur) => {
        const cycles = lfsrCycles(st.mask, st.width), n = states(), lens = cycles.map((c) => c.length);
        $(".lf-cycles").innerHTML = st.width <= RING_MAX ? cyclesSvg(cycles, cur) : "";
        // the lengths: a sum when the cycles are few, counts per length otherwise
        const byLen = new Map(); lens.forEach((l) => byLen.set(l, (byLen.get(l) || 0) + 1));
        const sum = lens.length <= 8 ? lens.join(" + ") : [...byLen].sort((u, v) => v[0] - u[0]).map(([l, k]) => `${k} × ${l}`).join(" + ");
        $(".lf-cycles-text").innerHTML = `הצעד הפיך, כי ה-1 של הפולינום הוא תמיד tap : מהמצב הבא אפשר לשחזר את הביט שיצא. לכן לכל מצב יש קודם אחד בלבד, ` +
          `והמצבים מתחלקים למחזורים זרים. כאן ${ltr(n)} המצבים שאינם אפס מתחלקים ל-${ltr(lens.length)} ${lens.length === 1 ? "מחזור" : "מחזורים"} : ${ltr(`${sum} = ${n}`)}, ` +
          `והאפס חוזר לעצמו. ` + (lens.length === 1
            ? `<span class="lf-ok">מחזור אחד שעובר על כל ${ltr(n)} המצבים : הפולינום פרימיטיבי.</span>`
            : `המחזור של ${code(bits(SEED))} ${st.width <= RING_MAX ? " (עם המסגרת העבה)" : ""} הוא ${ltr(lens[0])}, ואף התחלה לא מגיעה ליותר מ-${ltr(Math.max(...lens))} מצבים.`);
      };
      const draw = () => {
        const walk = lfsrWalk(st.mask, st.width, SEED), total = walk.period, n = states();
        st.k = Math.min(st.k, total);
        box.querySelectorAll(".ex-tap").forEach((c) => { c.checked = ((st.mask >> (st.width - Number(c.dataset.k))) & 1) === 1; });
        const shown = walk.states.concat(walk.states[walk.back]).slice(0, st.k + 1);
        $(".lf-ring").innerHTML = st.width <= RING_MAX ? ring(walk, shown) : noRing();
        const cur = st.k < total ? walk.states[st.k] : walk.states[walk.back];
        drawCycles(cur);
        const tapsIdx = [];
        for (let i = 0; i < st.width; i++) if ((st.mask >> i) & 1) tapsIdx.push(i);
        let fb = 0; tapsIdx.forEach((i) => { fb ^= (cur >> i) & 1; });
        const next = lfsrNext(cur, st.mask, st.width);
        $(".ex-pos").textContent = `צעד ${st.k} מתוך ${total}`;
        $(".ex-prev").disabled = st.k === 0;
        $(".lf-poly").innerHTML = `הפולינום ${polyHtml(st.mask)}, המסכה ${code(bits(st.mask))} : היזון חוזר מהביטים ${ltr(tapsIdx.map((i) => `s[${i}]`).join(", "))}.`;
        $(".lf-state").innerHTML = `המצב אחרי ${ltr(st.k)} צעדים : ${code(bits(cur))}` + (st.k === total ? ` — חזר למצב ההתחלה.` : ".");
        $(".lf-fb").innerHTML = `הצעד הבא : ${ltr(`${code("fb")} = ${code(tapsIdx.map((i) => `s[${i}]`).join(" ^ "))} = ${tapsIdx.map((i) => (cur >> i) & 1).join(" ^ ")} = ${fb}`)}, ` +
          `ואז ${ltr(`${code(`(${bits(cur)} >> 1) | (${fb} << ${st.width - 1})`)} = ${code(bits(next))}`)}.`;
        const wrap = $(".lf-strip");
        wrap.innerHTML = stripHtml();
        wrap.scrollLeft = wrap.scrollWidth;                // the current step in view
        const maximal = total === n;
        $(".lf-sum").innerHTML = st.k < total
          ? `בוקרו ${ltr(st.k + 1)} מצבים מתוך ${ltr(n)}. ` + (maximal ? `הפולינום פרימיטיבי : המחזור יהיה ${ltr(n)}.` : `המחזור של הפולינום הזה הוא ${ltr(total)}, ולכן ${ltr(n - total)} מצבים לא יבוקרו לעולם.`)
          : maximal ? `<span class="lf-ok">מחזור מקסימלי : ${ltr(n)} צעדים, כל מצב שאינו אפס פעם אחת ✓</span>`
          : `<span class="lf-bad">מחזור של ${ltr(total)} צעדים בלבד : ${ltr(n - total)} מצבים לא בוקרו.</span>`;
        // the table: every polynomial up to 5 bits, only the primitive ones from 6
        const all = lfsrTable(st.width), prim = lfsrPrimitiveCount(st.width), full = st.width <= FULL_TABLE;
        const rows = full ? all : all.filter((r) => r.period === n);
        $(".lf-table-title").innerHTML = (full
          ? `כל ${ltr(all.length)} הפולינומים ${ltr(`x<sup>${st.width}</sup> + … + 1`)} ואורך המחזור של כל אחד מ-${code(bits(SEED))}`
          : `${ltr(rows.length)} הפולינומים הפרימיטיביים מתוך ${ltr(all.length)} (מחזור ${ltr(n)} מ-${code(bits(SEED))})`) +
          `; לפי הנוסחה ${ltr(`φ(2<sup>${st.width}</sup> − 1) / ${st.width} = φ(${n}) / ${st.width} = ${prim}`)}`;
        $(".lf-table").innerHTML = `<table><thead><tr><th>הפולינום</th><th>המסכה</th><th>אורך המחזור</th></tr></thead><tbody>` +
          rows.map((r) => `<tr class="${r.mask === st.mask ? "is-cur" : ""}${r.period === n ? " is-max" : ""}"><td>${polyHtml(r.mask)}</td><td>${code(bits(r.mask))}</td><td>${ltr(r.period)}${r.period === n ? " ✓" : ""}</td></tr>`).join("") +
          `</tbody></table>`;
        answer(box, st.k >= total ? (maximal ? `הפולינום ${polyHtml(st.mask)} פרימיטיבי : מחזור מקסימלי של ${ltr(n)} צעדים.`
          : `הפולינום ${polyHtml(st.mask)} אינו פרימיטיבי : מחזור של ${ltr(total)} צעדים בלבד מתוך ${ltr(n)}.`) : null, ".lf-table tr.is-cur");
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
    help: {
      lfsr: "מסמנים taps ובוחרים רוחב : ״צעד״ ו״הפעלה״ מריצים את המצב מ-0…01 על טבעת המצבים (עד 6 ביטים), רצועת התזמון מראה את המצב, הביט שיוצא וביט ההיזון בכל צעד, והטבלה נותנת את אורך המחזור של כל פולינום. שלב ההוכחה מצייר את כל המחזורים של הפולינום, טבעת קטנה לכל מחזור.",
    },
    models: { lfsrNext, lfsrWalk, lfsrPeriod, lfsrPoly, lfsrTable, lfsrPrimitiveCount, lfsrStrip, lfsrCycles },
  });
})();
