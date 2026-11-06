// kinds: isqrt
//   isqrt                  0097        the integer square root of a 16-bit n, one result bit per step from bit 7 down: the root in binary with the bit being decided, a table of the eight steps (the trial 2rb + b², the remainder before it, in or out), and the square r² growing to (r + b)² by two r × b rectangles and a b × b square inside the dashed square of side √n
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, f, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAX = 65535;
  const BITS = 8;

  // The square root of a 16-bit n, one result bit per step from bit 7 down (0097 part b):
  // rem = n − r² all along; the trial for bit k (b = 2^k) is 2rb + b², the root shifted by
  // k + 1 OR one bit at 2k; when it fits, it is subtracted and the bit is set.
  const isqSteps = (n) => {
    let r = 0, rem = n;
    const out = [];
    for (let k = BITS - 1; k >= 0; k--) {
      const b = 2 ** k, trial = r * 2 ** (k + 1) + 2 ** (2 * k), before = rem, ok = trial <= rem;
      if (ok) { rem -= trial; r += b; }
      out.push({ k, b, trial, before, ok, r, rem });
    }
    return out;
  };
  const isqRoot = (n) => { const s = isqSteps(n)[BITS - 1]; return [s.r, s.rem]; };

  // The box: n typed (or a preset), then the bits decided one by one. Beside the table of
  // the steps, the step as areas: r² (blue), the two r × b rectangles and the b × b square
  // of the trial (green when it fits, orange when it does not), inside the dashed square
  // of side √n. The scale follows the step, so the trial always fits in the frame.
  const PRESETS = [[1000, "1000, הדוגמה של העמוד"], [65535, "65535, הגדול ביותר"], [4096, "4096 = 64², ריבוע"],
    [4095, "4095, אחד לפני ריבוע"], [2, "2"]];
  const S = 300, PAD = 12, LEFT = 34;
  const isqrtView = () => ({
    mount(box) {
      const N0 = Math.min(MAX, Math.max(0, Math.floor(Number(box.dataset.n ?? 1000)) || 0));
      const st = { n: N0, t: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>${ltr("n")}</span><input type="number" class="ex-num isq-n" min="0" max="${MAX}" step="1" value="${N0}" dir="ltr" inputmode="numeric" aria-label="n, מספר של 16 ביטים"></label>` +
        `<label>דוגמה <select class="isq-pre" data-nolink aria-label="דוגמה מוכנה"><option value="">בחרו</option>${PRESETS.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button><span class="fl-err isq-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">ביט אחד אחורה</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הביט הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 900, 400) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary isq-sum" aria-live="polite"></p>` +
        `<div class="isq-grid" data-steady>` +
        `<div class="isq-left"><p class="ex-title">השורש ${ltr("r")} בבינארי</p><div class="isq-rrow"></div>` +
        `<div class="isq-tabwrap"></div></div>` +
        `<div class="isq-right"><p class="ex-title">השלב כשטחים</p><div class="isq-pic"></div></div></div>` +
        `<span class="viz-legend"><span><i class="isq-key-old"></i>${ltr("r²")} עד עכשיו</span>` +
        `<span><i class="isq-key-add"></i>הניסיון ${ltr("2rb + b²")} כשהוא נכנס</span>` +
        `<span><i class="isq-key-miss"></i>ניסיון שלא נכנס</span>` +
        `<span><i class="isq-key-bound"></i>הריבוע של ${ltr("√n")}</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".isq-n");

      const bitRow = (steps) => {
        const r = st.t ? steps[st.t - 1].r : 0, now = st.t ? steps[st.t - 1].k : -1;
        let cells = "";
        for (let k = BITS - 1; k >= 0; k--) {
          const decided = k >= BITS - st.t, on = decided && ((r >> k) & 1);
          cells += `<td class="gs-b isq-rb${decided ? (on ? " isq-on" : " isq-off") : " isq-undec"}${k === now ? " is-now" : ""}">${decided ? (on ? 1 : 0) : "?"}</td>`;
        }
        const head = Array.from({ length: BITS }, (_, i) => `<td class="isq-ix">${BITS - 1 - i}</td>`).join("");
        return `<table class="gs-bits isq-rbits" dir="ltr" aria-label="השורש בבינארי, ביטים 7 עד 0"><tbody><tr>${head}<td></td></tr>` +
          `<tr>${cells}<td class="isq-val">= ${r}</td></tr></tbody></table>`;
      };
      const table = (steps) => {
        let s = `<table class="isq-steps" aria-label="שמונת השלבים"><thead><tr><th>ביט</th><th>הניסיון</th><th>השארית</th><th>נכנס?</th></tr></thead><tbody>`;
        steps.forEach((p, i) => {
          const done = i < st.t, now = i === st.t - 1;
          s += `<tr class="${done ? "is-done" : "is-todo"}${now ? " is-now" : ""}"><td>${p.k}</td>` +
            (done ? `<td>${p.trial}</td><td>${p.before}</td><td class="${p.ok ? "isq-yes" : "isq-no"}">${p.ok ? "כן ✓" : "לא ✗"}</td>`
              : `<td>–</td><td>–</td><td>–</td>`) + `</tr>`;
        });
        return s + `</tbody></table>`;
      };
      const picture = (steps) => {
        const n = st.n, root = Math.sqrt(n);
        const p = st.t ? steps[st.t - 1] : null;
        const r = p ? (st.t > 1 ? steps[st.t - 2].r : 0) : 0, b = p ? p.b : 0;
        const side = Math.max(r + b, root, 1), u = (S - LEFT - PAD) / side;
        const x0 = LEFT, y0 = PAD, rr = r * u, bb = b * u, sq = root * u;
        const cls = p && p.ok ? "isq-sq-add" : "isq-sq-miss";
        const lab = (x, y, w, h, v) => (w > 34 && h > 18 ? `<text class="isq-lab" x="${f(x + w / 2)}" y="${f(y + h / 2 + 5)}" text-anchor="middle">${v}</text>` : "");
        const aria = p
          ? `ביט ${p.k} : ‏r² = ${r * r}, ועוד שני מלבנים של ${r} על ${b} וריבוע של ${b} על ${b}, יחד ${p.trial}, ${p.ok ? "נכנסים" : "לא נכנסים"} בשארית ${p.before}`
          : `עוד לא הוחלט אף ביט : ‏r = 0, והריבוע המקווקו הוא √${n}`;
        let s = `<svg class="figure isq-fig isq-live" viewBox="0 0 ${S} ${S}" role="img" aria-label="${aria}">`;
        if (rr > 0) s += `<rect class="isq-sq-old" x="${x0}" y="${y0}" width="${f(rr)}" height="${f(rr)}"/>` + lab(x0, y0, rr, rr, r * r);
        if (p) {
          s += `<rect class="${cls}" x="${f(x0 + rr)}" y="${y0}" width="${f(bb)}" height="${f(rr)}"/>` +
            `<rect class="${cls}" x="${x0}" y="${f(y0 + rr)}" width="${f(rr)}" height="${f(bb)}"/>` +
            `<rect class="${cls} isq-small" x="${f(x0 + rr)}" y="${f(y0 + rr)}" width="${f(bb)}" height="${f(bb)}"/>` +
            lab(x0 + rr, y0, bb, rr, r * b) + lab(x0, y0 + rr, rr, bb, r * b) + lab(x0 + rr, y0 + rr, bb, bb, b * b);
        }
        s += `<rect class="isq-sq-bound" x="${x0}" y="${y0}" width="${f(sq)}" height="${f(sq)}"/>`;
        // the sides along the left edge
        if (rr > 14) s += `<text class="tick" x="${x0 - 6}" y="${f(y0 + rr / 2 + 5)}" text-anchor="end">${r}</text>`;
        if (p && bb > 14) s += `<text class="tick" x="${x0 - 6}" y="${f(y0 + rr + bb / 2 + 5)}" text-anchor="end">${b}</text>`;
        return s + `</svg>`;
      };

      const draw = () => {
        const steps = isqSteps(st.n);
        st.t = Math.min(Math.max(st.t, 0), BITS);
        if (document.activeElement !== input) input.value = String(st.n);
        $(".ex-pos").textContent = `ביט ${st.t} מתוך ${BITS}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.t === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.t === BITS;
        $(".isq-rrow").innerHTML = bitRow(steps);
        $(".isq-tabwrap").innerHTML = table(steps);
        $(".isq-pic").innerHTML = picture(steps);
        const p = st.t ? steps[st.t - 1] : null;
        if (!p) {
          $(".isq-sum").innerHTML = `מתחילים מ-${ltr("r = 0")} ומהשארית ${ltr(`rem = n = ${st.n}`)}. "הביט הבא" מחליט על ביט 7, ששווה 128.`;
        } else {
          const r0 = st.t > 1 ? steps[st.t - 2].r : 0;
          $(".isq-sum").innerHTML = `ביט ${ltr(p.k)}${NB}: הניסיון ${ltr(`2·${r0}·${p.b} + ${p.b}² = ${p.trial}`)}` +
            (p.ok ? ` נכנס בשארית ${ltr(p.before)}. מדליקים את הביט : ${ltr(`r = ${p.r}`)}, ונשארים ${ltr(`${p.before} − ${p.trial} = ${p.rem}`)}.`
              : ` גדול מהשארית ${ltr(p.before)}. הביט נשאר כבוי : ${ltr(`r = ${p.r}`)}.`);
        }
        if (st.t === BITS) {
          const [r, rem] = isqRoot(st.n);
          answer(box, `${ltr(`⌊√${st.n}⌋ = ${r}`)}, והשארית ${ltr(`${st.n} − ${r}² = ${rem}`)}`, ".isq-rbits .isq-val");
        } else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.t++; draw(); }, done: () => st.t >= BITS, restart: () => { st.t = 0; draw(); } });
      const set = (n) => { stop(); st.n = n; st.t = 0; $(".isq-err").textContent = ""; input.value = String(n); draw(); };
      input.addEventListener("change", () => {
        const x = Number(input.value);
        if (!Number.isInteger(x) || x < 0 || x > MAX) { $(".isq-err").textContent = `מספר שלם מ-0 עד ${MAX}`; input.value = String(st.n); return; }
        set(x);
      });
      // a preset moves n through the field, so the link and the remembered state follow it
      $(".isq-pre").addEventListener("change", () => {
        const v = $(".isq-pre").value;
        if (v === "") return;
        input.value = v;
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        $(".isq-pre").value = "";
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.t = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.t--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.t++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.t = BITS; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        input.value = String(N0);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { isqrt: isqrtView },
    help: {
      isqrt: "מקלידים n (או בוחרים דוגמה) ומתקדמים ביט אחד בכל פעם, מביט 7 למטה. הטבלה מראה בכל שלב את הניסיון 2rb + b², את השארית ואם הוא נכנס, והציור מראה את הריבוע r² עם שני המלבנים והריבוע הקטן של הניסיון, בתוך הריבוע המקווקו של √n. ניסיון שלא נכנס יוצא מהריבוע המקווקו.",
    },
    models: { isqSteps, isqRoot },
  });
})();
