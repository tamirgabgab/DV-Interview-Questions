// Home page touches: the hero's numbers count up from zero the first time they come into
// view (W339), and the sections and cards under the hero rise into view once (W344, a 40 ms
// stagger along a row of cards). The real numbers and the content are in the page; without
// the script, under reduced motion or in an automated browser (the page checks), nothing
// moves or hides. Beside the hero's text sits the interview builder (session 30; it
// replaced round M's live example of 0055), whose series is dealt as a fan of small cards
// (session 31); hero-board.js draws the hero's background. The hero's motto corrects
// itself once a visit: "לשנן" struck through, "להבין" written above it and set in its
// place (session 31, after Hallmark's headline); the page itself holds only "להבין".
(() => {
  const COUNT_MS = 900;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const still = reduce || navigator.webdriver;
  const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

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

  const STAGGER_MS = 60;
  // the sections and the cards rise into view once a visit (session 33), not on every load
  const firstVisit = (key) => {
    try { if (sessionStorage.getItem(key)) return false; sessionStorage.setItem(key, "1"); return true; } catch (e) { return false; }
  };
  const reveal = (content, cardsOnly = false) => {
    const items = [];
    if (!cardsOnly) content.querySelectorAll(":scope > :is(h2, p, .related-questions, .catalog-link, details)").forEach((el) => items.push([el, 0]));
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
  //
  // The series is a fan of small cards (the first on the right): each holds the id, the
  // difficulty and the minutes, and the title of the card under the pointer or the focus
  // shows in the line under the fan (the first card's title otherwise). A new series
  // gathers the cards into a pile and deals the new ones; nothing moves under reduced
  // motion or in an automated browser.
  const PICK = "dvq-builder";
  const builder = (panel) => {
    const I = window.dvqInterview;
    if (!panel || !I) return;
    const plan = panel.querySelector(".hb-plan"), sum = panel.querySelector(".hb-sum"), go = panel.querySelector(".hb-start");
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(PICK) || "null"); } catch (e) { /* none */ }
    const st = { level: "junior", minutes: 40, kinds: [...panel.querySelectorAll(".hb-topic")].map((b) => b.dataset.kind), seed: 1, ...(saved || {}) };
    let data = null, current = [], turn = 0, dealt = false;
    const peek = panel.querySelector(".hb-peek");
    const cards = () => [...plan.querySelectorAll(".hb-card")];
    // each card's place along a shallow arc, the first on the right
    const place = () => {
      const all = cards(), n = all.length;
      if (!n) return;
      const W = plan.clientWidth, cw = all[0].parentElement.offsetWidth, mid = (n - 1) / 2;
      const step = n > 1 ? Math.min(cw * 0.92, (W - cw) / (n - 1)) : 0;
      all.forEach((a, k) => {
        const u = mid - k;
        a.parentElement.style.transform = `translate(${((W - cw) / 2 + u * step).toFixed(1)}px, ${(u * u * 3).toFixed(1)}px) rotate(${(u * 4).toFixed(1)}deg)`;
        a.parentElement.style.zIndex = String(k + 1);
      });
    };
    const pile = () => {
      const li = plan.querySelector("li");
      return `translate(${((plan.clientWidth - (li ? li.offsetWidth : 0)) / 2).toFixed(1)}px, 1.6rem) rotate(0deg) scale(0.9)`;
    };
    const show = (a) => {
      cards().forEach((c) => c.classList.toggle("is-peek", c === a));
      const first = a || cards()[0];
      if (peek) peek.innerHTML = first ? `<b>${first.querySelector(".hb-id").textContent}</b> ${first.dataset.title}` : "";
    };
    // gather the old cards into the pile, put the new ones in and deal them
    const deal = (html) => {
      const mine = ++turn;
      const calm = still || !dealt;                      // the first series is laid down, not dealt
      if (html.includes("hb-card")) dealt = true;
      const lis = [...plan.querySelectorAll("li")].filter((li) => li.querySelector(".hb-card"));
      const gather = calm || !lis.length ? Promise.resolve() : Promise.all(lis.map((li, k) =>
        li.animate([{ transform: li.style.transform, opacity: 1 }, { transform: pile(), opacity: 0 }],
          { duration: 200, delay: (lis.length - 1 - k) * 35, easing: "cubic-bezier(.4, 0, 1, 1)", fill: "forwards" }).finished)).catch(() => {});
      gather.then(() => {
        if (mine !== turn) return;
        plan.innerHTML = html;
        place();
        show(null);
        if (calm) return;
        const from = pile();
        plan.querySelectorAll("li").forEach((li, k) => {
          if (!li.querySelector(".hb-card")) return;
          li.animate([{ transform: from, opacity: 0 }, { transform: li.style.transform, opacity: 1 }],
            { duration: 420, delay: k * 80, easing: "cubic-bezier(.2, .8, .2, 1)", fill: "backwards" });
        });
      });
    };
    plan.addEventListener("pointerover", (e) => { const a = e.target.closest(".hb-card"); if (a) show(a); });
    plan.addEventListener("pointerleave", () => { if (!plan.contains(document.activeElement)) show(null); });
    plan.addEventListener("focusin", (e) => { const a = e.target.closest(".hb-card"); if (a) show(a); });
    plan.addEventListener("focusout", (e) => { if (!plan.contains(e.relatedTarget)) show(null); });
    if ("ResizeObserver" in window) new ResizeObserver(place).observe(plan);
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
      const n = current.length;
      sum.textContent = n ? `${n === 1 ? "שאלה אחת" : `${n} שאלות`}, כ-${res.minutes} דקות. השעון בכל שאלה רץ מול הזמן שלה.` : "";
      const html = n
        ? current.map((q) => {
          const d = q[I.DIFF], m = I.targetMinutes(d, q[I.PARTS]), t = esc(q[I.TITLE]);
          // the link's name is its text: the id, the title (for screen readers only), the difficulty, the minutes
          return `<li><a class="hb-card" href="${I.siteUrl(q[I.URL])}" data-title="${t}">` +
            `<span class="hb-id">${q[I.ID]}</span><span class="hb-sr"> ${t}, </span><span class="hb-diff hb-${d}">${esc(data.diffs[d])}</span><span class="hb-min">${m} דק'</span></a></li>`;
        }).join("")
        : '<li class="hb-empty">אין שאלות ברמה ובנושאים האלה. בחרו עוד נושא.</li>';
      deal(html);
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
  });

  // The motto's correction (once a browser session): the old word is put in by this script
  // only, so the page, its search index and a reader without the script see "להבין".
  const MOTTO = "dvq-motto";
  const motto = (fix) => {
    let seen = false;
    try { seen = sessionStorage.getItem(MOTTO) === "1"; sessionStorage.setItem(MOTTO, "1"); } catch (e) { /* none */ }
    if (seen || still || !fix.animate) return;
    const word = fix.textContent;
    fix.innerHTML = `<span class="hh-new">${esc(word)}</span><span class="hh-old" aria-hidden="true">לשנן</span>` +
      '<svg class="hh-slash" viewBox="0 0 20 40" preserveAspectRatio="none" aria-hidden="true" focusable="false"><line x1="19" y1="8" x2="1" y2="32" pathLength="1"/></svg>';
    fix.classList.add("is-live");
    const [nw, old, slash] = [fix.querySelector(".hh-new"), fix.querySelector(".hh-old"), fix.querySelector(".hh-slash")];
    const line = slash.querySelector("line");
    // one animation per element, as a timeline of [ms, keyframe], after a short pause (the
    // first keyframe holds through it)
    const track = (el, frames) => {
      const end = frames[frames.length - 1][0];
      return el.animate(frames.map(([t, k]) => ({ offset: t / end, ...k })), { duration: end, delay: 450, fill: "both" });
    };
    const UP = "translateY(-0.95em) scale(0.5)";
    const run = [
      track(old, [[0, { opacity: 1, transform: "none" }], [1150, { opacity: 1, transform: "none" }], [1550, { opacity: 0, transform: "translateY(0.4em) rotate(9deg)" }], [2300, { opacity: 0, transform: "translateY(0.4em) rotate(9deg)" }]]),
      track(slash, [[0, { opacity: 0 }], [260, { opacity: 0 }], [300, { opacity: 1 }], [1150, { opacity: 1 }], [1450, { opacity: 0 }], [2300, { opacity: 0 }]]),
      track(line, [[0, { strokeDashoffset: 1 }], [300, { strokeDashoffset: 1 }], [560, { strokeDashoffset: 0 }], [2300, { strokeDashoffset: 0 }]]),
      track(nw, [[0, { opacity: 0, transform: UP, color: "#ffffff" }], [620, { opacity: 0, transform: UP, color: "#ffffff" }], [820, { opacity: 1, transform: UP, color: "#ffffff" }],
        [1150, { opacity: 1, transform: UP, color: "#ffffff" }], [1650, { opacity: 1, transform: "none", color: "#ffffff" }], [1800, { opacity: 1, transform: "none", color: "#ffffff" }],
        [2300, { opacity: 1, transform: "none", color: getComputedStyle(fix).color }]]),
    ];
    // the plain word again once the edit is done
    Promise.all(run.map((an) => an.finished)).then(() => { fix.classList.remove("is-live"); fix.textContent = word; }).catch(() => {});
  };

  // the path cards of the paths page come in the same way, once a visit
  document.addEventListener("DOMContentLoaded", () => {
    const content = document.querySelector(".md-content__inner");
    if (!content || reduce || navigator.webdriver || !("IntersectionObserver" in window)) return;
    if (content.querySelector(".home-hero") || !content.querySelector(":scope > .level-cards")) return;
    if (firstVisit("dvq-revealed:" + location.pathname)) reveal(content, true);
  });

  document.addEventListener("DOMContentLoaded", () => {
    const fix = document.querySelector(".home-hero .hh-fix");
    if (fix) motto(fix);                       // the old word at once; the edit starts a moment later
  });

  document.addEventListener("DOMContentLoaded", () => {
    const stats = document.querySelector(".home-hero .hh-stats");
    if (!stats || reduce || navigator.webdriver || !("IntersectionObserver" in window)) return;
    const content = stats.closest(".md-content__inner");
    if (content && firstVisit("dvq-revealed:" + location.pathname)) reveal(content);
    const seen = new IntersectionObserver((entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      seen.disconnect();
      stats.querySelectorAll("b").forEach(countUp);
    });
    seen.observe(stats);
  });
})();
