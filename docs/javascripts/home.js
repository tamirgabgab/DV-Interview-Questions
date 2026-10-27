// Home page touches: the hero's numbers count up from zero the first time they come into
// view (W339), and the sections and cards under the hero rise into view once (W344, a 40 ms
// stagger along a row of cards). The real numbers and the content are in the page; without
// the script, under reduced motion or in an automated browser (the page checks), nothing
// moves or hides.
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
