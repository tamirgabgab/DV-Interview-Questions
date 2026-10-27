// kinds: mice
//   mice                   0051        n bottles, b rounds, a poisoned bottle: the mice by round (who drinks, who dies), the digits read back, the bottles still possible; a decoder mode with a hidden bottle
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, f, ltr } = dvqExplorers.lib;

  // Poisoned bottles (0051): m mice tell the bottle's m digits in base b + 1. Mouse i
  // drinks from bottle y in round d, d the i-th digit of y (0: never), so it dies in the
  // round of its digit of the poisoned bottle and lives when that digit is 0.
  const miceNeeded = (n, b) => { let m = 0, reach = 1; while (reach < n) { reach *= b + 1; m++; } return m; };
  const miceDigits = (x, b, m) => Array.from({ length: m }, (_, i) => Math.floor(x / Math.pow(b + 1, i)) % (b + 1));
  const miceDeath = (x, m, b) => miceDigits(x, b, m);        // the round each mouse dies in, 0: it lives
  const miceFind = (death, b) => death.reduceRight((x, d) => x * (b + 1) + d, 0);
  // The bottles still possible after round r: every mouse that died so far fixes its
  // digit; a mouse alive after round r says its digit is 0 or above r.
  const miceCands = (n, b, death, r) => {
    const out = [];
    for (let y = 0; y < n; y++) {
      const dg = miceDigits(y, b, death.length);
      if (dg.every((d, i) => (death[i] && death[i] <= r ? d === death[i] : d === 0 || d > r))) out.push(y);
    }
    return out;
  };

  // The box (0051): bottles, rounds and the poisoned bottle; the rounds stepped one at a
  // time; a grid of the mice (columns, mouse 0 on the right) by round (rows) with the
  // number of bottles each mouse drinks from in that round and where it dies; the digits
  // read so far; the bottles still possible. "I decode" hides a random bottle and the
  // digits, and asks for the bottle from the deaths.
  const GRID_MAX = 120;
  const miceView = () => ({
    mount(box) {
      const d0 = { n: Number(box.dataset.n || 1000), b: Number(box.dataset.rounds || 2), x: Number(box.dataset.poison || 613) };
      const st = { ...d0, r: 0, quiz: false, secret: 0, solved: false };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>בקבוקים n</span><input type="number" class="ex-num mc-n" min="2" max="4096" step="1" value="${st.n}" dir="ltr" inputmode="numeric" aria-label="מספר הבקבוקים, 2 עד 4096"></label>` +
        `<label>סבבים b <select class="mc-b" aria-label="מספר הסבבים">${[1, 2, 3, 4, 5].map((v) => `<option value="${v}"${v === st.b ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label class="mc-xlab"><span>הבקבוק המורעל</span><input type="number" class="ex-num mc-x" min="0" step="1" value="${st.x}" dir="ltr" inputmode="numeric" aria-label="מספר הבקבוק המורעל"></label>` +
        `<button type="button" class="md-button mc-rand">בקבוק אקראי</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err mc-err"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">לפני הסבב הראשון</button>` +
        `<button type="button" class="md-button ex-prev">הסבב הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הסבב הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הסבבים</button><span class="ex-pos"></span></div>` +
        `<label class="mc-quizlab"><input type="checkbox" class="mc-quiz"> אני מפענח : התיבה מסתירה בקבוק, ואני מוצא אותו מהעכברים שמתו</label>` +
        `<div class="ex-controls mc-guessrow" hidden><label><span>הבקבוק לפי העכברים</span><input type="number" class="ex-num mc-guess" data-nolink min="0" step="1" dir="ltr" inputmode="numeric" aria-label="הניחוש שלי למספר הבקבוק"></label>` +
        `<button type="button" class="md-button md-button--primary mc-check">בדיקה</button><button type="button" class="md-button mc-show">הצגת הבקבוק</button><button type="button" class="md-button mc-new">בקבוק חדש</button></div>` +
        `<p class="ex-summary mc-sum" aria-live="polite"></p>` +
        `<div class="mc-grid"></div>` +
        `<span class="viz-legend"><span><i class="mc-key-drink"></i>שותה בסבב (מספר הבקבוקים)</span><span><i class="mc-key-dead"></i>מת בסוף הסבב</span><span><i class="mc-key-gone"></i>כבר מת</span></span>` +
        `<p class="mc-read"></p><div class="mc-cands"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const bad = () => $(".mc-err").textContent !== "";
      const poison = () => (st.quiz ? st.secret : st.x);
      const grid = (m, death) => {
        // mice as columns (mouse 0 on the right, like the lowest digit), rounds as rows
        const W = 640, LW = 92, top = 58, RH = 46, cw = (W - LW - 8) / Math.max(m, 1), H = top + st.b * RH + 52;
        const cx = (i) => W - 8 - cw * (i + 0.5);
        const counts = Array.from({ length: m }, () => Array(st.b + 1).fill(0));
        for (let y = 0; y < st.n; y++) miceDigits(y, st.b, m).forEach((d, i) => { counts[i][d]++; });
        let s = `<svg class="figure mc-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${m} עכברים ב-${st.b} סבבים : מי שותה ומי מת בכל סבב">`;
        for (let i = 0; i < m; i++) {
          const dead = death[i] && death[i] <= st.r;
          s += `<g class="mc-mouse${dead ? " is-dead" : ""}"><circle cx="${f(cx(i))}" cy="30" r="${Math.min(18, cw / 2 - 3)}"/><text x="${f(cx(i))}" y="35" text-anchor="middle">${i}</text></g>`;
        }
        s += `<text class="mc-rowlab" x="${LW - 10}" y="35" text-anchor="start" direction="rtl">עכבר</text>`;
        for (let r = 1; r <= st.b; r++) {
          const y = top + (r - 1) * RH;
          s += `<text class="mc-rowlab${r === st.r ? " is-now" : ""}" x="${LW - 10}" y="${y + RH / 2 + 5}" text-anchor="start" direction="rtl">סבב ${r}</text>`;
          for (let i = 0; i < m; i++) {
            const done = r <= st.r, gone = done && death[i] && death[i] < r, dies = death[i] === r;
            const cls = !done ? "is-later" : gone ? "is-gone" : dies ? "is-death" : "is-drink";
            const what = gone ? "—" : String(counts[i][r]);
            s += `<g class="mc-cell ${cls}"><title>mouse ${i}, round ${r}: ${gone ? "already dead" : `drinks from ${counts[i][r]} bottles${done && dies ? ", dies" : ""}`}</title>` +
                 `<rect x="${f(cx(i) - cw / 2 + 2)}" y="${y + 3}" width="${f(cw - 4)}" height="${RH - 6}" rx="5"/>` +
                 `<text x="${f(cx(i))}" y="${y + RH / 2 + 5}" text-anchor="middle">${done && dies ? "✗" : what}</text></g>`;
          }
        }
        const yd = top + st.b * RH + 30;
        s += `<text class="mc-rowlab" x="${LW - 10}" y="${yd}" text-anchor="start" direction="rtl">הספרה</text>`;
        const hide = st.quiz && !st.solved;
        for (let i = 0; i < m; i++) {
          const known = (death[i] && death[i] <= st.r) || st.r === st.b;
          s += `<text class="mc-digit${known && !hide ? " is-known" : ""}" x="${f(cx(i))}" y="${yd}" text-anchor="middle">${known && !hide ? (death[i] && death[i] <= st.r ? death[i] : 0) : "?"}</text>`;
        }
        return s + "</svg>";
      };
      const draw = () => {
        if (bad()) return;
        const m = miceNeeded(st.n, st.b), x = poison(), death = miceDeath(x, m, st.b), base = st.b + 1;
        $(".mc-b").value = String(st.b);
        $(".mc-xlab").hidden = st.quiz; $(".mc-rand").hidden = st.quiz;
        $(".mc-guessrow").hidden = !st.quiz;
        $(".ex-pos").textContent = `סבב ${st.r} מתוך ${st.b}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.r === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.r === st.b;
        $(".mc-sum").innerHTML = `${ltr(st.n)} בקבוקים ו-${st.b === 1 ? "סבב אחד" : `${ltr(st.b)} סבבים`} : לכל עכבר ${ltr(base)} תוצאות, ולכן ${ltr(m)} עכברים, כי ` +
          `${ltr(`${base}^${m} = ${Math.pow(base, m).toLocaleString("en-US")} ≥ ${st.n}`)}` + (m > 0 ? ` ו-${ltr(`${base}^${m - 1} = ${Math.pow(base, m - 1).toLocaleString("en-US")} < ${st.n}`)}.` : ".") +
          (st.quiz ? " הבקבוק המורעל מוסתר." : ` הבקבוק המורעל ${ltr(x)}, בבסיס ${ltr(base)} : ${code([...miceDigits(x, st.b, m)].reverse().join("") || "0")}.`);
        $(".mc-grid").innerHTML = grid(m, death);
        const known = death.map((d, i) => (d && d <= st.r ? d : st.r === st.b ? 0 : null));
        const cands = miceCands(st.n, st.b, death, st.r);
        const read = st.r === 0 ? "עוד לא עבר אף סבב : כל עכבר יכול עוד להיות כל ספרה."
          : st.quiz && !st.solved ? `אחרי סבב ${ltr(st.r)} : ${death.filter((d) => d && d <= st.r).length} עכברים מתו. הסבב שבו עכבר מת הוא הספרה שלו, ומי ששרד את כל הסבבים הוא 0.`
          : st.r < st.b ? `אחרי סבב ${ltr(st.r)} : מי שמת עד עכשיו כבר אמר את הספרה שלו; מי שחי יאמר אותה בהמשך (0 אם ישרוד עד הסוף).`
          : `כל הספרות ידועות : ${ltr(`${known.map((d, i) => `${d}·${base}^${i}`).reverse().join(" + ")} = ${miceFind(death, st.b)}`)}` + (st.quiz ? "" : ` ✓`);
        $(".mc-read").innerHTML = read;
        $(".mc-cands").innerHTML = `<p class="ex-title">הבקבוקים שעדיין אפשריים : ${ltr(cands.length)} מתוך ${ltr(st.n)}</p>` +
          (st.quiz && !st.solved ? `<p class="ex-note">רשת הבקבוקים מוסתרת עד שהבקבוק נמצא.</p>`
            : st.n <= GRID_MAX ? `<div class="mc-bottles" dir="ltr">${Array.from({ length: st.n }, (_, y) => `<span class="mc-bottle${cands.includes(y) ? "" : " is-out"}${y === x && !(st.quiz && !st.solved) ? " is-bad" : ""}">${y}</span>`).join("")}</div>`
            : `<p class="ex-note">רשת הבקבוקים מוצגת עד ${GRID_MAX} בקבוקים.</p>`);
      };
      const setField = () => {
        const n = Math.round(Number($(".mc-n").value)), x = Math.round(Number($(".mc-x").value));
        const err = !(n >= 2 && n <= 4096) ? "מספר הבקבוקים : 2 עד 4096" : !(x >= 0 && x < n) ? `הבקבוק המורעל : 0 עד ${n - 1}` : "";
        $(".mc-err").textContent = err;
        if (err) return;
        st.n = n; st.x = x; st.r = Math.min(st.r, st.b);
        if (st.secret >= n) st.secret = Math.floor(Math.random() * n);
        draw();
      };
      const say = (cls, html) => { const p = $(".mc-read"); p.innerHTML = `<span class="${cls}">${html}</span> ` + p.innerHTML; };
      const fresh = () => { st.secret = Math.floor(Math.random() * st.n); st.solved = false; st.r = 0; $(".mc-guess").value = ""; draw(); };
      $(".mc-n").addEventListener("change", setField);
      $(".mc-x").addEventListener("change", setField);
      [".mc-n", ".mc-x", ".mc-guess"].forEach((s) => $(s).addEventListener("keydown", (e) => { if (e.key === "Enter") $(s).blur(); }));
      $(".mc-b").addEventListener("change", () => { st.b = Number($(".mc-b").value); st.r = 0; st.solved = false; draw(); });
      $(".mc-rand").addEventListener("click", () => { st.x = Math.floor(Math.random() * st.n); $(".mc-x").value = st.x; st.r = 0; draw(); });
      $(".mc-quiz").addEventListener("change", () => { st.quiz = $(".mc-quiz").checked; if (st.quiz) fresh(); else draw(); });
      $(".ex-start").addEventListener("click", () => { st.r = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { st.r = Math.max(0, st.r - 1); draw(); });
      $(".ex-next").addEventListener("click", () => { st.r = Math.min(st.b, st.r + 1); draw(); });
      $(".ex-end").addEventListener("click", () => { st.r = st.b; draw(); });
      $(".mc-check").addEventListener("click", () => {
        const g = Number($(".mc-guess").value);
        if ($(".mc-guess").value.trim() === "" || !Number.isInteger(g)) { draw(); say("wv-bad", "הקלידו מספר בקבוק."); return; }
        if (st.r < st.b) { draw(); say("wv-bad", "קודם עוברים את כל הסבבים : מי ששרד עד הסוף הוא הספרה 0."); return; }
        if (g === st.secret) { st.solved = true; draw(); say("wv-ok", `✓ נכון, הבקבוק ${ltr(st.secret)}.`); return; }
        draw(); say("wv-bad", `✗ לא ${ltr(g)}. רמז : הספרה של עכבר i שווה לסבב שבו הוא מת, והמשקל שלה ${ltr(`${st.b + 1}^i`)}.`);
      });
      $(".mc-show").addEventListener("click", () => { st.r = st.b; st.solved = true; draw(); say("wv-ok", `הבקבוק ${ltr(st.secret)}.`); });
      $(".mc-new").addEventListener("click", fresh);
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, d0, { r: 0, quiz: false, solved: false });
        $(".mc-n").value = st.n; $(".mc-x").value = st.x; $(".mc-quiz").checked = false; $(".mc-err").textContent = ""; draw();
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { mice: miceView },
    help: {
      mice: "בוחרים מספר בקבוקים, מספר סבבים ובקבוק מורעל, ועוברים סבב אחרי סבב : בכל משבצת מספר הבקבוקים שהעכבר שותה מהם בסבב, ו-✗ במקום שבו הוא מת. השורה התחתונה היא הספרות שנקראו, ומתחת הבקבוקים שעדיין אפשריים. ״אני מפענח״ מסתיר בקבוק אקראי : עוברים את הסבבים, וכותבים את מספר הבקבוק מהעכברים שמתו.",
    },
    models: { miceNeeded, miceDigits, miceDeath, miceFind, miceCands },
  });
})();
