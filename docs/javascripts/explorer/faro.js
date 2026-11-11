// kinds: faro
//   faro                   0073        a deck of n cards (2 to 100) shuffled perfectly (out or in) one shuffle per step, the cards tinted by the cycle of their place and one cycle outlined on demand, until the deck is back; the modulus M, the order of 2 mod M and the cycle lengths beside it
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const PER = 13;

  // One perfect shuffle, top card first: out keeps the top card on top (an odd deck's top
  // half is the larger one), in puts it second.
  const faroShuffle = (deck, kind) => {
    const n = deck.length, h = kind === "out" ? Math.ceil(n / 2) : Math.floor(n / 2);
    const top = deck.slice(0, h), bottom = deck.slice(h);
    const [first, second] = kind === "out" ? [top, bottom] : [bottom, top];
    const out = [];
    first.forEach((c, i) => { out.push(c); if (i < second.length) out.push(second[i]); });
    return out;
  };
  const faroOrder = (n, kind) => {
    const deck = Array.from({ length: n }, (_, i) => i);
    let cur = faroShuffle(deck, kind), t = 1;
    while (cur.some((c, i) => c !== i)) { cur = faroShuffle(cur, kind); t++; }
    return t;
  };
  // The cycles of the places under one shuffle, each from its smallest place.
  const faroCycles = (n, kind) => {
    const after = faroShuffle(Array.from({ length: n }, (_, i) => i), kind), where = new Map();
    after.forEach((c, p) => where.set(c, p));
    const seen = new Set(), out = [];
    for (let s = 0; s < n; s++) {
      if (seen.has(s)) continue;
      const cyc = [];
      for (let p = s; !seen.has(p); p = where.get(p)) { seen.add(p); cyc.push(p); }
      out.push(cyc);
    }
    return out;
  };
  const modulus = (n, kind) => (n % 2 ? n : kind === "out" ? n - 1 : n + 1);
  const MAXN = 100;
  const pow2 = (t) => `2<sup>${t}</sup>`;
  const pow2mod = (t, m) => { let v = 1 % m; for (let i = 0; i < t; i++) v = (2 * v) % m; return v; };   // exact past 2^53

  const KINDS = { out: "out-shuffle, העליון נשאר למעלה", in: "in-shuffle, העליון יורד למקום השני" };

  const faroView = () => ({
    mount(box) {
      const d0 = { n: Math.min(MAXN, Math.max(2, Number(box.dataset.n || 8))), kind: box.dataset.shuffle === "in" ? "in" : "out" };
      const st = { ...d0, t: 0, mark: -1 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>קלפים ${ltr("n")}</span><input type="range" class="fa-n" min="2" max="${MAXN}" step="1" dir="ltr" aria-label="מספר הקלפים"><output class="fa-no"></output></label>` +
        `<label>הערבוב <select class="fa-kind" aria-label="סוג הערבוב">${Object.entries(KINDS).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label>סימון <select class="fa-cyc" aria-label="מעגל למסגר"></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">החפיסה המקורית</button>` +
        `<button type="button" class="md-button ex-prev">ערבוב אחד אחורה</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">ערבוב</button>` +
        `<button type="button" class="md-button ex-end">עד שהיא חוזרת</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary fa-sum" aria-live="polite"></p>` +
        `<div class="fa-fig" data-steady></div>` +
        `<span class="viz-legend"><span><i class="pm-key-c1"></i>הצבע : המעגל של המקום המקורי (חמישה צבעים, חוזרים)</span><span><i class="fa-key-mark"></i>המעגל שבחרתם בסימון</span><span><i class="pm-key-hl"></i>קלף שחזר למקומו</span></span>` +
        `<p class="fa-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const order = () => faroOrder(st.n, st.kind);

      const draw = () => {
        const n = st.n, e = order();
        st.t = Math.min(Math.max(st.t, 0), e);
        let deck = Array.from({ length: n }, (_, i) => i);
        for (let i = 0; i < st.t; i++) deck = faroShuffle(deck, st.kind);
        const cycles = faroCycles(n, st.kind), cyc = new Map();
        cycles.forEach((c, ci) => c.forEach((p) => cyc.set(p, ci)));
        // the cycle select: one option per cycle that moves, named by its first place
        const opts = `<option value="-1">בלי</option>` + cycles.map((c, ci) => (c.length > 1 ? `<option value="${ci}">המעגל של ${c[0]} (${c.length} מקומות)</option>` : "")).join("");
        if ($(".fa-cyc").dataset.opts !== opts) { $(".fa-cyc").innerHTML = opts; $(".fa-cyc").dataset.opts = opts; }
        if (!(st.mark >= 0 && st.mark < cycles.length && cycles[st.mark].length > 1)) st.mark = -1;
        $(".fa-cyc").value = String(st.mark);
        $(".fa-n").value = String(n); $(".fa-no").textContent = String(n);
        $(".fa-kind").value = st.kind;
        $(".ex-pos").textContent = `ערבוב ${st.t} מתוך ${e}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.t === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.t === e;
        // the deck in rows of 13, top first; a card's tint is the cycle of its own first place
        let rows = "";
        for (let r = 0; r * PER < n; r++) {
          const cells = deck.slice(r * PER, r * PER + PER).map((c, j) => {
            const p = r * PER + j, ci = cyc.get(c), fixed = cycles[ci].length === 1;
            return `<td class="pm-c ${fixed ? "is-off" : `c${(ci % 5) + 1}`}${ci === st.mark ? " fa-mark" : ""}${st.t && c === p ? " is-hl" : ""}">${c}</td>`;
          }).join("");
          rows += `<tr><th>${r * PER}</th>${cells}</tr>`;
        }
        $(".fa-fig").innerHTML = `<div class="pm-scroll" tabindex="0" role="region" aria-label="החפיסה אחרי ${st.t} ערבובים, מלמעלה"><table class="pm-cells fa-cells" dir="ltr"><tbody>${rows}</tbody></table></div>`;
        const M = modulus(n, st.kind), lens = cycles.map((c) => c.length).filter((l) => l > 1);
        // the map of one shuffle: 0-based for out (an even deck keeps its bottom card, an odd
        // one its top card, inside the formula), 1-based for in (an odd deck keeps its bottom card)
        const odd = n % 2 === 1, out = st.kind === "out";
        const rule = out ? `${ltr(`p → 2p mod ${M}`)} (ממספרים מ-0${odd ? "" : ", הקלף התחתון לא זז"})`
          : `${ltr(`q → 2q mod ${M}`)} (ממספרים מ-1${odd ? ", הקלף התחתון לא זז" : ""})`;
        const where = out ? ltr(`${pow2("t")} · p mod ${M}`) : ltr(`${pow2("t")} · (p + 1) mod ${M} − 1`);
        const bottom = (out && !odd) || (!out && odd) ? " (חוץ מהקלף התחתון)" : "";
        if (M === 1) {
          $(".fa-sum").innerHTML = `${ltr("M = 1")}${NB}: הערבוב לא מזיז אף קלף, ${ltr("e = 1")}.`;
        } else {
          $(".fa-sum").innerHTML = `${ltr(`M = ${M}`)}${NB}: כל ערבוב הוא ${rule}. ` +
            `<b>הסדר של 2 מודולו ${ltr(M)} הוא ${ltr(e)}</b>${NB}: ${ltr(`${pow2(e)} mod ${M} = 1`)}. ` +
            `המעגלים באורכים ${ltr([...new Set(lens)].sort((a, b) => a - b).join(", "))}, וכולם חוזרים יחד אחרי ${ltr(e)}.`;
        }
        const home = deck.filter((c, p) => c === p).length;
        $(".fa-note").innerHTML = M === 1
          ? (st.t === 0 ? "החפיסה בסדר המקורי, וערבוב של שני קלפים משאיר אותה כך." : `אחרי ערבוב אחד${NB}: שני הקלפים במקומם.`)
          : st.t === 0
          ? `החפיסה בסדר המקורי. הקלף במקום ${ltr("p")} נמצא אחרי ${ltr("t")} ערבובים במקום ${where}${bottom}.`
          : `אחרי ${ltr(st.t)} ערבובים${NB}: ${ltr(home)} מתוך ${ltr(n)} קלפים במקומם. ${ltr(`${pow2(st.t)} mod ${M} = ${pow2mod(st.t, M)}`)}.`;
        if (st.t === e) answer(box, M === 1 ? "החפיסה חזרה אחרי ערבוב אחד, כי ערבוב של שני קלפים לא מזיז אותם." : `החפיסה חזרה אחרי ${ltr(e)} ערבובים, הסדר של 2 מודולו ${ltr(M)}.`, ".fa-cells .is-hl");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.t++; draw(); }, done: () => st.t >= order(), restart: () => { st.t = 0; draw(); } });
      const restart = () => { stop(); st.t = 0; draw(); };
      $(".fa-n").addEventListener("input", () => { st.n = Number($(".fa-n").value); st.mark = -1; restart(); });
      $(".fa-kind").addEventListener("change", () => { st.kind = $(".fa-kind").value; st.mark = -1; restart(); });
      $(".fa-cyc").addEventListener("change", () => { st.mark = Number($(".fa-cyc").value); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.t = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.t--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.t++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.t = order(); draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, d0); restart(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { faro: faroView },
    help: {
      faro: "בוחרים מספר קלפים (עד 100) וסוג ערבוב, ומערבבים צעד אחרי צעד. כל קלף צבוע לפי המעגל של המקום המקורי שלו (חמישה צבעים, שחוזרים כשיש יותר מעגלים), קלף שלא זז מסומן בקו מקווקו, וקלף שחזר למקומו ממוסגר. ״סימון״ ממסגר את כל הקלפים של מעגל אחד. ״עד שהיא חוזרת״ קופץ למספר הערבובים, הסדר של 2 מודולו M.",
    },
    models: { faroShuffle, faroOrder, faroCycles, pow2mod },
  });
})();
