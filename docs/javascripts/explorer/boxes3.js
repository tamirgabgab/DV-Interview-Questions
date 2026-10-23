// kinds: boxes3
//   boxes3                 0004        three mislabelled boxes with hidden contents: draw a ball, the deduction line by line
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { ltr, seedControls } = dvqExplorers.lib;

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
      const st = { labels: ["RED", "BLACK", "MIXED"], content: null, draws: [], games: 0, solvedFirst: 0 };
      const newGame = (keepStats = true, rnd = Math.random) => {
        const cases = boxesCases().filter((c) => c.labels.join() === st.labels.join());
        st.content = cases[Math.floor(rnd() * cases.length)].content;
        st.draws = [];
        if (!keepStats) { st.games = 0; st.solvedFirst = 0; }
      };
      newGame(false);
      box.innerHTML =
        `<div class="ex-controls"><button type="button" class="md-button md-button--primary ex-new">משחק חדש</button>` +
        `<button type="button" class="md-button ex-shuffle">ערבוב התוויות</button>` +
        `<button type="button" class="md-button ex-reveal">גילוי התוכן</button><span class="b3-stats"></span></div>` +
        `<div class="b3-crates" role="group" aria-label="שלוש קופסאות, לחיצה דוגמת כדור"></div>` +
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
        if (!st.draws.length) {
          $(".b3-step").innerHTML = `כל התוויות שגויות. בחרו קופסה ודגמו ממנה כדור.`;
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
      $(".ex-reveal").addEventListener("click", () => draw(true));
      draw();
    },
  });

  dvqExplorers.register({
    views: { boxes3: boxes3View },
    help: {
      boxes3: "שלוש קופסאות עם תוויות שגויות : לוחצים על קופסה כדי להוציא כדור, וההיסק נכתב שורה אחרי שורה. ״סידור אחר״ מגריל תכולה.",
    },
    models: { boxesCases, boxesDraw, boxesFix, boxesDeduce },
  });
})();
