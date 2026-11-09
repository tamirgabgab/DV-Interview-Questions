// kinds: stairs
//   stairs                 0100        the ways to climb from stair 0 to stair n with jumps from a set S (data-n, data-steps "1.2", data-broken "5.7", data-pick, data-traps "b56.s13": buttons that load the trap cases of swTraps): the stairs in flights of ten rising to the right, every stair with its number of ways (the order matters), a broken stair crossed and 0; the jump sizes 1 to 6 toggled, n from 1 to 30, a stair picked by a tap shows the stairs that jump to it and the sum that makes it, and the button under the stairs breaks or mends the picked stair; the summary gives w(n), and without broken stairs also the count when the order does not matter
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = " ";
  const NMAX = 30, KMAX = 6, FLIGHT = 10;

  // --- the models, as tools/figures/q0100.py table() -----------------------------------------

  // w[i]: the climbs from stair 0 to stair i, the order of the jumps counted (BigInt)
  const swTable = (n, steps, broken = []) => {
    const bad = new Set(broken), w = [1n];
    for (let i = 1; i <= n; i++) w.push(bad.has(i) ? 0n : steps.reduce((a, s) => (s <= i ? a + w[i - s] : a), 0n));
    return w;
  };
  // the order does not matter: the loops swapped
  const swMultisets = (n, steps) => {
    const w = [1n, ...Array(n).fill(0n)];
    [...new Set(steps)].sort((a, b) => a - b).forEach((s) => { for (let i = s; i <= n; i++) w[i] += w[i - s]; });
    return w[n];
  };
  // "1.2" -> [1, 2]: sizes 1 to 6, no repeats, at least one; null otherwise
  const swSteps = (text) => {
    const v = String(text).split(".").filter(Boolean);
    if (!v.length || v.some((x) => !/^[1-6]$/.test(x))) return null;
    const out = [...new Set(v.map(Number))].sort((a, b) => a - b);
    return out.length === v.length ? out : null;
  };
  const swShort = (v) => {
    const s = v.toString();
    return s.length <= 5 ? s : `${s[0]}.${s[1]}e${s.length - 1}`;
  };
  const group = (v) => v.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  // the trap cases a box may offer (data-traps): S = {2, 3}, where stair 1 has no way; the
  // two adjacent broken stairs that block {1, 2}; the same two that {1, 3} jumps over
  const swTraps = {
    s23: { label: `<span dir="ltr">S = {2, 3}</span>`, steps: [2, 3], n: 10, broken: [], pick: 1 },
    b56: { label: "שבורות 5 ו-6", steps: [1, 2], n: 10, broken: [5, 6], pick: 7 },
    s13: { label: `<span dir="ltr">{1, 3}</span>, שבורות 5 ו-6`, steps: [1, 3], n: 10, broken: [5, 6], pick: 7 },
  };

  // --- the box ---------------------------------------------------------------------------------

  const stairsView = () => ({
    mount(box) {
      const n0 = Math.min(NMAX, Math.max(1, Math.floor(Number(box.dataset.n)) || 10));
      const steps0 = swSteps(box.dataset.steps || "") || [1, 2];
      const broken0 = (box.dataset.broken || "").split(".").map(Number).filter((b) => Number.isInteger(b) && b >= 1 && b <= n0);
      const pick0 = Math.min(n0, Math.max(0, Math.floor(Number(box.dataset.pick)) || n0));
      const st = { n: n0, steps: steps0.slice(), broken: new Set(broken0), pick: pick0 };
      const traps = (box.dataset.traps || "").split(".").filter((k) => swTraps[k]);
      box.innerHTML =
        `<div class="ex-controls"><div class="sw-jumps" role="group" aria-label="גדלי הקפיצה"><span class="sw-lab">קפיצות</span>` +
        Array.from({ length: KMAX }, (_, k) => `<button type="button" class="md-button sw-tog" data-s="${k + 1}" aria-label="קפיצה של ${k + 1}">${k + 1}</button>`).join("") +
        `</div><label>מדרגות <input type="number" class="ex-num sw-n" data-nolink min="1" max="${NMAX}" step="1" dir="ltr" inputmode="numeric" aria-label="מספר המדרגות, 1 עד ${NMAX}"></label></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button sw-break"></button>` +
        `<button type="button" class="md-button sw-mend">תיקון כל המדרגות</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לערך של העמוד</button>` +
        traps.map((k) => `<button type="button" class="md-button ex-preset sw-trap" data-trap="${k}">מקרה מלכודת${NB}: ${swTraps[k].label}</button>`).join("") +
        `</div>` +
        `<p class="ex-summary sw-sum" aria-live="polite"></p>` +
        `<div class="sw-flights" dir="ltr" role="group" aria-label="המדרגות${NB}: לחיצה על מדרגה בוחרת אותה"></div>` +
        `<span class="viz-legend"><span><i class="sw-key"></i>מדרגה ומספר הדרכים אליה</span><span><i class="sw-key-focus"></i>המדרגה שנבחרה</span>` +
        `<span><i class="sw-key-from"></i>קופצים ממנה למדרגה שנבחרה</span><span><i class="sw-key-broken"></i>מדרגה שבורה</span></span>` +
        `<p class="sw-note" aria-live="polite"></p>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const fl = $(".sw-flights");

      const draw = () => {
        const { n, steps } = st;
        const broken = [...st.broken].filter((b) => b <= n).sort((a, b) => a - b);
        const w = swTable(n, steps, broken);
        st.pick = Math.min(st.pick, n);
        box.querySelectorAll(".sw-tog").forEach((b) => b.setAttribute("aria-pressed", String(steps.includes(Number(b.dataset.s)))));
        $(".sw-n").value = String(n);
        const p = st.pick;
        $(".sw-break").textContent = p === 0 ? "את הקרקע אי אפשר לשבור" : st.broken.has(p) ? `תיקון מדרגה ${p}` : `שבירת מדרגה ${p}`;
        $(".sw-break").disabled = p === 0;
        $(".sw-mend").disabled = !broken.length;
        const from = new Set(st.broken.has(p) ? [] : steps.map((s) => p - s).filter((j) => j >= 0));
        const had = box.contains(document.activeElement) && document.activeElement.classList.contains("sw-st");
        let html = "";
        for (let f = 0; f * FLIGHT <= n; f++) {
          html += `<div class="sw-flight">`;
          for (let i = f * FLIGHT; i <= Math.min(n, f * FLIGHT + FLIGHT - 1); i++) {
            const isB = st.broken.has(i);
            let cls = "sw-st" + (isB ? " sw-broken" : "") + (i === p ? " sw-focus" : "") + (from.has(i) ? " sw-from" : "") + (i === n ? " sw-top" : "");
            const shown = isB ? "" : swShort(w[i]);
            if (shown.length >= 5) cls += " sw-long";
            const what = i === 0 ? "הקרקע" : `מדרגה ${i}`;
            const full = group(w[i]), extra = shown && shown !== full ? ` (${shown})` : "";
            html += `<div class="sw-cell" style="--j:${i % FLIGHT}">` +
              `<button type="button" class="${cls}" data-i="${i}" aria-pressed="${i === p}" ` +
              `aria-label="${what}${NB}: ${isB ? "שבורה" : `${full} דרכים${extra}`}"${isB ? "" : ` title="${full}"`}>${shown}</button>` +
              `<span class="sw-i" aria-hidden="true">${i}</span></div>`;
          }
          html += `</div>`;
        }
        fl.innerHTML = html;
        if (had) { const el = fl.querySelector(`[data-i="${p}"]`); if (el) el.focus({ preventScroll: true }); }
        // the sum of the picked stair
        const S = `{${steps.join(", ")}}`;
        let note;
        if (p === 0) note = `הקרקע${NB}: ${ltr("w(0) = 1")}, הדרך הריקה. ממנה קופצים ${steps.length === 1 ? "למדרגה" : "למדרגות"} ${steps.filter((s) => s <= n).join(", ") || "שמעל"}.`;
        else if (st.broken.has(p)) note = `מדרגה ${p} שבורה${NB}: ${ltr(`w(${p}) = 0`)}, ואף מדרגה לא מקבלת ממנה.`;
        else {
          const terms = steps.filter((s) => s <= p);
          note = terms.length
            ? `מדרגה ${p}, הסכום של המדרגות שקופצים מהן${terms.some((s) => st.broken.has(p - s)) ? ". מדרגה שבורה מוסיפה 0" : ""}${NB}:` +
              `<span class="sw-eq" dir="ltr">w(${p}) = ${terms.map((s) => `w(${p - s})`).join(" + ")}<br>= ${terms.map((s) => group(w[p - s])).join(" + ")} = ${group(w[p])}</span>`
            : `מדרגה ${p}${NB}: אין קפיצה קטנה מספיק, ${ltr(`w(${p}) = 0`)}.`;
        }
        $(".sw-note").innerHTML = note;
        let sum = `קפיצות ${ltr(S)} ו-${n} מדרגות${NB}: <strong>${ltr(group(w[n]))}</strong> דרכים, כשהסדר חשוב.`;
        if (broken.length) sum += ` בלי המדרגות השבורות${NB}: ${ltr(group(swTable(n, steps)[n]))}.`;
        else sum += ` כשהסדר לא חשוב${NB}: ${ltr(group(swMultisets(n, steps)))}.`;
        $(".sw-sum").innerHTML = sum;
        answer(box, w[n] > 0n ? `${ltr(group(w[n]))} דרכים להגיע למדרגה ${n}.` : `אין אף דרך להגיע למדרגה ${n}${NB}: ${ltr(0)}.`, ".sw-flights .sw-top");
      };

      box.querySelectorAll(".sw-tog").forEach((b) => b.addEventListener("click", () => {
        const s = Number(b.dataset.s);
        if (st.steps.includes(s)) { if (st.steps.length > 1) st.steps = st.steps.filter((x) => x !== s); }
        else st.steps = [...st.steps, s].sort((a, c) => a - c);
        draw();
      }));
      $(".sw-n").addEventListener("change", () => {
        const v = Math.round(Number($(".sw-n").value));
        if (Number.isFinite(v)) st.n = Math.min(NMAX, Math.max(1, v));
        draw();
      });
      $(".sw-break").addEventListener("click", () => {
        if (st.pick === 0) return;
        if (st.broken.has(st.pick)) st.broken.delete(st.pick); else st.broken.add(st.pick);
        draw();
      });
      $(".sw-mend").addEventListener("click", () => { st.broken.clear(); draw(); });
      box.querySelectorAll(".sw-trap").forEach((b) => b.addEventListener("click", () => {
        const t = swTraps[b.dataset.trap];
        Object.assign(st, { n: t.n, steps: t.steps.slice(), broken: new Set(t.broken), pick: t.pick });
        draw();
      }));
      $(".ex-reset").addEventListener("click", () => { st.n = n0; st.steps = steps0.slice(); st.broken = new Set(broken0); st.pick = pick0; draw(); });
      fl.addEventListener("click", (ev) => {
        const b = ev.target.closest(".sw-st");
        if (!b) return;
        st.pick = Number(b.dataset.i);
        draw();
      });
      // the link and the remembered state: "1.2_10_5.7_6" (jumps, stairs, broken, picked)
      box.dvqExtra = {
        get: () => `${st.steps.join(".")}_${st.n}_${[...st.broken].filter((b) => b <= st.n).sort((a, b) => a - b).join(".")}_${st.pick}`,
        set: (text) => {
          const m = /^([1-6.]+)_(\d+)_([\d.]*)_(\d+)$/.exec(text), steps = m && swSteps(m[1]);
          if (!steps) return false;
          const n = Number(m[2]), pick = Number(m[4]);
          const broken = m[3].split(".").filter(Boolean).map(Number);
          if (n < 1 || n > NMAX || pick > n || broken.some((b) => b < 1 || b > n)) return false;
          Object.assign(st, { n, steps, broken: new Set(broken), pick });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { stairs: stairsView },
    help: {
      stairs: "בוחרים גדלי קפיצה, 1 עד 6, ומספר מדרגות. על כל מדרגה מופיע מספר הדרכים להגיע אליה מהקרקע, כשהסדר של הקפיצות חשוב. לחיצה על מדרגה בוחרת אותה : המדרגות שקופצים מהן אליה צבועות, והשורה שמתחת נותנת את הסכום. הכפתור \"שבירת מדרגה\" שובר את המדרגה שנבחרה או מתקן אותה, ומדרגה שבורה מקבלת 0. הכפתורים \"מקרה מלכודת\" טוענים מקרה שבו קל לטעות : קבוצה בלי קפיצה של 1, או מדרגות שבורות צמודות.".replace(/ :/g, " :"),
    },
    models: { swTable, swMultisets, swSteps, swShort, swTraps },
  });
})();
