// kinds: concat
//   concat                 0107        the largest (or smallest) number from concatenation (data-nums "3.30.34.5.9", data-mode max or min, data-pair "2.0"): a list of up to 8 numbers typed or picked from the page's lists, the sorts side by side (by value, as strings, by a + b against b + a, and in the smallest mode the shortcut that moves the first non-zero number to the front and part c's rule), each join with the first digit where it falls from the answer marked; the values a / (10^|a| - 1) on a number line with the numbers under it in that order and their places in the answer; a pair of numbers picked in two selects with a + b, b + a and both values; in the smallest mode the candidates of part c, one per non-zero first number
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";
  const CAT = "‖";
  const NMAX = 8, VMAX = 999999;

  // --- the model, as tools/figures/q0107.py ------------------------------------------------
  // for the largest number: -1 when a goes first (a + b is larger), 1 when b does, 0 on a tie
  const ccOrder = (a, b) => (a + b > b + a ? -1 : a + b < b + a ? 1 : 0);
  // the places of the items (indices) sorted by the rule: descending for the largest,
  // ascending for the smallest; the sort is stable, as Python's
  const ccSorted = (s, desc) => s.map((_, i) => i).sort((i, j) => (desc ? ccOrder(s[i], s[j]) : ccOrder(s[j], s[i])));
  const join = (s, idx) => idx.map((i) => s[i]).join("");
  const ccLargest = (nums) => {
    const s = nums.map(String), out = join(s, ccSorted(s, true));
    return out[0] === "0" ? "0" : out;
  };
  // part c: every distinct non-zero value as the first, then the zeros, then the rest in
  // ascending order; the candidates as [first, its order (indices), the join], and the best
  const ccSmallest = (nums) => {
    const s = nums.map(String), up = ccSorted(s, false);
    const zeros = up.filter((i) => s[i] === "0"), rest = up.filter((i) => s[i] !== "0");
    if (!rest.length) return { best: "0", order: up, cands: [] };
    const cands = [], seen = new Set();
    rest.forEach((i, p) => {
      if (seen.has(s[i])) return;
      seen.add(s[i]);
      const order = [i, ...zeros, ...rest.filter((_, q) => q !== p)];
      cands.push([s[i], order, join(s, order)]);
    });
    const win = cands.reduce((b, c) => (c[2] < b[2] ? c : b));
    return { best: win[2], order: win[1], cands };
  };
  // the shortcut of part c: ascending, then the first non-zero string moved to the front
  const ccShortcut = (nums) => {
    const s = nums.map(String), up = ccSorted(s, false), k = up.findIndex((i) => s[i] !== "0");
    return k < 0 ? up : [up[k], ...up.slice(0, k), ...up.slice(k + 1)];
  };
  const ccNumSort = (nums, desc) => nums.map((_, i) => i).sort((i, j) => (desc ? nums[j] - nums[i] : nums[i] - nums[j]));
  const ccStrSort = (nums, desc) => {
    const s = nums.map(String);
    return s.map((_, i) => i).sort((i, j) => (s[i] === s[j] ? 0 : (s[i] < s[j]) === desc ? 1 : -1));
  };
  // 0.aaaa... cut after `places` digits, "1" for 9..9 and "0" for 0, as q0107.dec
  const ccDec = (a, places = 6) => (/^9+$/.test(a) ? "1" : a === "0" ? "0" : `0.${a.repeat(places).slice(0, places)}…`);
  const ccRho = (a) => Number(a) / (10 ** a.length - 1);
  // "3, 30, 34" or "3.30.34" or "3 30 34": 1 to NMAX whole numbers from 0 to VMAX, else null
  const ccParse = (text) => {
    const p = String(text || "").trim().split(/[\s,.;]+/).filter(Boolean);
    if (!p.length || p.length > NMAX || p.some((x) => !/^\d+$/.test(x) || Number(x) > VMAX)) return null;
    return p.map(Number);
  };
  const ccPresets = [
    ["הדוגמה", [3, 30, 34, 5, 9]],
    ["3 ו-30", [3, 30]],
    ["12 ו-1212", [12, 1212]],
    ["שני אפסים", [0, 0]],
    ["0, 1, 10", [0, 1, 10]],
    ["0, 0, 1", [0, 0, 1]],
    ["20, 1, 0", [20, 1, 0]],
    ["0, 2, 21", [0, 2, 21]],
  ];
  const presetOf = (nums) => ccPresets.findIndex(([, v]) => v.join() === nums.join());

  // --- drawing -------------------------------------------------------------------------
  const f1 = (x) => x.toFixed(1);
  const firstDiff = (a, b) => { for (let i = 0; i < Math.min(a.length, b.length); i++) if (a[i] !== b[i]) return i; return -1; };
  // a join drawn item by item (alternate tints show where one number ends), its first digit
  // that differs from the answer marked
  const joined = (s, order, want) => {
    const all = order.map((i) => s[i]).join(""), d = firstDiff(all, want);
    let at = 0, o = `<span class="cc-join" dir="ltr">`;
    order.forEach((i) => {
      o += `<span class="cc-it">`;
      for (const ch of s[i]) { o += at === d ? `<b class="cc-diff">${ch}</b>` : ch; at++; }
      o += "</span>";
    });
    return `${o}</span>`;
  };

  // the values rho on [0, 1], a dot per distinct value; the numbers in a row under the line in
  // ascending rho, each joined to its dot, with its place in the answer. A frame is as wide as
  // its number at the size reading-tools.js grows a label to on a phone (up to twice 14 px);
  // when the frames do not fit their slots the row is staggered in two (every other one lower)
  const W = 640, H = 150, X0 = 34, X1 = 606, AY = 46, LY = 112, DROP = 46;
  const frameW = (a) => 12 + 12.5 * a.length;
  const lineSvg = (s, order, pair) => {
    const X = (v) => X0 + v * (X1 - X0);
    const up = s.map((_, i) => i).sort((i, j) => ccRho(s[i]) - ccRho(s[j]) || (s[i] < s[j] ? -1 : s[i] > s[j] ? 1 : i - j));
    const n = s.length, slot = (X1 - X0) / n;
    const stag = s.some((a) => frameW(a) + 4 > slot), ly = (k) => LY + (stag && k % 2 ? DROP : 0);
    const cls = (i) => (i === pair[0] ? " is-a" : i === pair[1] ? " is-b" : "");
    let o = `<svg class="figure cc-line cc-live" viewBox="0 0 ${W} ${H + (stag ? DROP : 0)}" direction="ltr" role="img" ` +
      `aria-label="הערכים של המספרים על הקטע מ-0 עד 1, ומתחת המספרים לפי הסדר שלהם${NB}: ${up.map((i) => s[i]).join(", ")}">`;
    o += `<line class="cc-axis" x1="${X0}" x2="${X1}" y1="${AY}" y2="${AY}"/>`;
    for (let k = 0; k <= 10; k++) {
      const x = X(k / 10), big = k % 5 === 0;
      o += `<line class="cc-tick" x1="${f1(x)}" x2="${f1(x)}" y1="${AY - (big ? 7 : 4)}" y2="${AY + (big ? 7 : 4)}"/>`;
      if (big) o += `<text class="cc-tl" x="${f1(x)}" y="${AY - 13}" text-anchor="middle">${["0", "0.5", "1"][k / 5]}</text>`;
    }
    up.forEach((i, k) => {
      o += `<line class="cc-lead${cls(i)}" x1="${f1(X(ccRho(s[i])))}" y1="${AY + 6}" x2="${f1(X0 + (k + 0.5) * slot)}" y2="${ly(k) - 17}"/>`;
    });
    const dots = new Map();
    up.forEach((i) => { const v = ccRho(s[i]); if (![...dots.keys()].some((u) => Math.abs(u - v) < 1e-12)) dots.set(v, i); });
    dots.forEach((i, v) => {
      const mates = s.map((_, j) => j).filter((j) => Math.abs(ccRho(s[j]) - v) < 1e-12);
      const c = mates.includes(pair[0]) ? " is-a" : mates.includes(pair[1]) ? " is-b" : "";
      o += `<circle class="cc-dot${c}" cx="${f1(X(v))}" cy="${AY}" r="${c ? 6.5 : 5}"><title>${s[i]}: ${ccDec(s[i])}</title></circle>`;
    });
    up.forEach((i, k) => {
      const xl = X0 + (k + 0.5) * slot, w = frameW(s[i]), place = order.indexOf(i) + 1, y = ly(k);
      o += `<g class="cc-lab${cls(i)}"><title>${s[i]}: ${s[i]}/${10 ** s[i].length - 1}, place ${place}</title>` +
        `<rect x="${f1(xl - w / 2)}" y="${y - 16}" width="${w}" height="24" rx="5"/>` +
        `<text class="cc-num" x="${f1(xl)}" y="${y + 1}" text-anchor="middle">${s[i]}</text>` +
        `<circle class="cc-place" cx="${f1(xl)}" cy="${y + 23}" r="9"/>` +
        `<text class="cc-pl" x="${f1(xl)}" y="${y + 27}" text-anchor="middle">${place}</text></g>`;
    });
    return `${o}</svg>`;
  };

  const concatView = () => ({
    mount(box) {
      const n0 = ccParse(String(box.dataset.nums || "").split(".").join(", ")) || ccPresets[0][1].slice();
      const mode0 = box.dataset.mode === "min" ? "min" : "max";
      const fixPair = (nums, p) => {
        const ok = (i) => Number.isInteger(i) && i >= 0 && i < nums.length;
        let [a, b] = p;
        if (!ok(a)) a = 0;
        if (!ok(b) || b === a) b = nums.length > 1 ? (a === 0 ? 1 : 0) : a;
        return [a, b];
      };
      const p0 = fixPair(n0, String(box.dataset.pair || "0.1").split(".").map(Number));
      const init = { nums: n0, mode: mode0, pair: p0 };
      const st = { nums: n0.slice(), mode: mode0, pair: p0.slice(), err: "" };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הרשימה <select class="cc-preset" aria-label="איזו רשימה">${ccPresets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        `<label>המספרים <input type="text" class="cc-nums" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המספרים, מופרדים בפסיקים, למשל 3, 30, 34"></label>` +
        `<label>מחפשים <select class="cc-mode" aria-label="המספר הגדול ביותר או הקטן ביותר"><option value="max">את הגדול ביותר</option><option value="min">את הקטן ביותר</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls cc-pairrow">` +
        `<label>הזוג${NB}: a <select class="cc-a" aria-label="המספר הראשון של הזוג"></select></label>` +
        `<label>b <select class="cc-b" aria-label="המספר השני של הזוג"></select></label></div>` +
        `<p class="ex-summary cc-sum" aria-live="polite"></p>` +
        `<div class="cc-rowswrap"><table class="cc-rows" aria-label="המיונים זה ליד זה"><tbody></tbody></table></div>` +
        `<div class="cc-wrap cc-linewrap"></div>` +
        `<div class="cc-pair"></div>` +
        `<span class="viz-legend cc-legend"><span><i class="cc-key-dot"></i>הערך${NB}${ltr("a / (10<sup>|a|</sup> − 1)")}</span>` +
        `<span><i class="cc-key-place"></i>המקום בתשובה</span><span><i class="cc-key-a"></i>${ltr("a")}${NB}של הזוג</span>` +
        `<span><i class="cc-key-b"></i>${ltr("b")}${NB}של הזוג</span><span><i class="cc-key-diff"></i>הספרה הראשונה שבה שרשור נופל מהתשובה</span></span>` +
        `<div class="cc-cands"></div>` +
        `<p class="cc-note"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const syncFields = () => {
        const k = presetOf(st.nums);
        $(".cc-preset").value = k < 0 ? "custom" : String(k);
        $(".cc-nums").value = st.nums.join(", ");
        $(".cc-mode").value = st.mode;
        const opts = st.nums.map((v, i) => `<option value="${i}">${v}${st.nums.indexOf(v) !== i ? ` (${i + 1})` : ""}</option>`).join("");
        [".cc-a", ".cc-b"].forEach((sel, k2) => {
          const el = $(sel);
          if (el.dataset.opts !== opts) { el.innerHTML = opts; el.dataset.opts = opts; }
          el.value = String(st.pair[k2]);
        });
      };
      const pairHtml = (s) => {
        const [i, j] = st.pair, a = s[i], b = s[j], ab = a + b, ba = b + a;
        const sign = ab > ba ? ">" : ab < ba ? "<" : "=";
        const rho = (x) => `${ltr(`${x}/${10 ** x.length - 1}`)} = ${ltr(ccDec(x))}`;
        const max = st.mode === "max";
        let verdict;
        if (i === j) verdict = "בחרו שני מספרים שונים ברשימה.";
        else if (ab === ba) verdict = `שני השרשורים שווים, ולשני המספרים אותו ערך${NB}: הסדר ביניהם לא משנה.`;
        else {
          const first = (ab > ba) === max ? a : b, second = first === a ? b : a;
          verdict = `${ltr(`${ab} ${sign} ${ba}`)}, ולכן ${ltr(first)} לפני ${ltr(second)} ${max ? "בגדול ביותר" : "בקטן ביותר"}.`;
        }
        return `<table class="cc-ptab" aria-label="ההשוואה של הזוג"><tbody>` +
          `<tr><th scope="row">${ltr("a ‖ b")}</th><td dir="ltr">${a} ${CAT} ${b} = <b>${ab}</b></td></tr>` +
          `<tr><th scope="row">${ltr("b ‖ a")}</th><td dir="ltr">${b} ${CAT} ${a} = <b>${ba}</b></td></tr>` +
          `<tr><th scope="row">${ltr("ρ(a)")}</th><td>${rho(a)}</td></tr>` +
          `<tr><th scope="row">${ltr("ρ(b)")}</th><td>${rho(b)}</td></tr>` +
          `</tbody></table><p class="cc-verdict">${verdict}</p>`;
      };
      const draw = () => {
        const { nums, mode } = st, s = nums.map(String), max = mode === "max";
        const sm = ccSmallest(nums);
        const want = max ? ccLargest(nums) : sm.best;
        const order = max ? ccSorted(s, true) : sm.order;
        const rows = max
          ? [["מיון של המספרים, מהגדול", ccNumSort(nums, true)], ["מיון של המחרוזות, מהגדולה", ccStrSort(nums, true)],
            [`לפי ${ltr("a ‖ b")} מול ${ltr("b ‖ a")}`, ccSorted(s, true)]]
          : [["מיון של המספרים, מהקטן", ccNumSort(nums, false)], [`לפי ${ltr("a ‖ b")} מול ${ltr("b ‖ a")}`, ccSorted(s, false)],
            ["והראשון שאינו 0 קדימה", ccShortcut(nums)], ["כל ראשון אפשרי (סעיף ג)", sm.order]];
        const allZero = s.every((x) => x === "0");
        let html = "";
        rows.forEach(([name, ord]) => {
          const j = join(s, ord), lead = j[0] === "0" && !allZero;
          const ok = (allZero ? "0" : j) === want && !lead;
          const res = lead ? "מתחיל ב-0" : ok ? "נכון" : j < want ? "קטן יותר" : "גדול יותר";
          html += `<tr class="${ok ? "is-right" : "is-wrong"}"><th scope="row">${name}</th><td>${joined(s, ord, allZero ? j : want)}</td><td class="cc-res">${res}</td></tr>`;
        });
        $(".cc-rows tbody").innerHTML = html;
        $(".cc-linewrap").innerHTML = lineSvg(s, order, st.pair);
        $(".cc-pair").innerHTML = pairHtml(s);
        const cands = $(".cc-cands");
        if (max) { cands.hidden = true; cands.innerHTML = ""; } else {
          cands.hidden = false;
          cands.innerHTML = sm.cands.length
            ? `<p class="cc-head">המועמדים${NB}: ראשון שאינו 0, ${ltr(String(s.filter((x) => x === "0").length))} אפסים והשאר</p>` +
              `<div class="cc-cscroll" tabindex="0" role="region" aria-label="המועמדים של סעיף ג"><table class="cc-ctab"><tbody>${sm.cands.map(([x, ord, v]) =>
                `<tr class="${v === sm.best ? "is-right" : ""}"><th scope="row">${x}</th><td>${joined(s, ord, sm.best)}</td><td class="cc-res">${v === sm.best ? "הקטן" : ""}</td></tr>`).join("")}</tbody></table></div>`
            : `<p class="cc-head">כל המספרים 0, ולכן התשובה 0.</p>`;
        }
        const naive = max ? join(s, ccStrSort(nums, true)) : join(s, ccShortcut(nums));
        const naiveName = max ? "מיון המחרוזות נותן" : "ההזזה של הראשון שאינו 0 נותנת";
        $(".cc-sum").innerHTML = `${max ? "הגדול ביותר" : "הקטן ביותר"}${NB}: ${ltr(want)}. ` +
          (allZero ? "כל המספרים 0, ובמקום שרשור של אפסים התשובה היא 0." : `${naiveName} ${ltr(naive)}${naive === want ? ", גם הוא נכון כאן." : ", ולא זו התשובה."}`);
        $(".cc-note").innerHTML = st.err ? `<span class="cc-err">${st.err}</span>`
          : max ? `הסדר על הקו הוא הסדר בתשובה${NB}: מהערך הגבוה, מימין, לנמוך.`
            : `בקטן ביותר הקו נקרא משמאל, אבל הראשון נבחר מול האפסים שאחריו, ולא לפי הקו.`;
        answer(box, ltr(want), ".cc-rows tr.is-right .cc-join");
      };
      const setNums = (nums) => {
        st.nums = nums; st.err = "";
        st.pair = fixPair(nums, st.pair);
        syncFields(); draw();
      };
      $(".cc-preset").addEventListener("change", () => {
        const v = $(".cc-preset").value;
        if (v === "custom") { syncFields(); return; }
        st.pair = [0, 1];
        setNums(ccPresets[Number(v)][1].slice());
      });
      $(".cc-nums").addEventListener("change", () => {
        const v = ccParse($(".cc-nums").value);
        if (!v) { st.err = `צריך בין 1 ל-${NMAX} מספרים שלמים מ-0 עד ${VMAX}, מופרדים בפסיקים.`; draw(); return; }
        setNums(v);
      });
      $(".cc-mode").addEventListener("change", () => { st.mode = $(".cc-mode").value === "min" ? "min" : "max"; st.err = ""; draw(); });
      [".cc-a", ".cc-b"].forEach((sel, k) => $(sel).addEventListener("change", () => {
        st.pair[k] = Number($(sel).value);
        st.err = ""; draw();
      }));
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { nums: init.nums.slice(), mode: init.mode, pair: init.pair.slice(), err: "" });
        syncFields(); draw();
      });
      syncFields();
      draw();
    },
  });

  dvqExplorers.register({
    views: { concat: concatView },
    help: {
      concat: "בוחרים רשימה או כותבים עד 8 מספרים, ומחפשים את הגדול ביותר או את הקטן ביותר. הטבלה משווה מיונים ומסמנת את הספרה הראשונה שבה שרשור נופל מהתשובה. על הקו כל מספר הוא הערך a / (10^|a| − 1), עם המקום שלו בתשובה, ובשני השדות של הזוג בוחרים שני מספרים להשוואה. במצב הקטן ביותר מופיעים גם המועמדים של סעיף ג.",
    },
    cols: { concat: { main: ".cc-linewrap, .cc-legend, .cc-note", side: ".cc-pair, .cc-cands", w: "minmax(0, 1fr)" } },   // the sorts above, full width; the line, its legend and the note beside the pair and the candidates
    models: { ccOrder, ccSorted, ccLargest, ccSmallest, ccShortcut, ccNumSort, ccStrSort, ccDec, ccParse, ccPresets },
  });
})();
