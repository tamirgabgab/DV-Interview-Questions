// kinds: repunit
//   repunit                0005        the bonus proof by pigeonhole: R1, R11, R111 … dropped into the x remainder slots one by one until two share a slot, then R_i − R_j = 1…10…0 shown as a multiple of x
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, f, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";

  // The repunits R_k = 11…1 (k ones) modulo x, R_{k+1} = 10 R_k + 1, until the first k
  // whose remainder an earlier R_j already had: rems[k - 1] is R_k mod x, and i, j are the
  // two that share a slot (i > j). With x slots and x + 1 repunits, i <= x + 1.
  const repunitDrops = (x) => {
    const rems = [], seen = new Map();
    let r = 0;
    for (let k = 1; ; k++) {
      r = (10 * r + 1) % x;
      rems.push(r);
      if (seen.has(r)) return { rems, i: k, j: seen.get(r) };
      seen.set(r, k);
    }
  };
  // R_i − R_j: i − j ones then j zeros, and the quotient by x (exact, as a BigInt string).
  const repunitDiff = (x, i, j) => {
    const digits = "1".repeat(i - j) + "0".repeat(j), big = BigInt(digits);
    return { digits, quotient: (big / BigInt(x)).toString(), exact: big % BigInt(x) === 0n };
  };

  // The pigeonhole box (0005 bonus): a slider for x; the repunits dropped one per step into
  // the x remainder slots (ten per row), each with its remainder from the one before; at
  // the first collision the slot lights and the difference is written as x times a number.
  const PER = 10, SW = 60, SH = 44, GX = 20, GY = 10;
  const repunitView = () => ({
    mount(box) {
      const X0 = Math.min(40, Math.max(2, Number(box.dataset.x || 7)));
      const st = { x: X0, k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><label><span>x</span><input type="range" class="ex-x" min="2" max="40" step="1" value="${X0}" dir="ltr" aria-label="x, מ-2 עד 40"><output class="out-x">${X0}</output></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">המספר הבא</button>` +
        `<button type="button" class="md-button ex-prev">הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1600, 900, 350) +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-end">עד ההתנגשות</button><span class="ex-pos"></span></div>` +
        `<p class="ex-title rp-title"></p><div class="rp-slots"></div>` +
        `<span class="viz-legend"><span><i class="rp-key-new"></i>המספר שנזרק עכשיו</span><span><i class="rp-key-hit"></i>שני מספרים באותו שובך</span></span>` +
        `<p class="wv-step rp-step" aria-live="polite"></p><p class="ex-summary rp-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const run = () => repunitDrops(st.x);
      const ones = (k) => (k <= 24 ? "1".repeat(k) : `1…1 (${k} אחדות)`);
      const slots = (r) => {
        const rows = Math.ceil(st.x / PER), W = GX * 2 + PER * SW, H = GY + rows * (SH + 22) + 4;
        const at = new Map();
        for (let k = 1; k <= st.k; k++) { const v = r.rems[k - 1]; at.set(v, (at.get(v) || []).concat([k])); }
        const hit = st.k === r.i ? r.rems[r.i - 1] : null;
        let s = `<svg class="figure rp-svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${st.x} שובכים, אחד לכל שארית, ו-${st.k} מספרים שנזרקו">`;
        for (let v = 0; v < st.x; v++) {
          const x = GX + (v % PER) * SW, y = GY + Math.floor(v / PER) * (SH + 22), ks = at.get(v) || [];
          s += `<rect class="rp-slot${v === hit ? " is-hit" : ""}" x="${x + 3}" y="${y}" width="${SW - 6}" height="${SH}" rx="5"/>` +
               `<text class="tick" x="${x + SW / 2}" y="${y + SH + 15}" text-anchor="middle">${v}</text>`;
          ks.forEach((k, n) => {
            const cy = y + (ks.length === 1 ? SH / 2 : n === 0 ? SH / 3 : (2 * SH) / 3);
            s += `<text class="rp-chip${k === st.k ? " is-new" : ""}" x="${x + SW / 2}" y="${f(cy + 4)}" text-anchor="middle">R${k}</text>`;
          });
        }
        return s + "</svg>";
      };
      const draw = () => {
        const r = run();
        st.k = Math.min(st.k, r.i);
        $(".out-x").textContent = String(st.x);
        $(".rp-title").textContent = `${st.x} שובכים, אחד לכל שארית בחלוקה ב-${st.x} (מספר השארית מתחת לשובך)`;
        $(".rp-slots").innerHTML = slots(r);
        $(".ex-pos").textContent = `${st.k} מתוך ${r.i}`;
        const k = st.k, rem = k ? r.rems[k - 1] : 0, prev = k > 1 ? r.rems[k - 2] : 0;
        $(".rp-step").innerHTML = !k
          ? `עוד לא נזרק אף מספר. יש ${ltr(st.x)} שובכים, ולכן בין ${ltr(`x + 1 = ${st.x + 1}`)} המספרים ${ltr("R1 … R" + (st.x + 1))} יהיו בוודאות שניים באותו שובך.`
          : `\u200f${ltr(`R${k} = ${ones(k)}`)}${NB}: השארית שלו ${ltr(k === 1 ? `1 mod ${st.x} = ${rem}` : `(10 · ${prev} + 1) mod ${st.x} = ${rem}`)}` +
            (k > 1 ? `, כי ${ltr(`R${k} = 10 · R${k - 1} + 1`)}.` : ".") +
            (k === r.i ? ` <b>השובך ${ltr(rem)} כבר תפוס על ידי ${ltr(`R${r.j}`)}.</b>` : rem === 0 ? ` שארית 0${NB}: כבר ${ltr(`R${k}`)} עצמו מתחלק ב-${ltr(st.x)}.` : "");
        if (k === r.i) {
          const d = repunitDiff(st.x, r.i, r.j), show = d.digits.length <= 30;
          $(".rp-sum").innerHTML = `ל-${ltr(`R${r.i}`)} ול-${ltr(`R${r.j}`)} אותה שארית, ולכן ${ltr(st.x)} מחלק את ההפרש${NB}: ` +
            `${ltr(`R${r.i} − R${r.j} = ${show ? d.digits : "1…1 0…0"}`)}, ${ltr(r.i - r.j)} אחדות ואחריהן ${ltr(r.j)} אפסים` +
            (show ? `, וזה ${ltr(`${st.x} · ${d.quotient}`)}` : "") + `. ההתנגשות הגיעה אחרי ${ltr(r.i)} מספרים, לכל היותר ${ltr(`x + 1 = ${st.x + 1}`)} כמו שהעיקרון מבטיח.`;
        } else $(".rp-sum").textContent = "";
        $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = k >= r.i;
      };
      let stop = () => {};
      $(".ex-x").addEventListener("input", () => { stop(); st.x = Number($(".ex-x").value); st.k = 0; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); st.x = X0; st.k = 0; $(".ex-x").value = X0; draw(); });
      $(".ex-next").addEventListener("click", () => { stop(); st.k++; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.k > 0) { st.k--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = run().i; draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= run().i, restart: () => { st.k = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { repunit: repunitView },
    help: {
      repunit: "בוחרים x : ״המספר הבא״ ו״הפעלה״ זורקים את R1, R2, R3 … לשובך של השארית שלהם, עד ששניים נופלים לאותו שובך. אז השורה האחרונה כותבת את ההפרש כ-x כפול מספר.",
    },
    models: { repunitDrops, repunitDiff },
  });
})();
