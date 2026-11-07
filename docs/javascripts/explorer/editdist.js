// kinds: editdist
//   editdist               0037        the edit distance between an expected stream and an actual one, a packet a letter (data-a, data-b, A to Z, 1 to 12; data-prefer "gaps" or "changed", the rule at a tie; data-swap "1": two neighbouring packets that swapped count as one edit): the table of the prefixes, filled a cell at a time by the stepping buttons (the cell of the moment and its neighbours, the minimum they give and who gave it), and once full the path back from the corner shaded by what each step means, with the scoreboard's report under the table; the examples of the page, the rule at a tie and the swap as selects
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MAXLEN = 12;
  const EXAMPLES = [
    ["ABCDEFGH", "ABDEYGHH", "סעיף א"],
    ["ABCDEF", "ABDXEF", "השוויון של סעיף ב"],
    ["ABCDEFGHIJKL", "ABCEFGHIXJKL", "הרצועה של סעיף ג"],
    ["ABCDEFGH", "ABDCEFHG", "ההחלפות של סעיף ד"],
    ["ABCD", "BCDA", "חבילה שזזה רחוק"],
  ];

  // --- the models, as tools/figures/q0037.py table(), walk() and report() -----------------------

  // "abc d" -> "ABCD": letters A to Z, 1 to 12 of them; null otherwise
  const edParse = (text) => {
    const s = String(text).replace(/\s+/g, "").toUpperCase();
    return /^[A-Z]{1,12}$/.test(s) ? s : null;
  };
  const fits = (a, b, i, j) => i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1] && a[i - 1] !== b[j - 1];
  // d[i][j]: the fewest edits from the first i packets of a to the first j of b
  const edTable = (a, b, swap = false) => {
    const d = Array.from({ length: a.length + 1 }, (_, i) => Array.from({ length: b.length + 1 }, (_, j) => (i === 0 || j === 0 ? i + j : 0)));
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] !== b[j - 1] ? 1 : 0));
        if (swap && fits(a, b, i, j)) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
      }
    }
    return d;
  };
  const MOVE = { missing: [1, 0], extra: [0, 1], changed: [1, 1], swapped: [2, 2] };
  // the path back from the corner, from (0, 0): [kind, i, j] for every step ending at (i, j)
  const edWalk = (a, b, prefer = "gaps", swap = false) => {
    const d = edTable(a, b, swap), out = [];
    const order = prefer === "gaps" ? ["missing", "extra", "changed"] : ["changed", "missing", "extra"];
    let i = a.length, j = b.length;
    while (i || j) {
      if (i && j && a[i - 1] === b[j - 1] && d[i][j] === d[i - 1][j - 1]) { out.push(["same", i, j]); i--; j--; continue; }
      const kind = [...(swap ? ["swapped"] : []), ...order].find((k) => {
        const [di, dj] = MOVE[k];
        if (i < di || j < dj || (k === "swapped" && !fits(a, b, i, j))) return false;
        return d[i][j] === d[i - di][j - dj] + 1;
      });
      out.push([kind, i, j]);
      i -= MOVE[kind][0]; j -= MOVE[kind][1];
    }
    return out.reverse();
  };
  // the report in stream order: [kind, the expected packets, the actual ones]
  const edReport = (a, b, prefer = "gaps", swap = false) => edWalk(a, b, prefer, swap).filter(([k]) => k !== "same").map(([k, i, j]) => (
    k === "missing" ? [k, a[i - 1], null] : k === "extra" ? [k, null, b[j - 1]] : k === "changed" ? [k, a[i - 1], b[j - 1]] : [k, a.slice(i - 2, i), b.slice(j - 2, j)]));

  const NAME = { missing: "חסרה", extra: "מיותרת", changed: "שובשה", swapped: "התחלפו" };
  const line = ([k, i, j], a, b) =>
    k === "missing" ? `<b>חסרה</b> ${ltr(a[i - 1])}, מקום ${ltr(i)} בצפוי`
      : k === "extra" ? `<b>מיותרת</b> ${ltr(b[j - 1])}, מקום ${ltr(j)} בפועל`
        : k === "changed" ? `<b>שובשה</b> ${ltr(a[i - 1])} ל-${ltr(b[j - 1])}, מקום ${ltr(i)} בצפוי ו-${ltr(j)} בפועל`
          : `<b>התחלפו</b> ${ltr(a.slice(i - 2, i))} ל-${ltr(b.slice(j - 2, j))}, מקומות ${ltr(`${i - 1}–${i}`)} בצפוי`;

  // --- the box ---------------------------------------------------------------------------------

  const editdistView = () => ({
    mount(box) {
      const a0 = edParse(box.dataset.a || "") || "ABCDEFGH", b0 = edParse(box.dataset.b || "") || "ABDEYGHH";
      const prefer0 = box.dataset.prefer === "changed" ? "changed" : "gaps", swap0 = box.dataset.swap === "1";
      const st = { a: a0, b: b0, prefer: prefer0, swap: swap0, k: a0.length * b0.length };
      const field = (cls, label, aria) =>
        `<label><span>${label}</span><input type="text" class="ex-num ed-in ${cls}" data-nolink dir="ltr" maxlength="${MAXLEN + 6}" autocapitalize="characters" spellcheck="false" aria-label="${aria}"></label>`;
      box.innerHTML =
        `<div class="ex-controls">` +
        field("ed-a", "הצפוי", `הזרם הצפוי, אותיות A עד Z, עד ${MAXLEN}`) +
        field("ed-b", "בפועל", `הזרם בפועל, אותיות A עד Z, עד ${MAXLEN}`) +
        `<label>דוגמה <select class="ed-ex" data-nolink aria-label="דוגמה מהעמוד"><option value="">לבחירה</option>` +
        EXAMPLES.map(([x, y, t], n) => `<option value="${n}">${t}</option>`).join("") + `</select></label>` +
        `<span class="fl-err ed-err" aria-live="polite"></span></div>` +
        `<div class="ex-controls">` +
        `<label>בשוויון <select class="ed-prefer" data-nolink aria-label="הכלל כששני שכנים נותנים את המינימום"><option value="gaps">קודם חסרה ומיותרת</option><option value="changed">קודם שיבוש</option></select></label>` +
        `<label>הפעולות <select class="ed-ops" data-nolink aria-label="הפעולות המותרות"><option value="3">חסרה, מיותרת, שובשה</option><option value="4">גם החלפה של שכנות</option></select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לזרמים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">התא הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">התא הבא</button>` +
        `<button type="button" class="md-button ex-end">כל הטבלה</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(900, 450, 150) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary ed-sum" aria-live="polite"></p>` +
        `<div class="ed-wrap" dir="ltr" tabindex="0" role="region" aria-label="טבלת המרחקים בין הקידומות"><table class="ed-table"></table></div>` +
        `<span class="viz-legend"><span><i class="ed-key-now"></i>התא שמולא עכשיו</span><span><i class="ed-key-from"></i>השכן שנותן את המינימום</span>` +
        `<span><i class="ed-key-same"></i>אותה חבילה</span><span><i class="ed-key-miss"></i>חסרה</span><span><i class="ed-key-extra"></i>מיותרת</span>` +
        `<span><i class="ed-key-chg"></i>שובשה</span><span><i class="ed-key-swap"></i>התחלפו</span></span>` +
        `<p class="ed-note" aria-live="polite"></p><ol class="ed-report"></ol>`;
      answer(box, NB); answer(box, null);                 // the answer line keeps its place
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const total = () => st.a.length * st.b.length;

      const draw = () => {
        const { a, b, prefer, swap } = st, m = a.length, n = b.length, T = m * n;
        st.k = Math.max(0, Math.min(st.k, T));
        const d = edTable(a, b, swap), full = st.k === T;
        $(".ed-a").value = a; $(".ed-b").value = b;
        $(".ed-prefer").value = prefer; $(".ed-ops").value = swap ? "4" : "3";
        $(".ex-pos").textContent = `תא ${st.k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = full;
        // the cell of the moment (the last one filled, row by row) and the neighbours it read
        const now = st.k ? [Math.floor((st.k - 1) / n) + 1, ((st.k - 1) % n) + 1] : null;
        const filled = (i, j) => i === 0 || j === 0 || (i - 1) * n + j <= st.k;
        const opts = [];
        if (now) {
          const [i, j] = now, c = a[i - 1] !== b[j - 1] ? 1 : 0;
          opts.push(["up", i - 1, j, d[i - 1][j] + 1], ["left", i, j - 1, d[i][j - 1] + 1], ["diag", i - 1, j - 1, d[i - 1][j - 1] + c]);
          if (swap && fits(a, b, i, j)) opts.push(["swap", i - 2, j - 2, d[i - 2][j - 2] + 1]);
        }
        const best = now ? d[now[0]][now[1]] : null;
        const from = new Set(opts.filter((o) => o[3] === best).map((o) => `${o[1]},${o[2]}`));
        const nb = new Set(opts.map((o) => `${o[1]},${o[2]}`));
        const path = full ? edWalk(a, b, prefer, swap) : [];
        const kindAt = new Map(path.map(([k, i, j]) => [`${i},${j}`, k]));
        if (full) kindAt.set("0,0", "same");
        const CLS = { same: "ed-same", missing: "ed-miss", extra: "ed-extra", changed: "ed-chg", swapped: "ed-swap" };
        let t = `<thead><tr><th scope="col" class="ed-corner"><span class="ed-sr">הצפוי בשורות, בפועל בעמודות</span></th><th scope="col" class="ed-h0">·</th>` +
          [...b].map((x, j) => `<th scope="col"><span class="ed-pk">${x}</span><small>${j + 1}</small></th>`).join("") + `</tr></thead><tbody>`;
        for (let i = 0; i <= m; i++) {
          t += `<tr><th scope="row">${i ? `<span class="ed-pk">${a[i - 1]}</span><small>${i}</small>` : `<span class="ed-h0">·</span>`}</th>`;
          for (let j = 0; j <= n; j++) {
            const key = `${i},${j}`;
            let cls = "";
            if (kindAt.has(key)) cls += ` ${CLS[kindAt.get(key)]}`;
            if (now && now[0] === i && now[1] === j) cls += " is-now";
            else if (!full && from.has(key)) cls += " is-from";       // once full, the path alone
            else if (!full && nb.has(key)) cls += " is-nb";
            t += `<td${cls ? ` class="${cls.trim()}"` : ""}>${filled(i, j) ? d[i][j] : ""}</td>`;
          }
          t += `</tr>`;
        }
        $(".ed-table").innerHTML = t + `</tbody>`;
        $(".ed-sum").innerHTML = `הצפוי ${ltr(a)} מול בפועל ${ltr(b)}${NB}: טבלה של ${ltr(`${m + 1} × ${n + 1}`)}. ` +
          (swap ? "ארבע פעולות, גם החלפה של שכנות." : "שלוש פעולות.") + ` בשוויון${NB}: ${prefer === "gaps" ? "קודם חסרה ומיותרת" : "קודם שיבוש"}.`;
        // the note: the cell of the moment, or the path once the table is full
        let note;
        if (!now) note = `השורה והעמודה של 0 מוכנות${NB}: ${ltr("d[0][j] = j")} חבילות מיותרות, ${ltr("d[i][0] = i")} חבילות חסרות. "התא הבא" ממלא את התאים שורה אחרי שורה.`;
        else {
          const [i, j] = now, c = a[i - 1] !== b[j - 1] ? 1 : 0;
          const word = { up: "מלמעלה", left: "משמאל", diag: "באלכסון", swap: "מהחלפה" };
          const terms = opts.map(([w, r, q, v]) => `${word[w]} ${ltr(`${d[r][q]} + ${w === "diag" ? c : 1} = ${v}`)}`);
          const wins = opts.filter((o) => o[3] === best).map(([w]) => word[w]);
          note = `תא ${ltr(`(${i}, ${j})`)}, ${ltr(a[i - 1])} מול ${ltr(b[j - 1])}${c ? "" : ", אותה חבילה"}${NB}: ${terms.join(", ")}. ` +
            `המינימום <b>${ltr(best)}</b>, ${wins.length > 1 ? `שוויון${NB}: ${wins.join(" וגם ")}` : `מגיע ${wins[0]}`}.`;
          if (full) note += ` הטבלה מלאה${NB}: המסלול הצבוע חוזר מהפינה, ובכל תא לשכן שנתן את המינימום לפי הכלל לשוויון.`;
        }
        $(".ed-note").innerHTML = note;
        const diffs = path.filter(([k]) => k !== "same");
        $(".ed-report").innerHTML = full
          ? (diffs.length ? diffs.map((s) => `<li>${line(s, a, b)}</li>`).join("") : `<li>אין הבדלים${NB}: הזרמים זהים.</li>`)
          : `<li class="ed-wait">הדוח יופיע כשהטבלה תתמלא.</li>`;
        if (full) {
          const count = (k) => diffs.filter(([x]) => x === k).length;
          const parts = ["missing", "extra", "changed", "swapped"].filter((k) => count(k)).map((k) => `${NAME[k]} ${ltr(count(k))}`);
          answer(box, `מרחק <b>${ltr(d[m][n])}</b>${parts.length ? `${NB}: ${parts.join(", ")}` : ", הזרמים זהים"}.`, ".ed-table td.is-now, .ed-table tbody tr:last-child td:last-child");
        } else answer(box, null);
      };

      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= total(), restart: () => { st.k = 0; draw(); } });
      const set = (a, b) => { stop(); st.a = a; st.b = b; st.k = a.length * b.length; $(".ed-err").textContent = ""; draw(); };
      ["a", "b"].forEach((w) => {
        const el = $(`.ed-${w}`);
        el.addEventListener("change", () => {
          const v = edParse(el.value);
          if (!v) { $(".ed-err").textContent = `הזרם${NB}: 1 עד ${MAXLEN} אותיות, A עד Z`; return; }
          $(".ed-ex").value = "";
          set(w === "a" ? v : st.a, w === "b" ? v : st.b);
        });
        el.addEventListener("keydown", (e) => { if (e.key === "Enter") el.blur(); });
      });
      $(".ed-ex").addEventListener("change", () => {
        const e = EXAMPLES[Number($(".ed-ex").value)];
        if (!$(".ed-ex").value || !e) return;
        if (e[0] === "ABCDEFGH" && e[1] === "ABDCEFHG") st.swap = true;
        set(e[0], e[1]);
      });
      $(".ed-prefer").addEventListener("change", () => { st.prefer = $(".ed-prefer").value === "changed" ? "changed" : "gaps"; draw(); });
      $(".ed-ops").addEventListener("change", () => { st.swap = $(".ed-ops").value === "4"; draw(); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = total(); draw(); });
      $(".ex-reset").addEventListener("click", () => {
        stop(); $(".ed-ex").value = "";
        Object.assign(st, { a: a0, b: b0, prefer: prefer0, swap: swap0, k: a0.length * b0.length });
        $(".ed-err").textContent = ""; draw();
      });
      // the link and the remembered state: "ABCDEF_ABDXEF_gaps_0_36" (streams, rule, swap, cells)
      box.dvqExtra = {
        get: () => `${st.a}_${st.b}_${st.prefer}_${st.swap ? 1 : 0}_${st.k}`,
        set: (text) => {
          const m = /^([A-Z]{1,12})_([A-Z]{1,12})_(gaps|changed)_([01])_(\d+)$/.exec(text);
          if (!m || Number(m[5]) > m[1].length * m[2].length) return false;
          stop();
          Object.assign(st, { a: m[1], b: m[2], prefer: m[3], swap: m[4] === "1", k: Number(m[5]) });
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { editdist: editdistView },
    help: {
      editdist: "כותבים שני זרמים של חבילות, אות לכל חבילה : הצפוי והזרם בפועל. בטבלה, הצפוי בשורות ובפועל בעמודות, ובכל תא המרחק בין שתי הקידומות. \"התא הבא\" ממלא תא אחרי תא ומראה מאילו שכנים הוא בא, ו\"ההתחלה\" מרוקן את הטבלה. כשהטבלה מלאה, המסלול מהפינה צבוע לפי מה שכל צעד אומר, ומתחת לה הדוח. \"בשוויון\" בוחר את הכלל כששני שכנים נותנים את המינימום, ו\"הפעולות\" מוסיף החלפה של שתי חבילות צמודות.".replace(/ :/g, " :"),
    },
    models: { edParse, edTable, edWalk, edReport },
  });
})();
