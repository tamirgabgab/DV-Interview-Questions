// kinds: kaprekar
//   kaprekar               0012, 0013  a number, its sort-and-subtract chain to 495 / 6174, the histogram of chain lengths; a toggle for the first step as a column subtraction with the borrows
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, f, frame, ltr, seedControls } = dvqExplorers.lib;

  // Sort the digits and subtract (0012 with 3 digits, 0013 with 4): one step of the
  // routine, the chain of steps until the value stops changing (495 or 6174, or 0 for
  // repeated digits), and the distribution of chain lengths over every number.
  const kapStep = (x, d) => {
    const digits = String(x).padStart(d, "0").split("").sort();
    const smallest = Number(digits.join("")), largest = Number(digits.slice().reverse().join(""));
    return { x, digits: digits.slice().reverse().join(""), largest, smallest, diff: largest - smallest, special: largest - smallest === x };
  };
  // The column subtraction of the proof: largest minus smallest digit by digit from the
  // units, each column's borrow in and out and the digit it leaves.
  const kapColumns = (largest, smallest, d) => {
    const top = String(largest).padStart(d, "0"), bot = String(smallest).padStart(d, "0"), cols = [];
    let borrow = 0;
    for (let i = d - 1; i >= 0; i--) {
      const v = Number(top[i]) - Number(bot[i]) - borrow, out = v < 0 ? 1 : 0;
      cols.unshift({ top: Number(top[i]), bottom: Number(bot[i]), borrowIn: borrow, borrowOut: out, digit: v + 10 * out });
      borrow = out;
    }
    return cols;
  };
  const kapChain = (x, d, cap = 12) => {
    const steps = [];
    let v = x;
    for (let k = 0; k < cap; k++) {
      const s = kapStep(v, d);
      steps.push(s);
      if (s.diff === v) break;
      v = s.diff;
    }
    const last = steps[steps.length - 1];
    return { steps, end: last.diff, length: steps.length - 1, fixed: last.diff === last.x };
  };
  const kapHistogram = (d) => {
    const hist = {}, ends = {};
    for (let x = 0; x < Math.pow(10, d); x++) {
      const c = kapChain(x, d);
      const key = c.end;
      ends[key] = (ends[key] || 0) + 1;
      if (!hist[key]) hist[key] = [];
      hist[key][c.length] = (hist[key][c.length] || 0) + 1;
    }
    return { hist, ends };
  };

  // The Kaprekar box (0012, 0013): a typed or random number, its sort-and-subtract step,
  // the chain of steps until the value stops changing, and a histogram of chain lengths
  // over every number with the typed one marked.
  const kaprekarView = () => ({
    mount(box) {
      const d = Number(box.dataset.digits || 3), MAX = Math.pow(10, d) - 1;
      const FIXED = d === 3 ? 495 : 6174;
      const presets = (box.dataset.presets || (d === 3 ? "352,7,45,111,0" : "3524,95,1000,7777,0")).split(",").map(Number);
      const st = { x: Number(box.dataset.x || presets[0]) };
      const pad = (v) => String(v).padStart(d, "0");
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls"><label><span>המספר</span><input type="number" class="ex-x" min="0" max="${MAX}" step="1" dir="ltr" aria-label="מספר בין 0 ל-${MAX}"></label>` +
        `<button type="button" class="md-button md-button--primary ex-random">הגרלה</button>` +
        `<span class="kp-presets">דוגמאות : ` + presets.map((p) => `<button type="button" class="md-button ex-preset" data-x="${p}">${p}</button>`).join(" ") + `</span></div>` +
        `<div class="kp-table"></div><p class="kp-chain" aria-live="polite"></p>` +
        `<label><input type="checkbox" class="ex-cols" checked> החיסור במאונך של הצעד הראשון</label><div class="kp-cols"></div>` +
        `<p class="ex-title">מספר הצעדים עד שהערך מפסיק להשתנות, על כל ${ltr(num(MAX + 1))} המספרים; המספר שלכם מסומן</p><div class="kp-chart"></div><p class="ex-summary kp-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".ex-x");
      const H = kapHistogram(d);
      const draw = () => {
        const c = kapChain(st.x, d);
        if (document.activeElement !== input) input.value = st.x;
        $(".kp-table").innerHTML = `<table tabindex="0" aria-label="צעדי המיון והחיסור"><thead><tr><th>צעד</th><th>המספר</th><th>מהגדול לקטן</th><th>מהקטן לגדול</th><th>ההפרש</th><th>מיוחד?</th></tr></thead><tbody>` +
          c.steps.map((s, k) => `<tr${k === c.steps.length - 1 ? ' class="is-last"' : ""}><td>${ltr(k + 1)}</td><td>${ltr(pad(s.x))}</td><td>${ltr(s.digits)}</td><td>${ltr(pad(s.smallest))}</td><td>${ltr(pad(s.diff))}</td><td>${s.special ? "✓" : "✗"}</td></tr>`).join("") +
          `</tbody></table>`;
        const chain = c.steps.map((s) => pad(s.x)).concat(c.fixed ? [] : [pad(c.end)]);
        const first = c.steps[0];
        let text = first.special
          ? `<b>${ltr(pad(st.x))} מיוחד :</b> ההפרש שלו הוא הוא עצמו, ולכן השרשרת לא זזה.`
          : `${ltr(pad(st.x))} לא מיוחד. מפעילים את הצעד שוב על ההפרש : ${ltr(chain.join(" → "))}` +
            (c.fixed ? `, ואחרי ${c.length === 1 ? "צעד אחד" : `${ltr(c.length)} צעדים`} מגיעים ל-<b>${ltr(pad(c.end))}</b>, שהוא מיוחד ונשאר.` : `, ועדיין לא נעצר.`);
        if (c.end === 0 && !first.special) text += ` כל הספרות שוות, ולכן ההפרש הוא 0 ושם זה נגמר.`;
        $(".kp-chain").innerHTML = text;
        // the first step as a column subtraction, units first, with the borrows; the digits
        // the page's p and q predict beside it
        if ($(".ex-cols").checked) {
          const s0 = c.steps[0], cols = kapColumns(s0.largest, s0.smallest, d), ds = s0.digits.split("").map(Number);
          const p = ds[0] - ds[d - 1], q = d === 4 ? ds[1] - ds[2] : null;
          const NAMES = ["אחדות", "עשרות", "מאות", "אלפים"];
          const cell = (v, cls = "") => `<td class="${cls}">${v}</td>`;
          const head = cols.map((col, i) => cell(NAMES[d - 1 - i], "kp-col-name")).join("");
          const borrows = cols.map((col) => cell(col.borrowOut ? "1" : "", col.borrowOut ? "kp-borrow" : "")).join("");
          $(".kp-cols").innerHTML = `<table class="kp-sub" dir="ltr"><tbody><tr><td></td>${head}</tr><tr><td class="kp-col-name">לווה</td>${borrows}</tr>` +
            `<tr><td></td>${cols.map((col) => cell(col.top)).join("")}</tr><tr><td>−</td>${cols.map((col) => cell(col.bottom)).join("")}</tr>` +
            `<tr class="kp-res"><td>=</td>${cols.map((col) => cell(col.digit, col.borrowOut ? "kp-lent" : "")).join("")}</tr></tbody></table>` +
            `<p class="ex-note">${p === 0 ? "כל הספרות שוות, ולכן ההפרש 0 בלי שום לווה." :
              `החיסור מהאחדות שמאלה. ${cols.filter((col) => col.borrowOut).map((col) => NAMES[d - 1 - cols.indexOf(col)]).join(", ")} ${cols.filter((col) => col.borrowOut).length === 1 ? "לווה" : "לוות"} מהעמודה שמשמאל (ה-1 מעל). ` +
              (d === 4 ? `עם ${ltr(`p = ${ds[0]} − ${ds[3]} = ${p}`)} ו-${ltr(`q = ${ds[1]} − ${ds[2]} = ${q}`)} הדף צופה ${q >= 1 ? ltr(`p, q − 1, 9 − q, 10 − p = ${p}, ${q - 1}, ${9 - q}, ${10 - p}`) : ltr(`p − 1, 9, 9, 10 − p = ${p - 1}, 9, 9, ${10 - p}`)}${q === 0 ? " (q = 0, ולכן גם המאות לוות)" : ""}.`
                : `עם ${ltr(`p = ${ds[0]} − ${ds[2]} = ${p}`)} הספרות הן ${ltr(`p − 1, 9, 10 − p = ${p - 1}, 9, ${10 - p}`)}.`)}</p>`;
        } else $(".kp-cols").innerHTML = "";
        const hist = H.hist[FIXED] || [], hist0 = H.hist[0] || [];
        const n = Math.max(hist.length, hist0.length);
        const vals = Array.from({ length: n }, (_, k) => (hist[k] || 0) + (hist0[k] || 0));
        const ymax = Math.max(...vals), ticks = [];
        const stepT = ymax > 4000 ? 1000 : ymax > 400 ? 100 : 50;
        for (let v = 0; v <= ymax + stepT - 1; v += stepT) ticks.push(v);
        const fr = frame("התפלגות מספר הצעדים", n, ticks[ticks.length - 1], ticks, (v) => num(v));
        let s = fr.s;
        vals.forEach((v, k) => {
          const bw = Math.max(fr.slot * 0.6, 1), cls = k === c.length ? "by-enum" : "by-multiples";
          s += `<rect class="bar ${cls}" x="${f(fr.cx(k + 1) - bw / 2)}" y="${f(fr.Y(v))}" width="${f(bw)}" height="${f(BASE - fr.Y(v))}"><title>${k} צעדים : ${num(v)} מספרים (${num(hist[k] || 0)} מגיעים ל-${FIXED}, ${num(hist0[k] || 0)} ל-0)</title></rect>` +
               `<text class="tick" x="${f(fr.cx(k + 1))}" y="${f(fr.Y(v) - 4)}" text-anchor="middle" font-size="10">${num(v)}</text>` + fr.xtick(k + 1, k);
        });
        $(".kp-chart").innerHTML = s + fr.close();
        const toFixed = H.ends[FIXED] || 0, toZero = H.ends[0] || 0, longest = hist.length - 1;
        $(".kp-sum").innerHTML = `מתוך ${ltr(num(MAX + 1))} המספרים, ${ltr(num(toFixed))} מגיעים ל-${ltr(FIXED)} (אחרי ${ltr(longest)} צעדים לכל היותר) ו-${ltr(num(toZero))} מגיעים ל-0 : אלה המספרים שכל הספרות שלהם שוות${d === 3 ? "" : ""}. ` +
          `רק ${ltr(`0 ו-${FIXED}`)} מיוחדים, כלומר נעצרים ב-0 צעדים.`;

      };
      const set = (x) => { if (Number.isInteger(x) && x >= 0 && x <= MAX) st.x = x; draw(); };
      input.addEventListener("change", () => set(Math.round(Number(input.value))));
      $(".ex-cols").addEventListener("change", draw);
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") input.blur(); });
      const seed = seedControls(box, $(".kp-presets"), (rng) => set(Math.floor(rng() * (MAX + 1))));
      $(".ex-random").addEventListener("click", seed.draw);
      box.querySelectorAll(".ex-preset").forEach((b) => b.addEventListener("click", () => set(Number(b.dataset.x))));
      draw();
    },
  });

  dvqExplorers.register({
    views: { kaprekar: kaprekarView },
    help: {
      kaprekar: "מקלידים או מגרילים מספר : ״הצעד הבא״ ממיין ומחסר עד 495 או 6174, וההיסטוגרמה סופרת את אורכי השרשראות של כל המספרים. המתג ״החיסור במאונך״ מראה את הצעד הראשון עמודה אחרי עמודה, עם הלווים.",
    },
    models: { kapStep, kapColumns, kapChain, kapHistogram },
  });
})();
