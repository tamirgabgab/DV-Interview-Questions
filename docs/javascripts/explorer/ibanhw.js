// kinds: ibanhw
//   ibanhw                 0099        the hardware checker of part b (data-iban, data-version "final" or "buffer"): the IBAN as it arrives, a digit a clock (every letter as two digits, the first 6 the head), stepped clock by clock (step / play); the flip-flops of the chosen version bit by bit (h, r and the tail's counter n, or the head buffer, a counter and r), the tail of six zeros, the ones that changed this clock marked; the state that moved this clock with its ten edges and the one the digit took; at the end r + h against 1 and 98, valid or not
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const HEAD = 6;
  const IL = "IL620108000000099999999";
  const VERSIONS = {
    final: { name: "שארית לראש וזנב של אפסים, 17", ff: 17 },
    buffer: { name: "שמירת הראש, 34", ff: 34 },
  };

  // --- the models, as tools/figures/q0099.py step_hw, final_hw and run_* --------------------

  // the IBAN without spaces: two letters, two digits, then letters and digits, 5 to 34
  // characters; null otherwise
  const ihParse = (text) => {
    const s = String(text).replace(/\s+/g, "").toUpperCase();
    return /^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/.test(s) ? s : null;
  };
  // the digits as they arrive: the IBAN as written, every letter as two digits
  const ihStream = (s) => [...s].flatMap((c) => [...String(parseInt(c, 36))].map(Number));
  const ihStep = (r, d) => (10 * r + d) % 97;          // the two blocks: 10x + e, then mod 97
  // the registers after every clock: [{ regs, d, what, from }]; the last entry also carries
  // ok. final: h, r (97 + k in the head) and n, the counter of the tail of six zeros;
  // buffer: the head's digits b0..b5, a counter n and r, the head fed again at the end
  const ihTrace = (digits, version) => {
    const out = [];
    if (version === "buffer") {
      let r = 0, n = 0, buf = [];
      digits.forEach((d, k) => {
        if (k < HEAD) { buf = [...buf, d]; n++; out.push({ regs: { buf, n, r }, d, what: "keep" }); }
        else { const was = r; r = ihStep(r, d); out.push({ regs: { buf, n, r }, d, what: "r", from: was }); }
      });
      buf.forEach((d, k) => { const was = r; r = ihStep(r, d); out.push({ regs: { buf, n: HEAD - 1 - k, r }, d, what: "replay", from: was }); });
      if (out.length) out[out.length - 1].ok = r === 1;
      return out;
    }
    let h = 0, r = 97;
    digits.forEach((d) => {
      if (r >= 97) {
        const was = h;
        h = ihStep(h, d);
        r = r === 97 + HEAD - 1 ? 0 : r + 1;
        out.push({ regs: { h, r, n: 0 }, d, what: "h", from: was });
      } else {
        const was = r;
        r = ihStep(r, d);
        out.push({ regs: { h, r, n: 0 }, d, what: "r", from: was });
      }
    });
    if (r >= 97) { if (out.length) out[out.length - 1].ok = false; return out; }
    for (let t = 1; t <= 6; t++) {
      const was = r;
      r = ihStep(r, 0);
      out.push({ regs: { h, r, n: t }, d: 0, what: "tail", from: was });
    }
    out[out.length - 1].ok = r + h === 1 || r + h === 98;
    return out;
  };

  // --- the box ---------------------------------------------------------------------------------

  const bits = (v, n) => [...Array(n)].map((_, i) => (v >> (n - 1 - i)) & 1);
  const LAYOUT = {     // the flip-flops of each version: [name, width, value of regs]
    final: (g) => [["h", 7, g.h], ["r", 7, g.r], ["n", 3, g.n]],
    buffer: (g) => [...Array(HEAD)].map((_, k) => [`b${k}`, 4, g.buf[k] ?? 0]).concat([["n", 3, g.n], ["r", 7, g.r]]),
  };
  const START = { final: { h: 0, r: 97, n: 0 }, buffer: { buf: [], n: 0, r: 0 } };

  const ibanhwView = () => ({
    mount(box) {
      const s0 = ihParse(box.dataset.iban || "") || IL;
      const v0 = VERSIONS[box.dataset.version] ? box.dataset.version : "final";
      const st = { s: s0, v: v0, k: 0 };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>ה-IBAN</span><input type="text" class="ex-num ih-in" data-nolink dir="ltr" spellcheck="false" aria-label="ה-IBAN, אותיות וספרות"></label>` +
        `<label>הגרסה <select class="ih-ver" data-nolink aria-label="הגרסה של הבודק">${Object.entries(VERSIONS).map(([k, x]) => `<option value="${k}">${x.name}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button><span class="fl-err ih-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">השעון הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">השעון הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 450, 150) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ih-sum" aria-live="polite"></p>` +
        `<div class="ih-strip" dir="ltr" tabindex="0" role="region" aria-label="הספרות כפי שהן מגיעות, ספרה בכל שעון"></div>` +
        `<div class="ih-regs" dir="ltr" role="group" aria-label="הפליפ-פלופים, ביט אחרי ביט"></div>` +
        `<div class="ih-fan"></div>` +
        `<span class="viz-legend"><span><i class="ih-key-head"></i>ספרות הראש</span><span><i class="ih-key-now"></i>השעון של הרגע</span>` +
        `<span><i class="ih-key-tail"></i>ספרות 0 של הזנב</span><span><i class="ih-key-flip"></i>פליפ-פלופ שהשתנה</span><span><i class="ih-key-took"></i>הקשת של הספרה</span></span>` +
        `<p class="ih-note" aria-live="polite"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const trace = () => ihTrace(ihStream(st.s), st.v);
      const fan = (from, d, to, label) => {
        // the state that moved this clock and its ten edges, the one of the digit marked
        const W = 260, H = 330, x0 = 40, sy = 160;
        let g = `<svg class="ih-fig ih-live" viewBox="0 0 ${W} ${H}" role="img" aria-label="${label}">` +
          '<defs><marker id="ih-hl" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto"><path class="ih-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>';
        g += `<g class="ih-state ih-src"><circle cx="${x0}" cy="${sy}" r="22"/><text x="${x0}" y="${sy + 6}" text-anchor="middle">${from ?? "·"}</text></g>`;
        for (let e = 0; e < 10; e++) {
          const ty = 18 + e * 32, tx = x0 + 160, t = from == null ? "" : ihStep(from, e), took = from != null && e === d;
          g += `<path class="ih-edge${took ? " is-took" : from == null ? " is-off" : ""}" d="M${x0 + 22},${sy} C${x0 + 80},${sy} ${x0 + 80},${ty} ${tx - 20},${ty}" marker-end="url(#ih-hl)"/>`;
          g += `<text class="ih-lab${took ? " is-took" : ""}" x="${x0 + 104}" y="${ty - 4}" text-anchor="middle">${e}</text>`;
          g += `<g class="ih-state ih-small${took ? " is-took" : ""}"><circle cx="${tx}" cy="${ty}" r="15"/><text x="${tx}" y="${ty + 5}" text-anchor="middle">${t}</text></g>`;
        }
        return g + "</svg>";
      };

      const draw = () => {
        const tr = trace(), digits = ihStream(st.s), T = tr.length;
        st.k = Math.max(0, Math.min(st.k, T));
        $(".ih-in").value = st.s; $(".ih-ver").value = st.v;
        $(".ex-pos").textContent = `שעון ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === T;
        const cur = st.k ? tr[st.k - 1] : null, prev = st.k > 1 ? tr[st.k - 2].regs : START[st.v];
        const regs = cur ? cur.regs : START[st.v];
        // the stream: the digits as they arrive, and for the buffer version the head again
        const cells = digits.map((d, i) => [d, i < HEAD ? " ih-head" : ""]);
        if (st.v === "buffer") digits.slice(0, HEAD).forEach((d) => cells.push([d, " ih-head ih-replay"]));
        else if (tr.length > digits.length) for (let t = 0; t < 6; t++) cells.push([0, " ih-tail"]);
        $(".ih-strip").innerHTML = cells.map(([d, cls], i) => `<span class="ih-c${cls}${i === st.k - 1 ? " is-now" : ""}${i < st.k - 1 ? " is-past" : ""}">${d}</span>`).join("");
        // the flip-flops
        const lay = LAYOUT[st.v](regs), was = LAYOUT[st.v](prev);
        $(".ih-regs").innerHTML = lay.map(([name, w, v], gi) => {
          const old = bits(was[gi][2], w);
          return `<span class="ih-reg"><span class="ih-rname">${name}</span><span class="ih-bits">` +
            bits(v, w).map((b, i) => `<i class="ih-b${st.k && b !== old[i] ? " is-flip" : ""}">${b}</i>`).join("") +
            `</span><span class="ih-rval">${v}</span></span>`;
        }).join("");
        const ff = VERSIONS[st.v].ff;
        $(".ih-sum").innerHTML = `ה-IBAN הוא ${ltr(digits.length)} ספרות, ${ltr(HEAD)} מהן בראש. בגרסה הזו ${ltr(ff)} פליפ-פלופים ו-${ltr(T)} שעונים.`;
        // the clock of the moment
        let note, label = "המצב של הרגע ועשר הקשתות שלו";
        if (!cur) {
          note = `לפני השעון הראשון${NB}: ${st.v === "final" ? `${ltr("r = 97")}, ספרה 0 של הראש, ו-${ltr("h = 0")}` : "כל הפליפ-פלופים ב-0"}. ‏"השעון הבא" מכניס ספרה.`;
          $(".ih-fan").innerHTML = fan(null, -1, null, label);
        } else if (cur.what === "keep") {
          note = `שעון ${ltr(st.k)}${NB}: ספרת ראש ${ltr(cur.d)} נשמרת ב-${ltr(`b${st.k - 1}`)}, ארבעה פליפ-פלופים. השארית לא זזה.`;
          $(".ih-fan").innerHTML = fan(null, -1, null, label);
        } else {
          const reg = cur.what === "h" ? "h" : "r", to = cur.what === "h" ? regs.h : regs.r;
          const calc = ltr(`(10·${cur.from} + ${cur.d}) mod 97 = ${to}`);
          note = `שעון ${ltr(st.k)}${NB}: ` + (cur.what === "h" ? `ספרת ראש ${ltr(cur.d)} נכנסת ל-${ltr("h")}${NB}: ${calc}, ו-${ltr(`r = ${regs.r}`)}${regs.r ? ` (ספרה ${ltr(regs.r - 97)} של הראש)` : ", הראש נגמר"}`
            : cur.what === "replay" ? `ספרת ראש ${ltr(cur.d)} מוכנסת שוב מהמאגר אל ${ltr("r")}${NB}: ${calc}`
              : cur.what === "tail" ? `הזנב, ${ltr(`n = ${regs.n}`)}${NB}: הספרה 0 נכנסת ל-${ltr("r")}, כלומר כפול 10${NB}: ${calc}`
                : `הספרה ${ltr(cur.d)} נכנסת ל-${ltr(reg)}${NB}: ${calc}`) + ".";
          $(".ih-fan").innerHTML = fan(cur.from, cur.d, to, `${label}${NB}: ${cur.from}, ובספרה ${cur.d} אל ${to}`);
        }
        if (st.k === T && T) {
          const okv = tr[T - 1].ok;
          const end = st.v === "buffer" ? `${ltr(`r = ${regs.r}`)}` : regs.r < 97 ? ltr(`r + h = ${regs.r} + ${regs.h} = ${regs.r + regs.h}`) : "ה-IBAN קצר מהראש";
          note += ` בסוף${NB}: ${end}.`;
          answer(box, okv ? `תקין${NB}: ${end}.` : `לא תקין${NB}: ${end}${st.v === "buffer" ? ", ולא 1" : ", לא 1 ולא 98"}.`, ".ih-regs .ih-reg");
        } else answer(box, null);
        $(".ih-note").innerHTML = note;
      };

      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= trace().length, restart: () => { st.k = 0; draw(); } });
      $(".ih-in").addEventListener("change", () => {
        const s = ihParse($(".ih-in").value);
        $(".ih-err").textContent = s ? "" : `IBAN${NB}: שתי אותיות, שתי ספרות, ואחריהן אותיות וספרות, עד 34 תווים`;
        if (s) { stop(); st.s = s; st.k = 0; draw(); }
      });
      $(".ih-in").addEventListener("keydown", (e) => { if (e.key === "Enter") $(".ih-in").blur(); });
      $(".ih-ver").addEventListener("change", () => { stop(); st.v = $(".ih-ver").value; st.k = 0; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = trace().length; draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); Object.assign(st, { s: s0, v: v0, k: 0 }); $(".ih-err").textContent = ""; draw(); });
      // the link and the remembered state: "IL62..._final_7"
      box.dvqExtra = {
        get: () => `${st.s}_${st.v}_${st.k}`,
        set: (text) => {
          const m = /^([A-Z0-9]{5,34})_(final|buffer)_(\d+)$/.exec(text);
          if (!m || !ihParse(m[1])) return false;
          stop();
          Object.assign(st, { s: m[1], v: m[2], k: Number(m[3]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { ibanhw: ibanhwView },
    help: {
      ibanhw: "ה-IBAN נכנס לבודק ספרה אחת בכל שעון, כל אות כשתי ספרות, ו-6 הספרות הראשונות הן הראש. \"השעון הבא\" מכניס ספרה : הפליפ-פלופים מוצגים ביט אחרי ביט, ומסומנים אלה שהשתנו. הציור מראה את המצב שזז ואת עשר הקשתות שלו. \"הגרסה\" מחליפה בין הבודק של העמוד, 17 פליפ-פלופים עם זנב של שש ספרות 0, לבין הדרך הישירה ששומרת את הראש, 34.".replace(/ :/g, " :"),
    },
    models: { ihParse, ihStream, ihStep, ihTrace },
  });
})();
