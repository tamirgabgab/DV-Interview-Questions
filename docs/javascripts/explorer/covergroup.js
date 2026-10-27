// kinds: covergroup
//   covergroup             0053        the ALU covergroup: transactions by stimulus (uniform or dist) or by hand, the coverpoint bins, the cross as five 4 x 4 maps, the coverage against the number of transactions with the expected closure, and the ignored cells counted or not
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, f, ltr, mulberry32, seedControls } = dvqExplorers.lib;

  // The covergroup of 0053 as a model: op 0..4 (ADD, SUB, AND, OR, SHL), the value bins of
  // a and b (zero, max, msb, mid), carry counted for ADD, SUB and SHL, and the cross of
  // op, a and b without the 8 cells of SHL by 0x80 or 0xFF (ignore_bins). The coverage is
  // the LRM's average of the five items; countIgnored puts the 8 cells back (80 cells).
  const CG_OPS = ["ADD", "SUB", "AND", "OR", "SHL"], CG_BINS = ["zero", "max", "msb", "mid"];
  const cgBin = (v) => (v === 0 ? 0 : v === 255 ? 1 : v === 128 ? 2 : 3);
  const cgIgnored = (o, y) => o === 4 && (y === 1 || y === 2);
  const cgNew = () => ({ op: Array(5).fill(0), a: Array(4).fill(0), b: Array(4).fill(0), carry: [0, 0], x: Array.from({ length: 5 }, () => Array.from({ length: 4 }, () => Array(4).fill(0))), n: 0 });
  const cgSample = (st, o, a, b, c) => {
    const x = cgBin(a), y = cgBin(b);
    st.op[o]++; st.a[x]++; st.b[y]++;
    if (o === 0 || o === 1 || o === 4) st.carry[c]++;
    st.x[o][x][y]++;
    st.n++;
    return [x, y];
  };
  const cgCoverage = (st, countIgnored = false) => {
    const share = (arr) => arr.filter((v) => v > 0).length / arr.length;
    let hit = 0, total = 0;
    for (let o = 0; o < 5; o++) for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++) {
      if (!countIgnored && cgIgnored(o, y)) continue;
      total++; if (st.x[o][x][y] > 0) hit++;
    }
    return (100 * (share(st.op) + share(st.a) + share(st.b) + share(st.carry) + hit / total)) / 5;
  };
  const CG_DISTS = {
    uniform: [1 / 256, 1 / 256, 1 / 256, 253 / 256],
    dist: [0.2, 0.2, 0.2, 0.4],
    equal: [0.25, 0.25, 0.25, 0.25],
  };
  const cgCellProbs = (kind) => {
    const pv = CG_DISTS[kind], out = [];
    for (let o = 0; o < 5; o++) for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++) if (!cgIgnored(o, y)) out.push((pv[x] * pv[y]) / 5);
    return out;
  };
  // the integral of 1 - prod(1 - exp(-p t)) on a logarithmic grid, as on the page
  const cgExpected = (p, steps = 20000) => {
    const lo = 1e-3, hi = (60 + Math.log(p.length)) / Math.min(...p), du = (Math.log(hi) - Math.log(lo)) / steps;
    let e = lo, prev = 1;
    for (let k = 1; k <= steps; k++) {
      const t = lo * Math.exp(k * du);
      let prod = 1;
      for (const pi of p) prod *= 1 - Math.exp(-pi * t);
      const fv = 1 - prod;
      e += 0.5 * (prev * t * Math.exp(-du) + fv * t) * du;
      prev = fv;
    }
    return e;
  };
  // the ALU's carry: ADD overflows, SUB borrows, SHL shifts a 1 out (0 for a shift of 8 or more)
  const cgCarry = (o, a, b) => (o === 0 ? (a + b > 255 ? 1 : 0) : o === 1 ? (a < b ? 1 : 0) : o === 4 ? (b >= 1 && b <= 8 ? (a >> (8 - b)) & 1 : 0) : 0);

  // The box (0053): a stimulus and a seed; +100, +1,000, +10,000 transactions or up to the
  // closure of the cross; one transaction by hand; the coverpoints as rows of bins with
  // their counts; the cross as five maps (a down, b across) shaded by hits, the last cell
  // framed, the ignored cells hatched; the coverage against the number of transactions on a
  // log axis with the expected closure; a toggle that counts the ignored cells.
  const CAP = 6000000, CHECKS = [];
  for (let v = 1; v <= 1e7; v = Math.ceil(v * 1.25)) CHECKS.push(v);
  const covergroupView = () => ({
    mount(box) {
      const st = { kind: "uniform", cg: cgNew(), rng: mulberry32(1), last: null, curve: [], next: 0, ign: false };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הגירוי <select class="cv-kind" aria-label="התפלגות הגירוי"><option value="uniform">אחיד</option><option value="dist">dist : ערך קצה 1/5</option><option value="equal">dist : כל מחלקה 1/4</option></select></label>` +
        `<span class="cv-anchor"></span>` +
        `<button type="button" class="md-button md-button--primary cv-run" data-n="100"><bdi dir="ltr">+100</bdi></button>` +
        `<button type="button" class="md-button md-button--primary cv-run" data-n="1000"><bdi dir="ltr">+1,000</bdi></button>` +
        `<button type="button" class="md-button md-button--primary cv-run" data-n="10000"><bdi dir="ltr">+10,000</bdi></button>` +
        `<button type="button" class="md-button cv-close">עד הסגירה</button>` +
        `<button type="button" class="md-button ex-reset">ניקוי</button></div>` +
        `<div class="ex-fold"><p class="ex-fold-title">טרנזקציה ביד</p><div class="ex-controls cv-hand">` +
        `<label>op <select class="cv-op" data-nolink>${CG_OPS.map((o, i) => `<option value="${i}">${o}</option>`).join("")}</select></label>` +
        `<label><span>a</span><input type="text" class="ex-num cv-a" data-nolink value="0x80" dir="ltr" aria-label="a, עשרוני או 0x"></label>` +
        `<label><span>b</span><input type="text" class="ex-num cv-b" data-nolink value="0" dir="ltr" aria-label="b, עשרוני או 0x"></label>` +
        `<button type="button" class="md-button md-button--primary cv-one">דגימה</button><span class="fl-err cv-err"></span></div></div>` +
        `<label class="cv-ignlab"><input type="checkbox" class="cv-ign"> לספור גם את 8 התאים המושמטים (בלי ignore_bins)</label>` +
        `<p class="ex-summary cv-sum" aria-live="polite"></p>` +
        `<div class="cv-points"></div>` +
        `<div class="cv-map"></div>` +
        `<span class="viz-legend"><span><i class="cg-key-hit"></i>תא שנפגע (כהה יותר : יותר פגיעות)</span><span><i class="cg-key-r0"></i>עוד לא נפגע</span><span><i class="cg-key-ign"></i>מושמט</span><span><i class="cg-key-last"></i>הטרנזקציה האחרונה</span></span>` +
        `<div class="cv-curve"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const pick = (rng) => {
        const pv = CG_DISTS[st.kind];
        const val = () => {
          if (st.kind === "uniform") return Math.floor(rng() * 256);
          let u = rng(), k = 0;
          while (k < 3 && u >= pv[k]) { u -= pv[k]; k++; }
          if (k < 3) return [0, 255, 128][k];
          const m = 1 + Math.floor(rng() * 253);                // 1..253, skipping 128
          return m >= 128 ? m + 1 : m;
        };
        const o = Math.floor(rng() * 5), a = val(), b = val();
        return [o, a, b, cgCarry(o, a, b)];
      };
      const note = () => { while (st.next < CHECKS.length && CHECKS[st.next] <= st.cg.n) { st.curve.push([st.cg.n, cgCoverage(st.cg, st.ign)]); st.next++; } };
      const run = (count, untilClosed = false) => {
        let s = null;
        for (let i = 0; i < count; i++) {
          const [o, a, b, c] = pick(st.rng);
          s = [o, ...cgSample(st.cg, o, a, b, c)];
          note();
          if (untilClosed && i % 64 === 0 && cgCoverage(st.cg, false) >= 100 - 1e-9) break;
        }
        if (s) st.last = s;
        st.curve.push([st.cg.n, cgCoverage(st.cg, st.ign)]);
        draw();
      };
      const points = () => {
        const row = (name, labels, arr) => `<div class="cv-row"><span class="cv-name">${code(name)}</span>` +
          labels.map((l, i) => `<span class="cv-bin${arr[i] ? " is-hit" : ""}"><b>${l}</b><small>${arr[i].toLocaleString("en-US")}</small></span>`).join("") + `</div>`;
        return row("cp_op", CG_OPS, st.cg.op) + row("cp_a", CG_BINS, st.cg.a) + row("cp_b", CG_BINS, st.cg.b) + row("cp_carry", ["0", "1"], st.cg.carry);
      };
      const SHORTB = ["0", "FF", "80", "mid"];
      const map = () => {
        // one row of five maps, or 3 + 2 rows in a narrow box (bigger cells on a phone)
        const narrow = box.clientWidth > 0 && box.clientWidth < 520;
        const W = narrow ? 420 : 660, S = narrow ? 30 : 26, G = 14, x0 = 34, per = narrow ? 3 : 5, rowH = 4 * S + 54;
        const H = Math.ceil(5 / per) * rowH + 18;
        let s = `<svg class="figure cg-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="ה-cross : חמש מפות של 4 על 4, תאים שנפגעו צבועים">` +
          `<defs><pattern id="cv-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" class="cg-hatch-line"/></pattern></defs>`;
        for (let o = 0; o < 5; o++) {
          const gx = x0 + (o % per) * (4 * S + G), gy = Math.floor(o / per) * rowH;
          s += `<text class="cg-op" x="${gx + 2 * S}" y="${gy + 22}" text-anchor="middle">${CG_OPS[o]}</text>`;
          for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++) {
            const h = st.cg.x[o][x][y], ign = cgIgnored(o, y) && !st.ign;
            const lvl = h ? Math.min(4, 1 + Math.floor(Math.log10(h))) : 0;
            const last = st.last && st.last[0] === o && st.last[1] === x && st.last[2] === y;
            s += `<rect class="cg-cell ${ign ? "is-ign" : h ? `is-h${lvl}` : "is-r0"}${last ? " is-last" : ""}" x="${gx + y * S}" y="${gy + 34 + x * S}" width="${S - 2}" height="${S - 2}"><title>${CG_OPS[o]}, a ${CG_BINS[x]}, b ${CG_BINS[y]}: ${h.toLocaleString("en-US")}${ign ? " (ignored)" : ""}</title></rect>`;
          }
          if (o % per === 0) SHORTB.forEach((b, x) => { s += `<text class="tick" x="${gx - 5}" y="${gy + 34 + x * S + S / 2 + 4}" text-anchor="end">${b}</text>`; });
          SHORTB.forEach((b, y) => { s += `<text class="tick" x="${gx + y * S + S / 2 - 1}" y="${gy + 34 + 4 * S + 14}" text-anchor="middle">${b}</text>`; });
        }
        return s + `<text class="legend" x="${W - 8}" y="${H - 4}" text-anchor="end">rows: a, columns: b</text></svg>`;
      };
      const curve = (exp) => {
        const W = 640, H = 230, X0 = 46, R = 12, T = 14, B = 196, lmax = 7;
        const X = (n) => X0 + (Math.log10(Math.max(1, n)) / lmax) * (W - X0 - R), Y = (v) => B - (v / 100) * (B - T);
        let s = `<svg class="perf-chart cv-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="הכיסוי כפונקציה של מספר הטרנזקציות, ציר לוגריתמי">`;
        [0, 25, 50, 75, 100].forEach((v) => { s += `<line class="grid" x1="${X0}" x2="${W - R}" y1="${f(Y(v))}" y2="${f(Y(v))}"/><text class="tick" x="${X0 - 8}" y="${f(Y(v) + 4)}" text-anchor="end">${v}%</text>`; });
        for (let k = 0; k <= lmax; k++) s += `<text class="tick" x="${f(X(10 ** k))}" y="${B + 18}" text-anchor="middle">${k < 4 ? 10 ** k : `10^${k}`}</text>`;
        if (exp < 10 ** lmax) s += `<line class="ink-line" x1="${f(X(exp))}" x2="${f(X(exp))}" y1="${T}" y2="${B}" stroke-dasharray="5 4"/><text class="legend" x="${f(X(exp) - 4)}" y="${T + 12}" text-anchor="end">E ≈ ${Math.round(exp).toLocaleString("en-US")}</text>`;
        if (st.curve.length) s += `<polyline class="s1-line" fill="none" stroke-width="2.5" points="${st.curve.map(([n, v]) => `${f(X(n))},${f(Y(v))}`).join(" ")}"/>`;
        return s + `<line class="axis" x1="${X0}" x2="${W - R}" y1="${B}" y2="${B}"/></svg>`;
      };
      const draw = () => {
        const cov = cgCoverage(st.cg, st.ign), exp = cgExpected(cgCellProbs(st.kind));
        let hit = 0, total = 0, rare = null;
        for (let o = 0; o < 5; o++) for (let x = 0; x < 4; x++) for (let y = 0; y < 4; y++) {
          if (!st.ign && cgIgnored(o, y)) continue;
          total++;
          if (st.cg.x[o][x][y]) hit++; else if (!rare) rare = `${CG_OPS[o]}, a ${CG_BINS[x]}, b ${CG_BINS[y]}`;
        }
        $(".cv-sum").innerHTML = `${ltr(st.cg.n.toLocaleString("en-US"))} טרנזקציות : כיסוי ${ltr(cov.toFixed(2) + "%")}, ‏cross ${ltr(`${hit}/${total}`)}` +
          (hit < total ? `; למשל עוד חסר ${code(rare)}` : " ✓") + `. התוחלת לסגירת ה-cross בגירוי הזה : כ-${ltr(Math.round(exp).toLocaleString("en-US"))} טרנזקציות.` +
          (st.ign ? ` <span class="wv-bad">עם התאים המושמטים : ‏SHL בלבד יכול לפגוע בהם, וזה בסדר, אבל הם מורידים את הכיסוי.</span>` : "");
        $(".cv-points").innerHTML = points();
        $(".cv-map").innerHTML = map();
        $(".cv-curve").innerHTML = `<p class="ex-title">הכיסוי כפונקציה של מספר הטרנזקציות (ציר לוגריתמי), והתוחלת לסגירה</p>` + curve(exp);
      };
      const reset = () => { st.cg = cgNew(); st.curve = []; st.next = 0; st.last = null; };
      const seed = seedControls(box, $(".cv-anchor"), (rng) => { reset(); st.rng = rng; draw(); }, { seed: 1 });
      box.querySelectorAll(".cv-run").forEach((b) => b.addEventListener("click", () => run(Number(b.dataset.n))));
      $(".cv-close").addEventListener("click", () => run(CAP, true));
      $(".cv-kind").addEventListener("change", () => { st.kind = $(".cv-kind").value; reset(); draw(); });
      $(".cv-ign").addEventListener("change", () => { st.ign = $(".cv-ign").checked; st.curve = st.curve.length ? [[st.cg.n, cgCoverage(st.cg, st.ign)]] : []; draw(); });
      const num = (s) => { const t = String(s).trim().toLowerCase(); const v = t.startsWith("0x") ? parseInt(t.slice(2), 16) : /^\d+$/.test(t) ? Number(t) : NaN; return v >= 0 && v <= 255 ? v : NaN; };
      $(".cv-one").addEventListener("click", () => {
        const o = Number($(".cv-op").value), a = num($(".cv-a").value), b = num($(".cv-b").value);
        if (Number.isNaN(a) || Number.isNaN(b)) { $(".cv-err").textContent = "a ו-b : ‏0 עד 255, עשרוני או 0x"; return; }
        $(".cv-err").textContent = "";
        st.last = [o, ...cgSample(st.cg, o, a, b, cgCarry(o, a, b))];
        note(); st.curve.push([st.cg.n, cgCoverage(st.cg, st.ign)]);
        draw();
      });
      $(".ex-reset").addEventListener("click", () => { reset(); st.rng = mulberry32(Number(box.querySelector(".ex-seed").value) || 1); draw(); });
      void seed;
      draw();
    },
  });

  dvqExplorers.register({
    views: { covergroup: covergroupView },
    help: {
      covergroup: "בוחרים גירוי (אחיד או dist) ושולחים טרנזקציות : ‏+100, ‏+1,000, ‏+10,000 או עד שה-cross נסגר. העמודות הן ה-bins של כל coverpoint עם מספר הפגיעות, המפות הן ה-cross (שורות : a, עמודות : b), והגרף מראה את הכיסוי לפי מספר הטרנזקציות מול התוחלת. ״טרנזקציה ביד״ דוגמת ערכים שבוחרים, והמתג סופר גם את התאים המושמטים.",
    },
    models: { cgNew, cgSample, cgCoverage, cgCellProbs, cgExpected, cgCarry },
  });
})();
