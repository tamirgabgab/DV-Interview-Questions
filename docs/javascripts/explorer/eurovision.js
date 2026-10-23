// kinds: eurovision
//   eurovision             0008        the announcements one by one: the cups under Israel's total against the points left; a what-if box; the proof panel: the points left poured into the cups, the spill
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, H, TOP, W, X0, autoplay, f, ltr, speedSel } = dvqExplorers.lib;

  // Eurovision 2026 (0008): the grand final results, the announcement order (lowest jury
  // first), and the page's scan: after every announcement the public points left and the
  // room left under Israel's total; the first announcement after which Israel cannot win.
  const EURO_RESULTS = [
    ["Bulgaria", 204, 312], ["Israel", 123, 220], ["Romania", 64, 232], ["Australia", 165, 122], ["Italy", 134, 147],
    ["Finland", 141, 138], ["Denmark", 165, 78], ["Moldova", 43, 183], ["Ukraine", 54, 167], ["Greece", 73, 147],
    ["France", 144, 14], ["Poland", 133, 17], ["Albania", 60, 85], ["Norway", 115, 19], ["Croatia", 53, 71],
    ["Czechia", 104, 9], ["Serbia", 38, 52], ["Malta", 81, 8], ["Cyprus", 41, 34], ["Sweden", 35, 16],
    ["Belgium", 36, 0], ["Lithuania", 10, 12], ["Germany", 12, 0], ["Austria", 1, 5], ["United Kingdom", 1, 0],
  ];
  const EURO_PUBLIC_TOTAL = 36 * 58;
  // the order of the public announcements: by jury score, Denmark before Australia at 165
  const euroOrder = (results) => results.slice().sort((a, b) => a[1] - b[1] || (a[0] === "Australia") - (b[0] === "Australia"));
  // results with Israel's jury and public scores replaced (the "what if" box)
  const euroWithIsrael = (jury, pub) => EURO_RESULTS.map((r) => (r[0] === "Israel" ? ["Israel", jury, pub] : r));
  // the page's israel_cannot_win
  const euroCannotWin = (israelTotal, juryAbove, pointsLeft) => {
    let room = 0;
    for (const j of juryAbove) { if (j > israelTotal) return true; room += israelTotal - j; }
    return pointsLeft > room;
  };
  // the scan: one row per announcement from Israel's own on, with left, room and the verdict
  const euroScan = (results) => {
    const order = euroOrder(results);
    const idx = order.findIndex((r) => r[0] === "Israel");
    const total = order[idx][1] + order[idx][2];
    const above = order.slice(idx + 1);
    let left = EURO_PUBLIC_TOTAL - order.slice(0, idx + 1).reduce((s, r) => s + r[2], 0);
    let room = above.reduce((s, r) => s + Math.max(0, total - r[1]), 0);
    let lost = euroCannotWin(total, above.map((r) => r[1]), left);
    const rows = [{ country: "Israel", jury: order[idx][1], pub: order[idx][2], total, left, room, lost }];
    let passed = false;
    for (const [country, jury, pub] of above) {
      left -= pub;
      room -= Math.max(0, total - jury);
      passed = passed || jury + pub > total;
      lost = lost || passed || left > room;
      rows.push({ country, jury, pub, total: jury + pub, left, room, lost });
    }
    const first = rows.findIndex((r) => r.lost);               // 0 = right after Israel, -1 = never
    return { order, idx, total, above, rows, first, won: first < 0 };
  };

  // The pouring of the proof: after k announcements from Israel's own, the public points
  // left poured into the cups of the countries still to come, each up to Israel's total, in
  // their order; `share` (0 to 1) pours only that part, for the animation. What does not
  // fit spills: one more point in any cup takes that country past Israel.
  const euroPour = (results, k, share = 1) => {
    const sc = euroScan(results), row = sc.rows[k];
    let left = Math.round(row.left * share);
    const cups = sc.above.slice(k).map(([country, jury]) => {
      const room = Math.max(0, sc.total - jury), fill = Math.min(room, left);
      left -= fill;
      return { country, jury, room, fill };
    });
    return { cups, spill: left, total: sc.total, left: row.left, room: row.room };
  };

  // The Eurovision box (0008): a slider over the public announcements from Israel's own
  // to the last; the cups of the countries still to come (room under Israel's total)
  // against the points left, the moment of certain loss marked; a "what if" box for
  // Israel's own jury and public scores.
  const euroView = () => ({
    mount(box) {
      const st = { k: 0, jury: 123, pub: 220 };
      const num = (v) => Number(v).toLocaleString("en-US");
      box.innerHTML =
        `<div class="ex-controls"><label><span>הכרזות הקהל אחרי ישראל</span><input type="range" class="ex-k" min="0" max="7" step="1" value="0" dir="ltr"><output class="out-k"></output></label>` +
        `<button type="button" class="md-button ex-prev">הקודמת</button><button type="button" class="md-button md-button--primary ex-next">ההכרזה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(2200, 1300, 500) + `</div>` +
        `<div class="ex-controls eu-what"><span>מה אם לישראל היו</span><label>שופטים <input type="number" class="ex-jury" min="0" max="420" step="1" dir="ltr" aria-label="ניקוד השופטים של ישראל"></label>` +
        `<label>קהל <input type="number" class="ex-pub" min="0" max="432" step="1" dir="ltr" aria-label="ניקוד הקהל של ישראל"></label>` +
        `<button type="button" class="md-button ex-reset">הנתונים האמיתיים</button></div>` +
        `<div class="eu-chart"></div><p class="eu-step" aria-live="polite"></p><p class="ex-summary eu-sum"></p>` +
        `<section class="ex-proof eu-proof"><p class="ex-proof-title">שלב ההוכחה : מוזגים את הנקודות לכוסות</p>` +
        `<div class="ex-controls"><button type="button" class="md-button ex-pour">מזיגה</button></div>` +
        `<p class="ex-title eu-pour-title"></p><div class="eu-pour"></div>` +
        `<span class="viz-legend"><span><i class="by-multiples"></i>השופטים</span><span><i class="cup-room"></i>הכוס עד הסכום של ישראל</span><span><i class="pour-water"></i>הנקודות שנמזגו</span><span><i class="overflow"></i>נשפך</span></span>` +
        `<p class="eu-pour-text"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const slider = $(".ex-k");
      const draw = () => {
        const sc = euroScan(euroWithIsrael(st.jury, st.pub));
        const n = sc.rows.length - 1;
        slider.max = n; st.k = Math.min(st.k, n); slider.value = st.k;
        $(".out-k").textContent = `${st.k} / ${n}`;
        $(".ex-jury").value = st.jury; $(".ex-pub").value = st.pub;
        const row = sc.rows[st.k];
        // the cups: every country above Israel by the jury, announced or not
        const W = 640, H = 300, X0 = 48, BASE = 240, TOP = 20;
        const ymax = Math.max(sc.total, ...sc.above.map((r) => r[1] + r[2]), 1) * 1.08;
        const Y = (v) => BASE - (v / ymax) * (BASE - TOP);
        const slot = (W - X0 - 12) / Math.max(sc.above.length, 1), bw = slot * 0.6;
        let s = `<svg class="perf-chart eu-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="הכוסות של המדינות שמעל ישראל אחרי ${st.k} הכרזות">`;
        [0, 100, 200, 300, 400, 500].filter((v) => v < ymax).forEach((v) => {
          s += `<line class="grid" x1="${X0}" x2="${W - 12}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        });
        s += `<line class="s2-line" x1="${X0}" x2="${W - 12}" y1="${f(Y(sc.total))}" y2="${f(Y(sc.total))}" stroke-width="2" stroke-dasharray="6 4"/>` +
             `<text class="legend" x="${X0 + 4}" y="${f(Y(sc.total) - 6)}">Israel ${sc.total}</text>`;
        sc.above.forEach(([country, jury, pub], i) => {
          const x = X0 + i * slot + (slot - bw) / 2, announced = i < st.k, cx = x + bw / 2;
          s += `<rect class="bar by-multiples" x="${f(x)}" y="${f(Y(jury))}" width="${f(bw)}" height="${f(BASE - Y(jury))}"><title>${country} : שופטים ${jury}</title></rect>`;
          if (announced) {
            s += `<rect class="bar ${jury + pub > sc.total ? "by-enum" : "by-bfs"}" x="${f(x)}" y="${f(Y(jury + pub))}" width="${f(bw)}" height="${f(Y(jury) - Y(jury + pub))}"><title>${country} : קהל ${pub}, סך הכול ${jury + pub}</title></rect>`;
          } else if (jury < sc.total) {
            s += `<rect class="cup-room" x="${f(x)}" y="${f(Y(sc.total))}" width="${f(bw)}" height="${f(Y(jury) - Y(sc.total))}"><title>${country} : מקום פנוי ${sc.total - jury}</title></rect>`;
          }
          s += `<text class="tick" x="${f(cx)}" y="${BASE + 16}" text-anchor="middle" font-size="10">${country.length > 9 ? country.slice(0, 8) + "…" : country}</text>` +
               `<text class="tick" x="${f(cx)}" y="${BASE + 30}" text-anchor="middle" font-size="10">${announced ? jury + pub : jury}</text>`;
        });
        s += `<line class="axis" x1="${X0}" x2="${W - 12}" y1="${BASE}" y2="${BASE}"/></svg>`;
        $(".eu-chart").innerHTML = s;
        if (pourAnim) { cancelAnimationFrame(pourAnim); pourAnim = null; }
        drawPour();
        const left = row.left, room = row.room;
        let step = st.k === 0
          ? `מיד אחרי ההכרזה של ישראל (${ltr(`${sc.rows[0].jury} + ${sc.rows[0].pub} = ${sc.total}`)})  : `
          : `אחרי ההכרזה של ${ltr(row.country)} (${ltr(`${row.jury} + ${row.pub} = ${row.total}`)})  : `;
        step += `נותרו ${ltr(num(left))} נקודות קהל, והמקום הפנוי עד ${ltr(sc.total)} ב${n - st.k === 1 ? "כוס האחרונה" : `-${ltr(n - st.k)} הכוסות שנותרו`} הוא ${ltr(num(room))}. `;
        if (row.total > sc.total && st.k > 0) step += `<span class="eu-bad">✗ ${ltr(row.country)} עברה את ישראל, ההפסד ודאי.</span>`;
        else if (left > room) step += `<span class="eu-bad">✗ יותר מים מנפח (${ltr(`${num(left)} > ${num(room)}`)})  : מישהי חייבת לעבור את ישראל.</span>`;
        else step += `<span class="eu-ok">✓ הכול עוד נכנס (${ltr(`${num(left)} ≤ ${num(room)}`)})  : ישראל עדיין יכולה לנצח.</span>`;
        $(".eu-step").innerHTML = step;
        const real = st.jury === 123 && st.pub === 220;
        $(".eu-sum").innerHTML = (sc.won
          ? `עם ${ltr(`${st.jury} + ${st.pub} = ${sc.total}`)} אף מדינה לא עוברת את ישראל : היא מנצחת.`
          : sc.first === 0
            ? `עם ${ltr(`${st.jury} + ${st.pub} = ${sc.total}`)} ההפסד ודאי כבר ברגע ההכרזה של ישראל.`
            : `ההפסד ודאי אחרי ההכרזה ה-${ltr(sc.first)} שאחרי ישראל, של ${ltr(sc.rows[sc.first].country)}, כשנותרו ${ltr(n - sc.first)} הכרזות.`) +
          (real ? "" : ` (במציאות : 123 + 220 = 343, וההפסד ודאי אחרי צרפת, ההכרזה הרביעית.)`) +
          ` סדר ההכרזות נקבע לפי ניקוד השופטים${real ? "" : ", ולכן שינוי בניקוד השופטים של ישראל מזיז גם את מקומה בתור"}.`;
      };
      // the proof panel: the cups still to come, filled to the brim with the points left,
      // and the spill beside them
      let pourAnim = null;
      const drawPour = (share = 1) => {
        const res = euroWithIsrael(st.jury, st.pub), pr = euroPour(res, Math.min(st.k, euroScan(res).rows.length - 1), share), full = euroPour(res, Math.min(st.k, euroScan(res).rows.length - 1));
        const W = 640, H = 270, X0 = 48, BASE = 220, TOP = 16, n = pr.cups.length + 1;
        const ymax = Math.max(pr.total, full.spill, ...pr.cups.map((c) => c.jury), 1) * 1.1, Y = (v) => BASE - (v / ymax) * (BASE - TOP);
        const slot = (W - X0 - 12) / Math.max(n, 2), bw = slot * 0.6;
        let s = `<svg class="perf-chart eu-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${pr.left} נקודות הקהל שנותרו נמזגות לכוסות של ${pr.cups.length} המדינות שעוד לא הכריזו, כל כוס עד ${pr.total}, ומה שלא נכנס נשפך">`;
        [0, 100, 200, 300, 400, 500, 600].filter((v) => v < ymax).forEach((v) => {
          s += `<line class="grid" x1="${X0}" x2="${W - 12}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`;
        });
        pr.cups.forEach((c, i) => {
          const x = X0 + i * slot + (slot - bw) / 2, cx = x + bw / 2;
          s += `<rect class="bar by-multiples" x="${f(x)}" y="${f(Y(c.jury))}" width="${f(bw)}" height="${f(BASE - Y(c.jury))}"><title>${c.country} : שופטים ${c.jury}</title></rect>`;
          if (c.room > 0) s += `<rect class="cup-room" x="${f(x)}" y="${f(Y(pr.total))}" width="${f(bw)}" height="${f(Y(c.jury) - Y(pr.total))}"><title>${c.country} : מקום פנוי ${c.room}</title></rect>`;
          if (c.fill > 0) s += `<rect class="pour-water" x="${f(x)}" y="${f(Y(c.jury + c.fill))}" width="${f(bw)}" height="${f(Y(c.jury) - Y(c.jury + c.fill))}"><title>${c.country} : נמזגו ${c.fill}</title></rect>`;
          s += `<text class="tick" x="${f(cx)}" y="${BASE + 16}" text-anchor="middle" font-size="10">${c.country.length > 9 ? c.country.slice(0, 8) + "…" : c.country}</text>` +
               `<text class="tick" x="${f(cx)}" y="${BASE + 30}" text-anchor="middle" font-size="10">${c.fill} / ${c.room}</text>`;
        });
        const xs = X0 + pr.cups.length * slot + (slot - bw) / 2;
        if (pr.spill > 0) s += `<rect class="overflow" x="${f(xs)}" y="${f(Y(pr.spill))}" width="${f(bw)}" height="${f(BASE - Y(pr.spill))}"><title>נשפך : ${pr.spill}</title></rect>`;
        s += `<text class="tick" x="${f(xs + bw / 2)}" y="${BASE + 16}" text-anchor="middle" font-size="10" direction="rtl">נשפך</text><text class="tick" x="${f(xs + bw / 2)}" y="${BASE + 30}" text-anchor="middle" font-size="10">${pr.spill}</text>` +
             `<line class="israel-line" x1="${X0}" x2="${W - 12}" y1="${f(Y(pr.total))}" y2="${f(Y(pr.total))}"/><text class="legend" x="${X0 + 4}" y="${f(Y(pr.total) - 6)}">Israel ${pr.total}</text>` +
             `<line class="axis" x1="${X0}" x2="${W - 12}" y1="${BASE}" y2="${BASE}"/></svg>`;
        $(".eu-pour").innerHTML = s;
        $(".eu-pour-title").textContent = `הנקודות שנותרו, ${num(pr.left)}, נמזגות לכוסות של ${pr.cups.length} המדינות שעוד לא הכריזו, כל כוס עד ${pr.total}`;
        const sc = euroScan(res), row = sc.rows[Math.min(st.k, sc.rows.length - 1)], passed = st.k > 0 && sc.rows.slice(1, st.k + 1).some((r) => r.total > sc.total);
        $(".eu-pour-text").innerHTML = share < 1 ? "מוזגים…" : passed
          ? `מדינה שכבר הכריזה עברה את ישראל, ולכן ההפסד ודאי בלי קשר למזיגה.`
          : full.spill > 0
            ? `גם המזיגה הכי טובה לישראל, כל כוס עד הסף, משאירה ${ltr(num(full.spill))} נקודות בחוץ (${ltr(`${num(full.left)} − ${num(full.room)} = ${num(full.spill)}`)}). הנקודות האלה חייבות להגיע למדינה כלשהי, והיא עוברת את ${ltr(sc.total)} : זה ההפסד הוודאי.`
            : `הכול נכנס, ונשארים ${ltr(num(full.room - full.left))} מקומות פנויים${row.country === "Israel" ? "" : ` אחרי ${ltr(row.country)}`} : יש עדיין חלוקה של הנקודות שבה אף מדינה לא עוברת את ישראל.`;
      };
      $(".ex-pour").addEventListener("click", () => {
        if (pourAnim) cancelAnimationFrame(pourAnim);
        const t0 = performance.now();
        const frame = (now) => { const p = Math.min((now - t0) / 1400, 1); drawPour(p); pourAnim = p < 1 ? requestAnimationFrame(frame) : null; };
        pourAnim = requestAnimationFrame(frame);
      });
      slider.addEventListener("input", () => { st.k = Number(slider.value); draw(); });
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { st.k = Math.min(st.k + 1, Number(slider.max)); draw(); },
        done: () => st.k >= Number(slider.max),
        restart: () => { st.k = 0; draw(); },
      });
      $(".ex-next").addEventListener("click", () => { stop(); st.k = Math.min(st.k + 1, Number(slider.max)); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k = Math.max(st.k - 1, 0); draw(); });
      ["jury", "pub"].forEach((k) => $(`.ex-${k}`).addEventListener("change", () => {
        const v = Math.round(Number($(`.ex-${k}`).value));
        if (v >= 0 && v <= (k === "jury" ? 420 : 432)) { st[k] = v; st.k = 0; }
        draw();
      }));
      $(".ex-reset").addEventListener("click", () => { st.jury = 123; st.pub = 220; st.k = 0; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { eurovision: euroView },
    help: {
      eurovision: "״ההכרזה הבאה״ מוסיפה מדינה : הכוסות מתחת לסכום של ישראל כנגד הנקודות שנותרו. תיבת ה״מה אם״ משנה את הניקוד של ישראל. בשלב ההוכחה ״מזיגה״ ממלאת את הכוסות שנותרו עד הסף, ומה שלא נכנס נשפך.",
    },
    models: { EURO_RESULTS, EURO_PUBLIC_TOTAL, euroOrder, euroWithIsrael, euroCannotWin, euroScan, euroPour },
  });
})();
