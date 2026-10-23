// kinds: boxes
//   boxes                  0009        N boxes on a ring with their cycles, person 0's cut, a walk box by box, rounds without person 0; the copy link carries the arrangement and the walk; the proof panel: any cut of the long cycle
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { STATE_CODECS, W, autoplay, f, fmt, ltr, seedControls, speedSel } = dvqExplorers.lib;

  // Boxes and cycles (0009): notes[b] is the note in box b (1..N), notes[0] unused. The
  // notes are a permutation; its cycles, person 0's one cut, one person's walk, and the
  // closed forms of the two success rates the box compares.
  const permCycles = (notes) => {
    const n = notes.length - 1, seen = new Set(), cycles = [];
    for (let s = 1; s <= n; s++) {
      if (seen.has(s)) continue;
      const c = [s]; seen.add(s);
      for (let b = notes[s]; b !== s; b = notes[b]) { c.push(b); seen.add(b); }
      cycles.push(c);
    }
    return cycles;
  };
  // person 0: the first and the middle box of the one cycle longer than maxOpens, or null
  const permHelper = (notes, maxOpens) => {
    for (const c of permCycles(notes)) if (c.length > maxOpens) return [c[0], c[c.length >> 1]];
    return null;
  };
  // Any cut of the proof: person 0 swaps the notes of the long cycle's first box c0 and of
  // its box c_h (h = 1 .. L − 1); the cycle splits into pieces of h and L − h. The long
  // cycle, the pair of boxes, or null when no cycle is longer than maxOpens.
  const permCutAt = (notes, maxOpens, h) => {
    const c = permCycles(notes).find((cy) => cy.length > maxOpens);
    return c && h >= 1 && h < c.length ? { cycle: c, pair: [c[0], c[h]] } : null;
  };
  const permSwap = (notes, a, b) => { const out = [...notes]; out[a] = notes[b]; out[b] = notes[a]; return out; };
  // person `me`: the boxes opened in order, and whether the note was found
  const permWalk = (notes, me, maxOpens) => {
    const opened = [];
    let box = me;
    for (let k = 0; k < maxOpens; k++) {
      opened.push(box);
      if (notes[box] === me) return { opened, found: true };
      box = notes[box];
    }
    return { opened, found: false };
  };
  const permAllWin = (notes, maxOpens) => permCycles(notes).every((c) => c.length <= maxOpens);
  const permShuffle = (n, rnd = Math.random) => {
    const p = Array.from({ length: n }, (_, i) => i + 1);
    for (let i = n - 1; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [p[i], p[j]] = [p[j], p[i]]; }
    return [0, ...p];
  };
  // every person opens maxOpens boxes chosen at random: do all of them find their note?
  const permRandomPicks = (notes, maxOpens, rnd = Math.random) => {
    const n = notes.length - 1;
    for (let me = 1; me <= n; me++) {
      const boxes = permShuffle(n, rnd).slice(1, maxOpens + 1);
      if (!boxes.some((b) => notes[b] === me)) return false;
    }
    return true;
  };
  // P(no cycle longer than maxOpens) for maxOpens >= n / 2: 1 - sum_{k > maxOpens} 1 / k
  const permStrategyProb = (n, maxOpens) => {
    let p = 1;
    for (let k = maxOpens + 1; k <= n; k++) p -= 1 / k;
    return p;
  };
  const permRandomProb = (n, maxOpens) => Math.pow(maxOpens / n, n);

  // The boxes box (0009): N boxes on a ring with an arrow from every box to the box its
  // note names, one colour per cycle and the long cycle in red; person 0's cut as two
  // dashed arrows; a person's walk played opening by opening; and a counter of rounds
  // that compares the strategy without person 0 with random picks.
  const boxesView = () => ({
    mount(box) {
      const EXAMPLE = [0, 7, 11, 15, 16, 13, 2, 12, 14, 4, 5, 6, 3, 1, 8, 9, 10];
      const nmax = Number(box.dataset.nmax || 16);
      const W = 360, C = 180, R = 138, NODE = 15, CYC = 5;    // CYC colours for the cycles
      const num = (v) => Number(v).toLocaleString("en-US");
      const st = { n: nmax, notes: EXAMPLE, helper: true, me: 13, step: 0, runs: 0, strat: 0, rand: 0, h: null };   // h: the proof's cut, null = the middle
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מספר הקופסאות N</span><input type="range" class="ex-n" min="4" max="${nmax}" step="2" value="${st.n}" dir="ltr"><output class="out-n"></output></label>` +
        `<button type="button" class="md-button md-button--primary ex-shuffle">ערבוב</button>` +
        `<button type="button" class="md-button ex-example">הדוגמה מהדף</button>` +
        `<label><input type="checkbox" class="ex-helper" checked> אדם 0 חותך את המעגל הארוך</label></div>` +
        `<div class="bx-box"><div class="bx-ring"></div><div class="bx-panel">` +
        `<p class="bx-cycles"></p><p class="bx-helper"></p>` +
        `<div class="ex-controls bx-walk-row"><label>אדם <input type="number" class="ex-me" min="1" max="${nmax}" step="1" dir="ltr" aria-label="מספר האדם שהולך"></label>` +
        `<button type="button" class="md-button ex-prev">הפתיחה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הפתיחה הבאה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1500, 700, 250) +
        `<button type="button" class="md-button ex-all">עד הסוף</button>` +
        `<button type="button" class="md-button ex-start">מההתחלה</button></div>` +
        `<p class="bx-walk" aria-live="polite"></p></div></div>` +
        `<div class="ex-controls bx-stats-row">` +
        `<button type="button" class="md-button ex-rounds">1,000 סיבובים בלי אדם 0</button>` +
        `<button type="button" class="md-button ex-rounds-reset">איפוס המונים</button><span class="bx-runs"></span></div>` +
        `<div class="bx-bars"></div><p class="ex-summary bx-formula"></p>` +
        `<section class="ex-proof bx-proof"><p class="ex-proof-title">שלב ההוכחה : איפה לחתוך</p>` +
        `<p class="bx-cut-help"></p><div class="bx-cut-row" role="group" aria-label="הקופסאות של המעגל הארוך לפי הסדר; לחיצה בוחרת את הקופסה שאדם 0 מחליף עם הראשונה"></div>` +
        `<div class="bx-cut-chart"></div><p class="bx-cut-text"></p></section>`;
      const $ = (sel) => box.querySelector(sel);
      const ring = $(".bx-ring"), meIn = $(".ex-me"), helperCb = $(".ex-helper");
      const pt = (b, r) => { const a = -Math.PI / 2 + (2 * Math.PI * (b - 1)) / st.n; return [C + r * Math.cos(a), C + r * Math.sin(a)]; };
      const maxOpens = () => st.n / 2;
      const effective = () => {
        if (!st.helper) return { notes: st.notes, cut: null };
        const chosen = st.h === null ? null : permCutAt(st.notes, maxOpens(), st.h);
        const cut = chosen ? chosen.pair : permHelper(st.notes, maxOpens());
        return { notes: cut ? permSwap(st.notes, cut[0], cut[1]) : st.notes, cut };
      };
      // an arrow from box a to box b: a chord bent to its right, so a -> b and b -> a differ
      const arrow = (a, b, cls, dashed) => {
        const [x0, y0] = pt(a, R), [x1, y1] = pt(b, R);
        if (a === b) {
          const [ox, oy] = pt(a, R + 26);
          return `<circle class="bx-arrow ${cls}" cx="${f(ox)}" cy="${f(oy)}" r="9" fill="none"/>`;
        }
        const dx = x1 - x0, dy = y1 - y0, len = Math.hypot(dx, dy);
        const mx = (x0 + x1) / 2 + (-dy / len) * len * 0.22, my = (y0 + y1) / 2 + (dx / len) * len * 0.22;
        const u0 = [(mx - x0) / Math.hypot(mx - x0, my - y0), (my - y0) / Math.hypot(mx - x0, my - y0)];
        const u1 = [(x1 - mx) / Math.hypot(x1 - mx, y1 - my), (y1 - my) / Math.hypot(x1 - mx, y1 - my)];
        const sx = x0 + u0[0] * (NODE + 1), sy = y0 + u0[1] * (NODE + 1);
        const ex = x1 - u1[0] * (NODE + 2), ey = y1 - u1[1] * (NODE + 2);
        const hx = ex - u1[0] * 9, hy = ey - u1[1] * 9;
        return `<path class="bx-arrow ${cls}" d="M${f(sx)},${f(sy)} Q${f(mx)},${f(my)} ${f(ex)},${f(ey)}" fill="none"${dashed ? ' stroke-dasharray="6 4"' : ""}/>` +
               `<polygon class="bx-head ${cls}" points="${f(ex)},${f(ey)} ${f(hx + u1[1] * 4.5)},${f(hy - u1[0] * 4.5)} ${f(hx - u1[1] * 4.5)},${f(hy + u1[0] * 4.5)}"/>`;
      };
      // the proof panel: the long cycle as a row of its boxes in order, a tap picks c_h; the
      // largest piece for every h against the line N / 2, the middle range the only safe one
      const drawCut = () => {
        const m = maxOpens(), long = permCycles(st.notes).find((c) => c.length > m);
        const row = $(".bx-cut-row"), chart = $(".bx-cut-chart");
        if (!long) {
          row.innerHTML = ""; chart.innerHTML = ""; $(".bx-cut-help").textContent = "";
          $(".bx-cut-text").innerHTML = `אין כאן מעגל ארוך מ-${ltr(m)}, ולכן אין מה לחתוך. ״ערבוב״ נותן לרוב סידור עם מעגל ארוך.`;
          return;
        }
        const L = long.length, h = st.h !== null && st.h < L ? st.h : L >> 1, lo = L - m, hi = m;
        $(".bx-cut-help").innerHTML = `המעגל הארוך לפי הסדר, מהקופסה ${ltr(long[0])}. אדם 0 מחליף את הפתק של הקופסה הראשונה עם הפתק של קופסה אחרת עליו. לחצו על קופסה כדי לבחור את החיתוך${st.helper ? ", והטבעת למעלה מתעדכנת" : ""}.`;
        row.innerHTML = long.map((b, i) => i === 0
          ? `<span class="bx-cut-cell is-first">${b}</span>`
          : `<button type="button" class="bx-cut-cell${i === h ? " is-cut" : ""}${i <= h ? " is-a" : " is-b"}${i >= lo && i <= hi ? "" : " is-bad"}" data-h="${i}" aria-pressed="${i === h}" aria-label="${b}, חיתוך אחרי ${i} קופסאות">${b}</button>`).join("");
        // the chart: one column per h, the larger piece's length
        const w = 640, ht = 200, x0 = 46, right = 12, top = 14, base = 166, slot = (w - x0 - right) / (L - 1);
        const Y = (v) => base - (v / L) * (base - top);
        let svg = `<svg class="perf-chart" viewBox="0 0 ${w} ${ht}" role="img" aria-label="החתיכה הגדולה לכל נקודת חיתוך, מול הקו N / 2 = ${m}">`;
        [0, m, L].forEach((v) => { svg += `<line class="grid" x1="${x0}" x2="${w - right}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${x0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}</text>`; });
        for (let k = 1; k < L; k++) {
          const big = Math.max(k, L - k), ok = big <= m, cx = x0 + (k - 0.5) * slot, bw = Math.max(slot * 0.62, 2);
          svg += `<rect class="bar ${ok ? "by-bfs" : "by-enum"}"${k === h ? ' stroke="currentColor" stroke-width="2.5"' : ""} x="${f(cx - bw / 2)}" y="${f(Y(big))}" width="${f(bw)}" height="${f(base - Y(big))}"><title>חיתוך אחרי ${k} : ${k} + ${L - k}</title></rect>`;
          if (k === h || k === lo || k === hi || k === 1 || k === L - 1) svg += `<text class="tick" x="${f(cx)}" y="${base + 18}" text-anchor="middle">${k}</text>`;
        }
        svg += `<line class="ink-line" x1="${x0}" x2="${w - right}" y1="${f(Y(m))}" y2="${f(Y(m))}" stroke-width="1.5" stroke-dasharray="6 4"/>` +
               `<text class="legend" x="${x0 + 6}" y="${f(Y(m) - 6)}">N / 2 = ${m}</text><line class="axis" x1="${x0}" x2="${w - right}" y1="${base}" y2="${base}"/></svg>`;
        chart.innerHTML = `<p class="ex-title">החתיכה הגדולה לכל חיתוך h (ירוק : שתי החתיכות עד ${m})</p>` + svg;
        const ok = Math.max(h, L - h) <= m;
        $(".bx-cut-text").innerHTML = `חיתוך אחרי ${ltr(h)} קופסאות (החלפה בין ${ltr(long[0])} ל-${ltr(long[h])}) : המעגל באורך ${ltr(L)} מתפצל ל-${ltr(`${h} + ${L - h}`)}. ` +
          (ok ? `<span class="bx-ok">✓ שתי החתיכות עד ${ltr(m)}.</span> ` : `<span class="bx-bad">✗ חתיכה באורך ${ltr(Math.max(h, L - h))} עדיין ארוכה מ-${ltr(m)}.</span> `) +
          `שתי החתיכות עד ${ltr(m)} בדיוק כש-${ltr(`${L} − ${m} ≤ h ≤ ${m}`)}, כלומר ${ltr(`${lo} ≤ h ≤ ${hi}`)} : ${ltr(hi - lo + 1)} ${hi === lo ? "בחירה אחת" : "בחירות"} מתוך ${ltr(L - 1)}. ` +
          `האמצע, ${ltr(`h = ⌊${L} / 2⌋ = ${L >> 1}`)}, תמיד ביניהן, כי ${ltr(`L ≤ N`)}. זה החיתוך של אדם 0 בדף.`;
      };
      const draw = () => {
        drawCut();
        $(".out-n").textContent = String(st.n);
        const { notes, cut } = effective();
        const cycles = permCycles(notes), m = maxOpens();
        const colour = new Map();                    // box -> cycle class
        let k = 0;
        cycles.forEach((c) => {
          const cls = c.length > m ? "bx-long" : `bx-c${k++ % CYC}`;
          c.forEach((b) => colour.set(b, cls));
        });
        const walk = permWalk(notes, st.me, m);
        const shown = walk.opened.slice(0, st.step);
        const cur = shown[shown.length - 1];
        let s = `<svg class="figure bx-live" viewBox="0 0 ${W} ${W}" role="group" aria-label="${st.n} קופסאות במעגל, חץ מכל קופסה לקופסה שהפתק שלה מצביע עליה; לחיצה על קופסה בוחרת את האדם">`;
        for (let b = 1; b <= st.n; b++) {
          const dashed = cut && (b === cut[0] || b === cut[1]);
          const onPath = shown.includes(b) && shown.indexOf(b) < shown.length - 1;
          s += arrow(b, notes[b], colour.get(b) + (onPath ? " is-walked" : ""), dashed);
        }
        for (let b = 1; b <= st.n; b++) {
          const [x, y] = pt(b, R);
          const open = shown.indexOf(b);
          const cls = ["bx-node", colour.get(b), cut && (b === cut[0] || b === cut[1]) ? "is-cut" : "",
            open >= 0 ? "is-open" : "", b === cur ? "is-cur" : "", b === st.me ? "is-me" : ""].join(" ");
          s += `<g class="bx-g" data-b="${b}" tabindex="0" role="button" aria-label="קופסה ${b}, הפתק ${notes[b]}"><circle class="${cls}" cx="${f(x)}" cy="${f(y)}" r="${NODE}"><title>קופסה ${b} : הפתק ${notes[b]}</title></circle>` +
               `<text class="bx-num" x="${f(x)}" y="${f(y + 4)}" text-anchor="middle">${b}</text>`;
          if (open >= 0) { const [bx, by] = pt(b, R + 27); s += `<circle class="bx-badge" cx="${f(bx)}" cy="${f(by)}" r="9"/><text class="bx-badge-num" x="${f(bx)}" y="${f(by + 3.5)}" text-anchor="middle">${open + 1}</text>`; }
          s += `</g>`;
        }
        s += `</svg>`;
        ring.innerHTML = s;
        // the cycles, longest first in the text
        const longest = Math.max(...cycles.map((c) => c.length));
        $(".bx-cycles").innerHTML = (cycles.length === 1 ? "מעגל אחד : " : `${ltr(cycles.length)} מעגלים : `) + cycles.map((c) => {
          const cls = colour.get(c[0]);
          return `<span class="bx-chip ${cls}">${ltr(c.join(" → "))} (${c.length})</span>`;
        }).join(" ") + `. המעגל הארוך ביותר : ${ltr(longest)}, ומותר לפתוח ${ltr(m)}.`;
        const before = permHelper(st.notes, m);
        $(".bx-helper").innerHTML = !before
          ? `אדם 0 רואה שאין מעגל ארוך מ-${ltr(m)}, ולא נוגע בפתקים. כולם ימצאו את הפתק שלהם.`
          : st.helper
            ? `אדם 0 מחליף בין הפתקים של קופסה ${ltr(cut[0])} וקופסה ${ltr(cut[1])} (החצים המקווקווים) : המעגל באורך ${ltr(permCycles(st.notes).find((c) => c.length > m).length)} מתפצל לשניים, ${ltr(cycles.filter((c) => c.includes(cut[0]) || c.includes(cut[1])).map((c) => c.length).join(" + "))}.`
            : `<span class="bx-bad">בלי אדם 0 יש מעגל באורך ${ltr(permCycles(st.notes).find((c) => c.length > m).length)}, וכל מי שעליו נכשל.</span>`;
        meIn.value = st.me;
        const line = shown.map((b, i) => `${i + 1} : קופסה ${ltr(b)} ← הפתק ${ltr(notes[b])}`);
        let end = "";
        if (st.step >= walk.opened.length) {
          end = walk.found
            ? ` <span class="bx-ok">✓ אדם ${ltr(st.me)} מצא את הפתק שלו אחרי ${walk.opened.length === 1 ? "פתיחה אחת" : `${ltr(walk.opened.length)} פתיחות`}.</span>`
            : ` <span class="bx-bad">✗ ${ltr(m)} פתיחות נגמרו ואדם ${ltr(st.me)} לא מצא את הפתק שלו : הוא על מעגל באורך ${ltr(cycles.find((c) => c.includes(st.me)).length)}.</span>`;
        }
        $(".bx-walk").innerHTML = `אדם ${ltr(st.me)} מתחיל בקופסה ${ltr(st.me)}.` + (line.length ? " " + line.join(", ") + "." : "") + end;
        // the rounds so far
        $(".bx-runs").textContent = st.runs ? `${num(st.runs)} סיבובים עד כה` : "";
        const pStrat = permStrategyProb(st.n, m), pRand = permRandomProb(st.n, m);
        const bar = (label, wins, p) => {
          const pct = st.runs ? (100 * wins) / st.runs : 0;
          return `<div class="bx-bar"><span class="bx-bar-label">${label}</span><span class="bx-bar-track"><span class="bx-bar-fill" style="width:${f(Math.min(100, pct))}%"></span></span>` +
                 `<span class="bx-bar-val">${st.runs ? `${ltr(num(wins))} (${ltr(f(pct, 1) + "%")})` : "—"}, צפוי ${ltr(f(100 * p, p < 0.01 ? 4 : 1) + "%")}</span></div>`;
        };
        $(".bx-bars").innerHTML = bar("האסטרטגיה בלי אדם 0", st.strat, pStrat) + bar(`כל אחד פותח ${ltr(m)} קופסאות אקראיות`, st.rand, pRand);
        const terms = []; for (let j = m + 1; j <= st.n; j++) terms.push(`1/${j}`);
        $(".bx-formula").innerHTML = `הצפי : האסטרטגיה מצליחה כשאין מעגל ארוך מ-${ltr(m)}, בהסתברות ${ltr(`1 − (${terms.join(" + ")}) ≈ ${fmt(pStrat, 4)}`)}; ` +
          `בחירה אקראית מצליחה לכל אחד בהסתברות ${ltr(`1/2`)}, ולכולם ${ltr(`(1/2)^${st.n} ≈ ${pRand < 1e-3 ? pRand.toExponential(2).replace("e-", "·10^−") : fmt(pRand, 4)}`)}. עם אדם 0 האסטרטגיה מצליחה תמיד.`;
      };
      const steps = () => permWalk(effective().notes, st.me, maxOpens()).opened.length;
      const stop = autoplay($(".ex-play"), $(".ex-speed"), {
        step: () => { st.step = Math.min(st.step + 1, steps()); draw(); },
        done: () => st.step >= steps(),
        restart: () => { st.step = 0; draw(); },
      });
      const setN = (n) => { stop(); st.h = null; st.n = n; st.notes = permShuffle(n); st.me = Math.min(st.me, n); st.step = 0; st.runs = st.strat = st.rand = 0; draw(); };
      $(".ex-n").addEventListener("input", () => setN(Number($(".ex-n").value)));
      const seed = seedControls(box, $(".ex-example"), (rng) => { stop(); st.h = null; st.notes = permShuffle(st.n, rng); st.step = 0; draw(); }, { state: {
        get: () => STATE_CODECS.boxes.enc({ notes: st.notes, me: st.me, helper: st.helper, step: st.step }),
        set: (p) => {
          const d = STATE_CODECS.boxes.dec(p, nmax);
          if (!d) return false;
          stop(); st.h = null; st.n = d.n; $(".ex-n").value = d.n; st.notes = d.notes; st.me = d.me; st.helper = d.helper; helperCb.checked = d.helper;
          st.step = Math.min(d.step, steps()); draw(); return true;
        },
      } });
      $(".ex-shuffle").addEventListener("click", seed.draw);
      $(".bx-cut-row").addEventListener("click", (e) => {
        const b = e.target.closest("button[data-h]");
        if (!b) return;
        stop(); st.h = Number(b.dataset.h); st.step = 0; draw();
        const again = box.querySelector(`.bx-cut-row button[data-h="${st.h}"]`); if (again && e.detail === 0) again.focus();
      });
      $(".ex-example").addEventListener("click", () => { stop(); st.h = null; st.n = nmax; $(".ex-n").value = nmax; st.notes = EXAMPLE.slice(0, nmax + 1); st.me = 13; st.step = 0; draw(); });
      helperCb.addEventListener("change", () => { stop(); st.helper = helperCb.checked; st.step = 0; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); st.step = Math.min(st.step + 1, steps()); draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.step = Math.max(st.step - 1, 0); draw(); });
      $(".ex-all").addEventListener("click", () => { stop(); st.step = steps(); draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.step = 0; draw(); });
      meIn.addEventListener("change", () => {
        stop();
        const v = Math.round(Number(meIn.value));
        if (v >= 1 && v <= st.n) { st.me = v; st.step = 0; }
        draw();
      });
      meIn.addEventListener("keydown", (e) => { if (e.key === "Enter") meIn.blur(); });
      ring.addEventListener("click", (e) => {
        const g = e.target.closest(".bx-g");
        if (!g) return;
        stop(); st.me = Number(g.dataset.b); st.step = 0; draw();
      });
      ring.addEventListener("keydown", (e) => {
        const g = e.target.closest(".bx-g");
        if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); stop(); st.me = Number(g.dataset.b); st.step = 0; draw(); }
      });
      $(".ex-rounds").addEventListener("click", () => {
        const m = maxOpens();
        for (let r = 0; r < 1000; r++) {
          const notes = permShuffle(st.n);
          if (permAllWin(notes, m)) st.strat++;
          if (permRandomPicks(notes, m)) st.rand++;
        }
        st.runs += 1000;
        draw();
      });
      $(".ex-rounds-reset").addEventListener("click", () => { st.runs = st.strat = st.rand = 0; draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { boxes: boxesView },
    help: {
      boxes: "N קופסאות במעגל עם המעגלים שלהן בצבעים : ״ערבוב״ מגריל סידור, בוחרים אדם ועוקבים אחרי הפתיחות שלו, ו״1,000 סיבובים״ משווה את האסטרטגיה לבחירה אקראית. ״העתקת קישור״ שומר את המצב. בשלב ההוכחה בוחרים בעצמכם איפה אדם 0 חותך את המעגל הארוך, ורואים מתי שתי החתיכות קצרות מספיק.",
    },
    models: { permCycles, permHelper, permCutAt, permSwap, permWalk, permAllWin, permShuffle, permRandomPicks, permStrategyProb, permRandomProb },
  });
})();
