// kinds: luhn
//   luhn                   0098        check digits: a number typed or picked (test cards, an ID), its Luhn check shown digit by digit (the doubled places, what each digit adds, the sum); a place chosen and its digit changed or swapped with its right neighbour, with "caught" or "slipped by"; beside it two 10 x 10 maps of the errors (neighbour swaps or a single change in a doubled place), Luhn against a chosen scheme (weights 1 and 2, EAN 1 and 3, ISBN mod 11)
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = "\u00a0", RLM = "\u200f";
  const MAXLEN = 19;

  // --- the models ------------------------------------------------------------------------------

  // the digits of a text, spaces and dashes skipped; null when anything else is in it
  const luDigits = (text) => {
    const s = String(text).replace(/[\s-]/g, "");
    return /^\d{1,19}$/.test(s) ? [...s].map(Number) : null;
  };
  // Luhn's doubled digit: 2d, minus 9 when two digits
  const luD = (d) => (2 * d > 9 ? 2 * d - 9 : 2 * d);
  // per digit, left to right: the digit, whether its place is doubled (an even place from the
  // right), and what it adds
  const luTerms = (ds) => ds.map((d, i) => {
    const dbl = (ds.length - 1 - i) % 2 === 1;
    return { d, dbl, add: dbl ? luD(d) : d };
  });
  const luSum = (ds) => luTerms(ds).reduce((s, t) => s + t.add, 0);
  const luValid = (ds) => luSum(ds) % 10 === 0;
  // the check digit that completes ds (without it) to a valid number
  const luCheck = (ds) => (10 - (luSum([...ds, 0]) % 10)) % 10;
  // a scheme: what a digit adds in an odd place and in an even place (from the right), mod m
  const SCHEMES = {
    luhn: { odd: (d) => d, even: luD, mod: 10, name: "Luhn" },
    w12: { odd: (d) => d, even: (d) => 2 * d, mod: 10, name: "משקלים 1 ו-2" },
    ean: { odd: (d) => d, even: (d) => 3 * d, mod: 10, name: "EAN-13, משקלים 1 ו-3" },
    isbn: { odd: (d) => d, even: (d) => 2 * d, mod: 11, name: "ISBN-10, מודולו 11" },
  };
  // the 10 x 10 map of a scheme: cell [a][b] is "same" on the diagonal, else "miss" when the
  // error slips by and "ok" when it is caught. kind "swap": a and b swapped in two neighbouring
  // places; kind "single": a changed to b in an even (doubled, weighted) place
  const luMap = (name, kind) => {
    const { odd, even, mod } = SCHEMES[name];
    const r = (v) => ((v % mod) + mod) % mod;
    return Array.from({ length: 10 }, (_, a) => Array.from({ length: 10 }, (_, b) => {
      if (a === b) return "same";
      const diff = kind === "swap" ? odd(a) + even(b) - odd(b) - even(a) : even(b) - even(a);
      return r(diff) === 0 ? "miss" : "ok";
    }));
  };
  // the unordered pairs that slip by (a swap map is symmetric) and all the cells that do
  const luMissCount = (map) => map.reduce((s, row, a) => s + row.filter((c, b) => c === "miss" && b > a).length, 0);
  const luMissCountAll = (map) => map.reduce((s, row) => s + row.filter((c) => c === "miss").length, 0);
  // an error at place k (0-based from the left): "single" adds 1 to the digit (mod 10),
  // "swap" swaps it with its right neighbour
  const luMutate = (ds, kind, k) => {
    const m = ds.slice();
    if (kind === "single") m[k] = (m[k] + 1) % 10;
    else if (k + 1 < m.length) [m[k], m[k + 1]] = [m[k + 1], m[k]];
    return m;
  };

  // --- drawing -------------------------------------------------------------------------------------

  const group = (ds) => ds.join("").replace(/(\d{4})(?=\d)/g, "$1 ");
  // the strip: one column per digit, the doubled places filled, the chosen place(s) framed
  const stripSvg = (ds, mark) => {
    const terms = luTerms(ds), n = ds.length, colw = 21, x0 = 6, rowh = 30;
    const W = x0 * 2 + Math.max(n, 8) * colw, H = 10 + rowh * 2;
    const left = x0 + ((Math.max(n, 8) - n) * colw) / 2;
    const label = `המספר ${group(ds)}${NB}: ספרה בכל עמודה, המקומות המודגשים מוכפלים, והשורה התחתונה היא מה שכל ספרה מוסיפה. הסכום ${luSum(ds)}`;
    let s = `<svg class="lu-strip" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">`;
    terms.forEach((t, i) => {
      const x = left + i * colw;
      s += `<rect class="lu-cell${t.dbl ? " lu-dbl" : ""}" x="${(x + 1).toFixed(1)}" y="5" width="${colw - 2}" height="${rowh * 2}" rx="3"/>`;
      s += `<text class="lu-t" x="${(x + colw / 2).toFixed(1)}" y="${(5 + rowh * 0.68).toFixed(1)}" text-anchor="middle">${t.d}</text>`;
      s += `<text class="lu-t" x="${(x + colw / 2).toFixed(1)}" y="${(5 + rowh * 1.68).toFixed(1)}" text-anchor="middle">${t.add}</text>`;
    });
    s += `<line class="lu-rule" x1="${left}" x2="${left + n * colw}" y1="${5 + rowh}" y2="${5 + rowh}"/>`;
    if (mark) {
      const [k, w] = mark;
      s += `<rect class="lu-pos" x="${(left + k * colw).toFixed(1)}" y="3" width="${colw * w}" height="${rowh * 2 + 4}" rx="4"/>`;
    }
    return s + "</svg>";
  };
  // a 10 x 10 map, a (the digit before) down, b (after, or the neighbour) across
  const mapSvg = (map, title, now) => {
    const c = 15, x0 = 22, y0 = 20, W = x0 + 10 * c + 4, H = y0 + 10 * c + 4;
    const miss = luMissCountAll(map);
    let s = `<svg class="lu-map" viewBox="0 0 ${W} ${H}" role="img" aria-label="${title}${NB}: ${miss} מתוך 90 התאים חומקים">`;
    for (let k = 0; k < 10; k++) {
      s += `<text class="lu-mh" x="${x0 + k * c + c / 2}" y="${y0 - 6}" text-anchor="middle">${k}</text>`;
      s += `<text class="lu-mh" x="${x0 - 6}" y="${y0 + k * c + c / 2 + 4}" text-anchor="end">${k}</text>`;
    }
    map.forEach((row, a) => row.forEach((cell, b) => {
      const x = x0 + b * c, y = y0 + a * c;
      s += `<rect class="lu-m lu-m-${cell}" x="${x}" y="${y}" width="${c}" height="${c}"/>`;
      if (cell === "miss") s += `<text class="lu-mx" x="${x + c / 2}" y="${y + c / 2 + 4}" text-anchor="middle">×</text>`;
    }));
    if (now) s += `<rect class="lu-m-now" x="${x0 + now[1] * c}" y="${y0 + now[0] * c}" width="${c}" height="${c}"/>`;
    return s + "</svg>";
  };

  const PRESETS = [
    ["4111111111111111", "כרטיס בדיקה של Visa, 4111"],
    ["4012888888881881", "כרטיס בדיקה של Visa, 4012"],
    ["5555555555554444", "כרטיס בדיקה של Mastercard"],
    ["378282246310005", "כרטיס בדיקה של American Express, 15 ספרות"],
    ["4111111111109115", "עם 0 ו-9 שכנים"],
    ["000000018", "תעודת זהות מומצאת, 9 ספרות"],
  ];
  const SCHEME_OPTS = [["w12", "משקלים 1 ו-2"], ["ean", "ברקוד EAN-13, משקלים 1 ו-3"], ["isbn", "ISBN-10, מודולו 11"]];
  const KIND_OPTS = [["swap", "החלפה של שתי שכנות"], ["single", "טעות בספרה אחת, במקום מוכפל"]];

  const luhnView = () => ({
    mount(box) {
      const d = box.dataset;
      const N0 = luDigits(d.number || "") ? String(d.number).replace(/[\s-]/g, "") : "4111111111111111";
      const S0 = SCHEMES[d.scheme] && d.scheme !== "luhn" ? d.scheme : "ean";
      const K0 = d.map === "single" ? "single" : "swap";
      const st = { last: null };       // the last error made by a button: { kind, k, before, after, a, b }
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>המספר</span><input type="text" class="ex-num lu-num" value="${N0}" dir="ltr" inputmode="numeric" spellcheck="false" maxlength="23" aria-label="המספר${NB}: עד ${MAXLEN} ספרות, רווחים ומקפים מותרים"></label>` +
        `<label>דוגמה <select class="lu-pre" data-nolink aria-label="מספר בדיקה מוכן"><option value="">בחרו</option>${PRESETS.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה למספר של העמוד</button><span class="fl-err lu-err"></span></div>` +
        `<div class="ex-controls">` +
        `<label><span>המקום משמאל</span><input type="number" class="ex-num lu-k" min="1" max="${N0.length}" step="1" value="1" dir="ltr" inputmode="numeric" aria-label="המקום של הטעות, מספר הספרה משמאל"></label>` +
        `<button type="button" class="md-button md-button--primary lu-single">שינוי הספרה ב-1</button>` +
        `<button type="button" class="md-button lu-swap">החלפה עם הספרה שמימין</button></div>` +
        `<div class="ex-controls">` +
        `<label>השוואה ל- <select class="lu-scheme" aria-label="השיטה שמשווים אליה">${SCHEME_OPTS.map(([v, t]) => `<option value="${v}"${v === S0 ? " selected" : ""}>${t}</option>`).join("")}</select></label>` +
        `<label>סוג הטעות <select class="lu-kind" aria-label="סוג הטעות במפות">${KIND_OPTS.map(([v, t]) => `<option value="${v}"${v === K0 ? " selected" : ""}>${t}</option>`).join("")}</select></label></div>` +
        `<div class="lu-stripwrap" data-steady></div>` +
        `<span class="viz-legend"><span><i class="lu-key-dbl"></i><span>מקום מוכפל</span></span><span><i class="lu-key-cell"></i><span>מקום רגיל</span></span></span>` +
        `<div class="lu-maps" data-steady><div><p class="ex-title lu-t1"></p><div class="lu-m1"></div></div><div><p class="ex-title lu-t2"></p><div class="lu-m2"></div></div></div>` +
        `<span class="viz-legend"><span><i class="lu-key-ok"></i><span>הטעות נתפסת</span></span><span><i class="lu-key-miss"></i><span>הטעות חומקת (×)</span></span></span>` +
        `<p class="ex-summary lu-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".lu-num"), kIn = $(".lu-k");
      let ds = luDigits(N0);
      const draw = () => {
        const n = ds.length;
        kIn.max = String(n);
        let k = Math.min(Math.max(1, Math.round(Number(kIn.value)) || 1), n);
        if (String(k) !== kIn.value && document.activeElement !== kIn) kIn.value = String(k);
        const kind = $(".lu-kind").value, scheme = $(".lu-scheme").value;
        const total = luSum(ds), ok = total % 10 === 0;
        const last = st.last;
        const mark = last ? [last.k, last.kind === "swap" ? 2 : 1] : [k - 1, 1];
        $(".lu-stripwrap").innerHTML = stripSvg(ds, mark);
        // the last error's cell: a swap is a cell of the swap maps, a single change only of the
        // single maps and only when its place was doubled
        const now = last && last.kind === kind && (kind === "swap" || last.dbl) ? [last.a, last.b] : null;
        const m1 = luMap("luhn", kind), m2 = luMap(scheme, kind);
        const cnt = (m) => (kind === "swap" ? `${ltr(luMissCount(m))} מתוך ${ltr(45)}` : `${ltr(luMissCountAll(m))} מתוך ${ltr(90)}`);
        $(".lu-t1").innerHTML = `${RLM}Luhn${NB}: חומקות ${cnt(m1)}`;
        $(".lu-t2").innerHTML = `${RLM}${SCHEMES[scheme].name}${NB}: חומקות ${cnt(m2)}`;
        $(".lu-m1").innerHTML = mapSvg(m1, "Luhn", now);
        $(".lu-m2").innerHTML = mapSvg(m2, SCHEMES[scheme].name, now);
        let text = `הסכום ${ltr(total)}${ok ? `, מתחלק ב-10${NB}: המספר תקין.` : `, לא מתחלק ב-10${NB}: המספר לא תקין.`}`;
        if (n > 1) text += ` ספרת הביקורת שמתאימה לשאר היא ${ltr(luCheck(ds.slice(0, -1)))}.`;
        if (last) {
          const what = last.kind === "swap" ? `החלפת ${ltr(`${last.a}${last.b}`)} ל-${ltr(`${last.b}${last.a}`)} במקום ${ltr(last.k + 1)}` : `שינוי ${ltr(last.a)} ל-${ltr(last.b)} במקום ${ltr(last.k + 1)}`;
          const verdict = !last.beforeOk ? "המספר לא היה תקין גם לפני כן, אז אין כאן מה לתפוס"
            : last.afterOk ? `המספר עדיין תקין${NB}: הטעות חומקת` : `המספר כבר לא תקין${NB}: הטעות נתפסה`;
          text += ` ${what}${NB}: ${verdict}.`;
        }
        $(".lu-sum").innerHTML = text;
        answer(box, ok ? `תקין${NB}: הסכום ${ltr(total)} מתחלק ב-10.` : `לא תקין${NB}: הסכום ${ltr(total)}.`);
      };
      const setNumber = (text, keepLast = false) => {
        const got = luDigits(text);
        if (!got) { $(".lu-err").textContent = `רק ספרות, עד ${MAXLEN}`; input.value = ds.join(""); return; }
        $(".lu-err").textContent = "";
        ds = got;
        if (!keepLast) st.last = null;
        draw();
      };
      input.addEventListener("change", () => setNumber(input.value));
      kIn.addEventListener("change", () => { st.last = null; draw(); });
      $(".lu-scheme").addEventListener("change", draw);
      $(".lu-kind").addEventListener("change", draw);
      $(".lu-pre").addEventListener("change", () => {
        const v = $(".lu-pre").value;
        if (!v) return;
        input.value = v;
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        $(".lu-pre").value = "";
      });
      const mutate = (kind) => {
        const n = ds.length;
        let k = Math.min(Math.max(1, Math.round(Number(kIn.value)) || 1), n) - 1;
        if (kind === "swap" && k + 1 >= n) k = n - 2;
        if (k < 0) return;
        const before = ds, after = luMutate(ds, kind, k);
        st.last = { kind, k, a: before[k], b: kind === "swap" ? before[k + 1] : after[k], dbl: luTerms(before)[k].dbl,
          beforeOk: luValid(before), afterOk: luValid(after) };
        kIn.value = String(k + 1);
        input.value = after.join("");
        setNumber(input.value, true);
      };
      $(".lu-single").addEventListener("click", () => mutate("single"));
      $(".lu-swap").addEventListener("click", () => mutate("swap"));
      $(".ex-reset").addEventListener("click", () => {
        input.value = N0;
        kIn.value = "1";
        $(".lu-scheme").value = S0;
        $(".lu-kind").value = K0;
        setNumber(N0);
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { luhn: luhnView },
    help: {
      luhn: "מקלידים מספר (או בוחרים מספר בדיקה), ורואים את בדיקת Luhn ספרה אחרי ספרה\u00a0: המקומות המודגשים מוכפלים, והשורה התחתונה היא מה שכל ספרה מוסיפה לסכום. בוחרים מקום משמאל, ו\"שינוי הספרה ב-1\" או \"החלפה עם הספרה שמימין\" יוצרים טעות ואומרים אם היא נתפסה. שתי המפות מראות לכל זוג ספרות a (שורה) ו-b (עמודה) אם הטעות נתפסת או חומקת (×)\u00a0: משמאל Luhn, ומימין השיטה שבוחרים להשוות אליה.",
    },
    models: { luDigits, luD, luTerms, luSum, luValid, luCheck, luMap, luMissCount, luMissCountAll, luMutate },
  });
})();
