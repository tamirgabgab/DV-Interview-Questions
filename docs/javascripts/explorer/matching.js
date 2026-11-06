// kinds: matching
//   matching               0093        stable matching (Gale–Shapley): the candidates' and the jobs' preference lists as two tables, the proposals played one at a time (a proposal, a job that takes it, trades up or refuses), who proposes (candidates or jobs), the size (3 to 6), random lists, and the lists edited by clicking two entries of one row to swap them; at the end the matching, its proposals, and how many stable matchings there are
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the script
// tag); under Node tools/explorer_node.js loads every kind file and merges the models for the
// question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";
  const RLM = "\u200f";

  // the example of the page (0-based): candidate i's jobs and job j's candidates, best first
  const EX_C = ["504213", "031245", "102534", "254130", "230451", "025314"].map((r) => [...r].map(Number));
  const EX_J = ["421053", "015342", "052341", "032451", "324501", "523041"].map((r) => [...r].map(Number));

  // --- the models (tests/0093 compares them with tools/figures/q0093.py) -------------------------

  const cName = (i) => String.fromCharCode(65 + i);
  const jName = (j) => String(j + 1);
  const ranksOf = (prefs) => prefs.map((lst) => { const r = []; lst.forEach((y, k) => { r[y] = k; }); return r; });
  // the example cut to the first n candidates and jobs
  const smRestrict = (n) => [EX_C.slice(0, n).map((l) => l.filter((j) => j < n)), EX_J.slice(0, n).map((l) => l.filter((i) => i < n))];
  // the proposal algorithm with a queue of free proposers (as the page's code): the matching
  // (match[i] = proposer i's receiver) and the steps {p, r, kind, freed}, kind "take", "swap" or "no"
  const smGS = (P, Q) => {
    const n = P.length, rq = ranksOf(Q), nxt = Array(n).fill(0), held = Array(n).fill(null), free = [...Array(n).keys()], steps = [];
    while (free.length) {
      const i = free.shift(), j = P[i][nxt[i]++];
      if (held[j] === null) { held[j] = i; steps.push({ p: i, r: j, kind: "take", freed: null }); }
      else if (rq[j][i] < rq[j][held[j]]) { free.push(held[j]); steps.push({ p: i, r: j, kind: "swap", freed: held[j] }); held[j] = i; }
      else { free.push(i); steps.push({ p: i, r: j, kind: "no", freed: null }); }
    }
    const match = Array(n).fill(null);
    held.forEach((i, j) => { match[i] = j; });
    return { match, steps };
  };
  // the blocking pairs [proposer, receiver] of a matching
  const smBlocking = (P, Q, match) => {
    const n = P.length, rp = ranksOf(P), rq = ranksOf(Q), partner = [];
    match.forEach((j, i) => { partner[j] = i; });
    const out = [];
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if (rp[i][j] < rp[i][match[i]] && rq[j][i] < rq[j][partner[j]]) out.push([i, j]);
    return out;
  };
  // every stable matching, by trying all n! matchings in lexicographic order
  const smAll = (P, Q) => {
    const n = P.length, out = [], p = [...Array(n).keys()];
    for (;;) {
      if (!smBlocking(P, Q, p).length) out.push(p.slice());
      let k = n - 2;
      while (k >= 0 && p[k] > p[k + 1]) k--;
      if (k < 0) return out;
      let l = n - 1;
      while (p[l] < p[k]) l--;
      [p[k], p[l]] = [p[l], p[k]];
      for (let a = k + 1, b = n - 1; a < b; a++, b--) [p[a], p[b]] = [p[b], p[a]];
    }
  };
  const flip = (m) => { const out = []; m.forEach((j, i) => { out[j] = i; }); return out; };
  const isPerm = (row, n) => row.length === n && new Set(row).size === n && row.every((v) => v >= 0 && v < n);
  const smEncode = (C, J) => `${C.map((r) => r.join("")).join("-")}_${J.map((r) => r.join("")).join("-")}`;
  const smDecode = (text, n) => {
    const m = /^([0-5-]+)_([0-5-]+)$/.exec(text);
    if (!m) return null;
    const rows = (s) => s.split("-").map((r) => [...r].map(Number));
    const C = rows(m[1]), J = rows(m[2]);
    return C.length === n && J.length === n && C.every((r) => isPerm(r, n)) && J.every((r) => isPerm(r, n)) ? [C, J] : null;
  };

  // --- the box -------------------------------------------------------------------------------------

  const shuffle = (n) => {
    const a = [...Array(n).keys()];
    for (let k = n - 1; k > 0; k--) { const r = Math.floor(Math.random() * (k + 1)); [a[k], a[r]] = [a[r], a[k]]; }
    return a;
  };
  const same = (A, B) => JSON.stringify(A) === JSON.stringify(B);
  const pairText = (m) => m.map((j, i) => `${cName(i)}–${jName(j)}`).join(", ");

  const view = () => ({
    mount(box) {
      const side0 = box.dataset.side === "job" ? "job" : "cand";
      const st = { n: 6, C: EX_C.map((r) => r.slice()), J: EX_J.map((r) => r.slice()), side: side0, k: 0, sel: null };
      let run = null;
      const compute = () => {
        run = st.side === "cand" ? smGS(st.C, st.J) : smGS(st.J, st.C);
        st.k = Math.min(st.k, run.steps.length);
      };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>מי מציע</span><select class="sm-side" aria-label="מי מציע"><option value="cand">המועמדים</option><option value="job">המשרות</option></select></label>` +
        `<label><span>גודל</span><select class="sm-n" aria-label="כמה מועמדים וכמה משרות">${[3, 4, 5, 6].map((n) => `<option value="${n}">${n}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button sm-rand">הגרלה</button>` +
        `<button type="button" class="md-button ex-reset">חזרה לדוגמה של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">התחלה</button>` +
        `<button type="button" class="md-button ex-prev">ההצעה הקודמת</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">ההצעה הבאה</button>` +
        `<button type="button" class="md-button ex-end">סוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1200, 600, 200) +
        `<span class="ex-pos"></span></div>` +
        `<div class="sm-tables"></div>` +
        `<div class="sm-pairs" data-steady></div>` +
        `<span class="viz-legend"><span><i class="sm-key-now"></i>ההצעה של הצעד</span><span><i class="sm-key-hold"></i>מחזיקים זה בזה עכשיו</span>` +
        `<span><i class="sm-key-out"></i>נדחה</span><span><i class="sm-key-sel"></i>נבחר להחלפה</span></span>` +
        `<p class="ex-summary sm-sum" aria-live="polite"></p>` +
        `<p class="sm-note"></p>`;
      const $ = (q) => box.querySelector(q);

      // the state after k proposals: who holds whom, how far each proposer went, who was refused where
      const stateAt = (k) => {
        const n = st.n, held = Array(n).fill(null), went = Array(n).fill(0), out = new Set();
        run.steps.slice(0, k).forEach(({ p, r, kind, freed }) => {
          went[p]++;
          if (kind === "take") held[r] = p;
          else if (kind === "swap") { out.add(`${freed},${r}`); held[r] = p; }
          else out.add(`${p},${r}`);
        });
        return { held, went, out };
      };

      const table = (who, rows) => {
        const isC = who === "c", proposes = (st.side === "cand") === isC;
        const title = isC ? "המועמדים" : "המשרות";
        const role = proposes ? "מציעים" : "מקבלים הצעות";
        const head = `<tr><th></th>${rows.map((_, k) => `<th>${k + 1}</th>`).join("")}</tr>`;
        return `<div class="sm-tab"><p class="sm-cap"><b>${title}</b> <span class="sm-role">${role}</span></p>` +
          `<table class="sm-prefs"><thead>${head}</thead><tbody>${rows.map((r, x) => `<tr><th>${isC ? cName(x) : jName(x)}</th>` +
          r.map((y, pos) => `<td><button type="button" class="sm-chip" data-t="${who}" data-row="${x}" data-pos="${pos}">${isC ? jName(y) : cName(y)}</button></td>`).join("") + "</tr>").join("")}</tbody></table></div>`;
      };

      const draw = () => {
        const n = st.n, T = run.steps.length;
        st.k = Math.min(Math.max(st.k, 0), T);
        const k = st.k, { held, went, out } = stateAt(k), last = k ? run.steps[k - 1] : null;
        const pc = st.side === "cand";
        $(".sm-side").value = st.side;
        $(".sm-n").value = String(n);
        $(".sm-tables").innerHTML = table("c", st.C) + table("j", st.J);
        // marks: in proposer terms (p, r); the candidate table is P when candidates propose
        const holder = held;     // holder[r] = proposer
        box.querySelectorAll(".sm-chip").forEach((b) => {
          const isC = b.dataset.t === "c", x = Number(b.dataset.row), pos = Number(b.dataset.pos);
          const y = (isC ? st.C : st.J)[x][pos];
          const p = pc === isC ? x : y, r = pc === isC ? y : x;          // the proposer and receiver of this entry
          const cls = [];
          if (holder[r] === p) cls.push("sm-hold");
          else if (out.has(`${p},${r}`)) cls.push("sm-out");
          if (last && last.p === p && last.r === r) cls.push("sm-now");
          if (pc === isC && pos >= went[x] && holder[r] !== p) cls.push("sm-todo");
          if (st.sel && st.sel.t === b.dataset.t && st.sel.row === x && st.sel.pos === pos) cls.push("sm-sel");
          b.className = `sm-chip ${cls.join(" ")}`;
          const who = isC ? `מועמד ${cName(x)}` : `משרה ${jName(x)}`, what = isC ? `משרה ${jName(y)}` : `מועמד ${cName(y)}`;
          b.setAttribute("aria-label", `${who}, מקום ${pos + 1}${NB}: ${what}. לחיצה על שני מקומות באותה שורה מחליפה ביניהם`);
          b.setAttribute("aria-pressed", st.sel && st.sel.t === b.dataset.t && st.sel.row === x && st.sel.pos === pos ? "true" : "false");
        });
        const pairs = [];
        for (let r = 0; r < n; r++) if (held[r] !== null) pairs.push(pc ? [held[r], r] : [r, held[r]]);
        pairs.sort((a, b) => a[0] - b[0]);
        $(".sm-pairs").innerHTML = `<span class="sm-plab">הזוגות עכשיו${NB}:</span> ` + (pairs.length
          ? pairs.map(([i, j]) => `<span class="sm-pair">${ltr(`${cName(i)}–${jName(j)}`)}</span>`).join("") : "<span class=\"sm-none\">עוד אין</span>");
        $(".ex-pos").textContent = `הצעה ${k} מתוך ${T}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === T;
        const who = (i) => (pc ? `${cName(i)}` : `משרה ${jName(i)}`), toWhom = (j) => (pc ? `למשרה ${jName(j)}` : `ל-${cName(j)}`);
        let sum;
        if (!last) sum = `ההתחלה${NB}: אף אחד לא מחזיק אף אחד. ${pc ? "כל מועמד יציע למשרה הראשונה ברשימה שלו." : "כל משרה תציע למועמד הראשון ברשימה שלה."}`;
        else if (last.kind === "take") sum = `הצעה ${ltr(k)}${NB}: ${who(last.p)} ${pc ? "מציע" : "מציעה"} ${toWhom(last.r)}, ${pc ? "שעוד פנויה ומחזיקה אותו" : "שעוד פנוי ומחזיק אותה"}.`;
        else if (last.kind === "swap") sum = `הצעה ${ltr(k)}${NB}: ${who(last.p)} ${pc ? "מציע" : "מציעה"} ${toWhom(last.r)}. ${pc ? "היא מעדיפה אותו" : "הוא מעדיף אותה"} על ${who(last.freed)}, ש${pc ? "משתחרר וימשיך ברשימה שלו" : "משתחררת ותמשיך ברשימה שלה"}.`;
        else sum = `הצעה ${ltr(k)}${NB}: ${who(last.p)} ${pc ? "מציע" : "מציעה"} ${toWhom(last.r)}, ${pc ? "שמעדיפה" : "שמעדיף"} את ${who(stateAt(k).held[last.r])} ${pc ? "ודוחה אותו" : "ודוחה אותה"}.`;
        $(".sm-sum").innerHTML = sum;
        let note = "";
        if (k === T) {
          const cm = pc ? run.match : flip(run.match);
          const other = pc ? flip(smGS(st.J, st.C).match) : smGS(st.C, st.J).match;
          const S = smAll(st.C, st.J);
          note = `${RLM}${ltr(T)} הצעות. השידוך יציב, ויש ${S.length === 1 ? "רק שידוך יציב אחד" : `${ltr(S.length)} שידוכים יציבים`} ` +
            `ברשימות האלה. ${pc ? "כל מועמד קיבל" : "כל משרה קיבלה"} את הטוב ביותר שאפשר בשידוך יציב, ${pc ? "וכל משרה את הגרוע ביותר" : "וכל מועמד את הגרוע ביותר"}.` +
            (same(cm, other) ? " כשהצד השני מציע יוצא אותו שידוך." : ` כש${pc ? "המשרות מציעות" : "המועמדים מציעים"} יוצא ${ltr(pairText(other))}.`);
          answer(box, `השידוך היציב כש${pc ? "המועמדים מציעים" : "המשרות מציעות"}${NB}: ${ltr(pairText(cm))}.`, ".sm-pairs");
        } else answer(box, null);
        if (st.sel) note = `נבחר מקום ${ltr(st.sel.pos + 1)} בשורה של ${st.sel.t === "c" ? `מועמד ${cName(st.sel.row)}` : `משרה ${jName(st.sel.row)}`}. לחיצה על מקום אחר באותה שורה תחליף ביניהם. ` + note;
        $(".sm-note").innerHTML = note;
      };

      const stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= run.steps.length, restart: () => { st.k = 0; draw(); } });
      const setPrefs = (C, J) => { st.C = C; st.J = J; st.sel = null; st.k = 0; compute(); };
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = run.steps.length; draw(); });
      $(".sm-side").addEventListener("change", () => { stop(); st.side = $(".sm-side").value === "job" ? "job" : "cand"; st.k = 0; st.sel = null; compute(); draw(); });
      $(".sm-n").addEventListener("change", () => {
        stop();
        const n = Number($(".sm-n").value);
        st.n = [3, 4, 5, 6].includes(n) ? n : 6;
        const [C, J] = smRestrict(st.n);
        setPrefs(C, J); draw();
      });
      $(".sm-rand").addEventListener("click", () => {
        stop();
        const n = st.n;
        setPrefs(Array.from({ length: n }, () => shuffle(n)), Array.from({ length: n }, () => shuffle(n)));
        draw();
      });
      $(".ex-reset").addEventListener("click", () => { stop(); st.n = 6; st.side = side0; const [C, J] = smRestrict(6); setPrefs(C, J); draw(); });
      // editing: a click selects an entry, a click on another entry of the same row swaps them
      $(".sm-tables").addEventListener("click", (e) => {
        const b = e.target.closest(".sm-chip");
        if (!b) return;
        stop();
        const t = b.dataset.t, row = Number(b.dataset.row), pos = Number(b.dataset.pos);
        if (st.sel && st.sel.t === t && st.sel.row === row && st.sel.pos !== pos) {
          const lists = (t === "c" ? st.C : st.J).map((r) => r.slice());
          [lists[row][pos], lists[row][st.sel.pos]] = [lists[row][st.sel.pos], lists[row][pos]];
          if (t === "c") setPrefs(lists, st.J); else setPrefs(st.C, lists);
        } else st.sel = st.sel && st.sel.t === t && st.sel.row === row && st.sel.pos === pos ? null : { t, row, pos };
        draw();
        const again = box.querySelector(`.sm-chip[data-t="${t}"][data-row="${row}"][data-pos="${pos}"]`);
        if (again) again.focus();
      });
      // the lists (when not the example's) and the proposal shown ride in the link
      box.dvqExtra = {
        get: () => {
          const [C0, J0] = smRestrict(st.n), own = !(same(st.C, C0) && same(st.J, J0));
          return own ? `${st.k}.${smEncode(st.C, st.J)}` : st.k ? `${st.k}` : "";
        },
        set: (text) => {
          const m = /^(\d+)(?:\.(.+))?$/.exec(text);
          if (!m) return false;
          if (m[2]) {
            const d = smDecode(m[2], st.n);
            if (!d) return false;
            setPrefs(d[0], d[1]);
          }
          if (Number(m[1]) > run.steps.length) return false;
          st.k = Number(m[1]);
          draw();
          return true;
        },
      };
      compute();
      draw();
    },
  });

  dvqExplorers.register({
    views: { matching: view },
    help: {
      matching: "שתי טבלאות של דירוגים : לכל מועמד המשרות שלו מהטובה לפחות טובה, ולכל משרה המועמדים שלה. בחיצים עוברים הצעה אחרי הצעה : מי שמציע הולך לפי הסדר ברשימה שלו, ומי שמקבל מחזיק את ההצעה הטובה ביותר שקיבל עד עכשיו ודוחה את השאר. \"מי מציע\" מחליף צד. לחיצה על מקום בטבלה ואחר כך על מקום אחר באותה שורה מחליפה ביניהם, ו\"הגרלה\" מגרילה רשימות חדשות.",
    },
    models: { smGS, smBlocking, smAll, smRestrict, smEncode, smDecode },
  });
})();
