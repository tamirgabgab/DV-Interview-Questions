// kinds: selfdesc
//   selfdesc               0085        self-describing numbers in base b (data-base) in three modes: edit (data-mode="edit", data-digits), a typed number with the real count of every digit under its position, the mismatches marked, and the two sums; search (data-mode="search", bases 2 to 8), the search of the page step by step, every cut and every full candidate its own step, with the counters and the numbers found so far; bases (data-mode="bases", bases 2 to 16), the numbers of a base found by the same search, the four places of the pattern of b >= 7 marked, and how many each base has
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const RLM = "‏";
  const DIG = "0123456789ABCDEF";
  const BMIN = 2, BMAX = 16, SEARCH_MAX = 8;

  // --- the models ------------------------------------------------------------------------------

  // a number of b digits in base b from the text field (0-9 and A-F, any case, spaces
  // ignored); null when it has another length or a digit that is not below b
  const sdParse = (text, b) => {
    const t = String(text).replace(/\s+/g, "").toUpperCase();
    if (t.length !== b) return null;
    const d = [...t].map((c) => DIG.indexOf(c));
    return d.every((v) => v >= 0 && v < b) ? d : null;
  };
  // counts[i]: how many times the digit i appears in d
  const sdCounts = (d) => d.map((_, i) => d.filter((x) => x === i).length);
  const sdText = (d) => d.map((v) => DIG[v]).join("");
  // The search of the page in order: {kind: "cut", pre, v} when the value v at position
  // pre.length makes the digits so far add up to more than b, or sum(i * d[i]) does (the
  // larger values are cut with it); {kind: "check", d, ok} for every full candidate.
  const sdEvents = (b) => {
    const out = [], d = [];
    const rec = (total, weight) => {
      const i = d.length;
      if (i === b) {
        const c = sdCounts(d);
        out.push({ kind: "check", d: d.slice(), ok: c.every((x, k) => x === d[k]) });
        return;
      }
      for (let v = 0; v < b; v++) {
        if (total + v > b || weight + i * v > b) { out.push({ kind: "cut", pre: d.slice(), v }); return; }
        d.push(v);
        rec(total + v, weight + i * v);
        d.pop();
      }
    };
    rec(0, 0);
    return out;
  };
  const cache = new Map();
  // {sols, checked, cuts} of base b, from the events
  const sdSearch = (b) => {
    if (!cache.has(b)) {
      const ev = sdEvents(b);
      cache.set(b, {
        ev,
        sols: ev.filter((e) => e.kind === "check" && e.ok).map((e) => e.d),
        checked: ev.filter((e) => e.kind === "check").length,
        cuts: ev.filter((e) => e.kind === "cut").length,
      });
    }
    const r = cache.get(b);
    return { sols: r.sols, checked: r.checked, cuts: r.cuts };
  };
  // the list of part c: b >= 7 one number, base 4 two, base 5 one
  const sdFamily = (b) => {
    if (b >= 7) {
      const d = new Array(b).fill(0);
      d[0] = b - 4; d[1] = 2; d[2] = 1; d[b - 4] = 1;
      return [d];
    }
    return { 4: [[1, 2, 1, 0], [2, 0, 2, 0]], 5: [[2, 1, 2, 0, 0]] }[b] || [];
  };

  // --- drawing -------------------------------------------------------------------------------------

  // A left-to-right table: the positions, the digits (a digit not yet written is an empty
  // dashed cell, a cut value its own frame) and, when given, the real count of each position.
  const table = (b, digits, counts, { cut = -1, marks = [], label = "" } = {}) => {
    const ix = Array.from({ length: b }, (_, i) => `<td class="gs-b sd-ix">${i}</td>`).join("");
    const dig = Array.from({ length: b }, (_, i) => {
      if (i === cut) return `<td class="gs-b sd-cut">${DIG[digits[i]]}</td>`;
      if (i >= digits.length) return `<td class="gs-b sd-empty"></td>`;
      return `<td class="gs-b is-one${marks.includes(i) ? " is-mark" : ""}">${DIG[digits[i]]}</td>`;
    }).join("");
    const cnt = Array.from({ length: b }, (_, i) => {
      if (!counts) return `<td class="gs-b sd-empty"></td>`;
      const v = counts[i];
      return `<td class="gs-b ${v === digits[i] ? "sd-ok" : "sd-bad"}">${v < DIG.length ? DIG[v] : v}</td>`;
    }).join("");
    return `<div class="gs-scroll" tabindex="0" role="region" aria-label="${label}"><table class="gs-bits sd-tab" dir="ltr" aria-label="${label}"><tbody>` +
      `<tr class="sd-ixrow"><th>i</th>${ix}</tr><tr><th>d[i]</th>${dig}</tr><tr><th>count(i)</th>${cnt}</tr></tbody></table></div>`;
  };
  // "the digit i appears c times", in Hebrew: no time, once, c times
  const times = (i, c) => `הספרה ${ltr(i)} ${c === 0 ? "לא מופיעה בכלל" : c === 1 ? "מופיעה פעם אחת" : `מופיעה ${ltr(c)} פעמים`}`;
  const sums = (d) => [d.reduce((a, x) => a + x, 0), d.reduce((a, x, i) => a + i * x, 0)];
  const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
  const baseSel = (lo, hi, b) =>
    `<label>הבסיס <select class="sd-base" aria-label="הבסיס b, מ-${lo} עד ${hi}">` +
    Array.from({ length: hi - lo + 1 }, (_, k) => `<option value="${lo + k}"${lo + k === b ? " selected" : ""}>${lo + k}</option>`).join("") + `</select></label>`;
  const clampBase = (v, lo, hi, dflt) => { const n = Number(v); return Number.isInteger(n) && n >= lo && n <= hi ? n : dflt; };
  // a start that does not describe itself: the digit b - 1 and then zeros ("9000000000")
  const firstGuess = (b) => [b - 1].concat(new Array(b - 1).fill(0));

  // --- edit: a typed number and its counts ---------------------------------------------------------

  const editMount = (box) => {
    const b0 = clampBase(box.dataset.base, BMIN, BMAX, 10);
    const d0 = sdParse(box.dataset.digits || "", b0) || firstGuess(b0);
    const st = { b: b0, d: d0.slice() };
    box.innerHTML =
      `<div class="ex-controls">${baseSel(BMIN, BMAX, b0)}` +
      `<label><span>המספר</span><input type="text" class="ex-num sd-digits" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המספר${NB}: b ספרות, 0 עד 9 ו-A עד F"></label>` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err sd-err" role="status"></span></div>` +
      `<div class="sd-wrap"></div>` +
      `<span class="viz-legend">${key("gs-key-one", `הספרה ${ltr("d[i]")}`)}${key("sd-key-ok", "הספירה מתאימה")}${key("sd-key-bad", "הספירה לא מתאימה")}</span>` +
      `<p class="ex-summary sd-sum" aria-live="polite"></p><p class="sd-note"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const { b, d } = st, c = sdCounts(d);
      const bad = d.map((x, i) => i).filter((i) => c[i] !== d[i]);
      $(".sd-base").value = String(b);
      if (document.activeElement !== $(".sd-digits")) $(".sd-digits").value = sdText(d);
      $(".sd-wrap").innerHTML = table(b, d, c, { label: `המספר ${sdText(d)} בבסיס ${b}, ומתחת לכל מקום כמה פעמים הספרה שלו מופיעה` });
      const [s1, s2] = sums(d);
      $(".sd-sum").innerHTML = bad.length
        ? `${ltr(b - bad.length)} מתוך ${ltr(b)} המקומות מתאימים. הראשון שלא${NB}: במקום ${ltr(bad[0])} כתוב ${ltr(DIG[d[bad[0]]])}, אבל ${times(bad[0], c[bad[0]])}.`
        : `כל ${ltr(b)} המקומות מתאימים.`;
      $(".sd-note").innerHTML = `הסכומים${NB}: ${ltr(`Σ d[i] = ${s1}`)} ו-${ltr(`Σ i·d[i] = ${s2}`)}. במספר שמתאר את עצמו שניהם ${ltr(b)}.`;
      answer(box, bad.length ? null : `${ltr(sdText(d))} מתאר את עצמו בבסיס ${ltr(b)}.`, ".sd-wrap td.is-one");
    };
    $(".sd-base").addEventListener("change", () => {
      st.b = clampBase($(".sd-base").value, BMIN, BMAX, st.b);
      st.d = firstGuess(st.b);
      $(".sd-err").textContent = "";
      $(".sd-digits").value = sdText(st.d);
      draw();
    });
    $(".sd-digits").addEventListener("change", () => {
      const v = sdParse($(".sd-digits").value, st.b);
      if (!v) { $(".sd-err").textContent = `המספר${NB}: בדיוק ${st.b} ספרות, כל אחת קטנה מ-${st.b}`; return; }
      $(".sd-err").textContent = "";
      st.d = v;
      draw();
    });
    $(".ex-reset").addEventListener("click", () => { st.b = b0; st.d = d0.slice(); $(".sd-err").textContent = ""; $(".sd-digits").value = sdText(st.d); draw(); });
    draw();
  };

  // --- search: the search of the page, step by step ------------------------------------------------

  const searchMount = (box) => {
    const b0 = clampBase(box.dataset.base, BMIN, SEARCH_MAX, 4);
    const st = { b: b0, k: 0 };
    box.innerHTML =
      `<div class="ex-controls">${baseSel(BMIN, SEARCH_MAX, b0)}` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
      `<div class="ex-controls ex-play-row">` +
      `<button type="button" class="md-button ex-start">ההתחלה</button>` +
      `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
      `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
      `<button type="button" class="md-button ex-end">עד הסוף</button>` +
      `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1100, 500, 150) +
      `<button type="button" class="md-button sd-nextsol">הפתרון הבא</button>` +
      `<span class="ex-pos"></span></div>` +
      `<div class="sd-wrap"></div>` +
      `<span class="viz-legend">${key("gs-key-one", "ספרה שנכתבה")}${key("sd-key-cut", "הערך שנחתך, איתו כל הגדולים ממנו")}${key("sd-key-ok", "הספירה מתאימה")}${key("sd-key-bad", "הספירה לא מתאימה")}</span>` +
      `<p class="ex-summary sd-sum" aria-live="polite"></p><p class="sd-note"></p><p class="sd-found"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const events = () => { sdSearch(st.b); return cache.get(st.b).ev; };
    const draw = () => {
      const E = events(), T = E.length, b = st.b;
      st.k = Math.min(Math.max(st.k, 0), T);
      const k = st.k, e = k ? E[k - 1] : null, done = k === T;
      $(".sd-base").value = String(b);
      $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
      $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
      $(".ex-next").disabled = $(".ex-end").disabled = done;
      const seen = E.slice(0, k), checked = seen.filter((x) => x.kind === "check").length, cuts = seen.filter((x) => x.kind === "cut").length;
      const found = seen.filter((x) => x.kind === "check" && x.ok).map((x) => sdText(x.d));
      $(".sd-nextsol").disabled = !E.slice(k).some((x) => x.kind === "check" && x.ok);
      let note = "";
      if (!e) {
        $(".sd-wrap").innerHTML = table(b, [], null, { label: `בסיס ${b}, לפני הצעד הראשון` });
        note = `ממלאים את ${ltr(b)} המקומות לפי הסדר, כל ערך מ-${ltr(0)} ומעלה. כל צעד הוא חיתוך, או מועמד מלא שנבדק.`;
      } else if (e.kind === "cut") {
        const i = e.pre.length, d = e.pre.concat([e.v]), [s1, s2] = sums(d);
        $(".sd-wrap").innerHTML = table(b, d, null, { cut: i, label: `חיתוך במקום ${i} בערך ${e.v}, אחרי ${sdText(e.pre) || "כלום"}` });
        note = `במקום ${ltr(i)} הערך ${ltr(e.v)}${NB}: ` + (s1 > b ? `הספרות כבר מסתכמות ל-${ltr(s1)}, יותר מ-${ltr(b)}` : `הסכום ${ltr(`Σ i·d[i] = ${s2}`)} כבר יותר מ-${ltr(b)}`) +
          `. הערך הזה וכל הגדולים ממנו נחתכים, ${e.pre.length ? `וחוזרים למקום ${ltr(i - 1)}` : "והחיפוש נגמר"}.`;
      } else {
        const c = sdCounts(e.d), bad = e.d.map((x, i) => i).filter((i) => c[i] !== e.d[i]);
        $(".sd-wrap").innerHTML = table(b, e.d, c, { label: `המועמד ${sdText(e.d)} והספירה שלו` });
        note = e.ok ? `<b>${ltr(sdText(e.d))} מתאר את עצמו.</b>`
          : `המועמד ${ltr(sdText(e.d))} נבדק${NB}: במקום ${ltr(bad[0])} כתוב ${ltr(DIG[e.d[bad[0]]])}, אבל ${times(bad[0], c[bad[0]])}.`;
      }
      $(".sd-sum").innerHTML = `עד עכשיו${NB}: ${ltr(checked)} מועמדים מלאים נבדקו ו-${ltr(cuts)} חיתוכים, מתוך ${ltr((b ** b).toLocaleString("en-US"))} מחרוזות של ${ltr(b)} ספרות.`;
      $(".sd-note").innerHTML = note;
      $(".sd-found").innerHTML = found.length ? `נמצאו${NB}: ${found.map((x) => ltr(x)).join(", ")}.` : "";
      answer(box, done ? (found.length ? `בבסיס ${ltr(b)} ${found.length === 1 ? "יש מספר אחד" : `יש ${ltr(found.length)} מספרים`}${NB}: ${found.map((x) => ltr(x)).join(", ")}.` : `בבסיס ${ltr(b)} אין אף מספר שמתאר את עצמו.`) : null);
    };
    const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= events().length, restart: () => { st.k = 0; draw(); } });
    $(".sd-base").addEventListener("change", () => { stop(); st.b = clampBase($(".sd-base").value, BMIN, SEARCH_MAX, st.b); st.k = 0; draw(); });
    $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
    $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
    $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
    $(".ex-end").addEventListener("click", () => { stop(); st.k = events().length; draw(); });
    $(".sd-nextsol").addEventListener("click", () => {
      stop();
      const E = events(), j = E.findIndex((x, m) => m >= st.k && x.kind === "check" && x.ok);
      if (j >= 0) { st.k = j + 1; draw(); }
    });
    $(".ex-reset").addEventListener("click", () => { stop(); st.b = b0; st.k = 0; draw(); });
    draw();
  };

  // --- bases: the numbers of every base ------------------------------------------------------------

  const basesMount = (box) => {
    const b0 = clampBase(box.dataset.base, BMIN, BMAX, 12);
    const st = { b: b0 };
    box.innerHTML =
      `<div class="ex-controls">${baseSel(BMIN, BMAX, b0)}` +
      `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
      `<div class="sd-strip"></div>` +
      `<div class="sd-wrap"></div>` +
      `<span class="viz-legend">${key("gs-key-one", `הספרה ${ltr("d[i]")}`)}${key("sd-key-mark", `המקומות של התבנית, ${ltr("b ≥ 7")}`)}${key("sd-key-ok", "הספירה מתאימה")}</span>` +
      `<p class="ex-summary sd-sum" aria-live="polite"></p><p class="sd-note"></p>`;
    const $ = (sel) => box.querySelector(sel);
    const strip = () => {
      const bs = Array.from({ length: BMAX - BMIN + 1 }, (_, k) => BMIN + k);
      const row = (name, f) => `<tr><th>${name}</th>${bs.map((b) => `<td class="gs-b${b === st.b ? " sd-cur" : ""}">${f(b)}</td>`).join("")}</tr>`;
      const label = "כמה מספרים שמתארים את עצמם יש בכל בסיס מ-2 עד 16";
      return `<div class="gs-scroll" tabindex="0" role="region" aria-label="${label}"><table class="gs-bits sd-tab sd-count" dir="ltr" aria-label="${label}"><tbody>` +
        row("b", (b) => b) + row("#", (b) => sdSearch(b).sols.length) + `</tbody></table></div>`;
    };
    const draw = () => {
      const b = st.b, r = sdSearch(b);
      $(".sd-base").value = String(b);
      $(".sd-strip").innerHTML = strip();
      const marks = b >= 7 ? [0, 1, 2, b - 4] : [];
      $(".sd-wrap").innerHTML = r.sols.length
        ? r.sols.map((d) => table(b, d, sdCounts(d), { marks, label: `${sdText(d)} בבסיס ${b}, עם הספירה של כל מקום` })).join("")
        : table(b, [], null, { label: `בבסיס ${b} אין מספר שמתאר את עצמו` });
      $(".sd-sum").innerHTML = `החיפוש בבסיס ${ltr(b)} בדק ${ltr(r.checked.toLocaleString("en-US"))} מועמדים מלאים, עם ${ltr(r.cuts.toLocaleString("en-US"))} חיתוכים, ` +
        (r.sols.length ? `ומצא ${r.sols.length === 1 ? "מספר אחד" : `${ltr(r.sols.length)} מספרים`}${NB}: ${r.sols.map((d) => ltr(sdText(d))).join(", ")}.` : "ולא מצא אף מספר.");
      $(".sd-note").innerHTML = b >= 7
        ? `${RLM}${ltr(`b = ${b}`)}${NB}: התבנית. במקום ${ltr(0)} הספרה ${ltr(`b − 4 = ${b - 4}`)}${b - 4 > 9 ? ` (${ltr(DIG[b - 4])})` : ""}, במקום ${ltr(1)} הספרה ${ltr(2)}, במקום ${ltr(2)} הספרה ${ltr(1)}, ובמקום ${ltr(b - 4)} הספרה ${ltr(1)}.`
        : b === 4 || b === 5
          ? `בסיס קטן${NB}: המקרה ${ltr("z ≥ 3")} צריך ${ltr("b ≥ 7")}, ומה שנמצא כאן בא מהמקרים ${ltr("z = 1")} ו-${ltr("z = 2")}.`
          : `אין${NB}: המקרה ${ltr("z ≥ 3")} צריך ${ltr("b ≥ 7")}, והמקרים ${ltr("z = 1")} ו-${ltr("z = 2")} נותנים רק את הבסיסים ${ltr(4)} ו-${ltr(5)}.`;
    };
    $(".sd-base").addEventListener("change", () => { st.b = clampBase($(".sd-base").value, BMIN, BMAX, st.b); draw(); });
    $(".ex-reset").addEventListener("click", () => { st.b = b0; draw(); });
    draw();
  };

  const selfdescView = () => ({
    mount(box) {
      const mode = box.dataset.mode;
      if (mode === "search") searchMount(box);
      else if (mode === "bases") basesMount(box);
      else editMount(box);
    },
  });

  dvqExplorers.register({
    views: { selfdesc: selfdescView },
    help: {
      selfdesc: "שלושה מצבים. בעורך מקלידים מספר בבסיס שנבחר (ספרות 0 עד 9 ו-A עד F), ומתחת לכל מקום מופיע כמה פעמים הספרה שלו באמת מופיעה, ירוק כשזה מתאים וכתום כשלא. בחיפוש כל צעד הוא חיתוך (ערך שהסכומים שלו עוברים את הבסיס) או מועמד מלא שנבדק, ו״הפתרון הבא״ קופץ למספר הבא שמתאר את עצמו. בטבלת הבסיסים בוחרים בסיס ורואים את המספרים שלו ואת ארבעת המקומות של התבנית.",
    },
    models: { sdParse, sdCounts, sdEvents, sdSearch, sdFamily },
  });
})();
