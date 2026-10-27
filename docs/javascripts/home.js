// Home page touches (W339): the hero's numbers count up from zero the first time they come
// into view. The real numbers are in the page; without the script, or under reduced
// motion, they simply stay as they are.
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

  document.addEventListener("DOMContentLoaded", () => {
    const stats = document.querySelector(".home-hero .hh-stats");
    if (!stats || reduce || !("IntersectionObserver" in window)) return;
    const seen = new IntersectionObserver((entries) => {
      if (!entries.some((e) => e.isIntersecting)) return;
      seen.disconnect();
      stats.querySelectorAll("b").forEach(countUp);
    });
    seen.observe(stats);
  });
})();
