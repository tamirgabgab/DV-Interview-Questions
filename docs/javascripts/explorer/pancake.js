// kinds: pancake
//   pancake                0090        a stack of pancakes to sort by flips (n from 3 to 8, or burnt pancakes up to 6): a click on a pancake turns it and every one above it over; the flips counted against the fewest (a BFS from the sorted stack over every stack of n), a hint that marks a flip one closer, undo, start over, a random stack; burnt pancakes show their burnt side as a thick edge
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests (tests/0090 compares them with tools/figures/q0090.py).
(() => {
  const { answer, ltr } = dvqExplorers.lib;
  const NB = "\u00a0";

  // --- the model ------------------------------------------------------------------------------

  // a stack is an array, its first item the top; a burnt pancake is a signed size, negative
  // when its burnt side faces up
  const pkFlip = (s, k, burnt) => s.slice(0, k).reverse().map((x) => (burnt ? -x : x)).concat(s.slice(k));
  const K0 = (burnt) => (burnt ? 1 : 2);   // a flip of one changes nothing on a plain stack
  // the fewest flips that sort every stack of n: a BFS from the sorted stack (a flip is its
  // own inverse), as { "3,1,2": d }
  const pkDist = (n, burnt) => {
    const start = Array.from({ length: n }, (_, i) => i + 1);
    const dist = { [start.join(",")]: 0 }, queue = [start];
    for (let h = 0; h < queue.length; h++) {
      const s = queue[h], d = dist[s.join(",")] + 1;
      for (let k = K0(burnt); k <= n; k++) {
        const t = pkFlip(s, k, burnt), key = t.join(",");
        if (!(key in dist)) { dist[key] = d; queue.push(t); }
      }
    }
    return dist;
  };
  // the k of a flip one closer to sorted (the smallest such k), or 0 when sorted
  const pkNext = (s, dist, burnt) => {
    const d = dist[s.join(",")];
    if (!d) return 0;
    for (let k = K0(burnt); k <= s.length; k++) if (dist[pkFlip(s, k, burnt).join(",")] === d - 1) return k;
    return 0;
  };
  // a shortest sorting: [k, ...]
  const pkBest = (s, dist, burnt) => {
    const out = [];
    for (let k = pkNext(s, dist, burnt); k; k = pkNext(s, dist, burnt)) { s = pkFlip(s, k, burnt); out.push(k); }
    return out;
  };
  // "3,1,5,4,2" -> the stack, or null unless it is 1..n once each (signed only when burnt)
  const pkParse = (text, burnt) => {
    const parts = String(text).split(/[\s,]+/).filter(Boolean);
    if (!parts.length || parts.length > 8 || parts.some((p) => !/^-?\d+$/.test(p))) return null;
    const s = parts.map(Number), n = s.length;
    if (!burnt && s.some((x) => x < 0)) return null;
    const seen = new Set(s.map(Math.abs));
    return seen.size === n && [...seen].every((v) => v >= 1 && v <= n) ? s : null;
  };
  const cache = {};
  const distOf = (n, burnt) => (cache[`${n}${burnt ? "b" : "p"}`] ||= pkDist(n, burnt));
  // the page's start for a size: plain, the first of the hardest stacks; burnt, the sorted
  // stack with every burnt side up (the hardest one up to 7)
  const pkHardest = (n, burnt) => {
    if (burnt) return Array.from({ length: n }, (_, i) => -(i + 1));
    const dist = distOf(n, false), worst = Math.max(...Object.values(dist));
    const keys = Object.keys(dist).filter((k) => dist[k] === worst).map((k) => k.split(",").map(Number));
    keys.sort((a, b) => { for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return a[i] - b[i]; return 0; });
    return keys[0];
  };

  // --- the box --------------------------------------------------------------------------------

  const N_MIN = 3, N_MAX = 8, BURNT_MAX = 6;
  const stackWords = (s) => `<code>[${s.join(`,${NB}`)}]</code>`;   // no-break spaces: it never wraps

  const pancakeView = () => ({
    mount(box) {
      const burnt0 = box.dataset.burnt === "1";
      const page = pkParse(box.dataset.stack || "", burnt0);
      const n0 = page ? page.length : Math.min(Math.max(Number(box.dataset.n) || 5, N_MIN), burnt0 ? BURNT_MAX : N_MAX);
      const st = { burnt: burnt0, start: page || pkHardest(n0, burnt0), flips: [], hint: 0, last: 0 };
      const sizes = Array.from({ length: N_MAX - N_MIN + 1 }, (_, i) => N_MIN + i);
      box.innerHTML =
        `<div class="ex-controls">` +
        `<label><span>פנקייקים</span><select class="pk-n" aria-label="כמה פנקייקים בערימה">${sizes.map((n) => `<option value="${n}">${n}</option>`).join("")}</select></label>` +
        `<label><span>סוג</span><select class="pk-mode" aria-label="פנקייקים רגילים או שרופים"><option value="0">רגילים</option><option value="1">שרופים</option></select></label>` +
        `</div>` +
        `<div class="ex-controls pk-acts">` +
        `<button type="button" class="md-button pk-hintb">רמז</button>` +
        `<button type="button" class="md-button pk-undo">ביטול</button>` +
        `<button type="button" class="md-button pk-again">מההתחלה</button>` +
        `<button type="button" class="md-button pk-rand">הגרלה</button>` +
        `</div>` +
        `<div class="pk-stack" role="group" aria-label="הערימה, מלמעלה למטה. לחיצה על פנקייק הופכת אותו ואת כל מה שמעליו"></div>` +
        `<span class="viz-legend"><span><i class="pk-key-cake"></i>פנקייק, רחב כמו הגודל שלו</span>` +
        `<span class="pk-burntkey"><i class="pk-key-burnt"></i>הצד השרוף</span>` +
        `<span><i class="pk-key-flip"></i>ההפיכה האחרונה</span><span><i class="pk-key-hint"></i>רמז</span></span>` +
        `<p class="ex-summary pk-sum" aria-live="polite"></p>` +
        `<p class="pk-note"></p>`;
      const $ = (q) => box.querySelector(q);
      const n = () => st.start.length;
      const now = () => st.flips.reduce((s, k) => pkFlip(s, k, st.burnt), st.start);
      const draw = () => {
        const s = now(), dist = distOf(n(), st.burnt), N = n();
        $(".pk-n").value = String(N);
        $(".pk-mode").value = st.burnt ? "1" : "0";
        [...$(".pk-n").options].forEach((o) => { o.disabled = st.burnt && Number(o.value) > BURNT_MAX; });
        $(".pk-burntkey").style.display = st.burnt ? "" : "none";   // the legend span is a flex item: [hidden] would not hide it
        const rows = s.map((v, i) => {
          const size = Math.abs(v), w = 30 + (70 * size) / N;
          const cls = ["pk-row"];
          if (i < st.last) cls.push("is-flip");
          if (st.hint && i === st.hint - 1) cls.push("is-hint");
          const side = st.burnt ? (v > 0 ? " pk-down" : " pk-up") : "";
          const dis = !st.burnt && i === 0 ? " disabled" : "";
          const name = i === 0 ? (st.burnt ? "הפיכה של העליון לבד" : "העליון, הפיכה שלו לבד לא משנה כלום")
            : `הפיכה של ${i + 1} העליונים, עד הפנקייק ${size}`;
          const sideWord = st.burnt ? (v > 0 ? ", הצד השרוף למטה" : ", הצד השרוף למעלה") : "";
          return `<div class="${cls.join(" ")}"><button type="button" class="pk-cakeb${side}" data-k="${i + 1}" style="width:${w.toFixed(1)}%"${dis} aria-label="${size}${sideWord}. ${name}">${size}</button></div>`;
        });
        $(".pk-stack").innerHTML = rows.join("") + `<div class="pk-platebar" aria-hidden="true"></div>`;
        box.querySelectorAll(".pk-cakeb").forEach((b) => b.addEventListener("click", () => {
          st.flips = st.flips.concat([Number(b.dataset.k)]);
          st.last = Number(b.dataset.k); st.hint = 0;
          draw();
          const again = box.querySelector(`.pk-cakeb[data-k="${b.dataset.k}"]`);
          if (again && !again.disabled) again.focus();
        }));
        const left = dist[s.join(",")], from = dist[st.start.join(",")], used = st.flips.length;
        $(".pk-sum").innerHTML = `הפיכות${NB}: ${ltr(used)}. מכאן צריך לפחות ${ltr(left)}, ומההתחלה המינימום הוא ${ltr(from)}.`;
        $(".pk-undo").disabled = !used;
        $(".pk-again").disabled = !used;
        $(".pk-hintb").disabled = !left;
        let note;
        if (st.hint) note = `רמז${NB}: הופכים את ${ltr(st.hint)} העליונים${st.hint === 1 ? ", כלומר את העליון לבד" : ""}. זה מקרב את הערימה למיון בהפיכה אחת.`;
        else if (st.last) note = `ההפיכה האחרונה הפכה את ${ltr(st.last)} העליונים. עכשיו ${stackWords(s)}, מלמעלה למטה.`;
        else note = `הערימה ${stackWords(s)}, מלמעלה למטה${st.burnt ? ". מספר שלילי הוא פנקייק שהצד השרוף שלו למעלה" : ""}.`;
        $(".pk-note").innerHTML = note;
        if (!left) {
          const how = used === from ? "זה המינימום." : used < from ? "" : `המינימום${NB}: ${ltr(from)}.`;
          answer(box, used ? `ממוין אחרי ${ltr(used)} הפיכות. ${how}` : "הערימה כבר ממוינת.", ".pk-sum");
        } else answer(box, null);
      };
      const restart = (start, burnt) => { st.start = start; st.burnt = burnt; st.flips = []; st.hint = 0; st.last = 0; draw(); };
      $(".pk-n").addEventListener("change", () => {
        const N = Math.min(Number($(".pk-n").value) || 5, st.burnt ? BURNT_MAX : N_MAX);
        restart(pkHardest(N, st.burnt), st.burnt);
      });
      $(".pk-mode").addEventListener("change", () => {
        const burnt = $(".pk-mode").value === "1";
        restart(pkHardest(Math.min(n(), burnt ? BURNT_MAX : N_MAX), burnt), burnt);
      });
      $(".pk-hintb").addEventListener("click", () => { st.hint = pkNext(now(), distOf(n(), st.burnt), st.burnt); draw(); });
      $(".pk-undo").addEventListener("click", () => {
        st.flips = st.flips.slice(0, -1); st.hint = 0; st.last = st.flips.length ? st.flips[st.flips.length - 1] : 0; draw();
      });
      $(".pk-again").addEventListener("click", () => restart(st.start, st.burnt));
      $(".pk-rand").addEventListener("click", () => {
        const N = n();
        let s;
        do {
          s = Array.from({ length: N }, (_, i) => i + 1);
          for (let i = N - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [s[i], s[j]] = [s[j], s[i]]; }
          if (st.burnt) s = s.map((v) => (Math.random() < 0.5 ? -v : v));
        } while (!distOf(N, st.burnt)[s.join(",")]);
        restart(s, st.burnt);
      });
      // the start and the flips ride in the link: "3.1.5.4.2_3.5" (after the size and the kind)
      box.dvqExtra = {
        get: () => `${st.start.join(".")}_${st.flips.join(".")}`,
        set: (text) => {
          const r = /^(-?\d+(?:\.-?\d+)*)_((?:\d+(?:\.\d+)*)?)$/.exec(text);
          if (!r) return false;
          const start = pkParse(r[1].replace(/\./g, ","), st.burnt);
          const flips = r[2] ? r[2].split(".").map(Number) : [];
          if (!start || start.length !== n() || flips.length > 200 || flips.some((k) => k < K0(st.burnt) || k > start.length)) return false;
          st.start = start; st.flips = flips; st.hint = 0; st.last = flips.length ? flips[flips.length - 1] : 0;
          draw();
          return true;
        },
      };
      draw();
    },
  });

  dvqExplorers.register({
    views: { pancake: pancakeView },
    help: {
      pancake: "לוחצים על פנקייק כדי להפוך אותו ואת כל מה שמעליו. הדף סופר הפיכות ומשווה למינימום, שחושב ב-BFS על כל הערימות. \"רמז\" מסמן פנקייק שההפיכה שלו מקרבת למיון, \"ביטול\" מחזיר הפיכה אחת, \"מההתחלה\" חוזר לערימה שהתחלתם בה, ו\"הגרלה\" נותנת ערימה חדשה. בפנקייקים שרופים, הפס העבה הוא הצד השרוף, וצריך שכולם יהיו למטה.",
    },
    models: { pkFlip, pkDist, pkNext, pkBest, pkParse, pkHardest },
  });
})();
