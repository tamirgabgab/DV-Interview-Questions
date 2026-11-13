// kinds: thrice
//   thrice                 0106        the number that appears once when every other appears three times (data-nums "2.2.3.2", data-order good / swap / old): a typed array of up to 16 numbers from −128 to 127 or a ready one (the page's example, 99, negatives, one number twice among threes, a broken rule), fed number by number to ones and twos; the bits of x, ones and twos in 8 lanes with the bits that changed framed, the state of every lane against its true count of ones modulo 3, the mod-3 state diagram of a chosen lane with the move just made, a log of the steps, and at the end ones (and ones | twos) against the answer found by counting every value; the order of the two lines as a select (the page's, twos first, both from the old values) to see the counter break
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { answer, autoplay, ltr, speedSel } = dvqExplorers.lib;
  const NB = " ";
  const MINUS = "−";
  const NMAX = 16, VMIN = -128, VMAX = 127, W = 8;

  // --- the model, as tools/figures/q0106.py ------------------------------------------------
  // "2, 2, 3, 2", "2.2.3.2" or "-2 −2 1": 1 to NMAX whole numbers from VMIN to VMAX, else null
  const thParse = (text) => {
    const p = String(text || "").replace(/−/g, "-").trim().split(/[\s,;.]+/).filter(Boolean);
    if (!p.length || p.length > NMAX || p.some((x) => !/^-?\d+$/.test(x) || Number(x) < VMIN || Number(x) > VMAX)) return null;
    return p.map(Number);
  };
  // the two lines in the page's order ("good"), with twos first ("swap") or both from the old
  // values ("old"): ones and twos after every number (JavaScript's 32-bit integers; for
  // numbers of 8 bits every lane from 7 up holds the same state, so these are the values of
  // Python's unbounded integers too)
  const thTrace = (nums, order = "good") => {
    let ones = 0, twos = 0;
    return nums.map((x) => {
      if (order === "swap") { twos = (twos ^ x) & ~ones; ones = (ones ^ x) & ~twos; }
      else if (order === "old") { const o = (ones ^ x) & ~twos, t = (twos ^ x) & ~ones; ones = o; twos = t; }
      else { ones = (ones ^ x) & ~twos; twos = (twos ^ x) & ~ones; }
      return [ones, twos];
    });
  };
  // the ones of every lane (bit b of every number, the sign repeated above bit 7), lane 0 first
  const thLanes = (nums, width = W) => Array.from({ length: width }, (_, b) => nums.reduce((s, x) => s + ((x >> b) & 1), 0));
  // the values whose count is not a multiple of 3, in the order they first appear: [value, count]
  const thOdd = (nums) => {
    const seen = new Map();
    nums.forEach((x) => seen.set(x, (seen.get(x) || 0) + 1));
    return [...seen].filter(([, c]) => c % 3);
  };
  // the lane drawn in the diagram when the page names none: the one with the most ones (the lowest of a tie)
  const thLane = (nums) => {
    const c = thLanes(nums);
    return c.indexOf(Math.max(...c));
  };
  const thPresets = [
    ["הדוגמה", [2, 2, 3, 2]],
    ["99 פעם אחת", [0, 1, 0, 1, 0, 1, 99]],
    ["עם שליליים", [-2, -2, 1, 1, -3, 1, -3, -3, -4, -2]],
    ["אחד פעמיים", [5, 5, 7, 7, 7]],
    ["הכלל לא מתקיים", [2, 3, 2, 5, 2]],
  ];
  const ORDERS = [["good", "ones ואז twos, כמו בעמוד"], ["swap", "twos ואז ones"], ["old", "שתיהן מהערכים הישנים"]];
  const presetOf = (nums) => thPresets.findIndex(([, a]) => a.join() === nums.join());

  // --- drawing -------------------------------------------------------------------------
  const num = (v) => (v < 0 ? `${MINUS}${-v}` : String(v));
  const bitsOf = (v) => Array.from({ length: W }, (_, i) => (v >> (W - 1 - i)) & 1);
  const sgn = (v) => ((v & 0xff) ^ 0x80) - 0x80;              // the value of the low 8 bits, signed
  const state = (ones, twos, b) => (((twos >> b) & 1) << 1) | ((ones >> b) & 1);   // 0, 1, 2 or 3 (11)
  const STATE_TXT = ["0", "1", "2", "!"];

  // the register table: a column per lane (7 on the left), the lane buttons on top
  const regTable = (st, k, tr, lane) => {
    const x = k ? st.nums[k - 1] : null;
    const [o1, t1] = k ? tr[k - 1] : [0, 0];
    const [o0, t0] = k > 1 ? tr[k - 2] : [0, 0];
    const cnt = thLanes(st.nums.slice(0, k));
    let h = `<table class="m3-reg" dir="ltr"><thead><tr><th scope="col"><span class="m3-sr">השורה</span></th>`;
    for (let b = W - 1; b >= 0; b--) {
      h += `<th scope="col"><button type="button" class="m3-lanebtn${b === lane ? " is-sel" : ""}" data-b="${b}" aria-pressed="${b === lane}" aria-label="ביט ${b} בתרשים">${b}</button></th>`;
    }
    h += `<th scope="col" class="m3-vh">ערך</th></tr></thead><tbody>`;
    const row = (name, v, cls, prev) => {
      let r = `<tr><th scope="row">${name}</th>`;
      bitsOf(v === null ? 0 : v).forEach((bt, i) => {
        const b = W - 1 - i, chg = prev !== undefined && ((prev >> b) & 1) !== bt;
        r += `<td class="m3-b${v !== null && bt ? ` ${cls}` : ""}${chg ? " is-chg" : ""}${b === lane ? " is-lane" : ""}">${v === null ? "·" : bt}</td>`;
      });
      return r + `<td class="m3-v">${v === null ? "–" : num(sgn(v))}</td></tr>`;
    };
    h += row("x", x, "m3-x");
    h += row("ones", o1, "m3-one", k ? o0 : undefined);
    h += row("twos", t1, "m3-two", k ? t0 : undefined);
    h += `<tr><th scope="row">המצב</th>`;
    for (let b = W - 1; b >= 0; b--) {
      const s = state(o1, t1, b), bad = s === 3 || s !== cnt[b] % 3;
      h += `<td class="m3-b m3-st${s}${bad ? " is-bad" : ""}${b === lane ? " is-lane" : ""}">${STATE_TXT[s]}</td>`;
    }
    h += `<td class="m3-v"></td></tr><tr><th scope="row">הספירה</th>`;
    for (let b = W - 1; b >= 0; b--) h += `<td class="m3-b m3-cnt${b === lane ? " is-lane" : ""}" title="${cnt[b]} ones in bit ${b}">${cnt[b] % 3}</td>`;
    return h + `<td class="m3-v">mod 3</td></tr></tbody></table>`;
  };

  // the state diagram of one lane, as tools/figures/q0106.py fsm_svg draws it
  const NODES = [[80, 170], [190, 80], [300, 170]], BAD = [190, 152], NR = 28;
  const f1 = (v) => v.toFixed(1);
  const head = (tx, ty, vx, vy) => {
    const ex = tx - 9 * vx, ey = ty - 9 * vy;
    return [`M${f1(tx)},${f1(ty)} L${f1(ex - 5 * vy)},${f1(ey + 5 * vx)} L${f1(ex + 5 * vy)},${f1(ey - 5 * vx)} Z`, ex, ey];
  };
  const arc = (a, b, bow) => {
    const [x0, y0] = NODES[a], [x1, y1] = NODES[b];
    const dx = x1 - x0, dy = y1 - y0, L = Math.hypot(dx, dy), nx = dy / L, ny = -dx / L;
    const cx = (x0 + x1) / 2 + bow * nx, cy = (y0 + y1) / 2 + bow * ny;
    const ul = Math.hypot(x0 - cx, y0 - cy), sx = x0 - (NR * (x0 - cx)) / ul, sy = y0 - (NR * (y0 - cy)) / ul;
    const vl = Math.hypot(x1 - cx, y1 - cy), vx = (x1 - cx) / vl, vy = (y1 - cy) / vl;
    const [hd, ex, ey] = head(x1 - (NR + 1) * vx, y1 - (NR + 1) * vy, vx, vy);
    const lx = 0.25 * x0 + 0.5 * cx + 0.25 * x1 + 13 * nx, ly = 0.25 * y0 + 0.5 * cy + 0.25 * y1 + 13 * ny;
    return [`M${f1(sx)},${f1(sy)} Q${f1(cx)},${f1(cy)} ${f1(ex)},${f1(ey)}`, hd, lx, ly];
  };
  const loop = (s, a) => {
    const [x, y] = NODES[s], p = (ang, r) => [x + r * Math.cos(ang), y + r * Math.sin(ang)];
    const [sx, sy] = p(a - 0.5, NR), [tx, ty] = p(a + 0.5, NR + 1), [c1x, c1y] = p(a - 0.75, NR * 2.5), [c2x, c2y] = p(a + 0.75, NR * 2.5);
    const vl = Math.hypot(tx - c2x, ty - c2y);
    const [hd, ex, ey] = head(tx, ty, (tx - c2x) / vl, (ty - c2y) / vl);
    const [lx, ly] = p(a, NR * 2.45);
    return [`M${f1(sx)},${f1(sy)} C${f1(c1x)},${f1(c1y)} ${f1(c2x)},${f1(c2y)} ${f1(ex)},${f1(ey)}`, hd, lx, ly];
  };
  const ARCS = [[0, 1, 26], [1, 2, 26], [2, 0, 110]], LOOPS = [Math.PI, -Math.PI / 2, 0];
  const fsmSvg = (lane, now, taken, label) => {
    let o = `<svg class="figure m3-fsm m3-live" viewBox="0 0 380 252" style="max-width:20rem" direction="ltr" role="img" aria-label="${label}">`;
    ARCS.forEach(([a, b, bow], s) => {
      const [d, hd, lx, ly] = arc(a, b, bow);
      o += `<g class="m3-arc${taken === `one${s}` ? " is-taken" : ""}"><title>a 1: ${s} → ${(s + 1) % 3}</title><path d="${d}" fill="none"/>` +
        `<path class="m3-head" d="${hd}"/><text class="m3-lab" x="${f1(lx)}" y="${f1(ly + 5)}" text-anchor="middle">1</text></g>`;
    });
    LOOPS.forEach((a, s) => {
      const [d, hd, lx, ly] = loop(s, a);
      o += `<g class="m3-loop${taken === `zero${s}` ? " is-taken" : ""}"><title>a 0: stays at ${s}</title><path d="${d}" fill="none"/>` +
        `<path class="m3-head" d="${hd}"/><text class="m3-lab" x="${f1(lx)}" y="${f1(ly + 5)}" text-anchor="middle">0</text></g>`;
    });
    NODES.forEach(([x, y], s) => {
      const code = ["00", "01", "10"][s];
      o += `<g class="m3-node m3-n${s}${now === s ? " is-now" : ""}"><title>twos ${code[0]}, ones ${code[1]}: count ${s} mod 3</title>` +
        `<circle cx="${x}" cy="${y}" r="${NR}"/><text class="m3-code" x="${x}" y="${y + 1}" text-anchor="middle">${code}</text>` +
        `<text class="m3-cnt" x="${x}" y="${y + 17}" text-anchor="middle">≡${s}</text></g>`;
    });
    o += `<g class="m3-node m3-n3${now === 3 ? " is-now" : ""}"><title>twos 1, ones 1: never reached by the page's order</title>` +
      `<circle cx="${BAD[0]}" cy="${BAD[1]}" r="20"/><text class="m3-code" x="${BAD[0]}" y="${BAD[1] + 5}" text-anchor="middle">11</text></g>`;
    o += `<text class="m3-lanelab" x="372" y="20" text-anchor="end">bit ${lane}</text>`;
    return o + "</svg>";
  };

  // the log: a row per number fed so far
  const logRows = (st, k, tr) => {
    if (!k) return `<tr><td colspan="4" class="m3-empty">עוד לא נכנס מספר</td></tr>`;
    let h = "";
    for (let i = 0; i < k; i++) {
      h += `<tr${i === k - 1 ? ' class="is-now"' : ""}><td>${i + 1}</td><td>${num(st.nums[i])}</td><td>${num(tr[i][0])}</td><td>${num(tr[i][1])}</td></tr>`;
    }
    return h;
  };

  const threeView = () => ({
    mount(box) {
      const g0 = thParse(String(box.dataset.nums || "").split(".").join(" "));
      const o0 = ORDERS.some(([v]) => v === box.dataset.order) ? box.dataset.order : "good";
      const init = { nums: g0 || thPresets[0][1].slice(), order: o0 };
      const st = { nums: init.nums.slice(), order: init.order, k: 0, lane: thLane(init.nums), err: "", picked: false };
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label>המערך <select class="m3-preset" aria-label="איזה מערך">${thPresets.map(([name], i) => `<option value="${i}">${name}</option>`).join("")}<option value="custom">משלכם</option></select></label>` +
        `<label>המספרים <input type="text" class="m3-nums" dir="ltr" spellcheck="false" autocomplete="off" aria-label="המספרים, מופרדים בפסיקים, עד 16 מספרים מ-−128 עד 127"></label>` +
        `<label>הסדר <select class="m3-order" aria-label="הסדר של שתי השורות">${ORDERS.map(([v, t]) => `<option value="${v}">${t}</option>`).join("")}</select></label>` +
        `<label>הביט בתרשים <select class="m3-lane" aria-label="הביט שהתרשים מראה">${Array.from({ length: W }, (_, b) => `<option value="${b}">${b}</option>`).join("")}</select></label>` +
        `<button type="button" class="md-button ex-reset">חזרה לערכים של העמוד</button></div>` +
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(1400, 800, 350) +
        `<span class="ex-pos"></span></div>` +
        `<p class="ex-summary m3-sum" aria-live="polite"></p>` +
        `<div class="m3-regwrap" tabindex="0" role="region" aria-label="x, ones ו-twos בשמונה ביטים, המצב של כל ביט והספירה האמיתית שלו"></div>` +
        `<p class="m3-note"></p>` +
        `<span class="viz-legend m3-legend"><span><i class="m3-key-x"></i>ביט 1 ב-x</span><span><i class="m3-key-n1"></i>ביט 1 ב-ones${NB}: ספירה 1</span>` +
        `<span><i class="m3-key-n2"></i>ביט 1 ב-twos${NB}: ספירה 2</span><span><i class="m3-key-chg"></i>ביט שהצעד שינה</span>` +
        `<span><i class="m3-key-bad"></i>מצב שלא מתאים לספירה</span><span><i class="m3-key-taken"></i>המעבר של הצעד</span></span>` +
        `<div class="m3-fsmwrap"></div>` +
        `<div class="m3-logwrap" tabindex="0" role="region" aria-label="יומן הצעדים${NB}: המספר, ones ו-twos אחרי כל מספר"><table class="m3-log" dir="ltr"><thead><tr><th>#</th><th>x</th><th>ones</th><th>twos</th></tr></thead><tbody></tbody></table></div>`;
      answer(box, NB); answer(box, null);
      const $ = (sel) => box.querySelector(sel);
      const play = $(".ex-play"), speed = $(".ex-speed");
      const syncFields = () => {
        const i = presetOf(st.nums);
        $(".m3-preset").value = i < 0 ? "custom" : String(i);
        $(".m3-nums").value = st.nums.map(num).join(", ").replace(new RegExp(MINUS, "g"), "-");
        $(".m3-order").value = st.order;
        $(".m3-lane").value = String(st.lane);
      };
      const finalText = (tr) => {
        const [ones, twos] = tr[tr.length - 1], odd = thOdd(st.nums), any = ones | twos;
        const oddTxt = odd.map(([v, c]) => `${ltr(num(v))} ${c === 1 ? "פעם אחת" : c === 2 ? "פעמיים" : `${c} פעמים`}`).join(", ");
        if (odd.length === 1) {
          const [v, c] = odd[0];
          if (c % 3 === 1) {
            return ones === v
              ? `${ltr(`ones = ${num(ones)}`)}, המספר שמופיע פעם אחת. גם הספירה של כל ערך מוצאת ${ltr(num(v))}, וכל השאר מופיעים שלוש פעמים.`
              : `${ltr(`ones = ${num(ones)}`)}, אבל הספירה מוצאת ${ltr(num(v))}${NB}: הסדר של השורות שבר את המונה.`;
          }
          return ones === 0 && twos === v
            ? `${ltr(num(v))} מופיע פעמיים, ולכן הוא ב-twos${NB}: ${ltr(`ones = 0, twos = ${num(twos)}`)}. ‏${ltr(`ones | twos = ${num(any)}`)} מוצא אותו (סעיף ג).`
            : `${ltr(num(v))} מופיע פעמיים, אבל ${ltr(`ones = ${num(ones)}, twos = ${num(twos)}`)}${NB}: הסדר של השורות שבר את המונה.`;
        }
        if (!odd.length) return `כל מספר מופיע מספר פעמים שמתחלק ב-3, ולכן ${ltr(`ones = ${num(ones)}, twos = ${num(twos)}`)}.`;
        return `הכלל לא מתקיים${NB}: ${oddTxt}. ‏${ltr(`ones = ${num(ones)}, ones | twos = ${num(any)}`)}${st.nums.includes(ones) ? "" : `, ו-${ltr(num(ones))} בכלל לא במערך`}.`;
      };
      const draw = () => {
        const n = st.nums.length, tr = thTrace(st.nums, st.order);
        st.k = Math.min(Math.max(st.k, 0), n);
        const k = st.k, done = k === n, lane = st.lane;
        $(".ex-pos").textContent = `צעד ${k} מתוך ${n}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = done;
        const reg = $(".m3-regwrap"), had = reg.contains(document.activeElement) && document.activeElement.dataset ? document.activeElement.dataset.b : null;
        reg.innerHTML = regTable(st, k, tr, lane);
        if (had !== null && had !== undefined) { const b = reg.querySelector(`[data-b="${had}"]`); if (b) b.focus(); }
        const [o1, t1] = k ? tr[k - 1] : [0, 0], [o0, t0] = k > 1 ? tr[k - 2] : [0, 0];
        const now = state(o1, t1, lane), xb = k ? (st.nums[k - 1] >> lane) & 1 : null, from = state(o0, t0, lane);
        const taken = k && from < 3 && st.order === "good" ? `${xb ? "one" : "zero"}${from}` : null;
        $(".m3-fsmwrap").innerHTML = fsmSvg(lane, now, taken,
          `המונה של ביט ${lane}${NB}: שלושה מצבים, 00, 01 ו-10, לספירה 0, 1 ו-2 מודולו 3. עכשיו ${["00", "01", "10", "11"][now]}`);
        $(".m3-log tbody").innerHTML = logRows(st, k, tr);
        const log = $(".m3-logwrap"), cur = log.querySelector("tr.is-now");
        if (cur) log.scrollTop = Math.max(0, cur.offsetTop - log.clientHeight + cur.offsetHeight + 4);
        else log.scrollTop = 0;
        let sum, note;
        if (!k) {
          sum = `${n} מספרים. ‏${ltr("ones = twos = 0")}${NB}: כל ביט במצב 00, הספירה 0.`;
          note = st.err ? `<span class="m3-err">${st.err}</span>` :
            `כל צעד מכניס מספר אחד${NB}: ${ltr("ones = (ones ^ x) & ~twos")}, ואחר כך ${ltr("twos = (twos ^ x) & ~ones")}` +
            (st.order === "good" ? " עם ones החדש." : st.order === "swap" ? ", אבל כאן twos מחושב ראשון." : ", אבל כאן שתיהן מהערכים הישנים.");
        } else {
          const x = st.nums[k - 1];
          sum = `צעד ${k}${NB}: נכנס ${ltr(`x = ${num(x)}`)}. עכשיו ${ltr(`ones = ${num(o1)}, twos = ${num(t1)}`)}.`;
          const cnt = thLanes(st.nums.slice(0, k))[lane];
          const fromTxt = ["00", "01", "10", "11"][from], toTxt = ["00", "01", "10", "11"][now];
          note = `בביט ${lane}${NB}: ‏x נותן ${xb}, והמצב ${ltr(`${fromTxt} → ${toTxt}`)}. עד עכשיו ${cnt} ${cnt === 1 ? "מספר" : "מספרים"} עם 1 בביט הזה, ` +
            (now === cnt % 3 ? `ו-${ltr(`${cnt} mod 3 = ${cnt % 3}`)}, כמו המצב.` : `אבל ${ltr(`${cnt} mod 3 = ${cnt % 3}`)}${NB}: המצב לא מתאים לספירה.`);
        }
        $(".m3-sum").innerHTML = sum;
        $(".m3-note").innerHTML = note;
        answer(box, done ? finalText(tr) : null, done ? ".m3-reg tbody tr:nth-child(2) td.m3-b" : []);
      };
      const stop = autoplay(play, speed, { step: () => { st.k++; draw(); }, done: () => st.k >= st.nums.length, restart: () => { st.k = 0; draw(); } });
      const restart = () => { stop(); st.k = 0; draw(); };
      const setNums = (nums) => {
        st.nums = nums; st.err = "";
        if (!st.picked) st.lane = thLane(nums);
        syncFields(); restart();
      };
      $(".m3-preset").addEventListener("change", () => {
        const pr = thPresets[Number($(".m3-preset").value)];
        if (!pr || $(".m3-preset").value === "custom") { syncFields(); return; }
        setNums(pr[1].slice());
      });
      $(".m3-nums").addEventListener("change", () => {
        const v = thParse($(".m3-nums").value);
        if (!v) {
          st.err = `צריך בין 1 ל-${NMAX} מספרים שלמים מ-${ltr(num(VMIN))} עד ${VMAX}, מופרדים בפסיקים.`;
          stop(); st.k = 0; draw(); return;
        }
        setNums(v);
      });
      $(".m3-order").addEventListener("change", () => {
        const v = $(".m3-order").value;
        if (ORDERS.some(([o]) => o === v)) st.order = v;
        st.err = ""; restart();
      });
      const pickLane = (b) => { st.lane = b; st.picked = true; $(".m3-lane").value = String(b); draw(); };
      $(".m3-lane").addEventListener("change", () => {
        const b = Number($(".m3-lane").value);
        if (Number.isInteger(b) && b >= 0 && b < W) pickLane(b);
      });
      $(".m3-regwrap").addEventListener("click", (ev) => { const btn = ev.target.closest(".m3-lanebtn"); if (btn) pickLane(Number(btn.dataset.b)); });
      $(".ex-start").addEventListener("click", () => { stop(); st.k = 0; draw(); });
      $(".ex-prev").addEventListener("click", () => { stop(); st.k--; draw(); });
      $(".ex-next").addEventListener("click", () => { st.k++; draw(); });
      $(".ex-end").addEventListener("click", () => { stop(); st.k = st.nums.length; draw(); });
      $(".ex-reset").addEventListener("click", () => {
        Object.assign(st, { nums: init.nums.slice(), order: init.order, err: "", picked: false, lane: thLane(init.nums) });
        syncFields(); restart();
      });
      syncFields();
      draw();
    },
  });

  dvqExplorers.register({
    views: { thrice: threeView },
    help: {
      thrice: "בוחרים מערך או כותבים עד 16 מספרים מ-−128 עד 127. כל צעד מכניס מספר אחד ל-ones ול-twos, ובטבלה כל עמודה היא ביט : המצב שלו לפי הרגיסטרים מול הספירה האמיתית של האחדים בו, מודולו 3. לחיצה על מספר של ביט מראה אותו בתרשים המצבים. בשדה הסדר אפשר להחליף את הסדר של שתי השורות ולראות את המונה נשבר.",
    },
    cols: { thrice: { main: ".m3-regwrap, .m3-note, .m3-legend", side: ".m3-fsmwrap, .m3-logwrap", w: "minmax(0, 1.1fr)" } },   // the registers and the step's note beside the diagram of one lane and the log
    models: { thParse, thTrace, thLanes, thOdd, thLane, thPresets },
  });
})();
