// kinds: divfsm winfsm
//   divfsm                 0055        divisible by m: one number fed digit by digit to one machine, chosen in a list: concatenated at the LSB (read from the MSB, the state is the remainder) or at the MSB (read from the LSB, x = remainder * B^-k); m, the base (k bits a cycle or decimal), digits typed, added or drawn; the ring shows the current state, the edges out of it and the edge just taken
//   winfsm                 0056        divisible by m over a window of the last L digits: a digit enters at the LSB (the highest leaves) or at the MSB (the lowest leaves), chosen in a list; m, the base, L, the window after reset and the digits that enter; the data path (the window, the digit in, the digit out, the remainder updated) and, up to 16 windows, the machine with a state per window
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, code, f, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Divisible by m (0055), m and the base B coprime. From the MSB the state is the
  // remainder: r' = (B r + d) mod m. From the LSB it is x = remainder * B^-k: x' = (x + d) *
  // B^-1 mod m. divRun feeds the number's digits (written highest first) to one machine:
  // the MSB machine from the left end, the LSB machine from the right end; it returns the
  // states before the first digit and after each one.
  const divInv = (b, m) => { for (let y = 0; y < m; y++) if ((b * y) % m === 1 % m) return y; return null; };
  const divTable = (m, b, lsb) => {
    const inv = divInv(b % m, m);
    return Array.from({ length: m }, (_, s) => Array.from({ length: b }, (_, d) => (lsb ? ((s + d) * inv) % m : (s * b + d) % m)));
  };
  const divRun = (digits, m, b, lsb) => {
    const t = divTable(m, b, lsb), seq = lsb ? [...digits].reverse() : digits, out = [0];
    seq.forEach((d) => out.push(t[out[out.length - 1]][d]));
    return out;
  };
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);

  // A window of the last L base-B digits (0056), its value w below B^L. A digit d enters at
  // the LSB: w' = (B w + d) mod B^L, the highest digit leaves; or at the MSB: w' = d B^(L-1)
  // + floor(w / B), the lowest leaves. The remainder r = w mod m follows without the
  // window's value: r' = (B r + d - out * (B^L mod m)) mod m at the LSB, and r' = ((r - out)
  // * B^-1 + d * (B^(L-1) mod m)) mod m at the MSB (gcd(B, m) = 1). winRun returns, before
  // the first digit and after each one, the window, the remainder and the digit that left.
  const winStep = (w, d, b, L, msb) => (msb ? d * b ** (L - 1) + Math.floor(w / b) : (w * b + d) % b ** L);
  const winRun = (digits, m, b, L, init, msb) => {
    const cl = b ** L % m, ch = b ** (L - 1) % m, inv = divInv(b % m, m);
    const out = [{ w: init, r: init % m, out: null }];
    digits.forEach((d) => {
      const { w, r } = out[out.length - 1];
      const gone = msb ? w % b : Math.floor(w / b ** (L - 1));
      const r2 = msb ? ((((r - gone) % m) + m) * inv + d * ch) % m : (((r * b + d - gone * cl) % m) + m) % m;
      out.push({ w: winStep(w, d, b, L, msb), r: r2, out: gone });
    });
    return out;
  };

  const MS = [3, 5, 7, 9, 11, 13, 15];
  const BASES = [[2, "ביט אחד (בסיס 2)"], [4, "2 ביטים (בסיס 4)"], [8, "3 ביטים (בסיס 8)"], [16, "4 ביטים (בסיס 16)"], [10, "ספרה עשרונית"]];
  const MAXD = 16;
  const DIG = "0123456789abcdef";
  const parse = (text, b, max = MAXD) => {
    const s = String(text).trim().toLowerCase();
    if (!s.length || s.length > max) return null;
    const ds = [...s].map((c) => DIG.indexOf(c));
    return ds.every((d) => d >= 0 && d < b) ? ds : null;
  };
  const big = (ds, b) => ds.reduce((v, d) => v * BigInt(b) + BigInt(d), 0n);
  const toDigits = (v, b, len = MAXD) => { const out = []; do { out.unshift(Number(v % BigInt(b))); v /= BigInt(b); } while (v > 0n); return out.slice(-len); };
  const digitText = (ds) => ds.map((d) => DIG[d]).join("") || "0";
  // the list of the two directions, the same in both boxes
  const DIR_LIST = (cls) => `<label>הכיוון <select class="${cls}" aria-label="איפה הספרה החדשה נכנסת">` +
    `<option value="lsb">שרשור ל-LSB : הספרה החדשה נכנסת מימין</option><option value="msb">שרשור ל-MSB : הספרה החדשה נכנסת משמאל</option></select></label>`;

  // A machine on a ring: state 0 on top, the current state lit, the edges out of it (one
  // per target, with the digits that lead there) and the edge just taken. o: { n, b, t
  // (next[s][d]), cur, prev, last (the digit just read), label(s), title(s), accept(s), mk,
  // aria }. An edge out of the current state bends toward the centre, the edge just taken
  // away from it (or further in, on a ring of more than 6), so the two never overlap.
  const ring = (o) => {
    const { n, b, t, cur, prev, last, mk } = o;
    const R = n <= 5 ? 92 : n <= 9 ? 104 : 112, r = n <= 7 ? 22 : n <= 11 ? 18 : 19, loop = r + 34;
    const W = n > 11 ? 380 : 360, cx = W / 2, cy = loop + r + 22 + R, H = Math.round(cy + R + loop + 12);
    const pos = Array.from({ length: n }, (_, i) => [cx + R * Math.sin((2 * Math.PI * i) / n), cy - R * Math.cos((2 * Math.PI * i) / n)]);
    let s = `<svg class="figure dv-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${o.aria}">` +
      `<defs><marker id="${mk}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>`;
    const labels = [];
    const edge = (i, j, cls, lab, lcls, inward = true) => {
      const [x0, y0] = pos[i], [x1, y1] = pos[j];
      if (i === j) {
        const ux = (x0 - cx) / R, uy = (y0 - cy) / R, tx = -uy, ty = ux, out = loop;
        const a = [x0 + r * (ux * 0.8 - tx * 0.6), y0 + r * (uy * 0.8 - ty * 0.6)], c = [x0 + r * (ux * 0.8 + tx * 0.6), y0 + r * (uy * 0.8 + ty * 0.6)];
        s += `<path class="${cls}" d="M${f(a[0])},${f(a[1])} C${f(x0 + ux * out - tx * 22)},${f(y0 + uy * out - ty * 22)} ${f(x0 + ux * out + tx * 22)},${f(y0 + uy * out + ty * 22)} ${f(c[0])},${f(c[1])}" marker-end="url(#${mk})"/>`;
        labels.push([x0 + ux * (out + 6), y0 + uy * (out + 6) + 4, lab, lcls]);
        return;
      }
      const dx = x1 - x0, dy = y1 - y0, dist = Math.hypot(dx, dy), mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
      // on a large ring an outward edge would graze the states between its ends: the edge just
      // taken bends inward too, further than the edges out of the state
      const toward = (cx - mx) * dy - (cy - my) * dx >= 0 ? 1 : -1, sg = inward || n > 6 ? toward : -toward;
      const nx = (sg * dy) / dist, ny = (-sg * dx) / dist, bend = (inward || n <= 6 ? 0.22 : 0.4) * dist;
      const c = [(x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend];
      const trim = (px, py, k) => { const vx = c[0] - px, vy = c[1] - py, l = Math.hypot(vx, vy); return [px + (vx / l) * k, py + (vy / l) * k]; };
      const a = trim(x0, y0, r), e = trim(x1, y1, r + 2);
      s += `<path class="${cls}" d="M${f(a[0])},${f(a[1])} Q${f(c[0])},${f(c[1])} ${f(e[0])},${f(e[1])}" marker-end="url(#${mk})"/>`;
      labels.push([0.25 * a[0] + 0.5 * c[0] + 0.25 * e[0] + nx * 11, 0.25 * a[1] + 0.5 * c[1] + 0.25 * e[1] + ny * 11 + 4, lab, lcls]);
    };
    const groups = new Map();
    for (let d = 0; d < b; d++) { const j = t[cur][d]; if (!groups.has(j)) groups.set(j, []); groups.get(j).push(d); }
    // a loop just taken is the loop out of the current state too: drawn once, as taken
    const loopTaken = prev !== null && prev === cur;
    groups.forEach((dg, j) => {
      const one = b === 2 && dg.length === 1 && dg[0] === 1, taken = loopTaken && j === cur;
      edge(cur, j, `fs-edge${one ? " is-found" : ""}${taken ? " is-taken" : ""}`, dg.map((d) => DIG[d]).join(","), `fs-label halo${one ? " is-found" : ""}${taken ? " is-taken" : ""}`);
    });
    if (prev !== null && !loopTaken) edge(prev, cur, "fs-edge is-taken", DIG[last], "fs-label halo is-taken", false);
    pos.forEach(([x, y], i) => {
      const acc = o.accept(i);
      s += `<g class="fs-node${i === cur ? " is-cur" : ""}${acc ? " is-start" : ""}" data-s="${i}"><title>${o.title(i)}</title><circle cx="${f(x)}" cy="${f(y)}" r="${r}"/>` +
        (acc ? `<circle cx="${f(x)}" cy="${f(y)}" r="${r - 5}"/>` : "") +
        `<text x="${f(x)}" y="${f(y + 4.5)}" text-anchor="middle">${o.label(i)}</text></g>`;
    });
    labels.forEach(([x, y, lab, cls]) => { s += `<text class="${cls}" x="${f(x)}" y="${f(y)}" text-anchor="middle">${lab}</text>`; });
    return s + "</svg>";
  };
  const legendOf = (b, acc) => (b === 2
    ? `<span><i class="fs-key"></i>הביט 0</span><span><i class="fs-key-found"></i>הביט 1</span>`
    : `<span><i class="fs-key"></i>הספרות שמובילות לכל מצב</span>`) +
    `<span><i class="dv-key-taken"></i>המעבר האחרון</span><span><i class="dv-key-cur"></i>המצב הנוכחי</span><span><i class="dv-key-acc"></i>${acc}</span>`;

  // The box (0055): one number read by one machine, chosen in a list. Concatenated at the
  // LSB, each new digit is the number's new lowest digit: the number is read from its MSB
  // and the state is the remainder. Concatenated at the MSB, each new digit is the new
  // highest digit: the number is read from its LSB and the state is x = remainder * B^-k.
  // Under the ring the digits read, the number they spell and the state's meaning.
  const divfsmView = () => ({
    mount(box) {
      const d0 = { m: Number(box.dataset.m || 3), b: Number(box.dataset.base || 2), num: box.dataset.num || "1011", dir: box.dataset.dir === "msb" ? "msb" : "lsb" };
      const st = { m: d0.m, b: d0.b, ds: parse(d0.num, d0.b) || [1, 0, 1, 1], k: 0, dir: d0.dir };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>מחלקים ב-m <select class="dv-m" aria-label="המחלק m">${MS.map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<label>בכל מחזור <select class="dv-b" aria-label="הבסיס : כמה ביטים נכנסים בכל מחזור">${BASES.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>המספר</span><input type="text" class="ex-num dv-num" dir="ltr" maxlength="${MAXD}" spellcheck="false" aria-label="המספר בבסיס שנבחר, הספרה הגבוהה משמאל, עד ${MAXD} ספרות"></label>` +
        DIR_LIST("dv-dir") +
        `<button type="button" class="md-button dv-rand">מספר אקראי</button><span class="dv-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err dv-err"></span></div>` +
        `<div class="ex-controls dv-add"></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני הספרה הראשונה</button>` +
        `<button type="button" class="md-button ex-prev">הספרה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הספרה הבאה</button>` +
        `<button type="button" class="md-button ex-end">כל הספרות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary dv-sum" aria-live="polite"></p>` +
        `<div class="dv-digits"></div>` +
        `<div class="dv-pair"><div class="dv-side"><p class="ex-title dv-head"></p><div class="dv-ring"></div><p class="dv-read"></p></div></div>` +
        `<span class="viz-legend dv-legend"></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const n = () => st.ds.length;

      const draw = () => {
        const m = st.m, b = st.b, N = n(), inv = divInv(b % m, m), lsb = st.dir === "msb";   // a digit at the MSB: read from the LSB
        st.k = Math.min(st.k, N);
        $(".dv-m").value = String(m); $(".dv-b").value = String(b); $(".dv-dir").value = st.dir;
        [...$(".dv-m").options].forEach((o) => { o.disabled = gcd(Number(o.value), b) !== 1; });
        const states = divRun(st.ds, m, b, lsb), k = st.k;
        const read = lsb ? st.ds.slice(N - k) : st.ds.slice(0, k), v = big(read, b), all = big(st.ds, b);
        $(".ex-pos").textContent = `ספרה ${k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N;
        $(".dv-sum").innerHTML = `${code(digitText(st.ds))} בבסיס ${ltr(b)} הוא ${ltr(all.toLocaleString("en-US"))}. ` + (lsb
          ? `כל ספרה חדשה נכנסת כ-MSB, ולכן המכונה קוראת את המספר מה-LSB : ${ltr(`x' = (x + d)·${inv} mod ${m}`)}, כי ${ltr(`${b}⁻¹ = ${inv}`)} מודולו ${ltr(m)}` + (inv === 1 ? " : המכונה רק מחברת ספרות." : ".")
          : `כל ספרה חדשה נכנסת כ-LSB, ולכן המכונה קוראת את המספר מה-MSB : ${ltr(`r' = (${b}·r + d) mod ${m}`)}` + (b % m === 1 ? " : המכונה רק מחברת ספרות." : "."));
        // the digits: the machine has read the k on the left (from the MSB) or on the right (from the LSB)
        $(".dv-digits").innerHTML = `<span class="dv-tag">MSB →</span><span class="dv-cells">` +
          st.ds.map((d, i) => `<span class="dv-cell${!lsb && i < k ? " is-msb" : ""}${lsb && i >= N - k ? " is-lsb" : ""}">${DIG[d]}</span>`).join("") +
          `</span><span class="dv-tag">← LSB</span>`;
        $(".dv-head").textContent = lsb ? "שרשור ל-MSB : המצב הוא ‎x = r · B⁻ᵏ‎" : "שרשור ל-LSB : המצב הוא השארית";
        const seq = lsb ? [...st.ds].reverse() : st.ds;
        $(".dv-ring").innerHTML = ring({
          n: m, b, t: divTable(m, b, lsb), cur: states[k], prev: k ? states[k - 1] : null, last: k ? seq[k - 1] : null,
          mk: `dv-arrow-${box.dataset.dvqIndex || 0}`, label: (i) => i, title: (i) => `${lsb ? "x" : "r"} = ${i}`, accept: (i) => i === 0,
          aria: `${lsb ? "המכונה של שרשור ל-MSB" : "המכונה של שרשור ל-LSB"} : ${m} מצבים, המצב הנוכחי ${states[k]}`,
        });
        const d = k ? seq[k - 1] : null;
        $(".dv-read").innerHTML = k === 0 ? `עוד לא נקראה ספרה : ${ltr(lsb ? "x = 0" : "r = 0")}.`
          : `נקראו ${code(digitText(read))} = ${ltr(v.toLocaleString("en-US"))}. ` + (lsb
            ? `הצעד האחרון ${ltr(`(${states[k - 1]} + ${d})·${inv} mod ${m} = ${states[k]}`)}; השארית ${ltr(`x·${b}^${k} mod ${m} = ${Number(v % BigInt(m))}`)}.`
            : `הצעד האחרון ${ltr(`(${b}·${states[k - 1]} + ${d}) mod ${m} = ${states[k]}`)}, וזו השארית.`) +
            (states[k] === 0 ? ` <span class="wv-ok">מתחלק ✓</span>` : "");
        $(".dv-legend").innerHTML = legendOf(b, "עיגול כפול : המספר מתחלק (ומשם מתחילים)");
        $(".dv-add").innerHTML = b <= 4
          ? `<span class="ex-title">${lsb ? "שרשור ספרה משמאל (MSB) :" : "שרשור ספרה מימין (LSB) :"}</span> ` + Array.from({ length: b }, (_, dd) => `<button type="button" class="md-button md-button--primary dv-push" data-d="${dd}">${dd}</button>`).join(" ") +
            ` <button type="button" class="md-button dv-pop">מחיקת הספרה האחרונה</button>`
          : `<span class="ex-note">בבסיס ${ltr(b)} מקלידים את המספר בשדה (${ltr(b === 16 ? "0-9, a-f" : "0-9")}).</span>`;
        if (k === N) {
          const rem = Number(all % BigInt(m));
          answer(box, `${ltr(all.toLocaleString("en-US"))} ${rem === 0 ? "מתחלק" : "לא מתחלק"} ב-${ltr(m)} (שארית ${ltr(rem)}) : המכונה ${rem === 0 ? "במצב 0" : `במצב ${ltr(`${lsb ? "x" : "r"} = ${states[N]}`)}, לא במצב 0`}.`,
            box.querySelectorAll(".fs-node.is-cur"));
        } else answer(box, null);
      };
      const setNum = (ds) => { st.ds = ds; $(".dv-num").value = digitText(ds); $(".dv-err").textContent = ""; };
      const stop = autoplay(play, speed, { step: () => { st.k = Math.min(n(), st.k + 1); draw(); }, done: () => st.k >= n(), restart: () => { st.k = 0; draw(); } });
      $(".dv-num").addEventListener("change", () => {
        const ds = parse($(".dv-num").value, st.b);
        if (!ds) { $(".dv-err").textContent = `המספר : 1 עד ${MAXD} ספרות בבסיס ${st.b}`; return; }
        stop(); setNum(ds); st.k = 0; draw();
      });
      $(".dv-num").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".dv-num").blur(); });
      $(".dv-m").addEventListener("change", () => { stop(); st.m = Number($(".dv-m").value); st.k = 0; draw(); });
      $(".dv-dir").addEventListener("change", () => { stop(); st.dir = $(".dv-dir").value === "msb" ? "msb" : "lsb"; st.k = 0; draw(); });
      $(".dv-b").addEventListener("change", () => {
        stop();
        const nb = Number($(".dv-b").value), v = big(st.ds, st.b);
        st.b = nb; setNum(toDigits(v, nb));
        if (gcd(st.m, nb) !== 1) st.m = 3;
        st.k = 0; draw();
      });
      // a digit concatenated at the chosen end, and read at once: the machine's last step
      $(".dv-add").addEventListener("click", (e) => {
        const push = e.target.closest(".dv-push"), pop = e.target.closest(".dv-pop"), atMsb = st.dir === "msb";
        if (push && n() < MAXD) { stop(); const dd = Number(push.dataset.d); setNum(atMsb ? [dd, ...st.ds] : [...st.ds, dd]); st.k = n(); draw(); }
        if (pop && n() > 1) { stop(); setNum(atMsb ? st.ds.slice(1) : st.ds.slice(0, -1)); st.k = Math.min(st.k, n()); draw(); }
      });
      const seed = seedControls(box, $(".dv-anchor"), (rng) => {
        stop();
        const len = 6 + Math.floor(rng() * 5);
        setNum(Array.from({ length: len }, (_, i) => (i === 0 ? 1 + Math.floor(rng() * (st.b - 1)) : Math.floor(rng() * st.b))));
        st.k = 0; draw();
      }, { fresh: false });
      $(".dv-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(n(), st.k + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = n(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); Object.assign(st, { m: d0.m, b: d0.b, k: 0, dir: d0.dir }); setNum(parse(d0.num, d0.b) || [1, 0, 1, 1]); draw();
      });
      setNum(st.ds);
      draw();
    },
  });

  // The box (0056): the digits that enter a window of L digits, one machine chosen in a
  // list (a digit at the LSB or at the MSB). The data path: the window's cells, the digit
  // that enters, the digit that leaves and the remainder's update; up to 16 windows also
  // the machine with a state per window (a double circle: the window divides by m).
  const WMAX = 16, LMAX = 8;
  const winfsmView = () => ({
    mount(box) {
      const d0 = { m: Number(box.dataset.m || 3), b: Number(box.dataset.base || 2), L: Number(box.dataset.len || 3), init: box.dataset.init || "000",
        bits: box.dataset.num || "1101", dir: box.dataset.dir === "msb" ? "msb" : "lsb" };
      const st = { m: d0.m, b: d0.b, L: d0.L, init: [], ds: [], k: 0, dir: d0.dir };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>מחלקים ב-m <select class="wf-m" aria-label="המחלק m">${MS.map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<label>בכל מחזור <select class="wf-b" aria-label="הבסיס : כמה ביטים נכנסים בכל מחזור">${BASES.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>אורך החלון L</span><input type="range" class="wf-L" min="1" max="${LMAX}" step="1" value="${st.L}" dir="ltr" aria-label="אורך החלון, מ-1 עד ${LMAX} ספרות"><output class="wf-out-L">${st.L}</output></label>` +
        DIR_LIST("wf-dir") +
        `<label><span>החלון בהתחלה</span><input type="text" class="ex-num wf-init" dir="ltr" maxlength="${LMAX}" spellcheck="false" aria-label="החלון אחרי reset, L ספרות, הגבוהה משמאל"></label>` +
        `<label><span>הספרות שנכנסות</span><input type="text" class="ex-num wf-num" dir="ltr" maxlength="${MAXD}" spellcheck="false" aria-label="הספרות שנכנסות לחלון, לפי סדר ההגעה, עד ${MAXD}"></label>` +
        `<button type="button" class="md-button wf-rand">ספרות אקראיות</button><span class="wf-anchor"></span>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err wf-err"></span></div>` +
        `<div class="ex-controls wf-add"></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני הספרה הראשונה</button>` +
        `<button type="button" class="md-button ex-prev">הספרה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הספרה הבאה</button>` +
        `<button type="button" class="md-button ex-end">כל הספרות</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary wf-sum" aria-live="polite"></p>` +
        `<div class="wf-path" data-steady></div><p class="wf-rem"></p>` +
        `<div class="dv-pair"><div class="dv-side"><p class="ex-title wf-head"></p><div class="dv-ring wf-ring"></div></div></div>` +
        `<p class="dv-read wf-read"></p>` +
        `<span class="viz-legend dv-legend wf-legend"></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const n = () => st.ds.length;
      const fit = (ds) => { const pad = Array(Math.max(0, st.L - ds.length)).fill(0); return [...pad, ...ds].slice(-st.L); };

      const draw = () => {
        const { m, b, L } = st, N = n(), msb = st.dir === "msb", inv = divInv(b % m, m), size = b ** L;
        st.k = Math.min(st.k, N);
        $(".wf-m").value = String(m); $(".wf-b").value = String(b); $(".wf-dir").value = st.dir;
        $(".wf-L").value = String(L); $(".wf-out-L").textContent = String(L);
        [...$(".wf-m").options].forEach((o) => { o.disabled = gcd(Number(o.value), b) !== 1; });
        const init = Number(big(st.init, b)), run = winRun(st.ds, m, b, L, init, msb), k = st.k, now = run[k];
        const cl = b ** L % m, ch = b ** (L - 1) % m;
        $(".ex-pos").textContent = `ספרה ${k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N;
        $(".wf-sum").innerHTML = msb
          ? `ספרה נכנסת כ-MSB והספרה הנמוכה יוצאת : ${ltr(`w' = d·${b}^${L - 1} + ⌊w / ${b}⌋`)}. השארית בלי החלון : ${ltr(`r' = ((r − out)·${inv} + d·${ch}) mod ${m}`)}, כי ${ltr(`${b}⁻¹ = ${inv}`)} ו-${ltr(`${b}^${L - 1} mod ${m} = ${ch}`)}.`
          : `ספרה נכנסת כ-LSB והספרה הגבוהה יוצאת : ${ltr(`w' = (${b}·w + d) mod ${b}^${L}`)}. השארית בלי החלון : ${ltr(`r' = (${b}·r + d − out·${cl}) mod ${m}`)}, כי ${ltr(`${b}^${L} mod ${m} = ${cl}`)}.`;
        // the data path: the window's cells (the highest on the left), the digit in at one end, the digit out at the other
        const cells = toDigits(BigInt(now.w), b, L), pad = Array(L - cells.length).fill(0), win = [...pad, ...cells];
        const din = k ? st.ds[k - 1] : null, gone = k ? now.out : null;
        const inCell = k ? (msb ? 0 : L - 1) : -1;
        const out = `<span class="wf-io wf-out${k ? "" : " is-idle"}"><span class="dv-tag">יוצאת</span><span class="dv-cell is-gone">${k ? DIG[gone] : "·"}</span></span>`;
        const inn = `<span class="wf-io wf-in${k ? "" : " is-idle"}"><span class="dv-tag">נכנסת</span><span class="dv-cell is-in">${k ? DIG[din] : "·"}</span></span>`;
        const stream = `<span class="wf-stream" dir="ltr"><span class="dv-tag">הספרות</span><span class="dv-cells">` +
          st.ds.map((d, i) => `<span class="dv-cell${i < k ? " is-read" : ""}${i === k - 1 ? " is-now" : ""}">${DIG[d]}</span>`).join("") + `</span></span>`;
        $(".wf-path").innerHTML = stream +
          `<div class="wf-reg" dir="ltr">${msb ? inn : out}<span class="dv-tag">MSB</span><span class="dv-cells wf-win">` +
          win.map((d, i) => `<span class="dv-cell${i === inCell ? " is-in" : ""}">${DIG[d]}</span>`).join("") +
          `</span><span class="dv-tag">LSB</span>${msb ? out : inn}</div>`;
        $(".wf-rem").innerHTML = (k === 0
            ? `אחרי reset : החלון ${code(digitText(win))} = ${ltr(init)}, ${ltr(`r = ${init} mod ${m} = ${now.r}`)}.`
            : msb ? `${ltr(`r' = ((${run[k - 1].r} − ${gone})·${inv} + ${din}·${ch}) mod ${m} = ${now.r}`)}; החלון ${code(digitText(win))} = ${ltr(now.w)}, ${ltr(`${now.w} mod ${m} = ${now.w % m}`)}.`
              : `${ltr(`r' = (${b}·${run[k - 1].r} + ${din} − ${gone}·${cl}) mod ${m} = ${now.r}`)}; החלון ${code(digitText(win))} = ${ltr(now.w)}, ${ltr(`${now.w} mod ${m} = ${now.w % m}`)}.`);
        $(".wf-head").textContent = size <= WMAX ? `המכונה : מצב לכל חלון, ${size} מצבים` : `המכונה : ${size} חלונות, יותר מדי לציור`;
        $(".wf-ring").innerHTML = size <= WMAX ? ring({
          n: size, b, t: Array.from({ length: size }, (_, w) => Array.from({ length: b }, (_, d) => winStep(w, d, b, L, msb))),
          cur: now.w, prev: k ? run[k - 1].w : null, last: din, mk: `wf-arrow-${box.dataset.dvqIndex || 0}`,
          label: (w) => digitText(fit(toDigits(BigInt(w), b, L))), title: (w) => `${digitText(fit(toDigits(BigInt(w), b, L)))} = ${w}`, accept: (w) => w % m === 0,
          aria: `המכונה של החלון : ${size} מצבים, החלון הנוכחי ${digitText(win)}`,
        }) : `<p class="ex-note">‏${ltr(`${b}^${L} = ${size.toLocaleString("en-US")}`)} חלונות. נתיב הנתונים למעלה הוא אותה מכונה : רגיסטר הזזה של ${ltr(L)} ספרות ורגיסטר שארית.</p>`;
        $(".wf-read").innerHTML = `החלון ${code(digitText(win))} ` + (now.r === 0 ? `<span class="wv-ok">מתחלק ב-${ltr(m)} ✓</span>` : `לא מתחלק ב-${ltr(m)} (שארית ${ltr(now.r)})`) +
          (k ? `. ${msb ? "הספרה נכנסה משמאל, והימנית יצאה" : "הספרה נכנסה מימין, והשמאלית יצאה"}.` : ".");
        $(".wf-legend").innerHTML = size <= WMAX ? legendOf(b, "עיגול כפול : החלון מתחלק") : "";
        $(".wf-add").innerHTML = b <= 4
          ? `<span class="ex-title">${msb ? "ספרה נכנסת משמאל (MSB) :" : "ספרה נכנסת מימין (LSB) :"}</span> ` + Array.from({ length: b }, (_, dd) => `<button type="button" class="md-button md-button--primary wf-push" data-d="${dd}">${dd}</button>`).join(" ") +
            ` <button type="button" class="md-button wf-pop">מחיקת הספרה האחרונה</button>`
          : `<span class="ex-note">בבסיס ${ltr(b)} מקלידים את הספרות בשדה (${ltr(b === 16 ? "0-9, a-f" : "0-9")}).</span>`;
        if (k === N && N) answer(box, `אחרי ${ltr(N)} ספרות החלון הוא ${code(digitText(win))} = ${ltr(now.w)}, ${now.r === 0 ? "ומתחלק" : "ולא מתחלק"} ב-${ltr(m)} (שארית ${ltr(now.r)}).`, box.querySelectorAll(".wf-win, .fs-node.is-cur"));
        else answer(box, null);
      };
      const setInit = (ds) => { st.init = fit(ds); $(".wf-init").value = digitText(st.init); };
      const setNum = (ds) => { st.ds = ds; $(".wf-num").value = ds.length ? digitText(ds) : ""; $(".wf-err").textContent = ""; };
      const stop = autoplay(play, speed, { step: () => { st.k = Math.min(n(), st.k + 1); draw(); }, done: () => st.k >= n(), restart: () => { st.k = 0; draw(); } });
      $(".wf-num").addEventListener("change", () => {
        const ds = parse($(".wf-num").value, st.b);
        if (!ds) { $(".wf-err").textContent = `הספרות : 1 עד ${MAXD} ספרות בבסיס ${st.b}`; return; }
        stop(); setNum(ds); st.k = 0; draw();
      });
      $(".wf-init").addEventListener("change", () => {
        const ds = parse($(".wf-init").value, st.b, LMAX);
        if (!ds) { $(".wf-err").textContent = `החלון : עד ${st.L} ספרות בבסיס ${st.b}`; setInit(st.init); return; }
        stop(); setInit(ds); $(".wf-err").textContent = ""; st.k = 0; draw();
      });
      [$(".wf-num"), $(".wf-init")].forEach((el) => el.addEventListener("keydown", (e) => { if (e.key === "Enter") el.blur(); }));
      $(".wf-m").addEventListener("change", () => { stop(); st.m = Number($(".wf-m").value); st.k = 0; draw(); });
      $(".wf-dir").addEventListener("change", () => { stop(); st.dir = $(".wf-dir").value === "msb" ? "msb" : "lsb"; st.k = 0; draw(); });
      $(".wf-L").addEventListener("input", () => { stop(); st.L = Number($(".wf-L").value); setInit(st.init); st.k = 0; draw(); });
      $(".wf-b").addEventListener("change", () => {
        stop();
        const nb = Number($(".wf-b").value), v = big(st.init, st.b);
        st.b = nb;
        setInit(toDigits(v % BigInt(nb) ** BigInt(st.L), nb));   // the window's value, as far as it fits
        setNum(st.ds.map((d) => d % nb));
        if (gcd(st.m, nb) !== 1) st.m = 3;
        st.k = 0; draw();
      });
      $(".wf-add").addEventListener("click", (e) => {
        const push = e.target.closest(".wf-push"), pop = e.target.closest(".wf-pop");
        if (push && n() < MAXD) { stop(); setNum([...st.ds, Number(push.dataset.d)]); st.k = n(); draw(); }
        if (pop && n() > 1) { stop(); setNum(st.ds.slice(0, -1)); st.k = Math.min(st.k, n()); draw(); }
      });
      const seed = seedControls(box, $(".wf-anchor"), (rng) => {
        stop();
        setNum(Array.from({ length: 6 + Math.floor(rng() * 5) }, () => Math.floor(rng() * st.b)));
        st.k = 0; draw();
      }, { fresh: false });
      $(".wf-rand").addEventListener("click", () => seed.draw());
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(0, st.k - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.k = Math.min(n(), st.k + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = n(); draw(); });
      const reset = () => {
        Object.assign(st, { m: d0.m, b: d0.b, L: d0.L, k: 0, dir: d0.dir });
        setInit(parse(d0.init, d0.b, LMAX) || []); setNum(parse(d0.bits, d0.b) || [1, 1, 0, 1]);
      };
      $(".ex-reset").addEventListener("click", () => { stop(); reset(); draw(); });
      reset();
      draw();
    },
  });

  dvqExplorers.register({
    views: { divfsm: divfsmView, winfsm: winfsmView },
    help: {
      divfsm: "בוחרים ברשימה איפה הספרה החדשה נכנסת : שרשור ל-LSB (המכונה קוראת את המספר מה-MSB, והמצב הוא השארית) או שרשור ל-MSB (המכונה קוראת מה-LSB). בכל צעד המכונה קוראת עוד ספרה, והגרף מראה את המצב הנוכחי, את המעבר האחרון ואת המעברים שיוצאים ממנו. בוחרים m ובסיס (כמה ביטים במחזור), מקלידים מספר, משרשרים ספרות בכפתורים או מגרילים. בסוף המכונה במצב 0 בדיוק כשהמספר מתחלק.",
      winfsm: "החלון שומר רק את L הספרות האחרונות. בוחרים ברשימה איפה ספרה חדשה נכנסת : מימין (שרשור ל-LSB, הספרה השמאלית יוצאת) או משמאל (שרשור ל-MSB, הימנית יוצאת). נתיב הנתונים מראה את החלון, את הספרה שנכנסת ואת זו שיוצאת, ואת עדכון השארית בלי לחשב את החלון מחדש. כשיש עד 16 חלונות מופיעה גם המכונה עם מצב לכל חלון. בוחרים m, בסיס, L, החלון אחרי reset והספרות שנכנסות.",
    },
    models: { divInv, divTable, divRun, winRun, winStep },
  });
})();
