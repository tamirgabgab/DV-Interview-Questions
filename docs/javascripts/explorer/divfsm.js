// kinds: divfsm
//   divfsm                 0055        divisible by m: one number fed digit by digit to two machines side by side, from the MSB (the remainder) and from the LSB (x = remainder * B^-k); m, the base (k bits a cycle or decimal), digits typed, added or drawn; each ring shows its current state, the edges out of it and the edge just taken
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

  const MS = [3, 5, 7, 9, 11, 13, 15];
  const BASES = [[2, "ביט אחד (בסיס 2)"], [4, "2 ביטים (בסיס 4)"], [8, "3 ביטים (בסיס 8)"], [16, "4 ביטים (בסיס 16)"], [10, "ספרה עשרונית"]];
  const MAXD = 16;
  const DIG = "0123456789abcdef";
  const parse = (text, b) => {
    const s = String(text).trim().toLowerCase();
    if (!s.length || s.length > MAXD) return null;
    const ds = [...s].map((c) => DIG.indexOf(c));
    return ds.every((d) => d >= 0 && d < b) ? ds : null;
  };
  const big = (ds, b) => ds.reduce((v, d) => v * BigInt(b) + BigInt(d), 0n);
  const toDigits = (v, b) => { const out = []; do { out.unshift(Number(v % BigInt(b))); v /= BigInt(b); } while (v > 0n); return out.slice(-MAXD); };

  // The box (0055): the two machines of one number. A ring per machine with every state,
  // the current one lit, the edges out of it (by digit) and the edge just taken; under each
  // ring the digits it has read, the number they spell and the state's meaning.
  const divfsmView = () => ({
    mount(box) {
      const d0 = { m: Number(box.dataset.m || 3), b: Number(box.dataset.base || 2), num: box.dataset.num || "1011" };
      const st = { m: d0.m, b: d0.b, ds: parse(d0.num, d0.b) || [1, 0, 1, 1], k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>מחלקים ב-m <select class="dv-m" aria-label="המחלק m">${MS.map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<label>בכל מחזור <select class="dv-b" aria-label="הבסיס : כמה ביטים נכנסים בכל מחזור">${BASES.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label><span>המספר</span><input type="text" class="ex-num dv-num" dir="ltr" maxlength="${MAXD}" spellcheck="false" aria-label="המספר בבסיס שנבחר, הספרה הגבוהה משמאל, עד ${MAXD} ספרות"></label>` +
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
        `<div class="dv-pair"><div class="dv-side"><p class="ex-title">מה-MSB : המצב הוא השארית</p><div class="dv-ring dv-ring-m"></div><p class="dv-read dv-read-m"></p></div>` +
        `<div class="dv-side"><p class="ex-title">מה-LSB : המצב הוא ‎x = r · B⁻ᵏ‎</p><div class="dv-ring dv-ring-l"></div><p class="dv-read dv-read-l"></p></div></div>` +
        `<span class="viz-legend dv-legend"></span>`;
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const digitText = (ds) => ds.map((d) => DIG[d]).join("") || "0";
      const n = () => st.ds.length;

      const ring = (lsb, states) => {
        const m = st.m, b = st.b, t = divTable(m, b, lsb), cur = states[st.k], prev = st.k ? states[st.k - 1] : null;
        const seq = lsb ? [...st.ds].reverse() : st.ds, last = st.k ? seq[st.k - 1] : null;
        const R = m <= 5 ? 92 : m <= 9 ? 104 : 112, r = m <= 7 ? 22 : m <= 11 ? 18 : 15, loop = r + 34, W = 360, cx = W / 2, cy = loop + r + 22 + R, H = Math.round(cy + R + loop + 12);
        const pos = Array.from({ length: m }, (_, i) => [cx + R * Math.sin((2 * Math.PI * i) / m), cy - R * Math.cos((2 * Math.PI * i) / m)]);
        const mk = `dv-arrow-${lsb ? "l" : "m"}-${box.dataset.dvqIndex || 0}`;
        let s = `<svg class="figure dv-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${lsb ? "המכונה מה-LSB" : "המכונה מה-MSB"} : ${m} מצבים, המצב הנוכחי ${cur}">` +
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
          // the edges out of the state bend toward the centre, the edge just taken away from it,
          // so an edge and the one back between the same two states never overlap
          const dx = x1 - x0, dy = y1 - y0, dist = Math.hypot(dx, dy), mx = (x0 + x1) / 2, my = (y0 + y1) / 2;
          const toward = (cx - mx) * dy - (cy - my) * dx >= 0 ? 1 : -1, sg = inward ? toward : -toward;
          const nx = (sg * dy) / dist, ny = (-sg * dx) / dist, bend = 0.22 * dist;
          const c = [(x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend];
          const trim = (px, py, k) => { const vx = c[0] - px, vy = c[1] - py, l = Math.hypot(vx, vy); return [px + (vx / l) * k, py + (vy / l) * k]; };
          const a = trim(x0, y0, r), e = trim(x1, y1, r + 2);
          s += `<path class="${cls}" d="M${f(a[0])},${f(a[1])} Q${f(c[0])},${f(c[1])} ${f(e[0])},${f(e[1])}" marker-end="url(#${mk})"/>`;
          labels.push([0.25 * a[0] + 0.5 * c[0] + 0.25 * e[0] + nx * 11, 0.25 * a[1] + 0.5 * c[1] + 0.25 * e[1] + ny * 11 + 4, lab, lcls]);
        };
        // the edges out of the current state, one per target with the digits that lead there
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
          s += `<g class="fs-node${i === cur ? " is-cur" : ""}${i === 0 ? " is-start" : ""}" data-s="${i}"><title>${lsb ? "x" : "r"} = ${i}</title><circle cx="${f(x)}" cy="${f(y)}" r="${r}"/>` +
            (i === 0 ? `<circle cx="${f(x)}" cy="${f(y)}" r="${r - 5}"/>` : "") +
            `<text x="${f(x)}" y="${f(y + 4.5)}" text-anchor="middle">${i}</text></g>`;
        });
        labels.forEach(([x, y, lab, cls]) => { s += `<text class="${cls}" x="${f(x)}" y="${f(y)}" text-anchor="middle">${lab}</text>`; });
        return s + "</svg>";
      };

      const draw = () => {
        const m = st.m, b = st.b, N = n(), inv = divInv(b % m, m);
        st.k = Math.min(st.k, N);
        $(".dv-m").value = String(m); $(".dv-b").value = String(b);
        [...$(".dv-m").options].forEach((o) => { o.disabled = gcd(Number(o.value), b) !== 1; });
        const sm = divRun(st.ds, m, b, false), sl = divRun(st.ds, m, b, true);
        const k = st.k, top = st.ds.slice(0, k), low = st.ds.slice(N - k);
        const vm = big(top, b), vl = big(low, b), all = big(st.ds, b);
        $(".ex-pos").textContent = `ספרה ${k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N;
        $(".dv-sum").innerHTML = `${code(digitText(st.ds))} בבסיס ${ltr(b)} הוא ${ltr(all.toLocaleString("en-US"))}. ` +
          `מה-MSB ${ltr(`r' = (${b}·r + d) mod ${m}`)}; מה-LSB ${ltr(`x' = (x + d)·${inv} mod ${m}`)}, כי ${ltr(`${b}⁻¹ = ${inv}`)} מודולו ${ltr(m)}` +
          (inv === 1 ? " : שתי המכונות רק מחברות ספרות." : ".");
        // the digits: the MSB machine has read the k on the left, the LSB machine the k on the right
        $(".dv-digits").innerHTML = `<span class="dv-tag">MSB →</span><span class="dv-cells">` +
          st.ds.map((d, i) => `<span class="dv-cell${i < k ? " is-msb" : ""}${i >= N - k ? " is-lsb" : ""}">${DIG[d]}</span>`).join("") +
          `</span><span class="dv-tag">← LSB</span>`;
        $(".dv-ring-m").innerHTML = ring(false, sm);
        $(".dv-ring-l").innerHTML = ring(true, sl);
        const sd = k ? st.ds[k - 1] : null, ld = k ? st.ds[N - k] : null;
        $(".dv-read-m").innerHTML = k === 0 ? `עוד לא נקראה ספרה : ${ltr("r = 0")}.`
          : `נקראו ${code(digitText(top))} = ${ltr(vm.toLocaleString("en-US"))}. הצעד האחרון ${ltr(`(${b}·${sm[k - 1]} + ${sd}) mod ${m} = ${sm[k]}`)}, וזו השארית.` +
            (sm[k] === 0 ? ` <span class="wv-ok">מתחלק ✓</span>` : "");
        const remL = Number(vl % BigInt(m));
        $(".dv-read-l").innerHTML = k === 0 ? `עוד לא נקראה ספרה : ${ltr("x = 0")}.`
          : `נקראו ${code(digitText(low))} = ${ltr(vl.toLocaleString("en-US"))}. הצעד האחרון ${ltr(`(${sl[k - 1]} + ${ld})·${inv} mod ${m} = ${sl[k]}`)}; השארית ${ltr(`x·${b}^${k} mod ${m} = ${remL}`)}.` +
            (sl[k] === 0 ? ` <span class="wv-ok">מתחלק ✓</span>` : "");
        $(".dv-legend").innerHTML = b === 2
          ? `<span><i class="fs-key"></i>הביט 0</span><span><i class="fs-key-found"></i>הביט 1</span><span><i class="dv-key-taken"></i>המעבר האחרון</span><span><i class="dv-key-cur"></i>המצב הנוכחי</span>`
          : `<span><i class="fs-key"></i>הספרות שמובילות לכל מצב</span><span><i class="dv-key-taken"></i>המעבר האחרון</span><span><i class="dv-key-cur"></i>המצב הנוכחי</span>`;
        $(".dv-add").innerHTML = b <= 4
          ? `<span class="ex-title">הוספת ספרה בסוף :</span> ` + Array.from({ length: b }, (_, d) => `<button type="button" class="md-button md-button--primary dv-push" data-d="${d}">${d}</button>`).join(" ") +
            ` <button type="button" class="md-button dv-pop">מחיקת הספרה האחרונה</button>`
          : `<span class="ex-note">בבסיס ${ltr(b)} מקלידים את המספר בשדה (${ltr(b === 16 ? "0-9, a-f" : "0-9")}).</span>`;
        if (k === N) {
          const rem = Number(all % BigInt(m));
          answer(box, `${ltr(all.toLocaleString("en-US"))} ${rem === 0 ? "מתחלק" : "לא מתחלק"} ב-${ltr(m)} (שארית ${ltr(rem)}), ושתי המכונות מסכימות : ${rem === 0 ? "שתיהן במצב 0" : `${ltr(`r = ${sm[N]}`)} ו-${ltr(`x = ${sl[N]}`)}, אף אחת לא במצב 0`}.`,
            box.querySelectorAll(".fs-node.is-cur"));
        } else answer(box, null);
      };
      const setNum = (ds) => { st.ds = ds; $(".dv-num").value = digitText(ds); $(".dv-err").textContent = ""; };
      const stop = autoplay(play, speed, { step: () => { st.k = Math.min(n(), st.k + 1); draw(); }, done: () => st.k >= n(), restart: () => { st.k = 0; draw(); } });
      $(".dv-num").addEventListener("change", () => {
        const ds = parse($(".dv-num").value, st.b);
        if (!ds) { $(".dv-err").textContent = `המספר : 1 עד ${MAXD} ספרות בבסיס ${st.b}`; return; }
        stop(); setNum(ds); st.k = 0; draw();
      });
      $(".dv-num").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".dv-num").blur(); });
      $(".dv-m").addEventListener("change", () => { stop(); st.m = Number($(".dv-m").value); st.k = 0; draw(); });
      $(".dv-b").addEventListener("change", () => {
        stop();
        const nb = Number($(".dv-b").value), v = big(st.ds, st.b);
        st.b = nb; setNum(toDigits(v, nb));
        if (gcd(st.m, nb) !== 1) st.m = 3;
        st.k = 0; draw();
      });
      $(".dv-add").addEventListener("click", (e) => {
        const push = e.target.closest(".dv-push"), pop = e.target.closest(".dv-pop");
        if (push && n() < MAXD) { stop(); setNum([...st.ds, Number(push.dataset.d)]); st.k = n(); draw(); }
        if (pop && n() > 1) { stop(); setNum(st.ds.slice(0, -1)); st.k = Math.min(st.k, n()); draw(); }
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
        stop(); Object.assign(st, { m: d0.m, b: d0.b, k: 0 }); setNum(parse(d0.num, d0.b) || [1, 0, 1, 1]); draw();
      });
      setNum(st.ds);
      draw();
    },
  });

  dvqExplorers.register({
    views: { divfsm: divfsmView },
    help: {
      divfsm: "אותו מספר נכנס לשתי מכונות : לזו מה-MSB מהספרה הגבוהה, ולזו מה-LSB מהנמוכה. בכל צעד כל מכונה קוראת עוד ספרה, והגרף מראה את המצב הנוכחי, את המעבר האחרון ואת המעברים שיוצאים ממנו. בוחרים m ובסיס (כמה ביטים במחזור), מקלידים מספר, מוסיפים ספרות בכפתורים או מגרילים. בסוף שתי המכונות מסכימות אם המספר מתחלק.",
    },
    models: { divInv, divTable, divRun },
  });
})();
