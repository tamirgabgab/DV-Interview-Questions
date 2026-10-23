// kinds: river
//   river                  0032        cross by hand or let the BFS plan play; the state graph follows
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { W, f, frame, ltr, speedSel } = dvqExplorers.lib;

  // Wolf, goat and cabbage (0032): a state is four bits (farmer 1, wolf 2, goat 4,
  // cabbage 8; 0 near, 1 far). riverSafe is the page's test, riverMoves the crossings
  // from a state as [item, new state], riverPlan the BFS plan (what the farmer takes).
  const RIVER = { farmer: 1, wolf: 2, goat: 4, cabbage: 8 };
  const riverSafe = (s) => {
    const f = !!(s & 1), w = !!(s & 2), g = !!(s & 4), c = !!(s & 8);
    return g === f || (g !== w && g !== c);
  };
  const riverMoves = (s) => {
    const out = [];
    [null, "wolf", "goat", "cabbage"].forEach((item) => {
      if (item && !!(s & RIVER[item]) !== !!(s & 1)) return;
      out.push([item, s ^ 1 ^ (item ? RIVER[item] : 0)]);
    });
    return out;
  };
  const riverPlan = () => {
    const parent = new Map([[0, null]]);
    const queue = [0];
    for (let head = 0; head < queue.length; head++) {
      const s = queue[head];
      if (s === 15) break;
      riverMoves(s).forEach(([item, nxt]) => {
        if (riverSafe(nxt) && !parent.has(nxt)) { parent.set(nxt, [s, item]); queue.push(nxt); }
      });
    }
    const plan = [];
    for (let s = 15; parent.get(s) !== null; ) { const [p, item] = parent.get(s); plan.unshift(item); s = p; }
    return plan;
  };

  // The river box (0032): cross by hand (pick who boards the boat; an unsafe crossing is
  // shown and taken back), or let the BFS plan play; the state graph marks where you are.
  const riverView = () => ({
    mount(box) {
      const LETTER = { farmer: "F", wolf: "W", goat: "G", cabbage: "C" };
      const HEB = { wolf: "הזאב", goat: "העז", cabbage: "הכרוב" };
      const st = { s: 0, history: [], unsafe: null, plan: null, k: 0 };
      box.innerHTML =
        `<div class="ex-controls"><span>האיכר חוצה :</span>` +
        `<button type="button" class="md-button ex-go" data-item="">לבד</button>` +
        ["wolf", "goat", "cabbage"].map((i) => `<button type="button" class="md-button ex-go" data-item="${i}">עם ${HEB[i]}</button>`).join("") +
        `<button type="button" class="md-button ex-undo">צעד אחורה</button>` +
        `<button type="button" class="md-button ex-reset">מההתחלה</button>` +
        `<button type="button" class="md-button md-button--primary ex-solve">פתרון</button>` + speedSel(1800, 1100, 500) + `</div>` +
        `<div class="river-frame"></div><p class="ex-summary" aria-live="polite"></p>` +
        `<p class="ex-title">גרף המצבים : המצב הנוכחי מודגש, והמסלול שעברתם בכתום</p><div class="river-graph"></div>`;
      const $ = (sel) => box.querySelector(sel);
      let timer = null;
      const bankText = (s, side) => ["farmer", "wolf", "goat", "cabbage"].filter((n) => !!(s & RIVER[n]) === !!side).map((n) => LETTER[n]).join("") || "–";
      const frameSvg = (s, carried, moving, forward, unsafe) => {
        let out = `<svg class="figure river-fig" viewBox="0 0 640 190" style="max-width:40rem" role="img" aria-label="הנהר, שתי הגדות והסירה">` +
          `<rect class="bank" x="0" y="20" width="200" height="150" rx="8"/><rect class="bank" x="440" y="20" width="200" height="150" rx="8"/>` +
          `<rect class="river" x="200" y="20" width="240" height="150"/><text class="legend" x="100" y="160" text-anchor="middle">near</text><text class="legend" x="540" y="160" text-anchor="middle">far</text>`;
        const who = (name, x, y, cls) => `<g><circle class="${cls}" cx="${x}" cy="${y}" r="18"/><text class="st-text" x="${x}" y="${y + 5}" text-anchor="middle">${LETTER[name]}</text></g>`;
        const onBoat = moving ? new Set(["farmer", ...(carried ? [carried] : [])]) : new Set();
        [[0, 45], [1, 485]].forEach(([side, x0]) => {
          let k = 0;
          ["farmer", "wolf", "goat", "cabbage"].forEach((name) => {
            if (onBoat.has(name) || !!(s & RIVER[name]) !== !!side) return;
            const cls = unsafe && unsafe.includes(name) ? "st-bad" : name === "farmer" ? "st-stack" : "st-cell";
            out += who(name, x0 + 40 * k, 70, cls);
            k += 1;
          });
        });
        const bx = moving ? 320 : (s & 1 ? 365 : 215);
        out += `<rect class="boat" x="${bx - 50}" y="100" width="100" height="26" rx="10"/>`;
        if (moving) {
          out += who("farmer", carried ? bx - 20 : bx, 93, "st-stack") + (carried ? who(carried, bx + 20, 93, "st-cell") : "");
          const [x0, x1] = forward ? [250, 390] : [390, 250], d = forward ? 9 : -9;
          out += `<line class="ink-line" x1="${x0}" y1="150" x2="${x1}" y2="150" stroke-width="2"/><polygon class="ink-fill" points="${x1},150 ${x1 - d},145 ${x1 - d},155"/>`;
        }
        return out + "</svg>";
      };
      const graphSvg = () => {
        const X = (s) => 48 + ((s >> 1) & 7) * 78, Y = (s) => (s & 1 ? 190 : 60);
        const path = new Set();
        st.history.forEach(([a], i) => { const b = i + 1 < st.history.length ? st.history[i + 1][0] : st.s; path.add(`${Math.min(a, b)}-${Math.max(a, b)}`); });
        let out = `<svg class="figure river-graph" viewBox="0 0 640 250" style="max-width:40rem" role="img" aria-label="גרף המצבים עם המצב הנוכחי">`;
        for (let s = 0; s < 16; s++) {
          if (!riverSafe(s) || s & 1) continue;
          riverMoves(s).forEach(([, t]) => {
            if (!riverSafe(t)) return;
            const on = path.has(`${Math.min(s, t)}-${Math.max(s, t)}`);
            out += `<line class="${on ? "box-path" : "ink-line"}" x1="${X(s)}" y1="${Y(s) + 20}" x2="${X(t)}" y2="${Y(t) - 20}" stroke-width="${on ? 3 : 1}"${on ? "" : ' stroke-opacity="0.4"'}/>`;
          });
        }
        for (let s = 0; s < 16; s++) {
          const ok = riverSafe(s);
          const cls = s === st.s ? "st-cur" : s === 0 || s === 15 ? "st-ok" : ok ? "st-cell" : "st-bad";
          out += `<rect class="${cls}" x="${X(s) - 32}" y="${Y(s) - 20}" width="64" height="40" rx="6"/>` +
                 `<text class="st-text st-sm" x="${X(s)}" y="${Y(s) - 4}" text-anchor="middle">${bankText(s, 0)}</text><text class="st-text st-sm" x="${X(s)}" y="${Y(s) + 14}" text-anchor="middle">${bankText(s, 1)}</text>`;
          if (!ok) out += `<line class="pg-strike" x1="${X(s) - 26}" y1="${Y(s) + 16}" x2="${X(s) + 26}" y2="${Y(s) - 16}"/>`;
        }
        out += `<text class="legend" x="8" y="16">farmer near: near bank / far bank</text><text class="legend" x="8" y="240">farmer far</text>`;
        return out + "</svg>";
      };
      const eaten = (s) => {
        const f = !!(s & 1), w = !!(s & 2), g = !!(s & 4), c = !!(s & 8);
        if (w === g && g !== f) return ["wolf", "goat"];
        if (g === c && g !== f) return ["goat", "cabbage"];
        return null;
      };
      const draw = (moving = null) => {
        const s = st.s;
        $(".river-frame").innerHTML = frameSvg(moving ? moving.from : s, moving ? moving.item : null, !!moving, moving ? !(moving.from & 1) : true, st.unsafe ? eaten(st.unsafe.state) : null);
        const n = st.history.length;
        let text;
        if (st.unsafe) {
          const [a, b] = eaten(st.unsafe.state);
          text = `אסור : ${HEB[a]} ו${HEB[b]} נשארים לבד, ו${a === "wolf" ? "הזאב אוכל את העז" : "העז אוכלת את הכרוב"}. החצייה בוטלה.`;
        } else if (s === 15) {
          text = `כולם בצד הרחוק אחרי ${ltr(n)} חציות${n === 7 ? ", המינימום." : n > 7 ? `, ‏${ltr(n - 7)} יותר מהמינימום.` : "."}`;
        } else {
          text = `${n === 0 ? "ההתחלה" : `אחרי ${ltr(n)} חציות`} : על הגדה הקרובה ${ltr(bankText(s, 0))}, על הרחוקה ${ltr(bankText(s, 1))}. האיכר ב${s & 1 ? "צד הרחוק" : "צד הקרוב"}.`;
        }
        $(".ex-summary").innerHTML = text;
        box.querySelectorAll(".ex-go").forEach((b) => {
          const item = b.dataset.item || null;
          b.disabled = s === 15 || !!timer || (item !== null && !!(s & RIVER[item]) !== !!(s & 1));
        });
        $(".ex-undo").disabled = n === 0 || !!timer;
        $(".river-graph").innerHTML = graphSvg();

      };
      const cross = (item) => {
        const nxt = st.s ^ 1 ^ (item ? RIVER[item] : 0);
        st.unsafe = null;
        if (!riverSafe(nxt)) { st.unsafe = { state: nxt }; draw(); return false; }
        st.history.push([st.s, item]);
        st.s = nxt;
        draw();
        return true;
      };
      const stop = () => { if (timer) clearInterval(timer); timer = null; $(".ex-solve").textContent = "פתרון"; };
      box.querySelectorAll(".ex-go").forEach((b) => b.addEventListener("click", () => { stop(); cross(b.dataset.item || null); }));
      $(".ex-undo").addEventListener("click", () => { stop(); st.unsafe = null; if (st.history.length) { st.s = st.history.pop()[0]; } draw(); });
      $(".ex-reset").addEventListener("click", () => { stop(); st.s = 0; st.history = []; st.unsafe = null; draw(); });
      $(".ex-solve").addEventListener("click", () => {
        if (timer) { stop(); draw(); return; }
        st.s = 0; st.history = []; st.unsafe = null;
        const plan = riverPlan();
        let k = 0;
        const ms = Number($(".ex-speed").value);
        $(".ex-solve").textContent = "עצירה";
        timer = setInterval(() => {
          if (k >= plan.length) { stop(); draw(); return; }
          const item = plan[k];
          draw({ from: st.s, item });                               // on the boat
          setTimeout(() => { if (timer) cross(item); }, ms * 0.45);
          k += 1;
        }, ms);
        draw();
      });
      $(".ex-speed").addEventListener("change", () => { if (timer) { stop(); $(".ex-solve").click(); } });
      draw();
    },
  });

  dvqExplorers.register({
    views: { river: riverView },
    help: {
      river: "מעבירים את הזאב, העז והכרוב בלחיצה, או נותנים לתכנית ה-BFS לרוץ; גרף המצבים מתעדכן עם כל מעבר.",
    },
    models: { riverSafe, riverMoves, riverPlan },
  });
})();
