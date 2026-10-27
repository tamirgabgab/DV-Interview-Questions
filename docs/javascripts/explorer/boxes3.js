// kinds: boxes3 labelfix
//   boxes3                 0004        three mislabelled boxes with hidden contents: draw a ball, the deduction line by line
//   labelfix               0004        part b's fix_labels step by step: k and the ball, same and other, the two swaps on the labels array drawn as a 3-cycle
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, f, ltr, seedControls, speedSel } = dvqExplorers.lib;
  const NB = "\u00a0";

  // Three mislabelled boxes (0004): the twelve cases (a label order and a content where
  // every label is wrong), a draw from a box, and the page's rule applied to one draw.
  const BOX_LABELS = ["RED", "BLACK", "MIXED"];
  const boxesCases = () => {
    const perms = (a) => (a.length <= 1 ? [a] : a.flatMap((x, i) => perms(a.filter((_, j) => j !== i)).map((p) => [x, ...p])));
    const out = [];
    for (const labels of perms(BOX_LABELS)) for (const content of perms(BOX_LABELS))
      if (labels.every((l, i) => l !== content[i])) out.push({ labels, content });
    return out;
  };
  const boxesDraw = (content, i, rnd = Math.random) => (content[i] === "MIXED" ? (rnd() < 0.5 ? "RED" : "BLACK") : content[i]);
  // the page's fix_labels_simple, given the ball drawn from the box labelled MIXED
  const boxesFix = (labels, ball) => {
    const k = labels.indexOf("MIXED"), other = ball === "RED" ? "BLACK" : "RED", fixed = ["", "", ""];
    fixed[k] = ball;
    labels.forEach((l, i) => { if (l === ball) fixed[i] = other; });
    labels.forEach((l, i) => { if (l === other) fixed[i] = "MIXED"; });
    return fixed;
  };
  // what a draw from box i tells: the contents still possible afterwards
  const boxesDeduce = (labels, i, ball) => {
    const possible = boxesCases().filter((c) => c.labels.join() === labels.join()).map((c) => c.content);
    return possible.filter((content) => content[i] === ball || content[i] === "MIXED");
  };

  // The three boxes box (0004): every game hides one of the two possible contents behind
  // the labels; tap a box to draw a ball, the deduction appears line by line, and a draw
  // from a box labelled with a colour shows why one ball is not enough.
  const boxes3View = () => ({
    mount(box) {
      const HE = { RED: "אדום", BLACK: "שחור", MIXED: "אדום ושחור" };
      // assign (V4): after a draw the reader names the three contents and checks them before
      // the deduction is shown; answered once they are right, shown or revealed
      const st = { labels: ["RED", "BLACK", "MIXED"], content: null, draws: [], games: 0, solvedFirst: 0, answered: false, revealed: false };
      const newGame = (keepStats = true, rnd = Math.random) => {
        const cases = boxesCases().filter((c) => c.labels.join() === st.labels.join());
        st.content = cases[Math.floor(rnd() * cases.length)].content;
        st.draws = [];
        st.answered = st.revealed = false;
        box.querySelectorAll(".b3-pick").forEach((sel) => { sel.value = ""; });
        const why = box.querySelector(".b3-why"), msg = box.querySelector(".b3-msg");
        if (why) why.hidden = true;
        if (msg) msg.textContent = "";
        if (!keepStats) { st.games = 0; st.solvedFirst = 0; }
      };
      newGame(false);
      box.innerHTML =
        `<div class="ex-controls"><button type="button" class="md-button md-button--primary ex-new">משחק חדש</button>` +
        `<button type="button" class="md-button ex-shuffle">ערבוב התוויות</button>` +
        `<button type="button" class="md-button ex-reveal">גילוי התוכן</button><span class="b3-stats"></span>` +
        `<label><input type="checkbox" class="b3-self" checked> לשייך בעצמי לפני ההסבר</label></div>` +
        `<div class="b3-crates" role="group" aria-label="שלוש קופסאות, לחיצה דוגמת כדור"></div>` +
        `<div class="ex-controls b3-assign" hidden><span class="ex-title">מה בכל קופסה?</span>` +
        [0, 1, 2].map((i) => `<label>קופסה ${i} <select class="b3-pick" data-i="${i}" data-nolink aria-label="התוכן של קופסה ${i}"><option value="">בחרו</option>` +
          BOX_LABELS.map((c) => `<option value="${c}">${HE[c]}</option>`).join("") + `</select></label>`).join("") +
        `<button type="button" class="md-button md-button--primary b3-check">בדיקת השיוך</button><button type="button" class="md-button b3-why" hidden>הצגת ההסבר</button></div>` +
        `<p class="b3-msg" role="status"></p>` +
        `<p class="b3-step" aria-live="polite"></p><ol class="b3-lines"></ol><p class="ex-summary b3-sum"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const crate = (i, label, balls, open) => {
        const x = 20 + 200 * i, cx = x + 75;
        // the accessible name repeats the visible texts in order (axe: label-content-name-mismatch)
        const visible = [label === "MIXED" ? "אדום ושחור" : HE[label], open ? "" : "?", `קופסה ${i}${open ? ` : ${HE[st.content[i]]}` : ""}`].filter(Boolean).join(" ");
        let s = `<g class="b3-crate" data-i="${i}" tabindex="0" role="button" aria-label="${visible}, דגימת כדור מהקופסה">` +
          `<polygon class="crate-top" points="${x},50 ${x + 30},20 ${x + 180},20 ${x + 150},50"/>` +
          `<polygon class="crate-side" points="${x + 150},50 ${x + 180},20 ${x + 180},120 ${x + 150},150"/>` +
          `<rect class="crate-front" x="${x}" y="50" width="150" height="100"/>`;
        s += `<text class="crate-text" x="${cx}" y="108" font-size="${label === "MIXED" ? 18 : 22}">${label === "MIXED" ? "אדום ושחור" : HE[label]}</text>`;
        s += `<text class="crate-text" x="${cx + 30}" y="42" font-size="20">${open ? "" : "?"}</text>`;
        // revealed, the box shows what is in it: five balls of its colour, or mixed
        if (open) for (let b = 0; b < 5; b++) {
          const c = st.content[i] === "MIXED" ? (b % 2 ? "BLACK" : "RED") : st.content[i];
          s += `<circle class="b3-ball b3-${c.toLowerCase()}" cx="${x + 35 + 20 * b}" cy="132" r="7"/>`;
        }
        balls.forEach((b, k) => { s += `<circle class="b3-ball b3-${b.toLowerCase()}" cx="${x + 18 + 22 * k}" cy="166" r="8"><title>כדור ${HE[b]}</title></circle>`; });
        s += `<text class="tick" x="${cx}" y="192" font-size="13" direction="rtl" text-anchor="middle">קופסה ${i}${open ? ` : ${HE[st.content[i]]}` : ""}</text></g>`;
        return s;
      };
      const draw = (reveal = false) => {
        const balls = [[], [], []];
        st.draws.forEach((d) => balls[d.i].push(d.ball));
        $(".b3-crates").innerHTML = `<svg class="figure b3-live" viewBox="0 0 620 200">` +
          st.labels.map((l, i) => crate(i, l, balls[i], reveal)).join("") + `</svg>`;
        $(".b3-stats").textContent = st.games ? `${st.games} משחקים, ${st.solvedFirst} נפתרו בדגימה הראשונה` : "";
        const lines = [];
        let sum = "";
        const self = $(".b3-self").checked, waiting = self && st.draws.length > 0 && !st.answered && !reveal;
        $(".b3-assign").hidden = !waiting;
        if (!waiting && !st.answered) $(".b3-msg").textContent = "";
        if (!st.draws.length) {
          $(".b3-step").innerHTML = `כל התוויות שגויות. בחרו קופסה ודגמו ממנה כדור.`;
        } else if (waiting) {
          $(".b3-step").innerHTML = `יצא כדור ${HE[st.draws[st.draws.length - 1].ball]}. מה יש בכל קופסה? בחרו ובדקו, או דגמו עוד.`;
        } else {
          const first = st.draws[0];
          const k = st.labels.indexOf("MIXED");
          const left = boxesDeduce(st.labels, first.i, first.ball);
          if (first.i === k) {
            const fixed = boxesFix(st.labels, first.ball);
            const other = first.ball === "RED" ? "BLACK" : "RED";
            lines.push(`הקופסה "אדום ושחור" לא מעורבת (התווית שגויה), ויצא ממנה ${HE[first.ball]} : יש בה רק ${HE[first.ball]}.`);
            lines.push(`הקופסה שתוויתה "${HE[first.ball]}" לא מכילה ${HE[first.ball]} (תווית שגויה) ולא את התערובת (היא בקופסה ${ltr(k)})  : נשאר ${HE[other]}.`);
            lines.push(`הקופסה שתוויתה "${HE[other]}" מקבלת את מה שנשאר : אדום ושחור.`);
            $(".b3-step").innerHTML = `<span class="b3-ok">✓ דגימה אחת הספיקה.</span> התוויות הנכונות : ${fixed.map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}.`;
            sum = `הדגימה מהקופסה "אדום ושחור" מכריעה תמיד, כי שני הסידורים האפשריים נבדלים בה בצבע אחד וברור.`;
          } else {
            const otherOfLabel = st.labels[first.i] === "RED" ? "BLACK" : "RED";
            lines.push(`הקופסה "${HE[st.labels[first.i]]}" לא מכילה ${HE[st.labels[first.i]]}, ולכן היא או ${HE[otherOfLabel]} או אדום ושחור.`);
            lines.push(left.length === 2
              ? `כדור ${HE[first.ball]} מתאים לשתי האפשרויות : שני הסידורים עדיין פתוחים.`
              : `כדור ${HE[first.ball]} לא יכול לצאת מקופסה של ${HE[otherOfLabel]} בלבד : הקופסה מעורבת, ונשאר סידור אחד.`);
            if (left.length === 2) {
              $(".b3-step").innerHTML = `<span class="b3-bad">✗ דגימה מקופסה "${HE[st.labels[first.i]]}" לא מכריעה.</span> ` +
                (st.draws.length > 1 ? `דגימות נוספות : ${st.draws.slice(1).map((d) => `קופסה ${ltr(d.i)} ${HE[d.ball]}`).join(", ")}.` : `דגמו שוב, מאותה קופסה או מאחרת.`);
              const rest = boxesDeduce(st.labels, first.i, first.ball).filter((content) => st.draws.every((d) => content[d.i] === d.ball || content[d.i] === "MIXED"));
              if (rest.length === 1) $(".b3-step").innerHTML += ` <span class="b3-ok">✓ אחרי ${ltr(st.draws.length)} דגימות נשאר סידור אחד : ${rest[0].map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}.</span>`;
              else $(".b3-step").innerHTML += ` עדיין ${ltr(rest.length)} סידורים אפשריים.`;
            } else {
              $(".b3-step").innerHTML = `<span class="b3-ok">✓ הפעם התמזל : כדור ${HE[first.ball]} מקופסה "${HE[st.labels[first.i]]}" פוסל סידור אחד.</span> הסידור שנשאר : ${left[0].map((c, i) => `קופסה ${ltr(i)} = ${HE[c]}`).join(", ")}. אבל זה מזל, לא הבטחה : הצבע השני היה משאיר שני סידורים.`;
            }
            sum = `דגימה מקופסה שתוויתה צבע מבטיחה הכרעה רק אם יוצא הצבע שעל התווית; הצבע השני משאיר ספק. רק הקופסה "אדום ושחור" מבטיחה הכרעה בכדור אחד.`;
          }
        }
        $(".b3-lines").innerHTML = lines.map((l) => `<li>${l}</li>`).join("");
        $(".b3-sum").innerHTML = sum;
      };
      const drawFrom = (i) => {
        const ball = boxesDraw(st.content, i);
        if (!st.draws.length) { st.games++; if (i === st.labels.indexOf("MIXED")) st.solvedFirst++; }
        st.draws.push({ i, ball });
        draw();
      };
      $(".b3-crates").addEventListener("click", (e) => { const g = e.target.closest(".b3-crate"); if (g) drawFrom(Number(g.dataset.i)); });
      $(".b3-crates").addEventListener("keydown", (e) => { const g = e.target.closest(".b3-crate"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); drawFrom(Number(g.dataset.i)); } });
      const seed = seedControls(box, $(".ex-reveal"), (rng) => { newGame(true, rng); draw(); });
      $(".ex-new").addEventListener("click", seed.draw);
      $(".ex-shuffle").addEventListener("click", () => { st.labels = st.labels.slice().sort(() => Math.random() - 0.5); newGame(); draw(); });
      $(".ex-reveal").addEventListener("click", () => { st.revealed = true; draw(true); });
      $(".b3-self").addEventListener("change", () => draw(st.revealed));
      const say = (cls, html) => { const m = $(".b3-msg"); m.className = `b3-msg ${cls}`; m.innerHTML = html; };
      $(".b3-check").addEventListener("click", () => {
        const pick = [...box.querySelectorAll(".b3-pick")].map((sel) => sel.value);
        if (pick.some((v) => !v)) { say("", "בחרו תוכן לכל אחת משלוש הקופסאות."); return; }
        if (pick.join() !== st.content.join()) {
          say("b3-bad", `לא נכון. רמז${NB}: כל תווית שגויה. התחילו מהקופסה שדגמתם, ושאלו מה הכדור שיצא פוסל בה.`);
          $(".b3-why").hidden = false;
          return;
        }
        // right, but did the draws decide it, or was it a lucky guess?
        const rest = boxesCases().filter((c) => c.labels.join() === st.labels.join() &&
          st.draws.every((d) => c.content[d.i] === d.ball || c.content[d.i] === "MIXED"));
        st.answered = true;
        say(rest.length === 1 ? "b3-ok" : "", rest.length === 1 ? "✓ נכון, והדגימות הכריעו. ההסבר למטה."
          : `נכון, אבל בניחוש${NB}: הדגימות השאירו ${ltr(rest.length)} סידורים אפשריים. ההסבר למטה.`);
        draw();
      });
      $(".b3-why").addEventListener("click", () => { st.answered = true; $(".b3-why").hidden = true; say("", ""); draw(); });
      draw();
    },
  });

  // The page's fix_labels (0004 part b, solution 2) given the ball drawn from box k: the
  // two neighbours, same (labelled with the ball's colour) and other, and the labels after
  // each of the two swaps; together they rotate the three labels.
  const labelSwaps = (labels, ball) => {
    const k = labels.indexOf("MIXED"), n1 = (k + 1) % 3, n2 = (k + 2) % 3;
    const same = labels[n1] === ball ? n1 : n2, other = same === n1 ? n2 : n1;
    const after1 = labels.slice();
    [after1[k], after1[same]] = [after1[same], after1[k]];
    const after2 = after1.slice();
    [after2[same], after2[other]] = [after2[other], after2[same]];
    return { k, n1, n2, same, other, after1, after2 };
  };

  // The labels fix box (0004 part b): the labels array on three crates, played step by
  // step: k and the ball drawn from it, same and other, swap 1 (k, same) and swap 2 (same,
  // other), then the true contents; the arcs of the 3-cycle above the crates light as
  // their label arrives. "סידור חדש" draws another of the twelve cases.
  const LF_STEPS = 6;
  const labelfixView = () => ({
    mount(box) {
      const st = { labels: ["RED", "BLACK", "MIXED"], content: ["BLACK", "MIXED", "RED"], k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><button type="button" class="md-button ex-new">סידור חדש</button>` +
        `<button type="button" class="md-button ex-reset">הדוגמה מהדף</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button md-button--primary ex-next">השלב הבא</button>` +
        `<button type="button" class="md-button ex-prev">השלב הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(2200, 1300, 600) +
        `<button type="button" class="md-button ex-start">להתחלה</button>` +
        `<button type="button" class="md-button ex-end">לסוף</button><span class="ex-pos"></span></div>` +
        `<div class="lf-crates"></div>` +
        `<p class="lf-arr" dir="ltr"></p>` +
        `<p class="wv-step lf-step" aria-live="polite"></p><p class="ex-summary lf-vars"></p>`;
      const $ = (sel) => box.querySelector(sel);
      const ball = () => st.content[st.labels.indexOf("MIXED")];
      const labelsAt = (r) => (st.k >= 4 ? r.after2 : st.k >= 3 ? r.after1 : st.labels);
      const CX = (i) => 95 + 200 * i, TOP = 120;
      const svg = (r) => {
        const cur = labelsAt(r), b = ball(), open = st.k >= LF_STEPS - 1;
        // the 3-cycle: same -> k (the ball's colour), k -> other (MIXED, through same), other -> same
        const arcs = [[r.same, r.k, st.labels[r.same], st.k >= 3], [r.k, r.other, "MIXED", st.k >= 4], [r.other, r.same, st.labels[r.other], st.k >= 4]];
        let s = `<svg class="figure b3-live lf-live" viewBox="0 0 620 330" role="img" aria-label="שלוש הקופסאות עם התוויות ${cur.join(", ")}">`;
        if (st.k >= 2) arcs.forEach(([from, to, lab, done]) => {
          const x1 = CX(from), x2 = CX(to), h = Math.abs(from - to) === 2 ? 84 : 46, side = x2 > x1 ? -14 : 14;
          const y = TOP - 6, mx = (x1 + x2) / 2, my = y - h * 2, ex = x2 - side;
          // the head points along the curve's tangent at its end, from the control point
          const ux = ex - mx, uy = y - my, ul = Math.hypot(ux, uy), [dx, dy] = [ux / ul, uy / ul];
          const head = [[ex, y], [ex - 11 * dx - 6 * dy, y - 11 * dy + 6 * dx], [ex - 11 * dx + 6 * dy, y - 11 * dy - 6 * dx]];
          s += `<path class="lf-arc${done ? " is-done" : ""}" d="M ${x1 + side} ${y} Q ${mx} ${my} ${ex} ${y}"/>` +
               `<polygon class="lf-head${done ? " is-done" : ""}" points="${head.map(([u, v]) => `${f(u)},${f(v)}`).join(" ")}"/>` +
               `<text class="tick lf-arc-text" x="${mx}" y="${f(y - h - 6)}" text-anchor="middle">${lab}</text>`;
        });
        for (let i = 0; i < 3; i++) {
          const x = 20 + 200 * i, cx = CX(i), y0 = TOP, changed = (st.k === 3 && (i === r.k || i === r.same)) || (st.k === 4 && (i === r.same || i === r.other));
          s += `<g class="lf-crate${changed ? " is-changed" : ""}"><polygon class="crate-top" points="${x},${y0 + 30} ${x + 30},${y0} ${x + 180},${y0} ${x + 150},${y0 + 30}"/>` +
               `<polygon class="crate-side" points="${x + 150},${y0 + 30} ${x + 180},${y0} ${x + 180},${y0 + 100} ${x + 150},${y0 + 130}"/>` +
               `<rect class="crate-front" x="${x}" y="${y0 + 30}" width="150" height="100"/>` +
               `<text class="crate-text lf-label" x="${cx}" y="${y0 + 88}" font-size="20" text-anchor="middle">${cur[i]}</text></g>`;
          if (st.k >= 1 && i === r.k) s += `<circle class="b3-ball b3-${b.toLowerCase()}" cx="${x + 120}" cy="${y0 + 150}" r="9"><title>${b}</title></circle>`;
          const tags = [st.k >= 1 && i === r.k ? "k" : "", st.k >= 2 && i === r.same ? "same" : "", st.k >= 2 && i === r.other ? "other" : ""].filter(Boolean);
          s += `<text class="tick" x="${cx}" y="${y0 + 156}" text-anchor="middle">${i}${tags.length ? ` : ${tags.join(", ")}` : ""}</text>`;
          if (open) s += `<text class="tick lf-true${cur[i] === st.content[i] ? " is-ok" : ""}" x="${cx}" y="${y0 + 180}" text-anchor="middle">${st.content[i]} ${cur[i] === st.content[i] ? "✓" : "✗"}</text>`;
        }
        return s + "</svg>";
      };
      const draw = () => {
        const b = ball(), r = labelSwaps(st.labels, b), cur = labelsAt(r), oth = b === "RED" ? "BLACK" : "RED";
        $(".lf-crates").innerHTML = svg(r);
        const hl = st.k === 3 ? [r.k, r.same] : st.k === 4 ? [r.same, r.other] : [];
        $(".lf-arr").innerHTML = `labels = <span class="arr">${cur.map((l, i) => `<span${hl.includes(i) ? ' class="hl"' : ""}>${l}</span>`).join("")}</span>`;
        $(".ex-pos").textContent = `שלב ${st.k} מתוך ${LF_STEPS - 1}`;
        const steps = [
          `כל התוויות שגויות, והתוכן מוסתר. ״השלב הבא״ מריץ את ${ltr("fix_labels")} שורה אחרי שורה.`,
          `‏${ltr(`k = labels.index("MIXED") = ${r.k}`)}, ושולפים כדור מקופסה ${ltr(r.k)}${NB}: יצא ${ltr(b)}. התווית שלה שגויה, ולכן היא לא מעורבת, ויש בה רק ${ltr(b)}.`,
          `השכנים הם ${ltr(`n1 = ${r.n1}`)} ו-${ltr(`n2 = ${r.n2}`)}. בקופסה ${ltr(r.n1)} התווית ${ltr(st.labels[r.n1])}, ` +
            `${st.labels[r.n1] === b ? "כצבע הכדור" : "לא כצבע הכדור"}, ולכן ${ltr(`same = ${r.same}`)} ו-${ltr(`other = ${r.other}`)}. החצים הם הסיבוב של התוויות.`,
          `החלפה 1, בין ${ltr(`k = ${r.k}`)} ל-${ltr(`same = ${r.same}`)}${NB}: קופסה ${ltr(r.k)} מקבלת את ${ltr(b)}, והיא כבר נכונה. ${ltr("MIXED")} עובר זמנית ל-${ltr(r.same)}.`,
          `החלפה 2, בין ${ltr(`same = ${r.same}`)} ל-${ltr(`other = ${r.other}`)}${NB}: ${ltr(r.same)} מקבלת את ${ltr(oth)}, ו-${ltr("MIXED")} מגיע ל-${ltr(r.other)}. שתי ההחלפות יחד הן הסיבוב.`,
          `התוכן האמיתי מתחת לכל קופסה${NB}: שלוש התוויות נכונות, אחרי דגימה אחת ושתי החלפות.`,
        ];
        $(".lf-step").innerHTML = steps[st.k];
        $(".lf-vars").innerHTML = st.k ? `‏${ltr([`k = ${r.k}`, `ball = ${b}`].concat(st.k >= 2 ? [`n1 = ${r.n1}`, `n2 = ${r.n2}`, `same = ${r.same}`, `other = ${r.other}`] : []).join(", "))}` : "";
        $(".ex-prev").disabled = st.k === 0;
        $(".ex-next").disabled = st.k >= LF_STEPS - 1;
      };
      let stop = () => {};
      const setCase = (c) => { stop(); st.labels = c.labels.slice(); st.content = c.content.slice(); st.k = 0; draw(); };
      const seed = seedControls(box, $(".ex-reset"), (rng) => { const all = boxesCases(); setCase(all[Math.floor(rng() * all.length)]); });
      $(".ex-new").addEventListener("click", () => seed.draw());
      $(".ex-reset").addEventListener("click", () => setCase({ labels: ["RED", "BLACK", "MIXED"], content: ["BLACK", "MIXED", "RED"] }));
      $(".ex-next").addEventListener("click", () => { stop(); if (st.k < LF_STEPS - 1) { st.k++; draw(); } });
      $(".ex-prev").addEventListener("click", () => { stop(); if (st.k > 0) { st.k--; draw(); } });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = LF_STEPS - 1; draw(); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => { st.k++; draw(); }, done: () => st.k >= LF_STEPS - 1, restart: () => { st.k = 0; draw(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { boxes3: boxes3View, labelfix: labelfixView },
    help: {
      boxes3: "שלוש קופסאות עם תוויות שגויות : לוחצים על קופסה כדי להוציא כדור. כש״לשייך בעצמי״ מסומן, בוחרים מה בכל קופסה ובודקים, ורק אז ההיסק נכתב שורה אחרי שורה; אחרת הוא נכתב מיד. ״משחק חדש״ מגריל תכולה חדשה לאותן תוויות, ״ערבוב התוויות״ מסדר את התוויות מחדש, ו״גילוי התוכן״ פותח את הקופסאות.",
      labelfix: "״השלב הבא״ ו״הפעלה״ מריצים את fix_labels : מוצאים את k ושולפים כדור, מזהים את same ואת other, ומבצעים את שתי ההחלפות. החצים מעל הקופסאות הם הסיבוב של שלוש התוויות, ובסוף מופיע התוכן האמיתי. ״סידור חדש״ מגריל אחד מ-12 המקרים.",
    },
    models: { boxesCases, boxesDraw, boxesFix, boxesDeduce, labelSwaps },
  });
})();
