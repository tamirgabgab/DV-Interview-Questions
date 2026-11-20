// kinds: factory
//   factory                0112        the UVM factory during the build: the component tree of the page's testbench built top-down one component at a time; create or new on each line that builds, a type or an instance override of ParityDriver by ErrDriver with its path, and when the test sets it; per step the class built, the factory's table, the override that matched and why a path did not, and the log at the end
// Loaded after core.js on the pages that have this kind (hooks/questions.py adds the
// script tags); under Node tools/explorer_node.js loads every kind file and merges the
// models for the question tests.
(() => {
  const { code, ltr } = dvqExplorers.lib;
  const NB = " ";

  // tools/figures/q0112.py, line for line: the tree in pyuvm's build order (the full name,
  // the class asked for, the line that builds it), the times the test can set the override,
  // why(), factory_build() and the report lines.
  const TOP = "uvm_test_top";
  const FO = {
    TOP,
    ITEMS: 8,
    TREE: [
      [`${TOP}.env`, "Env", "env"],
      [`${TOP}.env.agt0`, "Agent", "agt0"],
      [`${TOP}.env.agt1`, "Agent", "agt1"],
      [`${TOP}.env.agt0.seqr`, "uvm_sequencer", "seqr"],
      [`${TOP}.env.agt0.drv`, "ParityDriver", "drv"],
      [`${TOP}.env.agt1.seqr`, "uvm_sequencer", "seqr"],
      [`${TOP}.env.agt1.drv`, "ParityDriver", "drv"],
    ],
    LINES: ["env", "agt0", "agt1", "seqr", "drv"],
    TIMES: ["build", "build_after", "connect", "before_run"],
    DRIVERS: [`${TOP}.env.agt0.drv`, `${TOP}.env.agt1.drv`],
  };
  const NAMES = [TOP, ...FO.TREE.map(([full]) => full)];
  const REQUESTED = Object.fromEntries([[TOP, "ErrTest"], ...FO.TREE.map(([full, req]) => [full, req])]);

  // fnmatch of a pattern of letters, digits, _ . * and ? (the box takes no other): * any
  // run, dots included, ? one character, against the whole name
  const foGlob = (p) => new RegExp(`^${p.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\?/g, ".")}$`, "s");
  const foMatch = (name, p) => foGlob(p).test(name);
  const foWhy = (full, p) => {
    if (foMatch(full, p)) return ["match", full];
    const parts = full.split(".");
    for (let k = 1; k < parts.length; k++) if (foMatch(parts.slice(k).join("."), p)) return ["suffix", parts.slice(0, k).join(".")];
    for (let k = parts.length - 1; k > 0; k--) if (foMatch(parts.slice(0, k).join("."), p)) return ["ancestor", parts.slice(0, k).join(".")];
    const others = NAMES.filter((n) => n !== full);
    const same = others.filter((n) => REQUESTED[n] === REQUESTED[full]), rest = others.filter((n) => REQUESTED[n] !== REQUESTED[full]);
    const hit = [...same, ...rest].find((n) => foMatch(n, p));
    return hit ? ["other", hit] : ["none", ""];
  };
  const foBuild = (how, mode, path = "", when = "build") => FO.TREE.map(([full, req, line], i) => {
    const on = mode !== "none" && (when === "build" || (when === "build_after" && i >= 1));
    let cls = req, via = null;
    const checks = [];
    if (how[line] === "create" && on && req === "ParityDriver") {
      if (mode === "inst") {
        checks.push(foWhy(full, path));
        if (checks[0][0] === "match") { cls = "ErrDriver"; via = "inst"; }
      } else if (mode === "type") { cls = "ErrDriver"; via = "type"; }
    }
    return { full, req, line, how: how[line], on, cls, via, checks };
  });
  const foWrong = (cls) => (cls === "ErrDriver" ? [...Array(FO.ITEMS).keys()].filter((s) => s % 4 === 3).length : 0);
  const foLog = (steps) => FO.DRIVERS.map((d) => { const c = steps.find((s) => s.full === d).cls; return `${d}: ${c}, ${foWrong(c)} parity errors`; });

  // --- the box ---------------------------------------------------------------------------

  const WHEN = {
    build: "ב-build_phase, לפני Env.create",
    build_after: "ב-build_phase, אחרי Env.create",
    connect: "ב-connect_phase",
    before_run: "לפני run_test",
  };
  const PARENT = { env: "uvm_test_top", agt0: "env", agt1: "env" };
  const short = (full) => full.slice(TOP.length + 1);
  const mono = (t) => `<span class="fo-mono" dir="ltr">${t}</span>`;
  const call = (s) => {
    const name = s.full.split(".").pop(), self = "self";
    return s.how === "create" ? `${s.req}.create("${name}", ${self})` : `${s.req}("${name}", ${self})`;
  };
  // the tree: containers for the test, env and the agents, a box for each sequencer and driver
  const GEOM = {
    [`${TOP}.env`]: [12, 30, 336, 226],
    [`${TOP}.env.agt0`]: [20, 58, 156, 190],
    [`${TOP}.env.agt1`]: [184, 58, 156, 190],
    [`${TOP}.env.agt0.seqr`]: [28, 86, 140, 62],
    [`${TOP}.env.agt0.drv`]: [28, 162, 140, 74],
    [`${TOP}.env.agt1.seqr`]: [192, 86, 140, 62],
    [`${TOP}.env.agt1.drv`]: [192, 162, 140, 74],
  };
  const CONT = new Set([`${TOP}.env`, `${TOP}.env.agt0`, `${TOP}.env.agt1`]);

  const factoryView = () => ({
    mount(box) {
      const st = { how: { env: "create", agt0: "create", agt1: "create", seqr: "create", drv: "create" }, mode: "inst", path: "env.agt1.drv", when: "build", k: 8 };
      const N = FO.TREE.length + 2;                       // 0: run_test, 1..7 the creations, 8: connect and the log
      box.innerHTML =
        `<div class="ex-controls fo-lines">` +
        FO.LINES.map((l) => `<label><code>${l}</code> <select class="fo-how" data-line="${l}" aria-label="השורה שבונה את ${l}${l === "seqr" || l === "drv" ? " בשני ה-agents" : ""}"><option value="create">create</option><option value="new">new</option></select></label>`).join("") +
        `</div>` +
        `<div class="ex-controls fo-ovr">` +
        `<label>ה-override <select class="fo-mode"><option value="type">type override</option><option value="inst" selected>instance override</option></select></label>` +
        `<label>הנתיב <input type="text" class="fo-path" dir="ltr" maxlength="60" spellcheck="false" autocomplete="off" value="${st.path}" aria-label="הנתיב של ה-instance override, תבנית glob עם * ו-?"></label>` +
        `<label>מתי <select class="fo-when">${FO.TIMES.map((w) => `<option value="${w}">${WHEN[w]}</option>`).join("")}</select></label>` +
        `<span class="fo-bad" aria-live="polite"></span></div>` +
        `<div class="ex-controls">` +
        `<button type="button" class="md-button ex-start">ההתחלה</button>` +
        `<button type="button" class="md-button ex-prev">הצעד הקודם</button>` +
        `<button type="button" class="md-button md-button--primary ex-next">הצעד הבא</button>` +
        `<button type="button" class="md-button ex-end">הסוף</button>` +
        `<span class="ex-pos fo-pos"></span></div>` +
        `<p class="ex-summary fo-sum" aria-live="polite"></p>` +
        `<div class="fo-fig"></div>` +
        `<span class="viz-legend fo-legend"><span><i class="fo-key-err"></i>נבנה <code>ErrDriver</code></span><span><i class="fo-key-new"></i>נבנה ב-<code>new</code></span><span><i class="fo-key-now"></i>הרכיב של הצעד</span><span><i class="fo-key-todo"></i>עוד לא נבנה</span></span>` +
        `<p class="fo-now" aria-live="polite"></p>` +
        `<section class="fo-card"><p class="fo-ctitle">הטבלה של ה-factory</p><p class="fo-table"></p>` +
        `<p class="fo-ctitle">מה ה-factory בדק</p><div class="fo-checks"></div>` +
        `<p class="fo-ctitle">הלוג של report_phase</p><pre class="fo-log" dir="ltr" tabindex="0" role="region" aria-label="שורות הלוג בסוף הריצה"></pre></section>`;
      const $ = (sel) => box.querySelector(sel);
      let steps = null;
      const compute = () => { steps = foBuild(st.how, st.mode, st.path, st.when); };
      const ovrText = () => `${st.mode === "type" ? "type" : "instance"} override${NB}: ${code("ErrDriver")} במקום ${code("ParityDriver")}${st.mode === "inst" ? `, בנתיב ${mono(st.path)}` : ""}.`;
      // the factory's table at step k: set before the first creation (build), after it
      // (build_after), at the end (connect); cleared by run_test (before_run)
      const inTable = (k) => (st.when === "build" || st.when === "build_after" ? k >= 1 : st.when === "connect" ? k === N - 1 : false);
      const verdict = () => {
        const d = FO.DRIVERS.map((full) => steps.find((s) => s.full === full));
        const part = (s) => `${code(short(s.full))} ${code(s.cls)} (${ltr(foWrong(s.cls))} שגיאות)`;
        let out = `בסוף${NB}: ${part(d[0])}, ${part(d[1])}.`;
        if (d.every((s) => s.cls !== "ErrDriver")) {
          if (st.how.drv === "new") out += ` השורה של ה-driver ב-${code("new")}, וה-factory לא נשאל.`;
          else if (st.when === "connect") out += " ה-override נקבע אחרי שה-drivers נבנו.";
          else if (st.when === "before_run") out += ` ${code("run_test")} מחק את ה-override.`;
          else out += " התבנית לא התאימה לאף driver.";
        }
        return out;
      };
      const reason = (s, [what, name]) => {
        if (what === "match") return `<span class="wv-ok">✓ מתאימה</span>, ונבנה ${code("ErrDriver")}.`;
        let r = "";
        if (what === "suffix") r = `התבנית מתאימה רק לסוף השם. חסר לה בהתחלה ${mono(name)} והנקודה שאחריו`;
        else if (what === "ancestor") r = `התבנית היא השם של ${mono(name)}, רכיב מעל ה-driver, שנבנה כ-${code(REQUESTED[name])}`;
        else if (what === "other") r = `התבנית מתאימה ל-${mono(name)}, ולא לרכיב הזה`;
        else r = "התבנית לא מתאימה לאף שם בעץ";
        return `<span class="wv-bad">✗ ${r}.</span> אין type override, ונבנה ${code(s.req)}.`;
      };
      const checks = (k) => {
        if (k === 0) return st.when === "before_run" ? `${code("run_test")} מנקה את הטבלה, וה-override שנקבע לפניו נמחק.` : "עוד לא נבנה אף רכיב מתחת לטסט.";
        if (k === N - 1) return st.when === "connect" ? "ה-override נכנס לטבלה, אבל אף אחד לא שואל אותה יותר." : "כל הרכיבים נבנו.";
        const s = steps[k - 1];
        if (s.how === "new") return `קריאה ישירה לבנאי${NB}: ה-factory לא נשאל, ונבנה ${code(s.req)}.`;
        if (s.req !== "ParityDriver") return `${code("create")} מבקש ${code(s.req)}. אין לו override, ונבנה ${code(s.req)}.`;
        if (!s.on) return `${code("create")} מבקש ${code("ParityDriver")}, והטבלה ריקה. נבנה ${code("ParityDriver")}.`;
        if (st.mode === "type") return `${code("create")} מבקש ${code("ParityDriver")}. ה-type override מחליף אותו בכל מקום, ונבנה ${code("ErrDriver")}.`;
        return `${code("create")} מבקש ${code("ParityDriver")} בשם המלא ${mono(s.full)}, מול התבנית ${mono(st.path)}${NB}: ${reason(s, s.checks[0])}`;
      };
      const describe = (k) => {
        if (k === 0) return `צעד 0${NB}: ${code("run_test")} בונה את הטסט בשם ${code(TOP)}.`;
        if (k === N - 1) return `צעד ${ltr(k)}${NB}: ${code("connect_phase")}, והעץ שלם.${st.when === "connect" ? " עכשיו הטסט קובע את ה-override." : ""}`;
        const s = steps[k - 1], name = s.full.split(".").pop();
        const parent = PARENT[s.line] || s.full.split(".").slice(-2, -1)[0];
        let out = `צעד ${ltr(k)}${NB}: ה-${code("build_phase")} של ${code(parent)} בונה את ${code(name)} ב-${mono(call(s))}.`;
        if (k === 1 && st.when === "build") out = `צעד 1${NB}: הטסט קובע את ה-override, ואז בונה את ${code("env")} ב-${mono(call(s))}.`;
        if (k === 1 && st.when === "build_after") out += " אחריו הטסט קובע את ה-override.";
        return out;
      };
      const node = (full, k) => {
        const i = FO.TREE.findIndex(([f]) => f === full), s = steps[i];
        const [x, y, w, h] = GEOM[full], name = full.split(".").pop();
        const built = i < k, now = i === k - 1;
        const cls = ["fo-node", CONT.has(full) ? "is-cont" : "is-leaf", built ? "" : "is-todo", now ? "is-now" : "",
                     built && s.how === "new" ? "is-new" : "", built && s.cls === "ErrDriver" ? "is-err" : ""].filter(Boolean).join(" ");
        const label = built ? s.cls : "—";
        if (CONT.has(full)) {
          return `<g class="${cls}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8"/>` +
            `<text class="fo-name" x="${x + 8}" y="${y + 17}">${name}</text>` +
            `<text class="fo-cls" x="${x + w - 8}" y="${y + 17}" text-anchor="end">${label}${built && s.how === "new" ? " (new)" : ""}</text></g>`;
        }
        return `<g class="${cls}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6"/>` +
          `<text class="fo-name" x="${x + w / 2}" y="${y + h / 2 - 6}" text-anchor="middle">${name}${built && s.how === "new" ? " (new)" : ""}</text>` +
          `<text class="fo-cls" x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle">${label}</text></g>`;
      };
      const figure = (k) => {
        const testCls = ["fo-node", "is-cont", k === 0 ? "is-now" : ""].filter(Boolean).join(" ");
        const built = FO.TREE.slice(0, Math.max(0, k)).map(([f]) => short(f));
        return `<svg class="figure fo-tree" viewBox="0 0 360 264" role="img" aria-label="עץ הרכיבים אחרי צעד ${k}${NB}: ${built.length ? `נבנו ${built.join(", ")}` : "רק הטסט"}">` +
          `<g class="${testCls}"><rect x="4" y="4" width="352" height="256" rx="8"/><text class="fo-name" x="12" y="21">${TOP}</text></g>` +
          FO.TREE.map(([full]) => node(full, k)).join("") + "</svg>";
      };
      const draw = () => {
        const k = st.k;
        $(".fo-pos").textContent = `צעד ${k} מתוך ${N - 1}`;
        $(".ex-start").disabled = $(".ex-prev").disabled = k === 0;
        $(".ex-next").disabled = $(".ex-end").disabled = k === N - 1;
        $(".fo-sum").innerHTML = verdict();
        $(".fo-fig").innerHTML = figure(k);
        $(".fo-now").innerHTML = describe(k);
        let table = inTable(k) ? ovrText() : "ריקה.";
        if (!inTable(k) && st.when === "connect") table = `ריקה. ה-override ייקבע רק ב-${code("connect_phase")}.`;
        if (!inTable(k) && st.when === "before_run") table = `ריקה. ${code("run_test")} מחק את ה-override.`;
        $(".fo-table").innerHTML = table;
        $(".fo-checks").innerHTML = `<p>${checks(k)}</p>`;
        $(".fo-log").textContent = k === N - 1 ? foLog(steps).join("\n") : "—\n";
        $(".fo-path").disabled = st.mode !== "inst";
      };
      const reload = () => { compute(); draw(); };
      box.querySelectorAll(".fo-how").forEach((el) => el.addEventListener("change", () => { st.how[el.dataset.line] = el.value; reload(); }));
      $(".fo-mode").addEventListener("change", (e) => { st.mode = e.target.value; reload(); });
      $(".fo-when").addEventListener("change", (e) => { st.when = e.target.value; reload(); });
      const pathIn = $(".fo-path");
      pathIn.addEventListener("change", () => {
        const v = pathIn.value.trim();
        if (/^[\w.*?]{1,60}$/.test(v)) { st.path = v; $(".fo-bad").textContent = ""; reload(); }
        else { $(".fo-bad").textContent = "בתבנית רק אותיות, ספרות, _ . * ?"; pathIn.value = st.path; }
      });
      const go = (k) => { st.k = Math.max(0, Math.min(N - 1, k)); draw(); };
      $(".ex-start").addEventListener("click", () => go(0));
      $(".ex-prev").addEventListener("click", () => go(st.k - 1));
      $(".ex-next").addEventListener("click", () => go(st.k + 1));
      $(".ex-end").addEventListener("click", () => go(N - 1));
      box.dvqExtra = {
        get: () => (st.k === N - 1 ? "" : String(st.k)),
        set: (text) => { const v = Number(text); if (!/^\d+$/.test(text) || v > N - 1) return false; go(v); return true; },
      };
      reload();
    },
  });

  dvqExplorers.register({
    views: { factory: factoryView },
    help: {
      factory: "התיבה בונה את העץ של הסביבה כמו pyuvm, מלמעלה למטה : הטסט בונה את env, ה-env את שני ה-agents, וכל agent את ה-sequencer וה-driver שלו. בשורה העליונה בוחרים איך כל שורה בונה, create או new (השורות seqr ו-drv משותפות לשני ה-agents, כי הם מריצים אותו build_phase). אחר כך בוחרים override של ParityDriver ב-ErrDriver, type או instance עם נתיב (glob עם * ו-?), ומתי הטסט קובע אותו. כל צעד בונה רכיב אחד, והכרטיס אומר מה ה-factory בדק, ולמה נתיב לא התאים. בצעד האחרון מופיע הלוג.",
    },
    models: { FO, foGlob, foMatch, foWhy, foBuild, foLog },
    cols: { factory: { side: ".fo-now, .fo-card" } },
  });
})();
