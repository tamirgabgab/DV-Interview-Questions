// kinds: randmn
//   randmn                 0078        randN from randM by rejection: M, N and the calls k a round chosen; the round's M^k outcomes as a grid tinted by the output (the rejected ones dashed), L, the expected calls k M^k / L for four values of k (the cheapest marked), whether an exact algorithm with a bounded number of calls exists (every prime of N divides M), and ten seeded rounds stepped one by one (the calls, v, accepted or not, the output)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, mulberry32, seedControls, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MMIN = 2, MMAX = 10, NMIN = 2, NMAX = 40, KMORE = 3, ROUNDS = 10, DRAW_MAX = 400;

  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  // the fewest calls k with M^k >= N
  const rnCalls = (m, n) => { let k = 1, size = m; while (size < n) { k++; size *= m; } return k; };
  // L: the largest multiple of N not above M^k (the accepted v are 0 .. L - 1)
  const rnLimit = (m, n, k) => { const size = m ** k; return size - (size % n); };
  // the expected calls k M^k / L as a reduced fraction [numerator, denominator]
  const rnExpected = (m, n, k) => { const a = k * m ** k, b = rnLimit(m, n, k), g = gcd(a, b); return [a / g, b / g]; };
  const rnFactors = (n) => { const out = []; for (let p = 2; p * p <= n; p++) if (n % p === 0) { out.push(p); while (n % p === 0) n /= p; } if (n > 1) out.push(n); return out; };
  // the fewest k with N | M^k (k calls give randN exactly, no rejection), 0 when none
  const rnExact = (m, n) => { let power = 1; for (let k = 1; k <= n.toString(2).length; k++) { power = (power * m) % n; if (power === 0) return k; } return 0; };
  // a round: the calls a_1 .. a_k (1..M) as base-M digits, v, accepted, the output
  const rnRound = (m, n, k, calls) => {
    const v = calls.reduce((acc, a) => m * acc + a - 1, 0), ok = v < rnLimit(m, n, k);
    return { calls, v, ok, out: ok ? (v % n) + 1 : 0 };
  };
  // ROUNDS rounds from a seed: every call is 1 + floor(M rnd)
  const rnRun = (m, n, k, seed, rounds = ROUNDS) => {
    const rnd = mulberry32(seed), out = [];
    for (let r = 0; r < rounds; r++) out.push(rnRound(m, n, k, Array.from({ length: k }, () => 1 + Math.floor(rnd() * m))));
    return out;
  };
  // the grid of a round's outcomes: the first floor(k/2) calls choose the row, the others the column
  const rnShape = (m, k) => ({ rows: m ** Math.floor(k / 2), cols: m ** Math.ceil(k / 2) });

  const frac = ([a, b]) => (b === 1 ? `${a}` : `${a}/${b}`);
  const dec = ([a, b]) => (a / b).toFixed(2);
  const both = (e) => (e[1] === 1 ? frac(e) : `${frac(e)} ≈ ${dec(e)}`);
  const sup = (b, e) => `${b}<sup>${e}</sup>`;

  const randmnView = () => ({
    mount(box) {
      const clamp = (v, lo, hi, d) => { const x = Math.floor(Number(v)); return Number.isFinite(x) ? Math.min(hi, Math.max(lo, x)) : d; };
      const M0 = clamp(box.dataset.m, MMIN, MMAX, 5), N0 = clamp(box.dataset.n, NMIN, NMAX, 7), SEED0 = clamp(box.dataset.seed, 1, 99999, 7);
      const st = { m: M0, n: N0, k: rnCalls(M0, N0), s: 0, seed: SEED0, run: [] };
      const slider = (cls, label, aria, min, max) =>
        `<label class="rn-lab"><span>${label}</span><input type="range" class="${cls}" min="${min}" max="${max}" step="1" dir="ltr" aria-label="${aria}"><output class="${cls}o"></output></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        slider("rn-m", `המקור ${ltr("M")}`, "M, הטווח של המקור randM", MMIN, MMAX) +
        slider("rn-n", `היעד ${ltr("N")}`, "N, הטווח של היעד randN", NMIN, NMAX) +
        slider("rn-k", `קריאות בסבב ${ltr("k")}`, "k, מספר הקריאות בכל סבב", 1, 4) +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני הסבב הראשון</button>` +
        `<button type="button" class="md-button ex-prev">הסבב הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הסבב הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הסבבים</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1500, 900, 450) +
        `<span class="ex-pos"></span>` +
        `<button type="button" class="md-button rn-new">הגרלה חדשה</button></div>` +
        `<p class="ex-summary rn-sum" aria-live="polite"></p>` +
        `<p class="rn-bound"></p>` +
        `<p class="ex-title">התוחלת לפי מספר הקריאות בסבב (✓ הכי זול)</p>` +
        `<div class="gs-scroll rn-ktab" tabindex="0" role="region" aria-label="התוחלת לפי k"></div>` +
        `<p class="ex-title rn-grid-title"></p>` +
        `<div class="gs-scroll rn-gridwrap" tabindex="0" role="region" aria-label="כל התוצאות של סבב"></div>` +
        `<span class="viz-legend"><span><i class="rn-key-t1"></i>תא שמתקבל, הצבע והמספר לפי הפלט</span><span><i class="rn-key-rej"></i>נדחה</span><span><i class="rn-key-now"></i>התא של הסבב הנוכחי</span></span>` +
        `<p class="ex-title">עשרה סבבים</p>` +
        `<div class="gs-scroll rn-log" tabindex="0" role="region" aria-label="הסבבים עד עכשיו"></div>` +
        `<p class="rn-now"></p>`;
      const $ = (s) => box.querySelector(s);
      const play = $(".ex-play"), speed = $(".ex-speed");

      const kTable = () => {
        const k0 = rnCalls(st.m, st.n), ks = Array.from({ length: KMORE + 1 }, (_, i) => k0 + i);
        const es = ks.map((k) => rnExpected(st.m, st.n, k)), best = ks[es.reduce((b, e, i) => (e[0] * es[b][1] < es[b][0] * e[1] ? i : b), 0)];
        return `<table class="rn-tab" aria-label="התוחלת לפי k"><thead><tr><th>${ltr("k")}</th><th>${ltr(sup("M", "k"))}</th><th>${ltr("L")}</th><th>נדחים</th><th>תוחלת הקריאות</th></tr></thead><tbody>` +
          ks.map((k, i) => {
            const size = st.m ** k, L = rnLimit(st.m, st.n, k);
            return `<tr class="${k === st.k ? "is-now" : ""}${k === best ? " is-best" : ""}"><td>${ltr(k)}</td><td>${ltr(size)}</td><td>${ltr(L)}</td><td>${ltr(size - L)}</td>` +
              `<td>${ltr(both(es[i]))}${k === best ? " ✓" : ""}</td></tr>`;
          }).join("") + `</tbody></table>`;
      };
      const grid = (cur) => {
        const size = st.m ** st.k;
        if (size > DRAW_MAX) return `<p class="rn-big">${ltr(`${sup(st.m, st.k)} = ${size}`)} תוצאות, יותר מדי לציור. הספירה למעלה והסבבים למטה עדיין נכונים.</p>`;
        const { rows, cols } = rnShape(st.m, st.k), L = rnLimit(st.m, st.n, st.k);
        let t = `<table class="rn-grid rn-live" dir="ltr" aria-label="${size} התוצאות של סבב, ${L} מתקבלות"><tbody>`;
        for (let r = 0; r < rows; r++) {
          t += "<tr>";
          for (let c = 0; c < cols; c++) {
            const v = r * cols + c, ok = v < L, out = (v % st.n) + 1;
            t += `<td class="rn-c ${ok ? `rn-t${((out - 1) % 7) + 1}` : "rn-rej"}${cur && cur.v === v ? " is-now" : ""}" title="v = ${v}">${ok ? out : "✗"}</td>`;
          }
          t += "</tr>";
        }
        return t + "</tbody></table>";
      };
      const log = () => {
        let calls = 0, outs = 0;
        let t = `<table class="rn-tab" aria-label="הסבבים"><thead><tr><th>סבב</th><th>הקריאות</th><th>${ltr("v")}</th><th>התוצאה</th><th>סך הקריאות</th></tr></thead><tbody>`;
        st.run.forEach((r, i) => {
          const on = i < st.s;
          if (on) { calls += st.k; if (r.ok) outs++; }
          const v = (x) => (on ? x : " ");
          t += `<tr class="${i === st.s - 1 ? "is-now" : ""}${on ? "" : " is-later"}"><td>${i + 1}</td><td>${v(ltr(r.calls.join(", ")))}</td><td>${v(ltr(r.v))}</td>` +
            `<td>${on ? (r.ok ? `פלט <strong>${ltr(r.out)}</strong>` : "נדחה") : " "}</td><td>${v(ltr(calls))}</td></tr>`;
        });
        return { html: t + `</tbody></table>`, calls, outs };
      };
      const draw = () => {
        const m = st.m, n = st.n, k = st.k, k0 = rnCalls(m, n), size = m ** k, L = rnLimit(m, n, k), e = rnExpected(m, n, k);
        st.s = Math.min(Math.max(st.s, 0), ROUNDS);
        const cur = st.s ? st.run[st.s - 1] : null;
        [["m", m], ["n", n], ["k", k]].forEach(([c, v]) => { $(`.rn-${c}`).value = String(v); $(`.rn-${c}o`).textContent = String(v); });
        $(".rn-k").min = String(k0); $(".rn-k").max = String(k0 + KMORE); $(".rn-k").value = String(k);
        $(".ex-pos").textContent = `סבב ${st.s} מתוך ${ROUNDS}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.s === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.s === ROUNDS;
        $(".rn-sum").innerHTML = `בכל סבב ${ltr(`k = ${k}`)} קריאות, ולכן ${ltr(`${sup(m, k)} = ${size}`)} תוצאות שוות הסתברות, ${ltr(`v = 0 … ${size - 1}`)}. ` +
          `מתקבלות ${ltr(`L = ${L}`)}, ${ltr(L / n)} לכל פלט, ונדחות ${ltr(size - L)}. ` +
          `<b>תוחלת${NB}: ${ltr(`k · ${sup("M", "k")} / L = ${both(e)}`)} קריאות.</b>`;
        const ex = rnExact(m, n), ps = rnFactors(n), bad = ps.filter((p) => m % p);
        $(".rn-bound").innerHTML = `סעיף ג${NB}: הגורמים הראשוניים של ${ltr(`N = ${n}`)} הם ${ltr(ps.join(", "))}. ` + (ex
          ? `כולם מחלקים את ${ltr(`M = ${m}`)}, ולכן יש אלגוריתם מדויק בלי דחייה${NB}: ${ltr(ex)} קריאות, כי ${ltr(`${sup(m, ex)} = ${m ** ex} = ${m ** ex / n} · ${n}`)}.`
          : `${ltr(bad.join(", "))} לא ${bad.length > 1 ? "מחלקים" : "מחלק"} את ${ltr(`M = ${m}`)}, ולכן אין אלגוריתם מדויק עם מספר קריאות חסום.`);
        $(".rn-ktab").innerHTML = kTable();
        $(".rn-grid-title").innerHTML = `כל ${ltr(size)} התוצאות של סבב${size <= DRAW_MAX ? `${NB}: ${gridHow(k)}` : ""}`;
        $(".rn-gridwrap").innerHTML = grid(cur);
        const lg = log();
        $(".rn-log").innerHTML = lg.html;
        let now;
        if (!cur) now = `עוד לא הוגרל סבב. בכל סבב קוראים ${ltr(k)} ${k > 1 ? "פעמים" : "פעם"} ל-${ltr(`rand${m}`)}, והקריאות הן הספרות של ${ltr("v")} בבסיס ${ltr(m)}.`;
        else {
          const digits = cur.calls.map((a, i) => `${a - 1}·${sup(m, k - 1 - i)}`).join(" + ");
          now = `סבב ${st.s}${NB}: הקריאות ${ltr(cur.calls.join(", "))}, ולכן ${ltr(`v = ${digits} = ${cur.v}`)}. ` +
            (cur.ok ? `${ltr(`${cur.v} < ${L}`)}, מתקבל${NB}: הפלט ${ltr(`${cur.v} mod ${n} + 1 = ${cur.out}`)}.` : `${ltr(`${cur.v} ≥ ${L}`)}, נדחה${NB}: זורקים את כל ${ltr(k)} הקריאות ומגרילים סבב חדש.`);
        }
        $(".rn-now").innerHTML = now;
        if (st.s === ROUNDS) {
          const per = lg.outs ? (lg.calls / lg.outs).toFixed(2) : "—";
          answer(box, `${ltr(ROUNDS)} סבבים, ${ltr(lg.calls)} קריאות ו-${ltr(lg.outs)} פלטים${NB}: ${ltr(per)} קריאות לפלט בריצה הזו, מול תוחלת של ${ltr(dec(e))}.`, ".rn-log tbody");
        } else answer(box, null);
      };
      // how the grid is laid out: the first floor(k/2) calls choose the row, the others the column
      function gridHow(k) {
        if (k === 1) return "תא לכל ערך של הקריאה";
        if (k === 2) return "שורה לכל ערך של הקריאה הראשונה, ועמודה לכל ערך של השנייה";
        const r = Math.floor(k / 2);
        return `${r > 1 ? `שורה לכל צירוף של ${ltr(r)} הקריאות הראשונות` : "שורה לכל ערך של הקריאה הראשונה"}, ועמודה לכל צירוף של ${ltr(k - r)} האחרות`;
      }

      const rerun = () => { st.run = rnRun(st.m, st.n, st.k, st.seed); };
      const stop = autoplay(play, speed, { step: () => { st.s++; draw(); }, done: () => st.s >= ROUNDS, restart: () => { st.s = 0; draw(); } });
      const restart = () => { stop(); st.s = 0; rerun(); draw(); };
      // a seeded run: the same seed replays the same calls (a slider redraws from it)
      const seed = seedControls(box, $(".rn-new"), (rng, sd) => { st.seed = sd; restart(); }, { fresh: false });
      $(".rn-new").addEventListener("click", () => seed.draw());
      $(".rn-m").addEventListener("input", () => { st.m = Number($(".rn-m").value); st.k = rnCalls(st.m, st.n); restart(); });
      $(".rn-n").addEventListener("input", () => { st.n = Number($(".rn-n").value); st.k = rnCalls(st.m, st.n); restart(); });
      $(".rn-k").addEventListener("input", () => { st.k = Number($(".rn-k").value); restart(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.s = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.s--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.s++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.s = ROUNDS; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, { m: M0, n: N0, k: rnCalls(M0, N0) }); box.dvqSeed.runSeed(SEED0); });
      box.dvqSeed.runSeed(SEED0);
    },
  });

  dvqExplorers.register({
    views: { randmn: randmnView },
    help: {
      randmn: "בוחרים את המקור M, את היעד N ואת מספר הקריאות בסבב k. למעלה החשבון של סבב (כמה תוצאות, כמה מתקבלות, התוחלת), טבלה של ארבעה ערכים של k עם הזול מסומן, והאם יש אלגוריתם מדויק עם מספר קריאות חסום. הטבלה הצבועה היא כל התוצאות של סבב, כל תא עם הפלט שלו, והנדחים מקווקווים. הצעדים מריצים עשרה סבבים אקראיים, סבב בכל צעד, והגרלה חדשה מחליפה אותם.",
    },
    models: { rnCalls, rnLimit, rnExpected, rnFactors, rnExact, rnRound, rnRun, rnShape },
    // on a computer: the table of k and the grid of one round on the left, the ten rounds
    // (a row a step) and the current round's line on the right; the bound stays above both
    cols: { randmn: { main: ".rn-ktab, .rn-gridwrap, .viz-legend, .ex-title:not(:has(+ .rn-log))", side: ".rn-log, .ex-title:has(+ .rn-log), .rn-now" } },
  });
})();
