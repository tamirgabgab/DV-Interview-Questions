// kinds: iban
//   iban                   0099        the check of an IBAN (data-iban, data-pos): the IBAN as written with its first four characters, moved to the end, every letter as two digits, then the remainder mod 97 digit by digit in rows of ten (step / play), and at the end valid or not (remainder 1); a place (1 to the length) where one character is changed or swapped with its neighbour, with "caught" or "slipped" against the IBAN before the change
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAXLEN = 34;
  // the published registry examples (ISO 13616) and the double error of 0099 part c
  const PRESETS = [["IL620108000000099999999", "ישראל, הדוגמה של העמוד"], ["GB82WEST12345698765432", "בריטניה, עם אותיות"],
    ["DE89370400440532013000", "גרמניה"], ["IL620108000000099999902", "שתי טעויות שעוברות"], ["IL620108000000099999990", "טעות אחת שנתפסת"]];
  const IL = PRESETS[0][0];

  // --- the models ------------------------------------------------------------------------------

  const ibNorm = (text) => String(text).replace(/\s+/g, "").toUpperCase();
  // the IBAN without spaces when it is two letters, two digits and then letters and digits,
  // 5 to 34 characters; null otherwise
  const ibParse = (text) => {
    const s = ibNorm(text);
    return /^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$/.test(s) ? s : null;
  };
  const ibGroup = (s) => s.replace(/(.{4})/g, "$1 ").trim();
  // a digit stays, a letter becomes two digits (A = 10 ... Z = 35)
  const val = (c) => parseInt(c, 36);
  // the digits of the moved IBAN, and for each digit what it came from: "num" a digit of the
  // rest, "let" a digit of a letter, "chk" a check digit (the first four come last)
  const ibDigits = (s) => {
    const m = s.slice(4) + s.slice(0, 4);
    let digits = "";
    const owner = [];
    [...m].forEach((c, k) => {
      const ds = String(val(c));
      digits += ds;
      const kind = /[A-Z]/.test(c) ? "let" : k >= m.length - 2 ? "chk" : "num";
      for (let i = 0; i < ds.length; i++) owner.push(kind);
    });
    return { moved: m, digits, owner };
  };
  // the remainder mod 97 after each digit: r = (10 r + d) mod 97
  const ibRunning = (digits) => {
    let r = 0;
    return [...digits].map((d) => (r = (10 * r + Number(d)) % 97));
  };
  const ibMod = (s) => { const run = ibRunning(ibDigits(s).digits); return run[run.length - 1]; };
  const ibValid = (s) => ibParse(s) !== null && ibMod(ibNorm(s)) === 1;
  // the check digits: 00 in their place, the remainder m, then 98 - m
  const ibCheck = (s) => String(98 - ibMod(s.slice(0, 2) + "00" + s.slice(4))).padStart(2, "0");
  // the character at place p (1-based) changed: a digit to the next digit, a letter to the
  // next letter, around; and swapped with the next one (with the one before at the end)
  const ibChange = (s, p) => {
    const c = s[p - 1];
    const n = /[0-9]/.test(c) ? String((Number(c) + 1) % 10) : String.fromCharCode(65 + ((c.charCodeAt(0) - 64) % 26));
    return s.slice(0, p - 1) + n + s.slice(p);
  };
  const ibSwap = (s, p) => {
    const i = p < s.length ? p - 1 : p - 2;
    return s.slice(0, i) + s[i + 1] + s[i] + s.slice(i + 2);
  };

  // --- drawing ---------------------------------------------------------------------------------

  const key = (cls, text) => `<span><i class="${cls}"></i><span>${text}</span></span>`;
  const chars = (s, cls) => [...s].map((c, i) => `<span class="${cls(i)}">${c}</span>`).join("");

  const ibanView = () => ({
    mount(box) {
      const s0 = ibParse(box.dataset.iban || "") || IL;
      const p0 = Math.min(s0.length, Math.max(1, Math.floor(Number(box.dataset.pos)) || 10));
      const st = { s: s0, k: 0, p: p0, before: null, same: false };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>${ltr("IBAN")}</span><input type="text" class="ex-num ib-in" dir="ltr" spellcheck="false" autocomplete="off" value="${ibGroup(s0)}" aria-label="IBAN, שתי אותיות, שתי ספרות ואחריהן אותיות וספרות"></label>` +
        `<label>דוגמה <select class="ib-pre" data-nolink aria-label="דוגמה מוכנה"><option value="">בחרו</option>${PRESETS.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button><span class="fl-err ib-err" role="status"></span></div>` +
        `<div class="ex-controls">` +
        `<label><span>מקום</span><input type="number" class="ex-num ib-pos" min="1" max="${s0.length}" step="1" value="${p0}" dir="ltr" inputmode="numeric" aria-label="המקום של הטעות, מ-1 עד אורך ה-IBAN"></label>` +
        `<button type="button" class="md-button ib-change">שינוי התו</button>` +
        `<button type="button" class="md-button ib-swap">החלפה עם השכן</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">מההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">ספרה אחורה</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הספרה הבאה</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(700, 350, 120) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ib-sum" aria-live="polite"></p>` +
        `<div class="ib-box" data-steady>` +
        `<div class="ib-lines"></div><div class="ib-wrap"></div></div>` +
        `<span class="viz-legend">${key("ib-key-head", "ארבעת התווים הראשונים")}${key("ib-key-let", "ספרות של אות")}${key("ib-key-chk", "ספרות הביקורת")}${key("ib-key-now", "הספרה של הצעד")}${key("ib-key-pos", "המקום שנבחר")}</span>` +
        `<p class="ib-note"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const input = $(".ib-in"), pos = $(".ib-pos");

      const draw = () => {
        const s = st.s, { moved, digits, owner } = ibDigits(s), run = ibRunning(digits), T = digits.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        st.p = Math.min(Math.max(st.p, 1), s.length);
        const k = st.k, done = k === T;
        $(".ex-pos").textContent = `צעד ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        if (document.activeElement !== input) input.value = ibGroup(s);
        pos.max = String(s.length);
        if (document.activeElement !== pos) pos.value = String(st.p);
        // the three lines: as written (the head and the chosen place marked), moved, digits
        const asWritten = chars(s, (i) => `ib-c${i < 4 ? " ib-head" : ""}${i === st.p - 1 ? " ib-at" : ""}`);
        const mv = chars(moved, (i) => `ib-c${i >= moved.length - 4 ? " ib-head" : ""}`);
        $(".ib-lines").innerHTML =
          `<p class="ib-line"><span class="ib-lab">כפי שנכתב</span><span class="ib-str" dir="ltr">${asWritten}</span></p>` +
          `<p class="ib-line"><span class="ib-lab">אחרי ההעברה</span><span class="ib-str" dir="ltr">${mv}</span></p>`;
        // the digits in rows of ten, the remainder under each digit up to the step
        const rows = [];
        for (let t = 0; t < T; t += 10) {
          let top = "", bot = "";
          for (let i = t; i < t + 10; i++) {
            if (i >= T) { top += `<td class="gs-b ib-pad"></td>`; bot += `<td class="gs-b ib-pad"></td>`; continue; }
            const kind = owner[i] === "let" ? " ib-let" : owner[i] === "chk" ? " ib-chk" : "";
            const now = i === k - 1 ? " ib-now" : "";
            top += `<td class="gs-b ib-d${kind}${now}">${digits[i]}</td>`;
            bot += i < k ? `<td class="gs-b ib-r${now}${done && i === T - 1 ? (run[i] === 1 ? " ib-last" : " ib-last ib-lastbad") : ""}">${run[i]}</td>` : `<td class="gs-b ib-r ib-fut">·</td>`;
          }
          rows.push(`<tr><th>d</th>${top}</tr><tr class="ib-rrow"><th>r</th>${bot}</tr>`);
        }
        const label = `הספרות של ${ibGroup(s)} אחרי ההעברה, ומתחתיהן השארית בחלוקה ל-97 אחרי ${k} ספרות`;
        $(".ib-wrap").innerHTML = `<div class="gs-scroll" tabindex="0" role="region" aria-label="${label}"><table class="gs-bits ib-tab" dir="ltr" aria-label="${label}"><tbody>${rows.join("")}</tbody></table></div>`;
        // the step and the verdict
        let note;
        if (!k) note = `ארבעת התווים הראשונים, ${ltr(s.slice(0, 4))}, עוברים לסוף, וכל אות נכתבת כשתי ספרות. מתחילים מ-${ltr("r = 0")}.`;
        else {
          const prev = k > 1 ? run[k - 2] : 0;
          note = `ספרה ${ltr(k)}${NB}: ${ltr(`r = (10·${prev} + ${digits[k - 1]}) mod 97 = ${run[k - 1]}`)}.`;
        }
        $(".ib-note").innerHTML = note;
        const r = run[T - 1], ok = r === 1;
        let sum = done ? `השארית בסוף${NB}: ${ltr(r)}. ${ok ? "ה-IBAN תקין." : "ה-IBAN לא תקין."}` : `נקראו ${ltr(k)} מתוך ${ltr(T)} הספרות.`;
        if (st.same) sum = `שני התווים שווים, וההחלפה לא שינתה את ה-IBAN. ${sum}`;
        else if (st.before !== null) {
          const was = ibValid(st.before);
          sum = (was ? (ok ? `<strong class="ib-slip">הטעות עברה</strong>${NB}: השארית עדיין 1. ` : `<strong class="ib-caught">הטעות נתפסה</strong>${NB}: השארית ${ltr(r)} במקום 1. `)
            : (ok ? "אחרי השינוי ה-IBAN תקין. " : "ה-IBAN היה לא תקין גם לפני השינוי. ")) + sum;
        }
        if (s.startsWith("IL") && s.length !== 23) sum += ` ל-IBAN ישראלי יש 23 תווים, ולזה יש ${ltr(s.length)}.`;
        $(".ib-sum").innerHTML = sum;
        if (done) answer(box, ok ? `השארית היא ${ltr(1)}${NB}: ה-IBAN תקין.` : `השארית היא ${ltr(r)} ולא ${ltr(1)}${NB}: ה-IBAN לא תקין.`, ".ib-wrap td.ib-last");
        else answer(box, null);
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= ibDigits(st.s).digits.length, restart: () => { st.k = 0; draw(); } });
      // a new IBAN through the field: the link and the remembered state follow the field
      const put = (s, before) => {
        input.value = ibGroup(s);
        input.dispatchEvent(new Event("input", { bubbles: true }));
        input.dispatchEvent(new Event("change", { bubbles: true }));
        st.before = before;
        st.same = false;
        draw();
      };
      input.addEventListener("change", () => {
        const s = ibParse(input.value);
        if (!s) { $(".ib-err").textContent = `ה-IBAN${NB}: שתי אותיות, שתי ספרות, ואחריהן אותיות וספרות, עד ${MAXLEN} תווים`; return; }
        $(".ib-err").textContent = "";
        stop();
        if (s !== st.s) { st.s = s; st.k = 0; st.before = null; st.same = false; }
        draw();
      });
      pos.addEventListener("change", () => {
        const v = Number(pos.value);
        if (!Number.isInteger(v) || v < 1 || v > st.s.length) { $(".ib-err").textContent = `המקום${NB}: מספר שלם מ-1 עד ${st.s.length}`; return; }
        $(".ib-err").textContent = "";
        st.p = v;
        draw();
      });
      // an error at the chosen place: the IBAN goes through the field, then the steps run to
      // the end so the verdict shows at once
      const inject = (fn) => {
        stop();
        const before = st.s, after = fn(before, st.p);
        put(after, before);
        st.same = after === before;
        st.k = ibDigits(st.s).digits.length;
        draw();
      };
      $(".ib-change").addEventListener("click", () => inject(ibChange));
      $(".ib-swap").addEventListener("click", () => inject(ibSwap));
      $(".ib-pre").addEventListener("change", () => {
        const v = $(".ib-pre").value;
        if (v === "") return;
        $(".ib-pre").value = "";
        put(v, null);
      });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = ibDigits(st.s).digits.length; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        $(".ib-err").textContent = "";
        st.p = p0;
        pos.value = String(p0);
        pos.dispatchEvent(new Event("input", { bubbles: true }));
        put(s0, null);
      });
      draw();
    },
  });

  dvqExplorers.register({
    views: { iban: ibanView },
    help: {
      iban: "מקלידים IBAN, או בוחרים דוגמה, ומתקדמים ספרה אחרי ספרה. ארבעת התווים הראשונים עוברים לסוף, כל אות נכתבת כשתי ספרות, ומתחת לכל ספרה מופיעה השארית בחלוקה ל-97 עד אליה. בסוף, שארית 1 היא IBAN תקין. בשורה השנייה בוחרים מקום, ומשנים את התו שם או מחליפים אותו עם השכן : התיבה אומרת אם הטעות נתפסה או עברה.",
    },
    models: { ibNorm, ibParse, ibGroup, ibDigits, ibRunning, ibMod, ibValid, ibCheck, ibChange, ibSwap },
  });
})();
