// kinds: lpmtrie
//   lpmtrie                0103        parts b and c, longest prefix match: a table of up to six 8-bit prefixes (value/length or bits*, each with a hop) and the trie drawn from it, binary (one bit a step) or multibit with two bits a step (the expanded entries marked); a typed address walked step by step with the best match so far, against the scan of part a
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, attr, autoplay, bitsOf, f, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const W = 8, ROWS = 6;

  // --- the models (tests/0103/test_0103.py checks them against tools/figures/q0103.py) ----

  // One row of the table: "v/k" (v from 0 to 2^w - 1, k from 0 to w) or bits and a star
  // ("101*", "*" for /0). { empty } for an empty field, { error } for a bad one, else the
  // prefix as a string of bits, its value with the bits past k cleared, and norm when the
  // value had bits past k (the row is stored normalized).
  const lpmParse = (text, w = W) => {
    const s = String(text).trim();
    if (!s) return { empty: true };
    let m = /^([01]*)\*$/.exec(s);
    if (m) {
      if (m[1].length > w) return { error: `לכל היותר ${w} ביטים לפני הכוכבית` };
      const bits = m[1];
      return { bits, len: bits.length, value: parseInt((bits + "0".repeat(w)).slice(0, w), 2), norm: false };
    }
    m = /^(\d+)\s*\/\s*(\d+)$/.exec(s);
    if (!m) return { error: "כתבו ערך/אורך, כמו 160/3, או ביטים וכוכבית, כמו 101*" };
    const v = Number(m[1]), k = Number(m[2]);
    if (v > 2 ** w - 1) return { error: `הערך הוא לכל היותר ${2 ** w - 1}` };
    if (k > w) return { error: `האורך הוא לכל היותר ${w}` };
    const all = v.toString(2).padStart(w, "0"), bits = all.slice(0, k);
    const value = parseInt((bits + "0".repeat(w)).slice(0, w), 2);
    return { bits, len: k, value, norm: value !== v, given: v };
  };
  const lpmHopOk = (h) => /^[A-Za-z0-9]{1,3}$/.test(String(h).trim());
  // the hop of the longest prefix the address bits start with; the later of two equal rows
  const lpmBest = (routes, bits) => {
    let got = null, len = -1;
    routes.forEach(([p, hop]) => { if (bits.startsWith(p) && p.length >= len) { got = hop; len = p.length; } });
    return got;
  };
  // the nodes of the binary trie: every prefix of every prefix string, the root ""
  const lpmNodes = (routes) => {
    const set = new Set([""]);
    routes.forEach(([p]) => { for (let i = 0; i <= p.length; i++) set.add(p.slice(0, i)); });
    return [...set].sort((a, b) => a.length - b.length || (a < b ? -1 : a > b ? 1 : 0));
  };
  const lpmHolder = (routes) => {
    const out = {};
    routes.forEach(([p, hop]) => { out[p] = hop; });
    return out;
  };
  // the walk of the binary trie: [node, its hop or null, the best so far] per node visited
  const lpmPath = (routes, bits) => {
    const nodes = new Set(lpmNodes(routes)), held = lpmHolder(routes), out = [];
    let b = null;
    for (let i = 0; i <= bits.length; i++) {
      const node = bits.slice(0, i);
      if (!nodes.has(node)) break;
      const h = node in held ? held[node] : null;
      if (h !== null) b = h;
      out.push([node, h, b]);
    }
    return out;
  };
  // x of every node in units: two children's subtrees side by side, a single child half a
  // unit off its parent (to the right of a 0 child, to the left of a 1 child)
  const lpmLayout = (nodeList) => {
    const nodes = new Set(nodeList), pos = {};
    const go = (n) => {
      const kids = ["0", "1"].map((b) => n + b).filter((k) => nodes.has(k));
      if (!kids.length) { pos[n] = 0; return [0, 0]; }
      if (kids.length === 1) {
        const [lo, hi] = go(kids[0]);
        pos[n] = pos[kids[0]] + (kids[0].endsWith("0") ? 0.5 : -0.5);
        return [Math.min(lo, pos[n]), Math.max(hi, pos[n])];
      }
      const [lo0, hi0] = go(kids[0]), [lo1, hi1] = go(kids[1]);
      const shift = hi0 - lo1 + 1;
      Object.keys(pos).forEach((x) => { if (x.startsWith(kids[1])) pos[x] += shift; });
      pos[n] = (pos[kids[0]] + pos[kids[1]]) / 2;
      return [lo0, hi1 + shift];
    };
    const [lo, hi] = go("");
    Object.keys(pos).forEach((x) => { pos[x] -= lo; });
    return { pos, width: hi - lo };
  };
  // a /k prefix is expanded to the next multiple of s, at least s
  const lpmTarget = (k, s) => Math.max(s, Math.ceil(k / s) * s);
  // The multibit trie's memories level by level, nodes numbered in the order the rows create
  // them: levels[d] holds 2^s entries per node, each [hop or null, child or null, the
  // original length of its hop's prefix (-1: none)]; names[d][n] is node n's bits.
  const lpmLevels = (routes, w, s) => {
    const F = 1 << s, L = w / s;
    const levels = Array.from({ length: L }, () => []), names = Array.from({ length: L }, () => []);
    const index = Array.from({ length: L }, () => new Map());
    const node = (d, name) => {
      if (!index[d].has(name)) {
        index[d].set(name, names[d].length);
        names[d].push(name);
        for (let j = 0; j < F; j++) levels[d].push([null, null, -1]);
      }
      return index[d].get(name);
    };
    node(0, "");
    routes.forEach(([p, hop]) => {
      const T = lpmTarget(p.length, s);
      let n = 0;
      for (let d = 0; d < T / s - 1; d++) {
        const i = n * F + parseInt(p.slice(d * s, (d + 1) * s), 2);
        const child = node(d + 1, p.slice(0, (d + 1) * s));
        levels[d][i][1] = child;
        n = child;
      }
      const d = T / s - 1, free = T - p.length;
      const base = n * F + (p.length > d * s ? parseInt(p.slice(d * s), 2) << free : 0);
      for (let j = 0; j < 1 << free; j++) {
        const e = levels[d][base + j];
        if (p.length >= e[2]) { e[0] = hop; e[2] = p.length; }
      }
    });
    return { levels, names };
  };
  // the walk of the multibit trie: per level read, the node, the s bits, the entry and the
  // best so far; it stops at an entry with no child
  const lpmMultiPath = (routes, w, s, addr) => {
    const { levels, names } = lpmLevels(routes, w, s), F = 1 << s, out = [];
    let n = 0, b = null;
    for (let d = 0; d < w / s; d++) {
      const chunk = (addr >> (w - (d + 1) * s)) & (F - 1), [hop, child, len] = levels[d][n * F + chunk];
      if (hop !== null) b = hop;
      out.push({ d, node: n, name: names[d][n], chunk, hop, child, len, best: b });
      if (child === null) break;
      n = child;
    }
    return out;
  };

  // --- the box ---------------------------------------------------------------------------

  const PRESETS = {
    nested: { addr: 185, rows: [["0/0", "D"], ["128/1", "A"], ["160/3", "B"], ["176/5", "C"], ["64/2", "E"], ["", ""]] },
    deflt: { addr: 100, rows: [["0/0", "D"], ["200/5", "A"], ["202/8", "B"], ["48/4", "C"], ["", ""], ["", ""]] },
    none: { addr: 0, rows: [["128/1", "A"], ["160/3", "B"], ["176/5", "C"], ["64/2", "E"], ["", ""], ["", ""]] },
  };
  const star = (p) => `${p}*`;
  const nodeName = (n) => (n === "" ? "השורש" : `הצומת <code>${n}</code>`);

  // the binary trie: every node, the walk up to step k lit, the best so far ringed
  const binarySvg = (routes, bits, k) => {
    const nodes = lpmNodes(routes), held = lpmHolder(routes), path = lpmPath(routes, bits);
    const { pos, width } = lpmLayout(nodes);
    const seen = path.slice(0, k), on = new Set(seen.map((x) => x[0]));
    const win = seen.filter((x) => x[1] !== null).map((x) => x[0]).pop();
    const cur = k ? seen[k - 1][0] : null;
    const U = 44, R = 13, DY = 36, X0 = 40, Y0 = 22;
    const deep = Math.min(W, Math.max(...nodes.map((n) => n.length)) + 1);   // room for the missing child under the deepest node
    const Wd = Math.max(240, Math.round(2 * X0 + width * U)), H = Y0 + deep * DY + 28;
    const off = (Wd - (2 * X0 + width * U)) / 2;
    const X = (n) => X0 + off + pos[n] * U, Y = (n) => Y0 + n.length * DY;
    let s = `<svg class="lpm-trie lpm-box-trie" viewBox="0 0 ${Wd} ${H}" style="max-width:${f(Wd / 16, 3)}rem" direction="ltr" role="img" aria-label="${attr(`עץ הביטים, ${nodes.length} צמתים, והחיפוש של ${parseInt(bits, 2)} אחרי ${k} צעדים`)}">`;
    nodes.forEach((n) => {
      if (!n) return;
      const par = n.slice(0, -1);
      s += `<line class="lpm-edge${on.has(n) ? " is-on" : ""}" x1="${f(X(par))}" y1="${f(Y(par))}" x2="${f(X(n))}" y2="${f(Y(n))}"/>`;
      const mx = (X(par) + X(n)) / 2, my = (Y(par) + Y(n)) / 2;
      s += `<text class="lpm-bit" x="${f(mx + (n.endsWith("0") ? -9 : 9))}" y="${f(my + 4)}" text-anchor="middle">${n.slice(-1)}</text>`;
    });
    const last = path[path.length - 1][0];
    if (k === path.length && last.length < bits.length) {          // the missing child where the walk stops
      const x0 = X(last), y0 = Y(last), x1 = x0 + (bits[last.length] === "0" ? -0.5 : 0.5) * U, y1 = y0 + DY;
      s += `<line class="lpm-edge lpm-miss" x1="${f(x0)}" y1="${f(y0)}" x2="${f(x1)}" y2="${f(y1 - R)}"/>` +
        `<text class="lpm-miss-t" x="${f(x1)}" y="${f(y1 + 4)}" text-anchor="middle">×</text>`;
    }
    nodes.forEach((n) => {
      const h = n in held ? held[n] : null;
      const cls = ["lpm-node", h !== null ? "has-hop" : "no-hop", on.has(n) ? "is-on" : "", n === win ? "is-win" : "", n === cur ? "is-cur" : ""].filter(Boolean).join(" ");
      const tip = `${n || "השורש"}${NB}: ${h !== null ? `הקידומת ${star(n)} אל ${h}` : "אין קידומת"}`;
      s += `<g class="${cls}"><circle cx="${f(X(n))}" cy="${f(Y(n))}" r="${R}"/>` +
        (h !== null ? `<text x="${f(X(n))}" y="${f(Y(n) + 4)}" text-anchor="middle">${attr(h)}</text>` : "") + `<title>${attr(tip)}</title></g>`;
    });
    for (let d = 0; d <= deep; d++) s += `<text class="lpm-depth" x="6" y="${f(Y0 + d * DY + 4)}">${d}</text>`;
    return s + "</svg>";
  };

  // the multibit trie: a node is a row of 2^s entries; an entry holds a hop (dashed when it
  // was expanded from a shorter prefix) and a line down to its child; the walk lit
  const multiSvg = (routes, s, addr, k) => {
    const { levels, names } = lpmLevels(routes, W, s), F = 1 << s, L = W / s;
    const walk = lpmMultiPath(routes, W, s, addr), seen = walk.slice(0, k);
    const CW = 30, CH = 28, NW = CW * F, GAP = 18, DY = 76, X0 = 40, Y0 = 22;
    // x of every node: leaves in order, a parent centred over its children
    const x = names.map((lv) => lv.map(() => 0));
    let next = 0;
    const place = (d, n) => {
      const kids = d + 1 < L ? levels[d].slice(n * F, n * F + F).map((e) => e[1]).filter((c) => c !== null) : [];
      if (!kids.length) { x[d][n] = next; next += NW + GAP; return; }
      kids.forEach((c) => place(d + 1, c));
      x[d][n] = (x[d + 1][kids[0]] + x[d + 1][kids[kids.length - 1]]) / 2;
    };
    place(0, 0);
    const used = names.filter((lv) => lv.length).length, Wd = Math.max(300, X0 + next - GAP + 16), H = Y0 + (used - 1) * DY + CH + 44;
    const off = (Wd - (X0 + next - GAP + 16)) / 2;
    const NX = (d, n) => X0 + off + x[d][n], NY = (d) => Y0 + d * DY;
    const lit = new Set(seen.map((e) => `${e.d}.${e.node}.${e.chunk}`)), on = new Set(seen.map((e) => `${e.d}.${e.node}`));
    const winAt = seen.filter((e) => e.hop !== null).pop(), cur = k ? seen[k - 1] : null;
    let out = `<svg class="lpm-trie lpm-multi" viewBox="0 0 ${f(Wd, 0)} ${H}" style="max-width:${f(Wd / 16, 3)}rem" direction="ltr" role="img" aria-label="${attr(`עץ של ${s} ביטים בצעד, ${names.reduce((a, lv) => a + lv.length, 0)} צמתים של ${F} כניסות, והחיפוש של ${addr} אחרי ${k} צעדים`)}">`;
    let edges = "", cells = "";
    names.forEach((lv, d) => lv.forEach((name, n) => {
      const x0 = NX(d, n), y0 = NY(d);
      for (let j = 0; j < F; j++) {
        const [hop, child, len] = levels[d][n * F + j], cx = x0 + j * CW, key = `${d}.${n}.${j}`;
        if (child !== null) {
          const on2 = lit.has(key) && seen.some((e) => e.d === d + 1 && e.node === child);
          edges += `<line class="lpm-edge${on2 ? " is-on" : ""}" x1="${f(cx + CW / 2)}" y1="${f(y0 + CH)}" x2="${f(NX(d + 1, child) + NW / 2)}" y2="${f(NY(d + 1))}"/>`;
        }
        const exp = hop !== null && len < (d + 1) * s;
        const cls = ["lpm-cell", hop !== null ? "has-hop" : "no-hop", exp ? "is-exp" : "", lit.has(key) ? "is-on" : "",
          winAt && key === `${winAt.d}.${winAt.node}.${winAt.chunk}` ? "is-win" : "", cur && key === `${cur.d}.${cur.node}.${cur.chunk}` ? "is-cur" : ""].filter(Boolean).join(" ");
        const chunk = j.toString(2).padStart(s, "0");
        const src = hop !== null ? (name + chunk).slice(0, len) : "";
        const tip = `${name + chunk}${NB}: ${hop !== null ? `${hop}, מהקידומת ${star(src)}${exp ? " שהורחבה" : ""}` : "בלי קפיצה"}${child !== null ? ", ויש בן" : ""}`;
        cells += `<g class="${cls}"><rect x="${f(cx)}" y="${f(y0)}" width="${CW}" height="${CH}"/>` +
          (hop !== null ? `<text x="${f(cx + CW / 2)}" y="${f(y0 + CH / 2 + 5)}" text-anchor="middle">${attr(hop)}</text>` : "") +
          `<title>${attr(tip)}</title></g>` +
          `<text class="lpm-chunk" x="${f(cx + CW / 2)}" y="${f(y0 - 4)}" text-anchor="middle">${chunk}</text>`;
      }
      cells += `<rect class="lpm-mnode${on.has(`${d}.${n}`) ? " is-on" : ""}" x="${f(x0)}" y="${f(y0)}" width="${NW}" height="${CH}"/>`;
    }));
    const end = walk[walk.length - 1];
    if (k === walk.length && end.d < L - 1) {                     // the entry with no child where the walk stops
      const cx = NX(end.d, end.node) + end.chunk * CW + CW / 2, cy = NY(end.d) + CH;
      edges += `<line class="lpm-edge lpm-miss" x1="${f(cx)}" y1="${f(cy)}" x2="${f(cx)}" y2="${f(cy + 22)}"/>`;
      cells += `<text class="lpm-miss-t" x="${f(cx)}" y="${f(cy + 38)}" text-anchor="middle">×</text>`;
    }
    for (let d = 0; d < used; d++) out += `<text class="lpm-depth" x="6" y="${f(NY(d) + CH / 2 + 5)}">${d}</text>`;
    return out + edges + cells + "</svg>";
  };

  const lpmView = () => ({
    mount(box) {
      const ds = box.dataset, start = PRESETS.nested;
      const st = { k: 0 };
      const rowHtml = (i) => `<tr data-i="${i}"><td class="lpm-n">${i + 1}</td>` +
        `<td><input type="text" class="lpm-pfx" dir="ltr" spellcheck="false" autocomplete="off" aria-label="הקידומת של שורה ${i + 1}, ערך/אורך או ביטים וכוכבית"></td>` +
        `<td><input type="text" class="lpm-hop" dir="ltr" spellcheck="false" autocomplete="off" maxlength="3" aria-label="הקפיצה של שורה ${i + 1}"></td>` +
        `<td class="lpm-bits" dir="ltr"></td><td class="lpm-hit"></td></tr>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>הכתובת <input type="number" class="ex-num lpm-addr" min="0" max="255" step="1" dir="ltr" aria-label="הכתובת, מספר מ-0 עד 255"></label>` +
        `<span class="lpm-abits" dir="ltr" aria-label="הביטים של הכתובת"></span>` +
        `<label>צעד של <select class="lpm-stride"><option value="1">ביט אחד</option><option value="2">שני ביטים</option></select></label>` +
        `<button type="button" class="md-button lpm-pre" data-p="nested">מקוננות</button>` +
        `<button type="button" class="md-button lpm-pre" data-p="deflt">ברירת מחדל</button>` +
        `<button type="button" class="md-button lpm-pre" data-p="none">אין התאמה</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1800, 1000, 450) +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<p class="wv-step lpm-step" aria-live="polite"></p>` +
        `<div class="lpm-figwrap"></div>` +
        `<span class="viz-legend lpm-legend"><span><i class="lpm-key-hop"></i>קידומת</span><span class="lpm-only2"><i class="lpm-key-exp"></i>הורחבה</span>` +
        `<span><i class="lpm-key-on"></i>הדרך</span><span><i class="lpm-key-win"></i>הטובה עד עכשיו</span></span>` +
        `<div class="lpm-tabwrap" tabindex="0" role="region" aria-label="טבלת הניתוב"><table class="lpm-tab"><thead><tr><th>#</th><th>הקידומת</th><th>הקפיצה</th><th>הביטים</th><th>מתאימה</th></tr></thead><tbody>` +
        Array.from({ length: ROWS }, (_, i) => rowHtml(i)).join("") + `</tbody></table></div>` +
        `<p class="lpm-note" aria-live="polite"></p><p class="lpm-naive"></p>` +
        `<div class="lpm-pathwrap" tabindex="0" role="region" aria-label="הדרך של החיפוש צעד אחרי צעד"></div>`;
      answer(box, NB); answer(box, null);           // the answer line keeps its place from the first step
      const $ = (sel) => box.querySelector(sel);
      const addrIn = $(".lpm-addr"), strideIn = $(".lpm-stride");
      const pfx = [...box.querySelectorAll(".lpm-pfx")], hops = [...box.querySelectorAll(".lpm-hop")];
      const fill = (p) => {
        addrIn.value = String(p.addr);
        p.rows.forEach(([a, b], i) => { pfx[i].value = a; hops[i].value = b; });
      };
      fill(start);
      const a0 = Number(ds.addr);
      if (Number.isInteger(a0) && a0 >= 0 && a0 <= 255) addrIn.value = String(a0);
      strideIn.value = ds.stride === "2" ? "2" : "1";
      let addr = Number(addrIn.value), addrErr = "";
      // the table as the fields hold it: the good rows in order, and a note per row
      const table = () => {
        const routes = [], rows = [];
        pfx.forEach((inp, i) => {
          const p = lpmParse(inp.value), h = hops[i].value.trim();
          let err = p.error || "";
          if (!p.empty && !p.error && !lpmHopOk(h)) err = h ? "קפיצה היא עד שלוש אותיות או ספרות" : "חסרה קפיצה";
          if (p.empty && h) err = "חסרה קידומת";
          rows.push({ p, h, err });
          if (!p.empty && !err) routes.push([p.bits, h]);
        });
        return { routes, rows };
      };
      const stride = () => Number(strideIn.value);
      const steps = (routes) => (stride() === 1 ? lpmPath(routes, bitsOf(addr, W)).length : lpmMultiPath(routes, W, 2, addr).length);
      const pathTable = (routes) => {
        const s = stride(), k = st.k;
        let rowsHtml = "";
        if (s === 1) {
          const path = lpmPath(routes, bitsOf(addr, W));
          for (let i = 0; i < path.length; i++) {     // a row per node of the walk, the later ones dotted
            const e = i < k ? path[i] : null;
            const cls = !e ? "is-later" : i === k - 1 ? "is-cur" : "";
            rowsHtml += `<tr class="${cls}"><td>${i}</td>` + (e
              ? `<td dir="ltr">${e[0] ? `<code>${e[0]}</code>` : "ε"}</td><td>${e[1] !== null ? `${attr(e[1])}` : "–"}</td><td class="lpm-b">${e[2] !== null ? attr(e[2]) : "אין"}</td>`
              : `<td>·</td><td>·</td><td>·</td>`) + `</tr>`;
          }
          return `<table class="lpm-path"><thead><tr><th>עומק</th><th>הצומת</th><th>קידומת בו</th><th>הטובה</th></tr></thead><tbody>${rowsHtml}</tbody></table>`;
        }
        const walk = lpmMultiPath(routes, W, 2, addr);
        for (let i = 0; i < walk.length; i++) {
          const e = i < k ? walk[i] : null;
          const cls = !e ? "is-later" : i === k - 1 ? "is-cur" : "";
          rowsHtml += `<tr class="${cls}"><td>${i}</td>` + (e
            ? `<td dir="ltr"><code>${e.name}${e.name ? "·" : ""}${e.chunk.toString(2).padStart(2, "0")}</code></td><td>${e.hop !== null ? attr(e.hop) : "–"}${e.child !== null ? " ↓" : ""}</td><td class="lpm-b">${e.best !== null ? attr(e.best) : "אין"}</td>`
            : `<td>·</td><td>·</td><td>·</td>`) + `</tr>`;
        }
        return `<table class="lpm-path"><thead><tr><th>רמה</th><th>הכניסה</th><th>בה</th><th>הטובה</th></tr></thead><tbody>${rowsHtml}</tbody></table>`;
      };
      const stepText = (routes, T) => {
        const k = st.k, bits = bitsOf(addr, W), s = stride();
        if (k === 0) return `ההתחלה${NB}: הכתובת ${ltr(addr)}, הביטים ${ltr(`<code>${bits}</code>`)}. החיפוש מתחיל בשורש, ועוד אין קידומת טובה.`;
        let t;
        if (s === 1) {
          const path = lpmPath(routes, bits), [node, h, b] = path[k - 1];
          t = `עומק ${ltr(node.length)}, ${nodeName(node)}${NB}: ` +
            (h !== null ? `יש בו את ${ltr(`<code>${star(node)}</code>`)} אל ${attr(h)}, והיא הטובה עד עכשיו.` : `אין בו קידומת, ${b !== null ? `הטובה נשארת ${attr(b)}.` : "ועדיין אין טובה."}`);
          if (k < T) t += ` הביט הבא, ${bits[node.length]}, מוביל ל${nodeName(node + bits[node.length])}.`;
          else if (node.length === W) t += ` כל ${W} הביטים נקראו, והחיפוש נגמר.`;
          else t += ` לצומת אין בן בכיוון הביט הבא, ${bits[node.length]}, ולכן החיפוש נעצר.`;
        } else {
          const e = lpmMultiPath(routes, W, 2, addr)[k - 1], chunk = e.chunk.toString(2).padStart(2, "0");
          const src = e.hop !== null ? (e.name + chunk).slice(0, e.len) : "";
          t = `רמה ${ltr(e.d)}, ${nodeName(e.name)}, הכניסה ${ltr(`<code>${chunk}</code>`)}${NB}: ` +
            (e.hop !== null ? `הקפיצה ${attr(e.hop)}, מ-${ltr(`<code>${star(src)}</code>`)}${e.len < (e.d + 1) * 2 ? " שהורחבה" : ""}, והיא הטובה עד עכשיו.` : `בלי קפיצה, ${e.best !== null ? `הטובה נשארת ${attr(e.best)}.` : "ועדיין אין טובה."}`);
          if (e.child !== null) t += " יש לכניסה בן, והחיפוש יורד לרמה הבאה.";
          else if (e.d === W / 2 - 1) t += " זו הרמה האחרונה, והחיפוש נגמר.";
          else t += " אין לכניסה בן, ולכן החיפוש נעצר.";
        }
        return t;
      };
      const draw = () => {
        const { routes, rows } = table(), T = steps(routes);
        st.k = Math.min(Math.max(st.k, 0), T);
        const bits = bitsOf(addr, W), s = stride(), k = st.k;
        const readBits = s === 1 ? (k ? lpmPath(routes, bits)[k - 1][0].length : 0) : 2 * k;
        $(".lpm-abits").innerHTML = [...bits].map((c, i) => `<b class="${i < readBits ? "is-read" : ""}">${c}</b>${i % 4 === 3 && i < W - 1 ? " " : ""}`).join("");
        // the table: each row's bits and whether it matches the address
        const best = lpmBest(routes, bits);
        let winRow = -1, wl = -1;
        rows.forEach((r, i) => { if (!r.p.empty && !r.err && bits.startsWith(r.p.bits) && r.p.len >= wl) { winRow = i; wl = r.p.len; } });
        const notes = [];
        rows.forEach((r, i) => {
          const tr = box.querySelector(`.lpm-tab tr[data-i="${i}"]`), ok = !r.p.empty && !r.err;
          const hit = ok && bits.startsWith(r.p.bits);
          tr.className = [r.err ? "is-bad" : "", hit ? "is-hit" : "", i === winRow ? "is-win" : ""].filter(Boolean).join(" ");
          pfx[i].toggleAttribute("aria-invalid", Boolean(r.err) && !r.p.empty);
          tr.querySelector(".lpm-bits").innerHTML = ok ? `<code>${star(r.p.bits)}</code>` : r.err ? "?" : "";
          tr.querySelector(".lpm-hit").textContent = !hit ? "" : "✓";
          if (r.err) notes.push(`שורה ${i + 1}${NB}: ${r.err}.`);
          else if (r.p.norm) notes.push(`שורה ${i + 1}${NB}: ${ltr(`${r.p.given}/${r.p.len}`)} נשמרת כ-${ltr(`${r.p.value}/${r.p.len}`)}, ‏${ltr(`<code>${star(r.p.bits)}</code>`)}, בלי הביטים שאחרי האורך.`);
        });
        if (addrErr) notes.unshift(addrErr);
        $(".lpm-note").innerHTML = notes.length ? notes.join(" ") : NB;
        const matching = routes.filter(([p]) => bits.startsWith(p));
        $(".lpm-naive").innerHTML = `הסריקה של סעיף א${NB}: ` + (matching.length
          ? `${matching.length === 1 ? "שורה אחת מתאימה" : `${ltr(matching.length)} מתאימות`}, הארוכה ${ltr(`/${wl}`)}, התשובה <b>${attr(best)}</b>.`
          : "אף שורה לא מתאימה, אין תשובה.");
        $(".lpm-figwrap").innerHTML = s === 1 ? binarySvg(routes, bits, k) : multiSvg(routes, 2, addr, k);
        box.classList.toggle("lpm-is-multi", s === 2);
        const pw = $(".lpm-pathwrap");
        pw.innerHTML = pathTable(routes);
        const row = pw.querySelector("tr.is-cur");               // the current row in view, inside the region only
        pw.scrollTop = row ? Math.max(0, row.offsetTop - pw.clientHeight + row.offsetHeight + 4) : 0;
        $(".lpm-step").innerHTML = stepText(routes, T);
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = k >= T;
        if (k < T) { answer(box, null); return; }
        const got = s === 1 ? lpmPath(routes, bits)[T - 1][2] : lpmMultiPath(routes, W, 2, addr)[T - 1].best;
        const same = got === best ? "אותה תשובה" : "תשובה אחרת";
        answer(box, got !== null
          ? `לכתובת ${ltr(addr)} הקפיצה ${attr(got)}, אחרי ${T === 1 ? "צעד אחד" : `${ltr(T)} צעדים`} בעץ${NB}; הסריקה של כל השורות נותנת ${attr(best)}, ${same}.`
          : `לכתובת ${ltr(addr)} אין קידומת מתאימה, אחרי ${T === 1 ? "צעד אחד" : `${ltr(T)} צעדים`} בעץ${NB}; גם הסריקה לא מוצאת שורה, ${same}.`,
        ".lpm-tab tr.is-win");
      };
      let stop = () => {};
      // a change of the table, the address or the stride starts the walk over, or shows its new
      // end when the walk was at its end (st.atEnd, taken when a field gets the focus)
      const changed = () => { stop(); st.k = st.atEnd ? steps(table().routes) : 0; st.atEnd = false; draw(); };
      const remember = () => { st.atEnd = st.k > 0 && st.k >= steps(table().routes); };
      box.addEventListener("focusin", (e) => { if (e.target.matches("input, select")) remember(); });
      addrIn.addEventListener("change", () => {
        const v = Number(addrIn.value);
        if (addrIn.value.trim() === "" || !Number.isInteger(v) || v < 0 || v > 255) addrErr = `הכתובת היא מספר שלם מ-0 עד 255; נשארת ${addr}.`;
        else { addrErr = ""; addr = v; }
        changed();
      });
      strideIn.addEventListener("change", changed);
      [...pfx, ...hops].forEach((inp) => inp.addEventListener("change", changed));
      box.querySelectorAll(".lpm-pre").forEach((b) => b.addEventListener("click", () => {
        remember();
        fill(PRESETS[b.dataset.p]);
        addr = Number(addrIn.value); addrErr = "";
        changed();
      }));
      $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.k > 0) { st.k--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = steps(table().routes); draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= steps(table().routes), restart: () => { st.k = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { lpmtrie: lpmView },
    help: {
      lpmtrie: "״הצעד הבא״ ו״הפעלה״ מריצים את החיפוש : צומת בכל צעד (בצעד של שני ביטים, כניסה), עם הדרך והטובה עד עכשיו. הכתובת, הצעד, המצבים המוכנים ושדות הטבלה (ערך/אורך או ביטים וכוכבית, וקפיצה) קובעים את הדוגמה; שורת הסריקה היא סעיף א.",
    },
    models: { lpmParse, lpmBest, lpmNodes, lpmHolder, lpmPath, lpmLayout, lpmTarget, lpmLevels, lpmMultiPath },
    cols: { lpmtrie: { main: ".lpm-figwrap, .lpm-legend", side: ".lpm-step, .lpm-tabwrap, .lpm-note, .lpm-naive, .lpm-pathwrap", w: "minmax(0, 0.85fr)" } },
  });
})();
