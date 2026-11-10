// kinds: ffn
//   ffn                    0076        f(f(n)) = 3n: n typed or stepped along the chain; n, f(n) and f(f(n)) = 3n with their base-3 digits (the leading digit and the appended 0 marked), the interval [3^k, 3^(k+1)] with its two halves and n on it, and the value worked out from the anchors 3^k and 2·3^k
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, f, ltr } = dvqExplorers.lib;
  const NB = " ";
  const SUP = "⁰¹²³⁴⁵⁶⁷⁸⁹";
  const pow3 = (k) => `3${[...String(k)].map((c) => SUP[c]).join("")}`;   // 3², 3¹⁰
  const MAX = 999999999;            // 3n stays an exact integer far below 2^53

  // The unique strictly increasing f with f(f(n)) = 3n (0076 part b): with
  // 3^k <= n < 3^(k+1), f(n) = n + 3^k on the first half [3^k, 2·3^k] and 3n − 3^(k+1)
  // on the second half [2·3^k, 3^(k+1)]; the two formulas agree at 2·3^k.
  const ffSplit = (n) => {
    let p = 1, k = 0;
    while (3 * p <= n) { p *= 3; k++; }
    const half = n <= 2 * p ? 1 : 2;
    return { n, k, p, mid: 2 * p, top: 3 * p, half, value: half === 1 ? n + p : 3 * n - 3 * p };
  };
  const ffValue = (n) => ffSplit(n).value;
  const ffBase3 = (n) => Number(n).toString(3);
  // The base-3 rule: leading 1 becomes 2; leading 2 becomes 1 and a 0 is appended.
  const ffRule = (n) => {
    const d = ffBase3(n);
    return d[0] === "1" ? `2${d.slice(1)}` : `1${d.slice(1)}0`;
  };

  // The box (0076 part b): a field for n with −1, +1 and "the next step of the chain"
  // (n becomes f(n)); a table of n, f(n) and f(f(n)) = 3n in base 3, right aligned so
  // the digits line up, the leading digit of n and of f(n) marked and the 0 that 3n adds
  // dashed; the interval [3^k, 3^(k+1)] with its two halves and n on it; and two lines
  // that work out f(n) and f(f(n)) from the anchors.
  const W = 440, H = 128, XA = 64, XB = 376, Y = 58;
  // a tick label shrinks with its digits, so up to 3^19 (10 digits) it stays inside the
  // box and clear of the middle label
  const tickFont = (v) => Math.min(21, Math.floor(150 / String(v).length));
  const ffnView = () => ({
    mount(box) {
      const N0 = Math.min(MAX, Math.max(1, Math.floor(Number(box.dataset.n || 14)) || 14));
      let n = N0;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>n</span><input type="number" class="ex-num ff-n" min="1" max="${MAX}" step="1" value="${N0}" dir="ltr" inputmode="numeric" aria-label="n, מספר טבעי"></label>` +
        `<button type="button" class="md-button ff-dec">n − 1</button>` +
        `<button type="button" class="md-button ff-inc">n + 1</button>` +
        `<button type="button" class="md-button md-button--primary ff-next">הבא בשרשרת</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button><span class="fl-err ff-err"></span></div>` +
        `<p class="ex-summary ff-sum" aria-live="polite"></p>` +
        `<p class="ex-title">השרשרת בבסיס 3</p><div class="ff-digits"></div>` +
        `<span class="viz-legend"><span><i class="ff-key-lead"></i>הספרה המובילה</span><span><i class="ff-key-zero"></i>ה-0 שנוסף בסוף</span></span>` +
        `<p class="ex-title ff-int-title"></p><div class="ff-line"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>החצי הראשון : שיפוע 1</span><span><i class="by-bfs"></i>החצי השני : שיפוע 3</span><span><i class="s2"></i>‏n</span></span>` +
        `<p class="ff-why ff-why1"></p><p class="ff-why ff-why2"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".ff-n");
      const why = (s, name, arg) => {
        const v = s.value;
        if (s.half === 1) {
          return `הערך ${ltr(`${name}(${arg})`)}${NB}: ${ltr(`${pow3(s.k)} = ${s.p} ≤ ${s.n} ≤ ${s.mid} = 2 · ${pow3(s.k)}`)}, החצי הראשון, ולכן ` +
            `${ltr(`${name}(${arg}) = ${s.n} + ${s.p} = ${v}`)}.`;
        }
        return `הערך ${ltr(`${name}(${arg})`)}${NB}: ${ltr(`2 · ${pow3(s.k)} = ${s.mid} ≤ ${s.n} ≤ ${s.top} = ${pow3(s.k + 1)}`)}, החצי השני, ולכן ` +
          `${ltr(`${name}(${arg}) = 3 · ${s.n} − ${s.top} = ${v}`)}.`;
      };
      const digitsTable = (rows) => {
        const width = Math.max(...rows.map((r) => r.digits.length));
        let t = `<table class="ff-table" aria-label="השרשרת בבסיס 3"><tbody>`;
        rows.forEach((r) => {
          t += `<tr><th scope="row">${r.label}</th>`;
          for (let i = 0; i < width - r.digits.length; i++) t += `<td class="ff-pad"></td>`;
          [...r.digits].forEach((ch, i) => {
            const cls = r.lead && i === 0 ? " is-lead" : r.zero && i === r.digits.length - 1 ? " is-zero" : "";
            t += `<td class="ff-d${cls}">${ch}</td>`;
          });
          t += `<td class="ff-val">= ${r.value}</td></tr>`;
        });
        return t + `</tbody></table>`;
      };
      const line = (s) => {
        const X = (v) => XA + ((v - s.p) * (XB - XA)) / (s.top - s.p);
        const xm = X(s.mid), xn = X(s.n);
        let g = `<svg class="figure ff-svg" viewBox="0 0 ${W} ${H}" style="max-width:28rem" role="img" aria-label="הקטע מ-${s.p} עד ${s.top}, החצי הראשון עד ${s.mid}, ו-n = ${s.n} בחצי ה${s.half === 1 ? "ראשון" : "שני"}">`;
        g += `<line class="s1-line" x1="${XA}" y1="${Y}" x2="${f(xm)}" y2="${Y}" stroke-width="${s.half === 1 ? 6 : 3}"/>`;
        g += `<line class="s3-line" x1="${f(xm)}" y1="${Y}" x2="${XB}" y2="${Y}" stroke-width="${s.half === 2 ? 6 : 3}"/>`;
        [[XA, s.p, pow3(s.k)], [xm, s.mid, `2·${pow3(s.k)}`], [XB, s.top, pow3(s.k + 1)]].forEach(([x, v, name]) => {
          g += `<line class="ink-line" x1="${f(x)}" y1="${Y - 9}" x2="${f(x)}" y2="${Y + 9}" stroke-width="1.5"/>` +
            `<text class="tick" x="${f(x)}" y="${Y + 34}" text-anchor="middle" style="font-size:${tickFont(v)}px">${v}</text>` +
            `<text class="tick" x="${f(x)}" y="${Y + 58}" text-anchor="middle" style="font-size:18px">${name}</text>`;
        });
        g += `<circle class="s2-dot" cx="${f(xn)}" cy="${Y}" r="8"><title>n = ${s.n}</title></circle>` +
          `<text class="legend" x="${f(Math.min(XB - 50, Math.max(XA + 50, xn)))}" y="${Y - 20}" text-anchor="middle" style="font-size:21px">n = ${s.n}</text>`;
        return g + `</svg>`;
      };
      const draw = () => {
        const s = ffSplit(n), v = s.value, t = ffSplit(v), w = t.value;
        if (document.activeElement !== input) input.value = String(n);
        $(".ff-sum").innerHTML = `בשרשרת${NB}: ${ltr(`f(${n}) = ${v}`)}, ו-${ltr(`f(${v}) = ${w} = 3 · ${n}`)} ✓`;
        $(".ff-digits").innerHTML = digitsTable([
          { label: "n", digits: ffBase3(n), value: n, lead: true },
          { label: "f(n)", digits: ffBase3(v), value: v, lead: true },
          { label: "f(f(n)) = 3n", digits: ffBase3(w), value: w, zero: true },
        ]);
        // a long n scrolls inside the box on a phone; only then is the strip a tab stop
        const strip = $(".ff-digits"), wide = strip.scrollWidth > strip.clientWidth + 1;
        if (wide) { strip.setAttribute("tabindex", "0"); strip.setAttribute("role", "region"); strip.setAttribute("aria-label", "השרשרת בבסיס 3, גלילה לצדדים"); }
        else ["tabindex", "role", "aria-label"].forEach((a) => strip.removeAttribute(a));
        $(".ff-int-title").innerHTML = `הקטע של n${NB}: מ-${ltr(`${pow3(s.k)} = ${s.p}`)} עד ${ltr(`${pow3(s.k + 1)} = ${s.top}`)}, והאמצע ${ltr(`2 · ${pow3(s.k)} = ${s.mid}`)}`;
        $(".ff-line").innerHTML = line(s);
        $(".ff-why1").innerHTML = why(s, "f", n);
        $(".ff-why2").innerHTML = why(t, "f", v) + ` זה ${ltr(`3 · ${n}`)}, כמו שהתנאי דורש.`;
        answer(box, `${ltr(`f(${n}) = ${v}`)}`);
        $(".ff-dec").disabled = n <= 1;
        $(".ff-next").disabled = v > MAX;
      };
      const set = (x) => { n = x; $(".ff-err").textContent = ""; input.value = String(n); draw(); };
      input.addEventListener("change", () => {
        const x = Number(input.value);
        if (!Number.isInteger(x) || x < 1 || x > MAX) { $(".ff-err").textContent = `מספר שלם מ-1 עד ${MAX}`; input.value = String(n); return; }
        set(x);
      });
      // a button moves n through the field, so the link and the remembered state follow it
      const move = (x) => { input.value = String(x); input.dispatchEvent(new Event("input", { bubbles: true })); input.dispatchEvent(new Event("change", { bubbles: true })); };
      $(".ff-dec").addEventListener("click", () => { if (n > 1) move(n - 1); });
      $(".ff-inc").addEventListener("click", () => { if (n < MAX) move(n + 1); });
      $(".ff-next").addEventListener("click", () => { const v = ffValue(n); if (v <= MAX) move(v); });
      $(".ex-reset").addEventListener("click", () => move(N0));
      draw();
    },
  });

  dvqExplorers.register({
    views: { ffn: ffnView },
    help: {
      ffn: "מקלידים n או מזיזים אותו ב-1 : הטבלה מראה את n, את f(n) ואת f(f(n)) = 3n בבסיס 3, עם הספרה המובילה וה-0 שנוסף, הקו מראה באיזה חצי של הקטע n נמצא, והשורות מתחת מחשבות כל ערך מהעוגנים. ״הבא בשרשרת״ מחליף את n ב-f(n).",
    },
    models: { ffSplit, ffValue, ffBase3, ffRule },
  });
})();
