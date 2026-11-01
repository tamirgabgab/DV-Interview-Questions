// kinds: faro
//   faro                   0073        a deck of n cards shuffled perfectly (out or in) one shuffle per step, the cards tinted by the cycle of their place, until the deck is back; the modulus M, the order of 2 mod M and the cycle lengths beside it
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
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

  const KINDS = { out: "out-shuffle, העליון נשאר למעלה", in: "in-shuffle, העליון יורד למקום השני" };

  const faroView = () => ({
    mount(box) {
      const d0 = { n: Math.min(52, Math.max(2, Number(box.dataset.n || 8))), kind: box.dataset.shuffle === "in" ? "in" : "out" };
      const st = { ...d0, t: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>קלפים ${ltr("n")}</span><input type="range" class="fa-n" min="2" max="52" step="1" dir="ltr" aria-label="מספר הקלפים"><output class="fa-no"></output></label>` +
        `<label>הערבוב <select class="fa-kind" aria-label="סוג הערבוב">${Object.entries(KINDS).map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
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
        `<span class="viz-legend"><span><i class="pm-key-c1"></i>הצבע : המעגל של המקום המקורי</span><span><i class="pm-key-hl"></i>קלף שחזר למקומו</span></span>` +
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
            return `<td class="pm-c ${fixed ? "is-off" : `c${(ci % 5) + 1}`}${st.t && c === p ? " is-hl" : ""}">${c}</td>`;
          }).join("");
          rows += `<tr><th>${r * PER}</th>${cells}</tr>`;
        }
        $(".fa-fig").innerHTML = `<div class="pm-scroll" tabindex="0" role="region" aria-label="החפיסה אחרי ${st.t} ערבובים, מלמעלה"><table class="pm-cells fa-cells" dir="ltr"><tbody>${rows}</tbody></table></div>`;
        const M = modulus(n, st.kind), lens = cycles.map((c) => c.length).filter((l) => l > 1);
        const rule = n % 2 ? `${ltr(`p → 2p mod ${M}`)} (‏${ltr("n")} אי-זוגי, ממספרים מ-0)`
          : st.kind === "out" ? `${ltr(`p → 2p mod ${M}`)} (ממספרים מ-0, הקלף התחתון לא זז)` : `${ltr(`q → 2q mod ${M}`)} (ממספרים מ-1)`;
        $(".fa-sum").innerHTML = `${ltr(`M = ${M}`)}${NB}: כל ערבוב הוא ${rule}. ` +
          `<b>הסדר של 2 מודולו ${ltr(M)} הוא ${ltr(e)}</b>${NB}: ${ltr(`2^${e} mod ${M} = 1`)}. ` +
          `${lens.length ? `המעגלים באורכים ${ltr([...new Set(lens)].sort((a, b) => a - b).join(", "))}, וכולם חוזרים יחד אחרי ${ltr(e)}.` : "הערבוב לא מזיז אף קלף."}`;
        const home = deck.filter((c, p) => c === p).length;
        $(".fa-note").innerHTML = st.t === 0
          ? `החפיסה בסדר המקורי. הקלף במקום ${ltr("p")} נמצא אחרי ${ltr("t")} ערבובים במקום ${n % 2 || st.kind === "out" ? ltr(`2^t · p mod ${M}`) : ltr(`2^t · (p + 1) mod ${M} − 1`)}.`
          : `אחרי ${ltr(st.t)} ערבובים${NB}: ${ltr(home)} מתוך ${ltr(n)} קלפים במקומם. ${ltr(`2^${st.t} mod ${M} = ${2 ** st.t % M || M}`)}.`;
        if (st.t === e) answer(box, `החפיסה חזרה אחרי ${ltr(e)} ערבובים, הסדר של 2 מודולו ${ltr(M)}.`, ".fa-cells .is-hl");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.t++; draw(); }, done: () => st.t >= order(), restart: () => { st.t = 0; draw(); } });
      const restart = () => { stop(); st.t = 0; draw(); };
      $(".fa-n").addEventListener("input", () => { st.n = Number($(".fa-n").value); restart(); });
      $(".fa-kind").addEventListener("change", () => { st.kind = $(".fa-kind").value; restart(); });
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
      faro: "בוחרים מספר קלפים וסוג ערבוב, ומערבבים צעד אחרי צעד. כל קלף צבוע לפי המעגל של המקום המקורי שלו, קלף שלא זז מסומן בקו מקווקו, וקלף שחזר למקומו ממוסגר. ״עד שהיא חוזרת״ קופץ למספר הערבובים, הסדר של 2 מודולו M.",
    },
    models: { faroShuffle, faroOrder, faroCycles },
  });
})();
