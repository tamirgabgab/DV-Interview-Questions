// kinds: uvmarch
//   uvmarch                0049        the UVM testbench drawn as in the figure: a click on a component explains it, one transaction stepped along its arrows, and a quiz ("who does this?") answered by clicking a component
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { autoplay, code, f, speedSel } = dvqExplorers.lib;

  // The layout, the arrows and the path of tools/figures/q0049.py (tests/0049 checks they
  // agree): id -> [label, x, y, w, h, container]; arrows [from, to, kind]; the path as the
  // arrows one transaction takes.
  const UV_LAYOUT = {
    top: ["tb_top", 8, 8, 664, 504, true],
    test: ["test", 18, 30, 644, 326, true],
    sequence: ["sequence", 120, 40, 110, 30, false],
    env: ["env", 28, 80, 624, 266, true],
    agent_in: ["agent (active)", 38, 104, 252, 232, true],
    sequencer: ["sequencer", 48, 132, 112, 44, false],
    driver: ["driver", 48, 240, 100, 44, false],
    monitor_in: ["monitor", 170, 240, 110, 44, false],
    scoreboard: ["scoreboard", 304, 132, 150, 64, false],
    coverage: ["coverage", 304, 240, 150, 44, false],
    agent_out: ["agent (passive)", 470, 104, 172, 232, true],
    monitor_out: ["monitor", 500, 240, 110, 44, false],
    vif_in: ["interface in", 48, 384, 232, 36, false],
    dut: ["DUT", 300, 376, 150, 120, false],
    vif_out: ["interface out", 470, 384, 172, 36, false],
  };
  const UV_ARROWS = [["sequence", "sequencer", "tlm"], ["sequencer", "driver", "tlm"], ["driver", "vif_in", "pin"], ["vif_in", "dut", "pin"],
    ["vif_in", "monitor_in", "pin"], ["dut", "vif_out", "pin"], ["vif_out", "monitor_out", "pin"], ["monitor_in", "scoreboard", "tlm"],
    ["monitor_in", "coverage", "tlm"], ["monitor_out", "scoreboard", "tlm"]];
  // the stages of one transaction: [arrow or null, the component lit, the text]
  const UV_STAGES = [
    [null, "test", "ה-test מרים objection ומריץ את ה-sequence על ה-sequencer של ה-agent האקטיבי : seq.start(sequencer)."],
    [["sequence", "sequencer"], "sequence", "ה-sequence יוצר item, ‏start_item מחכה שה-sequencer יבחר בו, ה-item מקבל ערכים ב-randomize, ו-finish_item מוסר אותו."],
    [["sequencer", "driver"], "driver", "ה-driver מושך את ה-item ב-get_next_item. ה-sequence חסום ב-finish_item עד שה-driver יגיד item_done."],
    [["driver", "vif_in"], "vif_in", "ה-driver מניע את האותות של ממשק הכניסה דרך ה-virtual interface, לפי הפרוטוקול, ואז item_done."],
    [["vif_in", "monitor_in"], "monitor_in", "מוניטור הכניסה דוגם את אותם אותות ובונה מהם טרנזקציה, בלי לדעת מה ה-sequence ביקש."],
    [["monitor_in", "scoreboard"], "scoreboard", "‏ap.write(tr) : ה-scoreboard מקבל את הקלט, ומודל הייחוס מחשב ממנו את הפלט הצפוי. גם ה-coverage מקבל עותק."],
    [["vif_in", "dut"], "dut", "ה-DUT מעבד את הקלט."],
    [["dut", "vif_out"], "vif_out", "ה-DUT מניע את ממשק היציאה. ה-agent של היציאה פסיבי : אף driver לא נוגע בו."],
    [["vif_out", "monitor_out"], "monitor_out", "מוניטור היציאה בונה טרנזקציה מהאותות."],
    [["monitor_out", "scoreboard"], "scoreboard", "‏ap.write(tr) : ה-scoreboard משווה את הפלט האמיתי לצפוי. בסוף, ב-check_phase, הוא מוודא שלא נשאר כלום בהמתנה."],
  ];
  const UV_PATH = UV_STAGES.filter(([e]) => e).map(([e]) => e);
  // what every component does, what it does not do, and its main calls
  const UV_INFO = {
    top: ["מודול SystemVerilog, לא class : שעון, איפוס, ה-DUT וה-interfaces.", "לא מכיל לוגיקת בדיקה.", "uvm_config_db#(virtual ...)::set, run_test()"],
    test: ["בוחר תצורה, יוצר את ה-env ומריץ sequences.", "לא מניע אותות בעצמו.", "build_phase, run_phase, raise_objection / drop_objection, factory overrides"],
    sequence: ["object שמייצר items ומחליט מה לשלוח, ברמת טרנזקציה.", "לא יודע איך האותות זזים; לא component.", "body(), start_item, randomize, finish_item"],
    env: ["מכיל את ה-agents, ה-scoreboard וה-coverage, ומחבר ביניהם.", "לא מייצר stimulus ולא בודק.", "build_phase, connect_phase"],
    agent_in: ["מאגד sequencer, ‏driver ומוניטור לממשק אחד. אקטיבי : שלושתם.", "לא מכיל בדיקות של התוצאה.", "is_active, build_phase, connect_phase"],
    sequencer: ["מתווך בין sequences ל-driver : תור ובחירה בין sequences.", "לא משנה את ה-items.", "seq_item_export, arbitration"],
    driver: ["מתרגם item לאותות לפי הפרוטוקול, דרך ה-virtual interface.", "לא בודק נכונות, ולא שולח ל-scoreboard.", "seq_item_port.get_next_item, item_done"],
    monitor_in: ["דוגם את אותות הכניסה, בונה טרנזקציה ומשדר אותה.", "לא משנה אף אות.", "analysis_port.write()"],
    scoreboard: ["מחשב את הצפוי ממוניטור הכניסה (מודל ייחוס) ומשווה ליציאה.", "לא מקבל טרנזקציות מה-driver או מה-sequence.", "uvm_analysis_imp, write(), check_phase"],
    coverage: ["‏uvm_subscriber שדוגם covergroups על הטרנזקציות.", "לא אומר אם התוצאה נכונה, רק מה נבדק.", "write(), covergroup.sample()"],
    agent_out: ["agent פסיבי : רק מוניטור, כי ה-DUT מניע את היציאה.", "לא יוצר sequencer ו-driver.", "is_active = UVM_PASSIVE"],
    monitor_out: ["דוגם את אותות היציאה, בונה טרנזקציה ומשדר אותה ל-scoreboard.", "לא משנה אף אות.", "analysis_port.write()"],
    vif_in: ["ה-interface של הכניסה : האותות, ולפעמים clocking block ו-assertions.", "לא class; מגיע לרכיבים כ-virtual interface.", "uvm_config_db::get ב-build_phase"],
    dut: ["הרכיב הנבדק.", "לא יודע שיש UVM.", "—"],
    vif_out: ["ה-interface של היציאה, שה-DUT מניע.", "אף driver לא מניע אותו בסביבת הבלוק.", "uvm_config_db::get"],
  };
  // the quiz: a question and the components that answer it
  const UV_QUIZ = [
    ["מי מתרגם טרנזקציה לשינויים באותות?", ["driver"]],
    ["מי בונה טרנזקציה מהאותות, בלי לשנות אותם?", ["monitor_in", "monitor_out"]],
    ["מי מחליט אם הפלט נכון?", ["scoreboard"]],
    ["מי בוחר בין כמה sequences שרוצים לשלוח בבת אחת?", ["sequencer"]],
    ["מי אומר מה לשלוח, עם randomize ו-constraints?", ["sequence"]],
    ["מי שם את ה-virtual interface ב-config_db וקורא ל-run_test?", ["top"]],
    ["מי מרים ומוריד objection ובוחר factory overrides?", ["test"]],
    ["מי עונה על השאלה ״מה כבר נבדק״?", ["coverage"]],
    ["איזה agent נשאר בלי driver גם בסביבת הבלוק?", ["agent_out"]],
    ["מי מחבר בין המוניטורים ל-scoreboard ב-connect_phase?", ["env"]],
  ];

  const uvCenter = (c) => { const [, x, y, w, h] = UV_LAYOUT[c]; return [x + w / 2, y + h / 2]; };
  const uvEdge = (c, to) => {
    const [, , , w, h] = UV_LAYOUT[c], [cx, cy] = uvCenter(c), dx = to[0] - cx, dy = to[1] - cy;
    const s = Math.min(dx ? w / 2 / Math.abs(dx) : Infinity, dy ? h / 2 / Math.abs(dy) : Infinity);
    return [cx + dx * s, cy + dy * s];
  };

  // The box (0049): the drawing with every component a button; a click shows its card; the
  // transaction stepped along the path (the arrow and the component lit, the text under
  // the drawing); a quiz mode asks "who does this?" and checks the component clicked.
  const uvmarchView = () => ({
    mount(box) {
      const st = { sel: "driver", k: 0, quiz: false, qi: 0, score: 0, tries: 0, said: "" };
      box.innerHTML =
        `<div class="ex-controls ex-play-row">` +
        `<button type="button" class="md-button ex-start">התחלה</button>` +
        `<button type="button" class="md-button ex-prev">השלב הקודם</button>` +
        `<button type="button" class="md-button ex-play">הפעלה</button>` + speedSel(2600, 1600, 900) +
        `<button type="button" class="md-button md-button--primary ex-next">השלב הבא</button>` +
        `<button type="button" class="md-button ex-end">עד הסוף</button><span class="ex-pos"></span></div>` +
        `<label class="uv-quizlab"><input type="checkbox" class="uv-quiz"> חידון : התיבה שואלת, ואני לוחץ על הרכיב</label>` +
        `<p class="ex-summary uv-stage" aria-live="polite"></p>` +
        `<div class="uv-draw"></div>` +
        `<div class="uv-card" data-steady></div>`;
      const $ = (sel) => box.querySelector(sel);
      let stop = () => {};
      const svg = () => {
        const stage = st.quiz ? null : UV_STAGES[st.k - 1] || null, edge = stage && stage[0], lit = stage && stage[1];
        let s = `<svg class="figure uv-live" viewBox="0 0 680 520" role="group" aria-label="סביבת UVM : לחיצה על רכיב מסבירה אותו">` +
          `<defs><marker id="uv-arrow-live" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>`;
        const box1 = (c, cont) => {
          const [label, x, y, w, h] = UV_LAYOUT[c], [cx, cy] = uvCenter(c);
          const cls = `uv-box${cont ? " is-cont" : ""} uv-${c}${st.sel === c && !st.quiz ? " is-sel" : ""}${lit === c ? " is-on" : ""}`;
          return `<g class="${cls}" data-c="${c}" tabindex="0" role="button" aria-label="${label}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${cont ? 8 : 6}"/>` +
            (cont ? `<text x="${x + 8}" y="${y + 17}">${label}</text>` : `<text x="${f(cx)}" y="${f(cy + 5)}" text-anchor="middle">${label}</text>`) + `</g>`;
        };
        Object.keys(UV_LAYOUT).forEach((c) => { if (UV_LAYOUT[c][5]) s += box1(c, true); });
        UV_ARROWS.forEach(([a, b, kind]) => {
          const [x1, y1] = uvEdge(a, uvCenter(b)), [x2, y2] = uvEdge(b, uvCenter(a));
          const on = edge && edge[0] === a && edge[1] === b;
          s += `<line class="uv-arrow uv-${kind}${on ? " is-on" : ""}" x1="${f(x1)}" y1="${f(y1)}" x2="${f(x2)}" y2="${f(y2)}" marker-end="url(#uv-arrow-live)"/>`;
        });
        Object.keys(UV_LAYOUT).forEach((c) => { if (!UV_LAYOUT[c][5]) s += box1(c, false); });
        return s + "</svg>";
      };
      const card = (c) => {
        const [what, not, calls] = UV_INFO[c];
        return `<p class="uv-ctitle">${code(UV_LAYOUT[c][0])}</p><p><b>תפקיד :</b> ${what}</p><p><b>לא עושה :</b> ${not}</p><p><b>קריאות חשובות :</b> <span dir="ltr">${calls}</span></p>`;
      };
      const draw = () => {
        const N = UV_STAGES.length;
        $(".ex-pos").textContent = `שלב ${st.k} מתוך ${N}`;
        $(".ex-prev").disabled = $(".ex-start").disabled = st.k === 0 || st.quiz;
        $(".ex-next").disabled = $(".ex-end").disabled = st.k === N || st.quiz;
        if (st.quiz) {
          const [q] = UV_QUIZ[st.qi];
          $(".uv-stage").innerHTML = `שאלה ${st.qi + 1} מתוך ${UV_QUIZ.length} : <b>${q}</b> לחצו על הרכיב. (נכון עד עכשיו : ${st.score} מתוך ${st.tries})`;
          $(".uv-card").innerHTML = st.said || `<p class="ex-note">הלחיצה על רכיב היא התשובה.</p>`;
        } else {
          $(".uv-stage").textContent = st.k ? UV_STAGES[st.k - 1][2] : "‏״השלב הבא״ מעביר טרנזקציה אחת לאורך המסלול. לחיצה על רכיב מסבירה אותו.";
          $(".uv-card").innerHTML = card(st.sel);
        }
        $(".uv-draw").innerHTML = svg();
      };
      const pick = (c) => {
        if (!st.quiz) { st.sel = c; draw(); return; }
        const [, ans] = UV_QUIZ[st.qi], ok = ans.includes(c);
        st.tries++; if (ok) st.score++;
        st.said = (ok ? `<p class="wv-ok">✓ נכון : ${code(UV_LAYOUT[c][0])}.</p>` : `<p class="wv-bad">✗ לא ${code(UV_LAYOUT[c][0])}. התשובה : ${ans.map((a) => code(UV_LAYOUT[a][0])).join(" או ")}.</p>`) + card(ans[0]);
        st.qi = (st.qi + 1) % UV_QUIZ.length;
        draw();
      };
      $(".uv-draw").addEventListener("click", (e) => { const g = e.target.closest("[data-c]"); if (g) pick(g.dataset.c); });
      $(".uv-draw").addEventListener("keydown", (e) => { const g = e.target.closest("[data-c]"); if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(g.dataset.c); } });
      $(".uv-quiz").addEventListener("change", () => { stop(); st.quiz = $(".uv-quiz").checked; st.qi = 0; st.score = 0; st.tries = 0; st.said = ""; draw(); });
      const go = (k) => { st.k = Math.max(0, Math.min(UV_STAGES.length, k)); if (st.k) st.sel = UV_STAGES[st.k - 1][1]; draw(); };
      $(".ex-start").addEventListener("click", () => { stop(); go(0); });
      $(".ex-prev").addEventListener("click", () => { stop(); go(st.k - 1); });
      $(".ex-next").addEventListener("click", () => go(st.k + 1));
      $(".ex-end").addEventListener("click", () => { stop(); go(UV_STAGES.length); });
      stop = autoplay($(".ex-play"), $(".ex-speed"), { step: () => go(st.k + 1), done: () => st.k >= UV_STAGES.length || st.quiz, restart: () => go(0) });
      draw();
    },
  });

  dvqExplorers.register({
    views: { uvmarch: uvmarchView },
    help: {
      uvmarch: "לחיצה על רכיב בסכימה מראה מה הוא עושה, מה הוא לא עושה ואת הקריאות החשובות שלו. ״השלב הבא״ מעביר טרנזקציה אחת מה-sequence עד ה-scoreboard, עם החץ והרכיב של כל שלב. במצב ״חידון״ התיבה שואלת ״מי עושה את זה?״, ולוחצים על הרכיב.",
    },
    models: { UV_LAYOUT, UV_ARROWS, UV_PATH, UV_INFO, UV_QUIZ, UV_STAGES },
  });
})();
