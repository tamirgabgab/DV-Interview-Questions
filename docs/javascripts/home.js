// Home page touches: the hero's numbers count up from zero the first time they come into
// view (W339), and the sections and cards under the hero rise into view once (W344, a 40 ms
// stagger along a row of cards). The real numbers and the content are in the page; without
// the script, under reduced motion or in an automated browser (the page checks), nothing
// moves or hides. The hero's waves stop while it is off screen, and beside its text sits
// the interview builder (session 30; it replaced round M's live example of 0055).
(() => {
  const COUNT_MS = 900;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const countUp = (el) => {
    const target = Number(el.textContent);
    if (!Number.isFinite(target) || target <= 0) return;
    const start = performance.now();
    const frame = (now) => {
      const t = Math.min(1, (now - start) / COUNT_MS);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3))));   // ease-out
      if (t < 1) requestAnimationFrame(frame);
    };
    el.textContent = "0";
    requestAnimationFrame(frame);
  };

  const STAGGER_MS = 40;
  const reveal = (content) => {
    const items = [];
    content.querySelectorAll(":scope > :is(h2, p, .related-questions, .catalog-link, details)").forEach((el) => items.push([el, 0]));
    content.querySelectorAll(":scope > :is(.level-cards, .how-it-works)").forEach((row) =>
      Array.from(row.children).forEach((el, i) => items.push([el, i % 3])));     // a row has three
    const seen = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-in");
        seen.unobserve(e.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    items.forEach(([el, k]) => {
      el.classList.add("w-reveal");
      if (k) el.style.setProperty("--w-delay", `${k * STAGGER_MS}ms`);
      seen.observe(el);
    });
  };

  // The interview builder in the hero (session 30, in place of M2's live example): a
  // level, a length and kinds give a series of questions that fits the time
  // (dvqInterview.buildPlan over questions.json, the ones not solved yet first); "another
  // series" draws again; "start" keeps the series in the browser and opens its first
  // question, where interview mode starts by itself (question-tools.js). The last choice
  // is remembered.
  const PICK = "dvq-builder";
  const builder = (panel) => {
    const I = window.dvqInterview;
    if (!panel || !I) return;
    const plan = panel.querySelector(".hb-plan"), sum = panel.querySelector(".hb-sum"), go = panel.querySelector(".hb-start");
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(PICK) || "null"); } catch (e) { /* none */ }
    const st = { level: "junior", minutes: 40, kinds: [...panel.querySelectorAll(".hb-topic")].map((b) => b.dataset.kind), seed: 1, ...(saved || {}) };
    let data = null, current = [];
    const paint = () => {
      panel.querySelectorAll("[data-level]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.level === st.level)));
      panel.querySelectorAll("[data-minutes]").forEach((b) => b.setAttribute("aria-pressed", String(Number(b.dataset.minutes) === st.minutes)));
      panel.querySelectorAll(".hb-topic").forEach((b) => b.setAttribute("aria-pressed", String(st.kinds.includes(b.dataset.kind))));
    };
    const fill = () => {
      paint();
      try { localStorage.setItem(PICK, JSON.stringify({ level: st.level, minutes: st.minutes, kinds: st.kinds })); } catch (e) { /* none */ }
      if (!data) return;
      const solved = data.qs.filter((q) => window.dvqMarks && window.dvqMarks.has(q[I.ID], "solved")).map((q) => q[I.ID]);
      const res = I.buildPlan(data.qs, { level: st.level, minutes: st.minutes, kinds: st.kinds, solved, seed: st.seed });
      current = res.plan;
      plan.classList.remove("is-new");
      void plan.offsetWidth;
      if (!reduce) plan.classList.add("is-new");
      plan.innerHTML = current.length
        ? current.map((q) => `<li><span class="hb-id">${q[I.ID]}</span><a href="${I.siteUrl(q[I.URL])}">${q[I.TITLE].replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]))}</a>` +
          `<span class="hb-min">${I.targetMinutes(q[I.DIFF], q[I.PARTS])} דק'</span></li>`).join("")
        : '<li class="hb-empty">אין שאלות ברמה ובנושאים האלה. בחרו עוד נושא.</li>';
      const n = current.length;
      sum.textContent = n ? `${n === 1 ? "שאלה אחת" : `${n} שאלות`}, כ-${res.minutes} דקות. השעון בכל שאלה רץ מול הזמן שלה.` : "";
      go.hidden = !n;
      if (n) go.href = I.siteUrl(current[0][I.URL]);
    };
    panel.addEventListener("click", (e) => {
      const b = e.target.closest("button");
      if (!b) return;
      if (b.dataset.level) st.level = b.dataset.level;
      else if (b.dataset.minutes) st.minutes = Number(b.dataset.minutes);
      else if (b.dataset.kind) {
        const on = st.kinds.includes(b.dataset.kind);
        st.kinds = on ? st.kinds.filter((k) => k !== b.dataset.kind) : [...st.kinds, b.dataset.kind];
      } else if (b.classList.contains("hb-shuffle")) st.seed = (st.seed % 100000) + 1 + Math.floor(Math.random() * 1000);
      else return;
      fill();
    });
    go.addEventListener("click", () => {
      if (!current.length) return;
      I.plan.set({ ids: current.map((q) => q[I.ID]), urls: current.map((q) => I.siteUrl(q[I.URL])), minutes: current.reduce((m, q) => m + I.targetMinutes(q[I.DIFF], q[I.PARTS]), 0), at: Date.now() });
    });
    document.addEventListener("dvq-marks", fill);
    I.loadIndex().then((d) => { data = d; panel.hidden = false; fill(); }).catch(() => { /* no list: the builder stays hidden */ });
  };

  document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".home-hero");
    if (!hero || !("IntersectionObserver" in window)) return;
    builder(hero.querySelector(".hh-builder"));
    // the hero's rolling waves run only while it is on screen
    new IntersectionObserver((entries) => {
      hero.classList.toggle("is-paused", !entries.some((e) => e.isIntersecting));
    }).observe(hero);
  });

  document.addEventListener("DOMContentLoaded", () => {
    const stats = document.querySelector(".home-hero .hh-stats");
    if (!stats || reduce || navigator.webdriver || !("IntersectionObserver" in window)) return;
    const content = stats.closest(".md-content__inner");
    if (content) reveal(content);
    const seen = new IntersectionObserver((entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      seen.disconnect();
      stats.querySelectorAll("b").forEach(countUp);
    });
    seen.observe(stats);
  });
})();
