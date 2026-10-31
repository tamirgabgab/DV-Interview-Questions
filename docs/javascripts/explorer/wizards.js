// kinds: wizards
//   wizards                0060        the three-wizard duel with the cat rule: my position, the two rivals and my wand; the first round solved backward with the value of every option of every wizard, my chance, and the chart of my chance against my wand with the best wand
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { BASE, RIGHT, TOP, W, X0, f, fmt, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";

  // The model (0060): p in turn order. A duel to the end, the opener first; after a kill
  // in the first round the survivor is next in turn, so it opens against the killer. The
  // first round backward: each wizard keeps the air unless a target is better by more
  // than 1e-12 (the page's rule), targets in order 1, 2, 3.
  const wzDuel = (x, y) => x / (x + y - x * y);
  const wzRound = (p) => {
    let after = [0, 0, 0];
    const trace = [];
    for (const w of [2, 1, 0]) {
      const opts = { air: after };
      let best = "air";
      for (let t = 0; t < 3; t++) {
        if (t === w) continue;
        const o = 3 - w - t, hit = [0, 0, 0];
        hit[o] = wzDuel(p[o], p[w]);
        hit[w] = 1 - hit[o];
        opts[t + 1] = hit.map((h, k) => p[w] * h + (1 - p[w]) * after[k]);
        if (opts[t + 1][w] > opts[best][w] + 1e-12) best = String(t + 1);
      }
      trace.push({ w: w + 1, opts: Object.fromEntries(Object.entries(opts).map(([k, v]) => [k, v[w]])), choice: best });
      after = opts[best];
    }
    return { win: after, trace };
  };
  const wzPlace = (me, own, rivals) => { const p = rivals.slice(); p.splice(me - 1, 0, own); return p; };
  const wzChance = (me, own, rivals) => wzRound(wzPlace(me, own, rivals)).win[me - 1];
  // the best wand: every 0.001 and the points just under the rivals and 0.5
  const wzBest = (me, rivals) => {
    const qs = [];
    for (let k = 1; k <= 1000; k++) qs.push(k / 1000);
    rivals.forEach((r) => qs.push(r - 1e-9));
    qs.push(0.5 - 1e-9);
    let best = { chance: -1, wand: 0 };
    qs.forEach((q) => { const v = wzChance(me, q, rivals); if (v > best.chance || (v === best.chance && q > best.wand)) best = { chance: v, wand: q }; });
    return best;
  };

  const POS = ["ראשון", "שני", "שלישי"];
  const pct = (v) => `${(v * 100).toFixed(1)}%`;
  const wandText = (q) => { const r = Math.round(q * 1000) / 1000; return Math.abs(q - r) > 1e-12 && q < r ? `${r}⁻` : String(r); };

  // The chart: my chance against my wand, broken where it jumps; the current wand and the best.
  const H = 230;
  const chart = (me, rivals, own, best) => {
    const X = (x) => X0 + x * (W - X0 - RIGHT), Y = (v) => BASE - v * (BASE - TOP);
    let s = `<svg class="perf-chart wz-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="הסיכוי שלי לנצח כפונקציה של השרביט">`;
    [0, 0.2, 0.4, 0.6, 0.8, 1].forEach((v) => {
      s += `<line class="grid" x1="${X0}" x2="${W - RIGHT}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v * 100}%</text>`;
      s += `<text class="tick" x="${f(X(v))}" y="${BASE + 18}" text-anchor="middle">${v}</text>`;
    });
    rivals.forEach((r) => { s += `<line class="grid" x1="${f(X(r))}" x2="${f(X(r))}" y1="${TOP}" y2="${BASE}" stroke-dasharray="4 4"/>`; });
    let pts = [], prev = null;
    const flush = () => { if (pts.length > 1) s += `<polyline class="s1-line" points="${pts.join(" ")}" fill="none" stroke-width="2.5"/>`; pts = []; };
    for (let k = 1; k <= 200; k++) {
      const x = k / 200 - 1e-7, v = wzChance(me, x, rivals);
      if (prev !== null && Math.abs(v - prev) > 0.04) flush();
      pts.push(`${f(X(x))},${f(Y(v))}`);
      prev = v;
    }
    flush();
    const now = wzChance(me, own, rivals);
    s += `<circle class="s3-dot" cx="${f(X(best.wand))}" cy="${f(Y(best.chance))}" r="6"><title>${pct(best.chance)}</title></circle>`;
    s += `<circle class="s2-dot" cx="${f(X(own))}" cy="${f(Y(now))}" r="6"><title>${pct(now)}</title></circle>`;
    return s + `<line class="axis" x1="${X0}" x2="${W - RIGHT}" y1="${BASE}" y2="${BASE}"/></svg>`;
  };

  const wizardsView = () => ({
    mount(box) {
      const st = { me: Number(box.dataset.me || 1), r1: Number(box.dataset.r1 || 0.6), r2: Number(box.dataset.r2 || 0.8), wand: Number(box.dataset.wand || 0.599) };
      box.innerHTML =
        `<div class="ex-controls"><label>אני <select class="wz-me">${POS.map((n, i) => `<option value="${i + 1}">${n}</option>`).join("")}</select></label>` +
        `<label><span class="wz-n1"></span><input type="range" class="wz-r1" min="0.05" max="1" step="0.05" dir="ltr"><output class="wz-o1"></output></label>` +
        `<label><span class="wz-n2"></span><input type="range" class="wz-r2" min="0.05" max="1" step="0.05" dir="ltr"><output class="wz-o2"></output></label>` +
        `<label><span>השרביט שלי</span><input type="range" class="wz-wand" min="0.001" max="1" step="0.001" dir="ltr"><output class="wz-ow"></output></label></div>` +
        `<div class="ex-controls"><button type="button" class="md-button wz-weak">ממש מתחת ליריב החלש</button>` +
        `<button type="button" class="md-button wz-sniper">צלף (1)</button>` +
        `<button type="button" class="md-button md-button--primary wz-best">השרביט הטוב ביותר</button></div>` +
        `<p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">הסבב הראשון מהסוף להתחלה${NB}: הסיכוי של הקוסם שבתור בכל אפשרות, והבחירה שלו מודגשת</p>` +
        `<div class="wz-tablewrap"></div>` +
        `<p class="ex-title">הסיכוי שלי לנצח לכל שרביט; הקווים המקווקווים הם היריבים</p><div class="wz-chart"></div>` +
        `<span class="viz-legend"><span><i class="s1"></i>הסיכוי שלי</span><span><i class="s2"></i>השרביט שבחרתי</span><span><i class="s3"></i>השרביט הטוב ביותר</span></span>`;
      const $ = (sel) => box.querySelector(sel);
      const rivals = () => [st.r1, st.r2];
      const sync = () => {
        $(".wz-me").value = String(st.me); $(".wz-r1").value = st.r1; $(".wz-r2").value = st.r2; $(".wz-wand").value = Math.min(1, Math.max(0.001, Math.round(st.wand * 1000) / 1000));
      };
      const draw = () => {
        const others = [1, 2, 3].filter((k) => k !== st.me);
        $(".wz-n1").textContent = `קוסם ${others[0]}`; $(".wz-n2").textContent = `קוסם ${others[1]}`;
        $(".wz-o1").textContent = String(st.r1); $(".wz-o2").textContent = String(st.r2); $(".wz-ow").textContent = wandText(st.wand);
        const p = wzPlace(st.me, st.wand, rivals()), res = wzRound(p), best = wzBest(st.me, rivals());
        const mine = res.win[st.me - 1];
        $(".ex-summary").innerHTML = `אני ${POS[st.me - 1]}, השרביט ${ltr(wandText(st.wand))}${NB}: הסיכוי שלי לנצח ${ltr(pct(mine))}. ` +
          `השרביט הטוב ביותר מול היריבים האלה הוא ${ltr(wandText(best.wand))}, עם ${ltr(pct(best.chance))}.`;
        let t = `<table class="wz-table"><thead><tr><th>התור</th><th>על 1</th><th>על 2</th><th>על 3</th><th>באוויר</th><th>הבחירה</th></tr></thead><tbody>`;
        res.trace.forEach(({ w, opts, choice }) => {
          t += `<tr${w === st.me ? ' class="is-me"' : ""}><td>קוסם ${w}${w === st.me ? " (אני)" : ""}</td>`;
          ["1", "2", "3", "air"].forEach((k) => {
            t += k in opts ? `<td${k === choice ? ' class="is-pick"' : ""}>${fmt(opts[k], 3)}</td>` : "<td>—</td>";
          });
          t += `<td>${choice === "air" ? "באוויר" : `על ${choice}`}</td></tr>`;
        });
        $(".wz-tablewrap").innerHTML = t + "</tbody></table>";
        $(".wz-chart").innerHTML = chart(st.me, rivals(), st.wand, best);
      };
      const read = () => { st.me = Number($(".wz-me").value); st.r1 = Number($(".wz-r1").value); st.r2 = Number($(".wz-r2").value); st.wand = Number($(".wz-wand").value); draw(); };
      ["wz-me", "wz-r1", "wz-r2", "wz-wand"].forEach((c) => $(`.${c}`).addEventListener(c === "wz-me" ? "change" : "input", read));
      const setWand = (q) => { st.wand = q; $(".wz-wand").value = Math.min(1, Math.max(0.001, Math.round(q * 1000) / 1000)); draw(); };
      $(".wz-weak").addEventListener("click", () => setWand(Math.max(0.001, Math.min(st.r1, st.r2) - 0.001)));
      $(".wz-sniper").addEventListener("click", () => setWand(1));
      $(".wz-best").addEventListener("click", () => { const b = wzBest(st.me, rivals()); setWand(Math.max(0.001, Math.round(b.wand * 1000) / 1000 - (b.wand < Math.round(b.wand * 1000) / 1000 - 1e-7 ? 0.001 : 0))); });
      sync();
      draw();
    },
  });

  dvqExplorers.register({
    views: { wizards: wizardsView },
    help: {
      wizards: "בוחרים מיקום, שני יריבים ושרביט : הטבלה פותרת את הסבב הראשון מהסוף להתחלה, עם הסיכוי של כל אפשרות, והגרף מראה את הסיכוי שלי לכל שרביט ואת השרביט הטוב ביותר.",
    },
    models: { wzDuel, wzRound, wzChance, wzBest },
  });
})();
