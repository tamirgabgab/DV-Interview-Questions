// kinds: frobenius
//   frobenius              0089        coins you cannot make up (data-coins, one to four coins of 1 to 20) in three modes: line (data-mode="line"), the amounts in rows of ten, payable or not, the largest one that is not framed and the run of min(coins) payable amounts after it; residues (data-mode="residues"), the amounts in columns by their remainder mod the smallest coin, Dijkstra settling one column a step, the first payable amount of each column and everything under it; pay (data-mode="pay", data-n), a typed amount paid with the coins (the first payable amount of its column and coins of the smallest one, and the fewest coins when that is fewer), or why it cannot be
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const RLM = "‏";
  const CMAX = 20, KMAX = 4, NMAX = 100000;

  // --- the models ------------------------------------------------------------------------------

  // the coins from the text field ("6, 9, 20", spaces or commas): one to four whole numbers
  // from 1 to 20, sorted, each once; null when the text is not that
  const fbParse = (text) => {
    const parts = String(text).split(/[\s,]+/).filter((t) => t !== "");
    if (!parts.length || parts.some((t) => !/^\d+$/.test(t))) return null;
    const c = [...new Set(parts.map(Number))].sort((x, y) => x - y);
    return c.length <= KMAX && c.every((v) => v >= 1 && v <= CMAX) ? c : null;
  };
  const gcd = (x, y) => (y ? gcd(y, x % y) : x);
  const fbGcd = (coins) => coins.reduce((g, c) => gcd(g, c), 0);
  // ok[n] for n = 0..upto
  const fbPayable = (coins, upto) => {
    const ok = [true];
    for (let n = 1; n <= upto; n++) ok.push(coins.some((c) => c <= n && ok[n - c]));
    return ok;
  };
  // Dijkstra on the remainders mod a = the smallest coin, ties to the smaller remainder (as
  // the page's heap of (dist, r) pairs): dist[r] the smallest payable amount with remainder r
  // (null when never), last[r] the coin added last, and the steps: the remainder settled and
  // the tentative distances right after it relaxed its coins.
  const fbApery = (coins) => {
    const a = coins[0];
    const dist = Array(a).fill(null), last = Array(a).fill(null), done = Array(a).fill(false), steps = [];
    dist[0] = 0;
    for (;;) {
      let r = -1;
      for (let i = 0; i < a; i++) if (!done[i] && dist[i] !== null && (r < 0 || dist[i] < dist[r])) r = i;
      if (r < 0) break;
      done[r] = true;
      for (const c of coins) {
        const nr = (r + c) % a, nd = dist[r] + c;
        if (dist[nr] === null || nd < dist[nr]) { dist[nr] = nd; last[nr] = c; }
      }
      steps.push({ r, d: dist[r], tent: dist.slice() });
    }
    return { dist, last, steps };
  };
  // the largest amount that cannot be paid; null when the gcd is more than 1, -1 when every
  // amount can be paid
  const fbFrob = (coins) => {
    if (fbGcd(coins) !== 1) return null;
    const { dist } = fbApery(coins);
    return Math.max(...dist) - coins[0];
  };
  // how to pay n: {ok, r, first, counts: [[coin, count], ...] largest coin first}, or
  // {ok: false, why, r, first} with why "gcd" (n is not a multiple of the gcd) or "below"
  // (n is under the first payable amount of its column, first); r is n mod the smallest coin
  const fbPay = (coins, n) => {
    const a = coins[0], { dist, last } = fbApery(coins), r = n % a;
    if (n % fbGcd(coins) !== 0) return { ok: false, why: "gcd", r, first: dist[r] };
    if (dist[r] === null || n < dist[r]) return { ok: false, why: "below", r, first: dist[r] };
    const cnt = new Map(coins.map((c) => [c, 0]));
    for (let s = r; dist[s] > 0; s = (s - last[s] % a + a) % a) cnt.set(last[s], cnt.get(last[s]) + 1);
    cnt.set(a, cnt.get(a) + (n - dist[r]) / a);
    return { ok: true, r, first: dist[r], counts: [...cnt].filter(([, k]) => k > 0).sort((x, y) => y[0] - x[0]) };
  };
  // the payment with the fewest coins: [[coin, count], ...] largest coin first (ties to the
  // larger coins), or null when n cannot be paid
  const fbFewest = (coins, n) => {
    const best = new Int32Array(n + 1).fill(-1), last = new Int32Array(n + 1);
    best[0] = 0;
    const desc = [...coins].reverse();
    for (let v = 1; v <= n; v++) {
      for (const c of desc) {
        if (c <= v && best[v - c] >= 0 && (best[v] < 0 || best[v - c] + 1 < best[v])) { best[v] = best[v - c] + 1; last[v] = c; }
      }
    }
    if (best[n] < 0) return null;
    const cnt = new Map();
    for (let v = n; v > 0; v -= last[v]) cnt.set(last[v], (cnt.get(last[v]) || 0) + 1);
    return [...cnt].sort((x, y) => y[0] - x[0]);
  };
  // the greedy payment, largest coin first: the coins and what is left (0 when it pays)
  const fbGreedy = (coins, n) => {
    let left = n;
    const out = [];
    for (const c of [...coins].reverse()) { const k = Math.floor(left / c); if (k) out.push([c, k]); left -= k * c; }
    return { counts: out, left };
  };

  // --- drawing -------------------------------------------------------------------------------------

  const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
  const coinsText = (coins) => coins.join(", ");
  const wrap = (label, rows, cls) =>
    `<div class="gs-scroll" tabindex="0" role="region" aria-label="${label}"><table class="gs-bits fb-tab ${cls}" dir="ltr" aria-label="${label}"><tbody>${rows.join("")}</tbody></table></div>`;
  const sumText = (counts) => counts.map(([c, k]) => (k === 1 ? `${c}` : `${k}·${c}`)).join(" + ");
  // how many coins of a are added to the head of the column
  const adds = (m, a) => (m === 0 ? "זה הראש עצמו." : m === 1 ? `מוסיפים מטבע אחד של ${ltr(a)}.` : `מוסיפים ${ltr(m)} מטבעות של ${ltr(a)}.`);
  // " (20 + 20 + 9)": the coins of an amount, in brackets, unless it is a single coin or 0
  const how2 = (coins, d) => {
    const p = fbPay(coins, d);
    return d && !(p.counts.length === 1 && p.counts[0][1] === 1) ? ` (${ltr(sumText(p.counts))})` : "";
  };
  const coinsField = (coins) =>
    `<label><span>המטבעות</span><input type="text" class="ex-num fb-coins" dir="ltr" spellcheck="false" autocomplete="off" value="${coinsText(coins)}" aria-label="המטבעות${NB}: אחד עד ארבעה ערכים מ-1 עד 20, מופרדים בפסיק"></label>`;

  // the shared start of every mode: the coins field with its error line and the reset button
  const setupCoins = (box, dflt, onChange) => {
    const $ = (sel) => box.querySelector(sel);
    $(".fb-coins").addEventListener("change", () => {
      const v = fbParse($(".fb-coins").value);
      if (!v) { $(".fb-err").textContent = `המטבעות${NB}: אחד עד ארבעה מספרים שלמים מ-1 עד 20`; return; }
      $(".fb-err").textContent = "";
      onChange(v);
    });
    $(".ex-reset").addEventListener("click", () => {
      $(".fb-err").textContent = "";
      $(".fb-coins").value = coinsText(dflt);
      onChange(dflt.slice(), true);
    });
  };
  const coinsOf = (box, dflt) => fbParse(box.dataset.coins || "") || dflt;

  // --- line: the amounts in rows of ten --------------------------------------------------------------

  const lineMount = (box) => {
    const c0 = coinsOf(box, [4, 7]);
    const st = { coins: c0.slice() };
    box.innerHTML =
      `<div class="ex-controls">${coinsField(c0)}` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err fb-err" role="status"></span></div>` +
      `<div class="fb-wrap"></div>` +
      `<span class="viz-legend">${key("fb-key-ok", "אפשר לשלם")}${key("fb-key-no", "אי אפשר לשלם")}${key("fb-key-g", "הגדול שאי אפשר")}${key("fb-key-run", "הרצף שאחריו")}</span>` +
      `<p class="ex-summary fb-sum" aria-live="polite"></p><p class="fb-note"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const coins = st.coins, a = coins[0], d = fbGcd(coins), g = fbFrob(coins);
      const upto = d === 1 ? Math.max(9, Math.ceil((g + a + 1) / 10) * 10 - 1) : 59;
      const ok = fbPayable(coins, upto);
      const rows = [`<tr><th></th>${Array.from({ length: 10 }, (_, u) => `<td class="fb-ix">${u}</td>`).join("")}</tr>`];
      for (let t = 0; t <= upto; t += 10) {
        let tds = "";
        for (let u = 0; u < 10; u++) {
          const n = t + u;
          let cls = ok[n] ? "fb-ok" : "fb-no";
          if (g !== null && n === g) cls += " fb-g";
          if (g !== null && ok[n] && n > g && n <= g + a) cls += " fb-run";
          tds += `<td class="gs-b ${cls}">${n}</td>`;
        }
        rows.push(`<tr><th>${t}</th>${tds}</tr>`);
      }
      $(".fb-coins").value = coinsText(coins);
      $(".fb-wrap").innerHTML = wrap(`הסכומים מ-0 עד ${upto} במטבעות ${coinsText(coins)}, ולכל סכום אם אפשר לשלם אותו`, rows, "fb-line");
      const bad = ok.reduce((k, v, n) => k + (!v && (g === null || n <= g) ? 1 : 0), 0);
      if (d !== 1) {
        $(".fb-sum").innerHTML = `ה-gcd של המטבעות הוא ${ltr(d)}${NB}: אפשר לשלם רק כפולות של ${ltr(d)}, ולכן יש אינסוף סכומים שאי אפשר, ואין גדול ביותר.`;
        $(".fb-note").innerHTML = "";
        answer(box, null);
        return;
      }
      if (g < 0) {
        $(".fb-sum").innerHTML = `יש מטבע של ${ltr(1)}${NB}: כל סכום אפשר לשלם.`;
        $(".fb-note").innerHTML = "";
        answer(box, `כל סכום אפשר לשלם.`);
        return;
      }
      $(".fb-sum").innerHTML = `הגדול שאי אפשר${NB}: ${ltr(g)}. אחריו ${ltr(a)} סכומים ברצף שאפשר (${ltr(`${g + 1}–${g + a}`)}), ומכאן כל סכום אפשרי. בסך הכול ${ltr(bad)} סכומים אי אפשר לשלם.`;
      $(".fb-note").innerHTML = coins.length === 2
        ? `שני מטבעות זרים${NB}: ${ltr(`ab − a − b = ${coins[0] * coins[1]} − ${coins[0]} − ${coins[1]} = ${coins[0] * coins[1] - coins[0] - coins[1]}`)}, ו-${ltr(`(a − 1)(b − 1)/2 = ${((coins[0] - 1) * (coins[1] - 1)) / 2}`)}.`
        : coins.length > 2 ? `לשלושה מטבעות ויותר אין נוסחה סגורה פשוטה. התשובה באה מהעמודות של סעיף ג.` : "";
      answer(box, `הסכום הגדול ביותר שאי אפשר לשלם במטבעות ${ltr(coinsText(coins))} הוא ${ltr(g)}.`, ".fb-wrap td.fb-g");
    };
    setupCoins(box, c0, (v) => { st.coins = v; draw(); });
    draw();
  };

  // --- residues: Dijkstra on the columns, one column a step ------------------------------------------

  const residuesMount = (box) => {
    const c0 = coinsOf(box, [6, 9, 20]);
    const st = { coins: c0.slice(), k: 0 };
    box.innerHTML =
      `<div class="ex-controls">${coinsField(c0)}` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err fb-err" role="status"></span></div>` +
      `<div class="ex-controls ex-play-row">` +
      `<button type="button" class="md-button ex-start">ההתחלה</button>` +
      `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
      `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
      `<button type="button" class="md-button ex-end">עד הסוף</button>` +
      `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1300, 700, 250) +
      `<span class="ex-pos"></span></div>` +
      `<div class="fb-wrap"></div>` +
      `<span class="viz-legend">${key("fb-key-first", "הראש של העמודה")}${key("fb-key-ok", "אפשר")}${key("fb-key-no", "אי אפשר")}${key("fb-key-tent", "הכי טוב עד עכשיו, עוד לא סגור")}${key("fb-key-g", "הגדול שאי אפשר")}</span>` +
      `<p class="ex-summary fb-sum" aria-live="polite"></p><p class="fb-note"></p>`;
    const $ = (sel) => box.querySelector(sel);
    let ap = fbApery(st.coins);
    const draw = () => {
      const coins = st.coins, a = coins[0], T = ap.steps.length;
      st.k = Math.min(Math.max(st.k, 0), T);
      const k = st.k, done = k === T;
      const settled = new Map(ap.steps.slice(0, k).map((s) => [s.r, s.d]));
      const tent = k ? ap.steps[k - 1].tent : [0].concat(Array(a - 1).fill(null));
      const top = Math.max(...ap.dist.filter((x) => x !== null));
      const R = Math.floor(top / a) + 2;
      const g = done ? fbFrob(coins) : null;
      const now = k ? ap.steps[k - 1].r : -1;
      $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
      $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
      $(".ex-next").disabled = $(".ex-end").disabled = done;
      $(".fb-coins").value = coinsText(coins);
      const head = `<tr><th>r</th>${Array.from({ length: a }, (_, r) => `<td class="fb-ix${r === now ? " fb-nowix" : ""}">${r}</td>`).join("")}</tr>`;
      const rows = [head];
      for (let m = 0; m < R; m++) {
        let tds = "";
        for (let r = 0; r < a; r++) {
          const n = r + a * m;
          let cls;
          if (settled.has(r)) {
            const d0 = settled.get(r);
            cls = n < d0 ? "fb-no" : n === d0 ? `fb-ok fb-first${r === now ? " fb-now" : ""}` : "fb-ok";
            if (g !== null && n === g) cls += " fb-g";
          } else if (done) cls = "fb-no";      // never reached: the gcd is more than 1
          else cls = tent[r] === n ? "fb-unk fb-tent" : "fb-unk";
          tds += `<td class="gs-b ${cls}">${n}</td>`;
        }
        rows.push(`<tr><th></th>${tds}</tr>`);
      }
      $(".fb-wrap").innerHTML = wrap(`הסכומים במטבעות ${coinsText(coins)} בעמודות לפי השארית בחלוקה ל-${a}, אחרי ${k} צעדים של Dijkstra`, rows, "fb-res");
      let note;
      if (!k) note = `ההתחלה${NB}: בעמודה ${ltr(0)} הראש הוא ${ltr(0)}, בלי מטבעות. כל צעד סוגר את העמודה הפתוחה שהמרחק אליה הכי קטן.`;
      else {
        const s = ap.steps[k - 1];
        note = `צעד ${ltr(k)}${NB}: שארית ${ltr(s.r)} נסגרת בסכום ${ltr(s.d)}${how2(coins, s.d)}` +
          `. מכאן ${ltr(`${s.d}, ${s.d + a}, ${s.d + 2 * a}, …`)} אפשר, ומה שמעליו בעמודה אי אפשר. מטבע ${ltr("c")} מנסה לשפר את העמודה ${ltr(`(${s.r} + c) mod ${a}`)}.`;
      }
      $(".fb-note").innerHTML = note;
      const gg = fbFrob(coins);
      if (!done) {
        $(".fb-sum").innerHTML = `נסגרו ${ltr(k)} מתוך ${ltr(a)} העמודות.`;
        answer(box, null);
      } else if (gg === null) {
        $(".fb-sum").innerHTML = `לחלק מהעמודות אי אפשר להגיע${NB}: ה-gcd של המטבעות הוא ${ltr(fbGcd(coins))}, ויש אינסוף סכומים שאי אפשר לשלם.`;
        answer(box, null);
      } else {
        const rr = ap.dist.indexOf(top);
        $(".fb-sum").innerHTML = gg < 0 ? `יש מטבע של ${ltr(1)}${NB}: כל סכום אפשר.`
          : `הראש הגבוה${NB}: ${ltr(top)} בעמודה ${ltr(rr)}. מעליו ${ltr(`${top} − ${a} = ${gg}`)}, הסכום הגדול ביותר שאי אפשר לשלם.`;
        answer(box, gg < 0 ? "כל סכום אפשר לשלם." : `הסכום הגדול ביותר שאי אפשר לשלם במטבעות ${ltr(coinsText(coins))} הוא ${ltr(gg)}.`, ".fb-wrap td.fb-g");
      }
    };
    const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= ap.steps.length, restart: () => { st.k = 0; draw(); } });
    setupCoins(box, c0, (v) => { stop(); st.coins = v; ap = fbApery(v); st.k = 0; draw(); });
    $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
    $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
    $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
    $(".ex-end").addEventListener("click", () => { stop(); st.k = ap.steps.length; draw(); });
    draw();
  };

  // --- pay: a typed amount --------------------------------------------------------------------------

  const payMount = (box) => {
    const c0 = coinsOf(box, [6, 9, 20]);
    const nIn = Number(box.dataset.n);
    const n0 = Number.isInteger(nIn) && nIn >= 0 && nIn <= NMAX ? nIn : 43;
    const st = { coins: c0.slice(), n: n0 };
    box.innerHTML =
      `<div class="ex-controls">${coinsField(c0)}` +
      `<label><span>הסכום</span><input type="text" inputmode="numeric" class="ex-num fb-n" dir="ltr" spellcheck="false" autocomplete="off" value="${n0}" aria-label="הסכום לתשלום${NB}: מספר שלם מ-0 עד ${NMAX}"></label>` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err fb-err" role="status"></span></div>` +
      `<div class="fb-wrap"></div>` +
      `<span class="viz-legend">${key("fb-key-first", "הראש של העמודה")}${key("fb-key-ok", "אפשר")}${key("fb-key-no", "אי אפשר")}${key("fb-key-pick", "הסכום שהוקלד")}</span>` +
      `<p class="ex-summary fb-sum" aria-live="polite"></p><p class="fb-note"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const { coins, n } = st, a = coins[0], p = fbPay(coins, n), { dist } = fbApery(coins), r = n % a;
      $(".fb-coins").value = coinsText(coins);
      if (document.activeElement !== $(".fb-n")) $(".fb-n").value = String(n);
      // the column of n: twelve amounts of remainder r around n and the column's head
      const head = dist[r];
      const end = Math.max(n, head === null ? n : head) + a;
      let lo = Math.max(r, end - 11 * a);
      if (head !== null && head < lo && head >= end - 15 * a) lo = Math.max(r, head - a);
      const cells = [];
      for (let v = lo; v <= end && cells.length < 16; v += a) {
        let cls = head !== null && v >= head ? "fb-ok" : "fb-no";
        if (v === head) cls += " fb-first";
        if (v === n) cls += " fb-pick";
        cells.push(`<td class="gs-b ${cls}">${v}</td>`);
      }
      $(".fb-wrap").innerHTML = wrap(`העמודה של השארית ${r} בחלוקה ל-${a}, סביב הסכום ${n}`, [`<tr><th>${r} mod ${a}</th>${cells.join("")}</tr>`], "fb-col");
      let sum, note = "";
      if (p.ok) {
        sum = `${RLM}${ltr(`${n} = ${n ? sumText(p.counts) : "0"}`)}.`;
        note = n ? `הסכום בעמודה של שארית ${ltr(r)}, שהראש שלה ${ltr(p.first)}${how2(coins, p.first)}. ${adds((n - p.first) / a, a)}` : "סכום 0, בלי מטבעות.";
        const few = n ? fbFewest(coins, n) : null, many = (cs) => cs.reduce((s, [, k]) => s + k, 0);
        if (few && many(few) < many(p.counts)) note += ` זו דרך אחת. הכי מעט מטבעות${NB}: ${ltr(sumText(few))}, ${ltr(many(few))} מטבעות.`;
        const gr = fbGreedy(coins, n);
        if (gr.left) note += ` החמדן, שמתחיל במטבע הגדול, היה נתקע${NB}: ${ltr(gr.counts.length ? `${sumText(gr.counts)}` : "0")} ונשארים ${ltr(gr.left)}.`;
        answer(box, `את ${ltr(n)} אפשר לשלם${NB}: ${ltr(n ? sumText(p.counts) : "0")}.`, ".fb-wrap td.fb-pick");
      } else if (p.why === "gcd") {
        sum = `את ${ltr(n)} אי אפשר לשלם.`;
        note = `כל סכום שמשלמים הוא כפולה של ה-gcd של המטבעות, ${ltr(fbGcd(coins))}, ו-${ltr(n)} לא כפולה שלו.`;
        answer(box, null);
      } else {
        sum = `את ${ltr(n)} אי אפשר לשלם.`;
        note = head === null ? `לעמודה של שארית ${ltr(r)} אי אפשר להגיע בכלל.`
          : `הסכום בעמודה של שארית ${ltr(r)}, שהראש שלה ${ltr(head)}${how2(coins, head)}. כל סכום בעמודה שקטן מהראש אי אפשר לשלם.`;
        answer(box, null);
      }
      $(".fb-sum").innerHTML = sum;
      $(".fb-note").innerHTML = note;
    };
    setupCoins(box, c0, (v, reset) => { st.coins = v; if (reset) { st.n = n0; $(".fb-n").value = String(n0); } draw(); });
    $(".fb-n").addEventListener("change", () => {
      const t = $(".fb-n").value.trim(), v = Number(t);
      if (!/^\d+$/.test(t) || v > NMAX) { $(".fb-err").textContent = `הסכום${NB}: מספר שלם מ-0 עד ${NMAX}`; return; }
      $(".fb-err").textContent = "";
      st.n = v;
      draw();
    });
    draw();
  };

  const frobeniusView = () => ({
    mount(box) {
      const mode = box.dataset.mode;
      if (mode === "residues") residuesMount(box);
      else if (mode === "pay") payMount(box);
      else lineMount(box);
    },
  });

  dvqExplorers.register({
    views: { frobenius: frobeniusView },
    help: {
      frobenius: "שלושה מצבים. בכולם מקלידים את המטבעות, אחד עד ארבעה ערכים מ-1 עד 20, ומאשרים ב-Enter. בציר הסכומים כל סכום צבוע לפי אם אפשר לשלם אותו, והגדול שאי אפשר ממוסגר. בעמודות כל צעד הוא צעד של Dijkstra : עמודה אחת נסגרת, הראש שלה מתגלה, וכל מה שמתחתיו נצבע. בתשלום מקלידים סכום, ורואים איך לשלם אותו, או למה אי אפשר.",
    },
    models: { fbParse, fbGcd, fbPayable, fbApery, fbFrob, fbPay, fbFewest, fbGreedy },
  });
})();
