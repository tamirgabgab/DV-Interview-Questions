// kinds: gray
//   gray                   0034        a pointer step through a synchroniser, bit by bit, in binary and in Gray, for 3 to 6 bits; a FIFO of 8 to 64 entries with the pointers one bit wider, the flags and a strip of the operations
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { W, bitsOf, code, ltr, seedControls, waveStrip } = dvqExplorers.lib;

  // Gray pointers (0034): the page's conversions, a sampled step b -> b + 1 where each
  // changing bit arrived or not, and the page's full / empty rules.
  const grayOf = (b) => b ^ (b >> 1);
  const grayToBin = (g, bits) => {
    let b = 0, acc = 0;
    for (let i = bits - 1; i >= 0; i--) { acc ^= (g >> i) & 1; b |= acc << i; }
    return b;
  };
  // `arrived` maps a bit index to 1 (the new value was sampled) or 0 (the old one);
  // bits that do not change are the same either way.
  const graySample = (b, bits, arrivedBin, arrivedGray) => {
    const size = 1 << bits, nb = (b + 1) % size;
    const ob = b, og = grayOf(b), ng = grayOf(nb);
    const changedBin = [], changedGray = [];
    for (let i = 0; i < bits; i++) {
      if (((ob ^ nb) >> i) & 1) changedBin.push(i);
      if (((og ^ ng) >> i) & 1) changedGray.push(i);
    }
    const pick = (oldV, newV, changed, arrived) => {
      let v = oldV;
      changed.forEach((i) => { if (arrived[i]) v = (v & ~(1 << i)) | (newV & (1 << i)); });
      return v;
    };
    const seenBin = pick(ob, nb, changedBin, arrivedBin || {});
    const seenGray = pick(og, ng, changedGray, arrivedGray || {});
    return {
      oldB: ob, newB: nb, oldG: og, newG: ng, changedBin, changedGray, seenBin, seenGray,
      binValid: seenBin === ob || seenBin === nb,
      seenGrayAsBin: grayToBin(seenGray, bits),
      wrongCount: changedBin.length >= 1 ? (1 << changedBin.length) - 2 : 0,
    };
  };
  // The FIFO strip: the operations so far, one column each (a burst is several), with the
  // pointers and the flags after it; a full FIFO refuses a write and an empty one a read,
  // so a burst stops early. Column 0 is the reset.
  const grayFlagsOps = (ops, size) => {
    const bits = Math.log2(size) + 1, wrap = 2 * size - 1;
    let w = 0, r = 0;
    const col = (op) => { const fl = grayFlags(w, r, bits); return { op, w, r, wg: fl.wg, rg: fl.rg, full: fl.full, empty: fl.empty, occupancy: fl.occupancy }; };
    const cols = [col(null)];
    ops.forEach((op) => {
      const fl = grayFlags(w, r, bits);
      if (op === "w" && !fl.full) { w = (w + 1) & wrap; cols.push(col("w")); }
      else if (op === "r" && !fl.empty) { r = (r + 1) & wrap; cols.push(col("r")); }
    });
    return cols;
  };
  const grayFlags = (w, r, bits) => {
    const wg = grayOf(w), rg = grayOf(r);
    const top = 3 << (bits - 2), rest = (1 << (bits - 2)) - 1;
    const empty = wg === rg;
    const full = (wg & top) === (~rg & top) && (wg & rest) === (rg & rest);
    const occupancy = (w - r) & ((1 << bits) - 1);
    return { wg, rg, empty, full, occupancy };
  };

  // The Gray pointer box (0034). data-mode="sync": a step b -> b + 1 of a 4-bit pointer
  // seen through a synchroniser, every changing bit tapped as arrived or not (or drawn
  // at random), in binary and in Gray side by side, for a pointer of 3 to 6 bits.
  // data-mode="flags": a FIFO of 8 to 64 entries with pointers one bit wider than the
  // address, write and read, the pointers in binary and Gray, empty and full by the
  // page's rules.
  const grayView = (box) => ({
    mount() {
      if (box.dataset.mode === "flags") { grayFlagsMount(box); return; }
      const st = { bits: 4, b: 7, arrBin: {}, arrGray: {} };
      let BITS = 4;
      box.innerHTML =
        `<div class="ex-controls"><label>רוחב <select class="ex-bits" aria-label="מספר הביטים של המצביע">${[3, 4, 5, 6].map((w) => `<option value="${w}"${w === 4 ? " selected" : ""}>${w} ביטים</option>`).join("")}</select></label>` +
        `<label><span>המצביע לפני הצעד</span><input type="range" class="ex-b" min="0" max="15" step="1" value="7" dir="ltr" aria-label="המצביע לפני הצעד"><output class="ex-bout"></output></label>` +
        `<button type="button" class="md-button ex-random">הגרלה : אילו ביטים הגיעו</button>` +
        `<button type="button" class="md-button ex-all">הכול הגיע</button>` +
        `<button type="button" class="md-button ex-none">כלום עוד לא הגיע</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של השאלה</button></div>` +
        `<p class="wv-hint">כל ביט שמשתנה בצעד עובר סנכרן משלו, ויכול להידגם ישן או חדש. לחיצה על ביט כזה בשורה "נדגם" הופכת אותו.</p>` +
        `<div class="gr-box"><div class="gr-side gr-bin"></div><div class="gr-side gr-gray"></div></div>` +
        `<p class="ex-summary gr-sum" aria-live="polite"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const side = (title, oldV, newV, changed, arrived, seen, kind) => {
        const bitsRow = (label, v, sampled) => `<div class="gr-row"><span class="gr-label">${label}</span><span class="gr-bits" dir="ltr">` +
          [...Array(BITS)].map((_, j) => {
            const i = BITS - 1 - j, ch = changed.includes(i), bit = (v >> i) & 1;
            if (sampled && ch) return `<button type="button" class="gr-bit gr-btn ${arrived[i] ? "is-new" : "is-old"}" data-kind="${kind}" data-i="${i}" aria-label="${bit}, ביט ${i} : ${arrived[i] ? "החדש הגיע" : "עדיין הישן"}, לחיצה הופכת">${bit}</button>`;
            return `<span class="gr-bit${ch && !sampled ? " is-changed" : ""}">${bit}</span>`;
          }).join("") + `</span><span class="gr-dec">${ltr(v)}</span></div>`;
        return `<p class="ex-title">${title}</p>` + bitsRow("ישן", oldV, false) + bitsRow("חדש", newV, false) + bitsRow("נדגם", seen, true);
      };
      const draw = () => {
        BITS = st.bits;
        const r = graySample(st.b, BITS, st.arrBin, st.arrGray);
        $(".ex-b").max = String((1 << BITS) - 1); $(".ex-b").value = st.b; $(".ex-bout").textContent = String(st.b);
        const bin = side(`בינארי : ${ltr(`${bitsOf(r.oldB, BITS)} → ${bitsOf(r.newB, BITS)}`)}, ${ltr(r.changedBin.length)} ביטים משתנים`, r.oldB, r.newB, r.changedBin, st.arrBin, r.seenBin, "bin");
        const gray = side(`‏Gray : ${ltr(`${bitsOf(r.oldG, BITS)} → ${bitsOf(r.newG, BITS)}`)}, ביט אחד משתנה`, r.oldG, r.newG, r.changedGray, st.arrGray, r.seenGray, "gray");
        const binV = r.binValid
          ? `<p class="gr-ok">הקורא רואה ${ltr(r.seenBin)} : ${r.seenBin === r.oldB ? "הערך הישן" : "הערך החדש"}, ערך שהמצביע באמת עבר בו ✓</p>`
          : `<p class="gr-bad">הקורא רואה ${ltr(r.seenBin)} : לא הישן ולא החדש. המצביע מעולם לא היה שם, והתפוסה שהקורא יחשב שגויה ב-${ltr(Math.abs(r.seenBin - r.oldB))} מילים ✗</p>`;
        const grayV = `<p class="gr-ok">הקורא רואה ${ltr(bitsOf(r.seenGray, BITS))}, כלומר ${ltr(r.seenGrayAsBin)} : ${r.seenGray === r.oldG ? "הערך הישן (במקרה הגרוע הוא מחכה מחזור נוסף)" : "הערך החדש"} ✓</p>`;
        $(".gr-bin").innerHTML = bin + binV;
        $(".gr-gray").innerHTML = gray + grayV;
        const k = r.changedBin.length;
        $(".gr-sum").innerHTML = `בצעד ${ltr(`${r.oldB} → ${r.newB}`)} משתנים ${ltr(k)} ביטים בבינארי : ${ltr(`2^${k} = ${1 << k}`)} צירופים של ישן/חדש, ${ltr(r.wrongCount)} מהם ערכים שגויים. ב-Gray משתנה ביט אחד : שני צירופים, שניהם ערכים שהמצביע עבר בהם.`;
      };
      const randomize = (rng) => {
        const r = graySample(st.b, BITS, {}, {});
        st.arrBin = {}; st.arrGray = {};
        r.changedBin.forEach((i) => { st.arrBin[i] = rng() < 0.5 ? 1 : 0; });
        r.changedGray.forEach((i) => { st.arrGray[i] = rng() < 0.5 ? 1 : 0; });
      };
      const setAll = (v) => { for (let i = 0; i < BITS; i++) { st.arrBin[i] = v; st.arrGray[i] = v; } };
      $(".ex-b").addEventListener("input", () => { st.b = Number($(".ex-b").value); draw(); });
      $(".ex-random").addEventListener("click", () => seed.draw());
      $(".ex-all").addEventListener("click", () => { setAll(1); draw(); });
      $(".ex-none").addEventListener("click", () => { setAll(0); draw(); });
      box.addEventListener("click", (e) => {
        const b = e.target.closest(".gr-btn");
        if (!b) return;
        const map = b.dataset.kind === "bin" ? st.arrBin : st.arrGray, i = Number(b.dataset.i);
        map[i] = map[i] ? 0 : 1;
        draw();
      });
      // the page's example: 4 bits, bits 3 and 0 arrived, 2 and 1 did not (1110); in Gray the old value
      const page = () => { st.bits = 4; $(".ex-bits").value = "4"; st.b = 7; st.arrBin = { 3: 1, 0: 1, 2: 0, 1: 0 }; st.arrGray = { 3: 0 }; draw(); };
      $(".ex-reset").addEventListener("click", page);
      // a new width: the step before the wrap (all bits change), nothing arrived yet
      $(".ex-bits").addEventListener("change", () => { st.bits = Number($(".ex-bits").value); st.b = (1 << (st.bits - 1)) - 1; st.arrBin = {}; st.arrGray = {}; draw(); });
      page();
      const seed = seedControls(box, $(".ex-reset"), (rng) => { randomize(rng); draw(); });
    },
  });
  const grayFlagsMount = (box) => {
    const st = { size: 16, w: 0, r: 0, hist: [], ops: [] };
    const KEEP = 64;                                       // columns kept on the strip
    const bitsN = () => Math.log2(st.size) + 1;          // one bit above the address
    box.innerHTML =
      `<div class="ex-controls"><label>עומק ה-FIFO <select class="ex-size" aria-label="מספר הכניסות">${[8, 16, 32, 64].map((v) => `<option value="${v}"${v === 16 ? " selected" : ""}>${v} כניסות</option>`).join("")}</select></label>` +
      `<button type="button" class="md-button md-button--primary ex-write">כתיבה</button>` +
      `<button type="button" class="md-button md-button--primary ex-read">קריאה</button>` +
      `<button type="button" class="md-button ex-write8"></button>` +
      `<button type="button" class="md-button ex-read8"></button>` +
      `<button type="button" class="md-button ex-prev">צעד אחורה</button>` +
      `<button type="button" class="md-button ex-start">איפוס</button></div>` +
      `<div class="gr-slots" dir="ltr" role="img"></div>` +
      `<div class="gr-ptrs"></div><p class="ex-summary gr-sum" aria-live="polite"></p>` +
      `<p class="ex-title">רצועת התזמון : עמודה לכל כתיבה או קריאה, המצביעים אחריה והדגלים</p>` +
      `<div class="wv-wrap gr-strip" tabindex="0" role="group" aria-label="רצועת התזמון של ה-FIFO, גלילה אופקית"></div>`;
    const $ = (sel) => box.querySelector(sel);
    const draw = () => {
      const BITS = bitsN(), SIZE = st.size, half = SIZE / 2, fl = grayFlags(st.w, st.r, BITS);
      $(".ex-write").disabled = fl.full; $(".ex-write8").disabled = fl.full;
      $(".ex-read").disabled = fl.empty; $(".ex-read8").disabled = fl.empty;
      $(".ex-write8").textContent = `${half} כתיבות`; $(".ex-read8").textContent = `${half} קריאות`;
      $(".ex-prev").disabled = !st.hist.length;
      const wa = st.w & (SIZE - 1), ra = st.r & (SIZE - 1);
      let cells = "";
      for (let i = 0; i < SIZE; i++) {
        const filled = ((i - ra) & (SIZE - 1)) < fl.occupancy;
        cells += `<span class="gr-slot${filled ? " is-full" : ""}"><span class="gr-w">${i === wa ? "W" : ""}</span><span class="gr-idx">${i}</span><span class="gr-r">${i === ra ? "R" : ""}</span></span>`;
      }
      const slots = $(".gr-slots");
      slots.innerHTML = cells;
      slots.style.setProperty("--gr-cols", String(Math.min(SIZE, 16)));
      slots.setAttribute("aria-label", `${SIZE} הכניסות של ה-FIFO, המלאות מודגשות, עם מצביעי הכתיבה והקריאה`);
      const split = (v, n) => { const s = bitsOf(v, BITS); return n === 1 ? `<span class="gr-top2">${s[0]}</span>${s.slice(1)}` : `<span class="gr-top">${s[0]}</span><span class="gr-top2">${s[1]}</span>${s.slice(2)}`; };
      $(".gr-ptrs").innerHTML = `<table><thead><tr><th>המצביע</th><th>בינארי (${ltr(BITS)} ביטים)</th><th>‏Gray</th><th>כתובת</th></tr></thead><tbody>` +
        `<tr><td>כתיבה ${code("wptr")}</td><td dir="ltr">${split(st.w, 1)}</td><td dir="ltr">${split(fl.wg, 2)}</td><td>${ltr(wa)}</td></tr>` +
        `<tr><td>קריאה ${code("rptr")}</td><td dir="ltr">${split(st.r, 1)}</td><td dir="ltr">${split(fl.rg, 2)}</td><td>${ltr(ra)}</td></tr></tbody></table>`;
      const wg = bitsOf(fl.wg, BITS), rg = bitsOf(fl.rg, BITS);
      const topFlip = wg.slice(0, 2) === rg.slice(0, 2).replace(/[01]/g, (c) => (c === "0" ? "1" : "0"));
      const low = BITS - 1, lowBits = bitsOf(wa, low);
      let sum = `תפוסה ${ltr(fl.occupancy)} מתוך ${ltr(SIZE)} (ההפרש בין המצביעים מודולו ${ltr(2 * SIZE)}). `;
      sum += fl.empty ? `<span class="gr-ok">ריק ✓</span> : שני ה-Gray שווים (${ltr(wg)} = ${ltr(rg)}). `
        : `ריק? לא : ${ltr(wg)} ≠ ${ltr(rg)}. `;
      sum += fl.full ? `<span class="gr-ok">מלא ✓</span> : שני הביטים העליונים הפוכים (${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))}) ו-${ltr(BITS - 2)} הנמוכים שווים (${ltr(wg.slice(2))}).`
        : `מלא? לא : ` + (topFlip ? `העליונים הפוכים, אבל הנמוכים ${ltr(wg.slice(2))} מול ${ltr(rg.slice(2))}.` : `העליונים ${ltr(wg.slice(0, 2))} מול ${ltr(rg.slice(0, 2))} אינם הפוכים.`);
      if (fl.occupancy === 0 && st.w !== 0) sum += ` בלי הביט הנוסף המצביעים היו ${ltr(lowBits)} ו-${ltr(bitsOf(ra, low))} : שווים, בדיוק כמו במצב מלא.`;
      if (fl.full) sum += ` ${ltr(low)} הביטים הנמוכים של שני המצביעים שווים (${ltr(lowBits)})  : בלי הביט הנוסף זה היה נראה ריק.`;
      $(".gr-sum").innerHTML = sum;
      // the strip: the last KEEP columns of the operations so far
      const all = grayFlagsOps(st.ops, SIZE), first = Math.max(0, all.length - KEEP), cols = all.slice(first);
      const SW = Math.round(16 + 7.6 * BITS), n = cols.length;
      const wrapEl = $(".gr-strip");
      wrapEl.innerHTML = waveStrip([
        { name: "wr", kind: "bit", values: cols.map((c) => (c.op === "w" ? 1 : 0)), cls: "wv-s2" },
        { name: "rd", kind: "bit", values: cols.map((c) => (c.op === "r" ? 1 : 0)), cls: "wv-s3" },
        { name: "wptr", kind: "bus", values: cols.map((c) => bitsOf(c.w, BITS)) },
        { name: "wptr Gray", kind: "bus", values: cols.map((c) => bitsOf(c.wg, BITS)) },
        { name: "rptr", kind: "bus", values: cols.map((c) => bitsOf(c.r, BITS)) },
        { name: "rptr Gray", kind: "bus", values: cols.map((c) => bitsOf(c.rg, BITS)) },
        { name: "full", kind: "bit", values: cols.map((c) => (c.full ? 1 : 0)), cls: "wv-s1" },
        { name: "empty", kind: "bit", values: cols.map((c) => (c.empty ? 1 : 0)), cls: "wv-s1" },
      ], n, { slotW: SW, labelW: 84, cursor: n - 1, ticks: (k) => first + k, label: `רצועת התזמון של ה-FIFO : ${n} עמודות` });
      wrapEl.scrollLeft = wrapEl.scrollWidth;
    };
    const step = (dw, dr) => {
      const BITS = bitsN(), wrap = 2 * st.size - 1;
      st.hist.push([st.w, st.r, st.ops.length]); if (st.hist.length > 200) st.hist.shift();
      for (let i = 0; i < dw; i++) if (!grayFlags(st.w, st.r, BITS).full) { st.w = (st.w + 1) & wrap; st.ops.push("w"); }
      for (let i = 0; i < dr; i++) if (!grayFlags(st.w, st.r, BITS).empty) { st.r = (st.r + 1) & wrap; st.ops.push("r"); }
      draw();
    };
    $(".ex-write").addEventListener("click", () => step(1, 0));
    $(".ex-read").addEventListener("click", () => step(0, 1));
    $(".ex-write8").addEventListener("click", () => step(st.size / 2, 0));
    $(".ex-read8").addEventListener("click", () => step(0, st.size / 2));
    $(".ex-prev").addEventListener("click", () => { const h = st.hist.pop(); if (h) { [st.w, st.r] = h; st.ops.length = h[2]; } draw(); });
    $(".ex-start").addEventListener("click", () => { st.w = 0; st.r = 0; st.hist = []; st.ops = []; draw(); });
    $(".ex-size").addEventListener("change", () => { st.size = Number($(".ex-size").value); st.w = 0; st.r = 0; st.hist = []; st.ops = []; draw(); });
    draw();
  };

  dvqExplorers.register({
    views: { gray: grayView },
    help: {
      gray: "בסנכרן בוחרים מצביע ורוחב, וכל ביט שמשתנה נדגם ישן או חדש (בלחיצה או ב״הגרלה״). ב-FIFO ״כתיבה״ ו״קריאה״ מזיזים את המצביעים, empty ו-full מחושבים לפי הכללים, ורצועת התזמון מוסיפה עמודה לכל פעולה.",
    },
    models: { grayOf, grayToBin, graySample, grayFlags, grayFlagsOps },
  });
})();
