// kinds: pcie ladder
//   pcie                   0020, 0021  address, length, MPS and RCB: the blocks, the count and the map of splits; a toggle to cut the boundaries by hand
//   ladder                 0021        part b's recurrence: C(0..N) as a row, a click on C(n) lights the m terms it sums, and a block strip per term with the first completion taking i blocks
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { bigComb, f, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";

  // PCIe completion splits (0020, 0021): a read of `len` bytes from `addr` is answered by
  // completions that cut only on RCB boundaries and never exceed MPS. pcieBlocks gives the
  // N blocks (f, RCB, ..., RCB, e), pcieSplits enumerates the splits in the page's order
  // (largest cut first; `limit` stops early), pcieCount counts them by a dynamic program
  // over the cut points, pcieByCompletions splits that count by the number of completions,
  // and pcieFormula is the closed form of 0021: S(N) - S(N - 1) + delta with
  // S(n) = sum_j (-1)^j C(n - m j, j) 2^(n - (m + 1) j), m = MPS / RCB. Counts are BigInt
  // (a 4 KB request over RCB 64 has 63 boundaries).
  const pcieBoundaries = (addr, len, rcb) => {
    const out = [];
    for (let b = (Math.floor(addr / rcb) + 1) * rcb; b < addr + len; b += rcb) out.push(b);
    return out;
  };
  const pciePoints = (addr, len, rcb) => [addr, ...pcieBoundaries(addr, len, rcb), addr + len];
  const pcieBlocks = (addr, len, rcb) => {
    const pts = pciePoints(addr, len, rcb);
    return pts.slice(1).map((b, i) => b - pts[i]);
  };
  // A split is a subset of the inner boundaries: the completions that a set of cuts forms,
  // and whether every one of them fits in MPS.
  const pcieSplitOf = (addr, len, mps, rcb, cuts) => {
    const pts = [addr, ...pcieBoundaries(addr, len, rcb).filter((b) => cuts.includes(b)), addr + len];
    const sizes = pts.slice(1).map((b, i) => b - pts[i]);
    return { sizes, ok: sizes.every((v) => v <= mps) };
  };
  const pcieSplits = (addr, len, mps, rcb, limit = Infinity) => {
    const end = addr + len, out = [];
    const extend = (pos, sizes) => {
      if (out.length >= limit) return;
      if (pos === end) { out.push(sizes); return; }
      const cuts = pos + mps >= end ? [end] : [];
      for (let b = (Math.floor(pos / rcb) + 1) * rcb; b < end && b <= pos + mps; b += rcb) cuts.push(b);
      cuts.sort((a, b) => b - a).forEach((cut) => extend(cut, sizes.concat([cut - pos])));
    };
    extend(addr, []);
    return out;
  };
  const pcieByCompletions = (addr, len, mps, rcb) => {
    // ways[i][k] = number of ways to cover pts[i]..end with k completions
    const pts = pciePoints(addr, len, rcb), n = pts.length;
    const ways = Array.from({ length: n }, () => []);
    ways[n - 1] = [1n];
    for (let i = n - 2; i >= 0; i--) {
      const row = [];
      for (let j = i + 1; j < n && pts[j] - pts[i] <= mps; j++) {
        ways[j].forEach((w, k) => { row[k + 1] = (row[k + 1] || 0n) + w; });
      }
      ways[i] = row;
    }
    return Array.from(ways[0], (w) => w || 0n);   // index k = number of completions (index 0 is 0)
  };
  const pcieCount = (addr, len, mps, rcb) => pcieByCompletions(addr, len, mps, rcb).reduce((a, b) => a + b, 0n);
  const pcieS = (n, m) => {
    if (n < 0) return 0n;
    let s = 0n;
    for (let j = 0; j <= Math.floor(n / (m + 1)); j++) {
      const term = bigComb(n - m * j, j) * (1n << BigInt(n - (m + 1) * j));
      s += j % 2 ? -term : term;
    }
    return s;
  };
  const pcieFormula = (addr, len, mps, rcb) => {
    const m = mps / rcb, N = pcieBlocks(addr, len, rcb).length;
    const delta = N === m + 1 && len <= mps ? 1n : 0n;
    return pcieS(N, m) - pcieS(N - 1, m) + delta;
  };

  // The PCIe box (0020, 0021): address, length, MPS and RCB; the request on the RCB grid
  // cut into its blocks, the count by the dynamic program and by the closed form, the
  // count per number of completions, and the map of the splits (rows, as on the page) when
  // there are few enough to draw.
  const pcieView = () => ({
    mount(box) {
      const PRESETS = [["0x1010", 256, 256, 64, "0020: ‏0x1010, ‏256 B, ‏MPS 256"], ["0x1010", 256, 128, 64, "0020 : אותה בקשה עם MPS 128"],
                       ["0x1000", 256, 256, 64, "0021 א : ‏0x1000, ‏256 B"], ["0x1000", 512, 256, 64, "0021 ב : ‏0x1000, ‏512 B"],
                       ["0x1010", 512, 256, 64, "0021 ב : ‏0x1010, ‏512 B"], ["0x1020", 128, 128, 64, "0021 ג : ‏0x1020, ‏128 B, ‏MPS 128 (δ = 1)"]];
      const defaults = { addr: box.dataset.addr || "0x1010", len: Number(box.dataset.len || 256), mps: Number(box.dataset.mps || 256), rcb: Number(box.dataset.rcb || 64) };
      const st = { ...defaults, cuts: null, shown: null };   // cuts: the boundaries chosen by hand, null = the greedy split's; shown: the cuts drawn
      const MAX_ROWS = 40;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>דוגמאות מהדפים <select class="ex-preset"><option value="">בחרו...</option>${PRESETS.map((p, i) => `<option value="${i}">${p[4]}</option>`).join("")}</select></label>` +
        `<label>הכתובת ${ltr("A")} <input type="text" class="ex-addr" value="${st.addr}" size="8" dir="ltr" inputmode="text" aria-label="כתובת הבקשה, בהקסדצימלי" spellcheck="false"></label>` +
        `<label><span>האורך ${ltr("L")} (בתים)</span><input type="range" class="ex-len" min="4" max="2048" step="4" value="${st.len}" dir="ltr"><output class="out-len" dir="ltr"></output></label>` +
        `<label>MPS <select class="ex-mps">${[128, 256, 512, 1024, 2048, 4096].map((v) => `<option value="${v}"${v === st.mps ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<label>RCB <select class="ex-rcb">${[64, 128].map((v) => `<option value="${v}"${v === st.rcb ? " selected" : ""}>${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button>` +
        `<label><input type="checkbox" class="ex-choose" checked> לבחור חיתוכים בעצמי</label></div>` +
        `<p class="ex-summary" aria-live="polite"></p><div class="pcie-blocks"></div><p class="pcie-choose"></p><div class="pcie-counts"></div><div class="pcie-map"></div>`;
      const $ = (sel) => box.querySelector(sel);
      const hex = (v) => "0x" + v.toString(16).toUpperCase();
      const big = (v) => v.toLocaleString("en-US");
      const parseAddr = () => {
        const t = $(".ex-addr").value.trim().toLowerCase().replace(/^0x/, "");
        const v = /^[0-9a-f]{1,8}$/.test(t) ? parseInt(t, 16) : NaN;
        return Number.isNaN(v) ? null : v;
      };
      // An address axis like the page figures: base .. base + span mapped to x0 .. x1
      const axis = (addr, len, rcb, x0, x1) => {
        const base = Math.floor(addr / rcb) * rcb;
        const endBlock = Math.ceil((addr + len) / rcb) * rcb;
        const span = endBlock + rcb - base;
        const sc = (x1 - x0) / span;
        const x = (a) => x0 + (a - base) * sc;
        const grid = (y0, y1, labelsY = 16) => {
          let g = "";
          const every = span <= 6 * rcb ? 1 : span <= 12 * rcb ? 2 : span <= 24 * rcb ? 4 : 8;
          for (let off = 0, i = 0; off <= span; off += rcb, i++) {
            g += `<line class="cs-rcb" x1="${f(x(base + off))}" y1="${y0}" x2="${f(x(base + off))}" y2="${y1}"/>`;
            if (i % every === 0) g += `<text class="coord halo" x="${f(x(base + off))}" y="${labelsY}" text-anchor="middle">${hex(base + off)}</text>`;
          }
          [addr, addr + len].forEach((a) => { g += `<line class="cs-req" x1="${f(x(a))}" y1="${y0}" x2="${f(x(a))}" y2="${y1}"/>`; });
          return g;
        };
        return { x, grid, span };
      };
      const segment = (ax, cls, start, size, y, h, title) => {
        const a = ax.x(start), b = ax.x(start + size);
        let g = `<rect class="${cls}" x="${f(a)}" y="${y}" width="${f(b - a)}" height="${h}" rx="3"><title>${title}</title></rect>`;
        if (b - a >= 22) g += `<text class="cs-size" x="${f((a + b) / 2)}" y="${f(y + h / 2 + 4.5)}" text-anchor="middle">${size}</text>`;
        else if (b - a >= 14) g += `<text class="cs-size" x="${f((a + b) / 2)}" y="${f(y + h / 2 + 3.5)}" text-anchor="middle" style="font-size:9px">${size}</text>`;
        // narrower bars keep only their tooltip: a label above would collide with the row before
        return g;
      };
      const blocksSvg = (addr, len, mps, rcb, cuts) => {
        const ax = axis(addr, len, rcb, 40, 600);
        const sizes = pcieBlocks(addr, len, rcb), N = sizes.length, m = mps / rcb;
        const d = N === m + 1 && len <= mps ? 1 : 0, H = cuts ? 160 : 132;
        let g = `<svg class="figure cs-fig pcie-live" viewBox="0 0 640 ${H}" style="max-width:40rem" role="${cuts ? "group" : "img"}" aria-label="הבקשה על רשת ה-RCB, חתוכה ל-${N} בלוקים${cuts ? "; לחיצה על גבול חותכת שם או מבטלת" : ""}">${ax.grid(26, cuts ? 122 : 96)}`;
        let pos = addr;
        sizes.forEach((sz, i) => {
          const cls = i === 0 ? "cs-first" : i === N - 1 ? "cs-last" : "cs-mid";
          g += segment(ax, cls, pos, sz, 50, 28, `block ${i + 1}: ${hex(pos)}–${hex(pos + sz - 1)}, ${sz} bytes`);
          pos += sz;
        });
        if (cuts) {
          // the completions the chosen cuts form, under the blocks; one above MPS is marked
          const sp = pcieSplitOf(addr, len, mps, rcb, cuts);
          let at = addr;
          sp.sizes.forEach((size, i) => {
            const r = size > mps ? "bad" : sp.sizes.length === 1 ? "one" : i === 0 ? "first" : i === sp.sizes.length - 1 ? "last" : "mid";
            g += segment(ax, `cs-${r}`, at, size, 88, 24, `${hex(at)}–${hex(at + size - 1)}: ${size} bytes${size > mps ? ` > MPS ${mps}` : ""}`);
            at += size;
          });
          pcieBoundaries(addr, len, rcb).forEach((b) => {
            const on = cuts.includes(b);
            g += `<g class="cs-pick${on ? " is-cut" : ""}" data-b="${b}" tabindex="0" role="button" aria-pressed="${on}" aria-label="${hex(b)}, ${on ? "חותכים כאן" : "לא חותכים כאן"}">` +
                 `<line class="cs-pick-line" x1="${f(ax.x(b))}" x2="${f(ax.x(b))}" y1="44" y2="116"/><circle class="cs-can" cx="${f(ax.x(b))}" cy="50" r="7"><title>${hex(b)}</title></circle></g>`;
          });
        } else pcieBoundaries(addr, len, rcb).forEach((b) => { g += `<circle class="cs-can" cx="${f(ax.x(b))}" cy="50" r="4"><title>boundary ${hex(b)}</title></circle>`; });
        g += `<text class="legend" x="40" y="${H - 14}">N = ${N}, |B| = ${N - 1}, f = ${sizes[0]}, e = ${sizes[N - 1]}, m = MPS / RCB = ${m}, δ = ${d}${d ? " (N = m + 1 and L ≤ MPS)" : ""}</text>`;
        return g + "</svg>";
      };
      const mapSvg = (addr, len, mps, rcb, rows, total) => {
        const labelW = Math.max(...rows.map((sp) => sp.join("+").length)) * 8.2 + 16;   // room for "48+64+64+64+16"
        const x0 = Math.min(330, Math.max(128, Math.round(labelW)));
        const ax = axis(addr, len, rcb, x0, 612);
        const row = 22, gap = 6, head = 24;
        const groups = new Map();
        rows.forEach((sp) => { if (!groups.has(sp.length)) groups.set(sp.length, []); groups.get(sp.length).push(sp); });
        let height = 30 + 4;
        groups.forEach((g) => { height += head + g.length * (row + gap); });
        let g = `<svg class="figure cs-fig pcie-live" viewBox="0 0 640 ${height}" style="max-width:40rem" role="img" aria-label="${rows.length} מתוך ${total} הפיצולים, שורה לכל פיצול">${ax.grid(24, height - 4)}`;
        let y = 30;
        groups.forEach((list, n) => {
          g += `<text class="legend halo" x="${x0 + 8}" y="${y + 15}" font-weight="700">${n} ${n === 1 ? "completion" : "completions"}: ${list.length}${rows.length < total ? "+" : ""} ${list.length === 1 && rows.length === total ? "split" : "splits"}</text>`;
          y += head;
          list.forEach((sp) => {
            g += `<text class="coord halo" x="${x0 - 10}" y="${y + 15}" text-anchor="end">${sp.join("+")}</text>`;
            let pos = addr;
            sp.forEach((size, i) => {
              const r = sp.length === 1 ? "one" : i === 0 ? "first" : i === sp.length - 1 ? "last" : "mid";
              g += segment(ax, `cs-${r}`, pos, size, y, row, `${hex(pos)}–${hex(pos + size - 1)}: ${size} bytes (${r})`);
              pos += size;
            });
            y += row + gap;
          });
        });
        return g + "</svg>";
      };
      const draw = () => {
        const addr = parseAddr();
        $(".out-len").textContent = String(st.len);
        if (addr === null) { $(".ex-summary").innerHTML = "הכתובת צריכה להיות מספר הקסדצימלי, למשל ‏<bdi dir=\"ltr\">0x1010</bdi>."; return; }
        const { len, mps, rcb } = st;
        if (mps < rcb) { $(".ex-summary").textContent = "בשאלה MPS ≥ RCB."; return; }
        const sizes = pcieBlocks(addr, len, rcb), N = sizes.length, m = mps / rcb;
        const byK = pcieByCompletions(addr, len, mps, rcb), total = byK.reduce((a, b) => a + b, 0n);
        const formula = pcieFormula(addr, len, mps, rcb);
        const crosses = (addr % 4096) + len > 4096;
        const first = pcieSplits(addr, len, mps, rcb, 1)[0];
        const blocksText = N === 1 ? `בלוק אחד של ${sizes[0]}` : `${sizes[0]}` + (N > 2 ? ` + ${N - 2} × ${rcb}` : "") + ` + ${sizes[N - 1]}`;
        $(".ex-summary").innerHTML =
          `בקשה של ${ltr(`${len} B`)} מכתובת ${ltr(hex(addr))} על רשת ${ltr(`RCB = ${rcb}`)} : ‏${ltr(`N = ${N}`)} בלוקים (${ltr(blocksText)}), ‏${ltr(`m = ${m}`)}. ` +
          `מספר הפיצולים החוקיים עם ${ltr(`MPS = ${mps}`)} : <b>${ltr(big(total))}</b>` +
          (total === formula ? ` (הנוסחה הסגורה נותנת אותו מספר).` : ` (הנוסחה הסגורה נותנת ${ltr(big(formula))}!).`) +
          (first ? ` הפיצול החמדני, עם הכי פחות Completions : ${ltr(first.join("+"))}.` : " אין פיצול חוקי.") +
          (crosses ? ` <b>הבקשה חוצה גבול 4 KB</b>, וזה אסור ב-PCIe; המספר מחושב כאילו מותר.` : "");
        // the hand-made split: the greedy split's cuts until a boundary is clicked, then the
        // clicked cuts for as long as they are all boundaries of the request
        const choose = $(".ex-choose").checked, B = pcieBoundaries(addr, len, rcb);
        if (st.cuts !== null && st.cuts.some((b) => !B.includes(b))) st.cuts = null;
        let at = addr;
        const cuts = st.cuts || (first ? first.slice(0, -1).map((v) => (at += v)) : []);
        st.shown = cuts;
        $(".pcie-blocks").innerHTML = `<p class="ex-title">הבלוקים : הבקשה על רשת ה-RCB, הגבולות הפנימיים בירוק${choose ? "; לחיצה על גבול חותכת שם, והשורה שמתחת היא ה-Completions" : ""}</p>${blocksSvg(addr, len, mps, rcb, choose ? cuts : null)}`;
        if (choose) {
          const sp = pcieSplitOf(addr, len, mps, rcb, cuts), all = 1n << BigInt(B.length), over = sp.sizes.filter((v) => v > mps);
          $(".pcie-choose").innerHTML = `החיתוכים שבחרתם : ${ltr(sp.sizes.join("+"))}, ${ltr(sp.sizes.length)} Completions. ` +
            (sp.ok ? `<span class="eu-ok">✓ כולם עד ${ltr(`MPS = ${mps}`)}.</span> ` : `<span class="eu-bad">✗ ${ltr(over.join(", "))} גדול מ-${ltr(`MPS = ${mps}`)}.</span> `) +
            `פיצול הוא בדיוק בחירה של תת-קבוצה של ${ltr(`|B| = ${B.length}`)} הגבולות : יש ${ltr(`2^${B.length} = ${big(all)}`)} תת-קבוצות, ומהן ${ltr(big(total))} לא משאירות קטע ארוך מ-MPS. זה מספר הפיצולים.`;
        } else $(".pcie-choose").innerHTML = "";
        const counts = byK.map((w, k) => (k && w ? `<tr><td>${k}</td><td>${big(w)}</td></tr>` : "")).join("");
        $(".pcie-counts").innerHTML = total > 1n ? `<p class="ex-title">כמה פיצולים יש לכל מספר Completions</p><table class="pcie-table" dir="ltr"><thead><tr><th>Completions</th><th>פיצולים</th></tr></thead><tbody>${counts}</tbody></table>` : "";
        if (total === 0n) { $(".pcie-map").innerHTML = ""; }
        else {
          const rows = pcieSplits(addr, len, mps, rcb, MAX_ROWS);
          const note = BigInt(rows.length) < total ? `רק ${rows.length} הראשונים מתוך ${big(total)} מצוירים, בסדר של הפונקציה (החיתוך הרחוק קודם)` : `כל ${rows.length === 1 ? "הפיצול היחיד" : `${rows.length} הפיצולים`}, מקובצים לפי מספר ה-Completions`;
          $(".pcie-map").innerHTML = `<p class="ex-title">${note}</p>${mapSvg(addr, len, mps, rcb, rows, Number(total))}` +
            `<span class="viz-legend"><span><i class="cs-first"></i>ה-Completion הראשון (או היחיד)</span><span><i class="cs-mid"></i>אמצעי</span><span><i class="cs-last"></i>אחרון</span><span><i class="cs-rcb"></i>גבול RCB</span><span><i class="cs-req"></i>קצות הבקשה</span></span>`;
        }

      };
      $(".ex-addr").addEventListener("input", draw);
      $(".ex-choose").addEventListener("change", draw);
      const pick = (g, keyboard) => {
        const b = Number(g.dataset.b);
        const cur = st.shown || [];
        st.cuts = cur.includes(b) ? cur.filter((v) => v !== b) : cur.concat([b]).sort((u, v) => u - v);
        draw();
        if (keyboard) { const again = box.querySelector(`.cs-pick[data-b="${b}"]`); if (again) again.focus(); }
      };
      $(".pcie-blocks").addEventListener("click", (e) => { const g = e.target.closest(".cs-pick"); if (g) pick(g, false); });
      $(".pcie-blocks").addEventListener("keydown", (e) => { const g = e.target.closest(".cs-pick"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(g, true); } });
      $(".ex-len").addEventListener("input", () => { st.len = Number($(".ex-len").value); draw(); });
      $(".ex-mps").addEventListener("change", () => { st.mps = Number($(".ex-mps").value); draw(); });
      $(".ex-rcb").addEventListener("change", () => { st.rcb = Number($(".ex-rcb").value); draw(); });
      $(".ex-preset").addEventListener("change", () => {
        const p = PRESETS[Number($(".ex-preset").value)];
        if (!p) return;
        [$(".ex-addr").value, st.len, st.mps, st.rcb] = p;
        $(".ex-len").value = st.len; $(".ex-mps").value = st.mps; $(".ex-rcb").value = st.rcb;
        draw();
      });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, defaults, { cuts: null });
        $(".ex-addr").value = st.addr; $(".ex-len").value = st.len; $(".ex-mps").value = st.mps; $(".ex-rcb").value = st.rcb; $(".ex-preset").value = "";
        draw();
      });
      draw();
    },
  });

  // Part b's recurrence (0021): C(n) splits of n blocks into runs of 1 to m blocks,
  // C(n) = C(n − 1) + ... + C(n − m) with C(0) = 1 and C(n) = 0 below 0; the terms of
  // C(n) are the cases "the first completion takes i blocks", each leaving C(n − i).
  const ladderC = (N, m) => {
    const c = [1];
    for (let n = 1; n <= N; n++) { let v = 0; for (let i = 1; i <= m && i <= n; i++) v += c[n - i]; c.push(v); }
    return c;
  };
  const ladderTerms = (n, m) => {
    const c = ladderC(n, m), out = [];
    for (let i = 1; i <= m && i <= n; i++) out.push({ i, rest: n - i, value: c[n - i] });
    return out;
  };

  // The ladder box (0021 part b): N up to 16 and m = MPS / RCB from 2 to 4; C(0..N) as a
  // row of cells, a click (or next / previous) picks C(n) and lights the terms it sums,
  // the sum written out, and a strip of n blocks per term with the first completion
  // covering i blocks and the rest left to C(n − i).
  const ladderView = () => ({
    mount(box) {
      const D = { N: Number(box.dataset.n || 9), m: Number(box.dataset.m || 4), n: Number(box.dataset.pick || 8) };
      const st = { ...D };
      box.innerHTML =
        `<div class="ex-controls"><label><span>‏N, מספר הבלוקים</span><input type="range" class="ld-N" min="1" max="16" step="1" value="${D.N}" dir="ltr" aria-label="מספר הבלוקים הגדול ביותר בשורה"><output class="ld-out-N"></output></label>` +
        `<label>‏m = MPS / RCB <select class="ld-m" aria-label="כמה בלוקים יכול Completion אחד להכיל">${[2, 3, 4].map((v) => `<option value="${v}">${v}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<div class="ex-controls ex-play-row"><button type="button" class="md-button ex-prev">‏n הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">‏n הבא</button><span class="ex-pos"></span></div>` +
        `<div class="ld-row" dir="ltr" role="group" aria-label="הערכים C(0) עד C(N), לחיצה בוחרת ערך"></div>` +
        `<p class="wv-step ld-eq" aria-live="polite"></p><div class="ld-strips"></div><p class="ex-summary ld-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const draw = () => {
        st.n = Math.max(1, Math.min(st.n, st.N));
        const c = ladderC(st.N, st.m), terms = ladderTerms(st.n, st.m), lit = new Map(terms.map((t) => [t.rest, t.i]));
        $(".ld-N").value = st.N; $(".ld-out-N").textContent = String(st.N); $(".ld-m").value = String(st.m);
        $(".ld-row").innerHTML = c.map((v, k) => `<button type="button" class="ld-cell${k === st.n ? " is-sel" : lit.has(k) ? " is-term" : ""}" data-n="${k}" aria-pressed="${k === st.n}" aria-label="C(${k}) = ${v}"${k === 0 ? " disabled" : ""}>` +
          `<small>C(${k})</small><b>${v}</b><small class="ld-i">${lit.has(k) ? `i = ${lit.get(k)}` : ""}</small></button>`).join("");
        $(".ex-pos").textContent = `‏n = ${st.n}`;
        $(".ex-prev").disabled = st.n <= 1; $(".ex-next").disabled = st.n >= st.N;
        $(".ld-eq").innerHTML = `ה-Completion הראשון מכסה ${terms.length === 1 ? "בלוק אחד" : `בין 1 ל-${ltr(terms.length)} בלוקים`}, וכל מקרה משאיר את אותה בעיה על פחות בלוקים${NB}: ` +
          `<span class="ld-math" dir="ltr">C(${st.n}) = ${terms.map((t) => `C(${t.rest})`).join(" + ")} = ${terms.map((t) => t.value).join(" + ")} = ${c[st.n]}</span>`;
        $(".ld-strips").innerHTML = terms.map((t) => `<div class="ld-line"><span class="ld-lab">‏i = ${t.i}</span><span class="ld-strip" dir="ltr">` +
          Array.from({ length: st.n }, (_, b) => `<i class="${b < t.i ? "ld-first" : "ld-rest"}${b === t.i - 1 ? " is-end" : ""}"></i>`).join("") +
          `</span><span class="ld-txt">${t.rest ? `ועוד ${ltr(`C(${t.rest}) = ${t.value}`)} ${t.value === 1 ? "דרך" : "דרכים"} לחלק את ${t.rest === 1 ? "הבלוק שנשאר" : `${ltr(t.rest)} הבלוקים שנשארו`}` : `Completion אחד לכל הבלוקים, ${ltr("C(0) = 1")}`}</span></div>`).join("");
        const tag = st.m === 4 && st.n === 8 ? ` זו הבקשה המיושרת של העמוד, 108 פיצולים.` : st.m === 4 && st.n === 9 ? ` זו הבקשה הלא מיושרת של העמוד, 208 פיצולים.` : "";
        $(".ld-sum").innerHTML = `בלי MPS כל אחד מ-${ltr(st.n - 1)} הגבולות הפנימיים חותך או לא, ${ltr(`2^${st.n - 1} = ${2 ** (st.n - 1)}`)} פיצולים. ` +
          (c[st.n] < 2 ** (st.n - 1) ? `עם Completion של עד ${ltr(st.m)} בלוקים נשארים ${ltr(c[st.n])}${NB}: הפיצולים שבהם Completion מכסה יותר מ-${ltr(st.m)} בלוקים נפסלים.` : `כאן ${ltr(`n ≤ ${st.m}`)}, ולכן אף פיצול לא נפסל.`) + tag;
      };
      $(".ld-row").addEventListener("click", (e) => { const b = e.target.closest(".ld-cell"); if (b && !b.disabled) { st.n = Number(b.dataset.n); draw(); const again = box.querySelector(`.ld-cell[data-n="${st.n}"]`); if (again) again.focus(); } });
      $(".ld-N").addEventListener("input", () => { st.N = Number($(".ld-N").value); draw(); });
      $(".ld-m").addEventListener("change", () => { st.m = Number($(".ld-m").value); draw(); });
      $(".ex-next").addEventListener("click", () => { st.n++; draw(); });
      $(".ex-prev").addEventListener("click", () => { st.n--; draw(); });
      $(".ex-reset").addEventListener("click", () => { Object.assign(st, D); draw(); });
      draw();
    },
  });

  dvqExplorers.register({
    views: { pcie: pcieView, ladder: ladderView },
    help: {
      pcie: "כתובת, אורך, MPS ו-RCB : התיבה חותכת את הבקשה לבלוקים, סופרת את הפיצולים בתכנות דינמי ובנוסחה סגורה, ומציירת את מפת הפיצולים כשהם מעטים. ה-presets טוענים את דוגמאות העמוד. עם ״לבחור חיתוכים בעצמי״ לוחצים על הגבולות כדי לחתוך או לא, ורואים את ה-Completions שנוצרים.",
      ladder: "לחיצה על C(n) בשורה, או ״n הבא״, מדליקה את האיברים שהוא סוכם : לכל i, ה-Completion הראשון מכסה i בלוקים, ומה שנשאר הוא C(n − i). N ו-m משנים את השורה.",
    },
    models: { pcieBoundaries, pcieBlocks, pcieSplitOf, pcieSplits, pcieByCompletions, pcieCount, pcieS, pcieFormula, ladderC, ladderTerms },
  });
})();
