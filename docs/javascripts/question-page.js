// The question page (18-question.css): the part timeline that fills while reading, the code window.
// The timeline (V12): the hook (qp_parts) wraps the parts of a page with two or more in
// div.qp-parts and gives each heading its letter, so the circles and the line are already
// drawn; this file fills the line in amber down to the reading line (two fifths down the
// window, never above the part bar's own line), lights the circle of every part passed,
// and puts a check in the circle of a part solved: every part once the question is marked solved
// (marks.js keeps only whole-question marks), or a part whose self-checks were all answered
// right (selfcheck.js). One passive scroll listener, at most one update a frame; nothing
// here changes the layout. The circles change colour with a short transition only without
// reduced motion and outside an automated browser (the page checks see a still page).
// The code window is CSS only.
(() => {
  const quiet = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;
  const readY = () => Math.max(140, window.innerHeight * 0.4);   // 140: the part bar's line (reading-tools.js)

  const timeline = (wrap) => {
    const parts = Array.from(wrap.querySelectorAll(":scope > h3.qp-part"));
    if (parts.length < 2) return;
    // the elements of each part: its heading's siblings up to the next part
    const groups = parts.map((h) => {
      const els = [];
      for (let el = h.nextElementSibling; el && !el.classList.contains("qp-part"); el = el.nextElementSibling) els.push(el);
      return els.flatMap((el) => (el.matches(".selfcheck") ? [el] : Array.from(el.querySelectorAll(".selfcheck"))));
    });
    const tools = document.querySelector(".question-tools[data-qid]");
    const qid = tools && tools.dataset.qid;

    const solved = () => {
      const all = Boolean(qid && window.dvqMarks && window.dvqMarks.has(qid, "solved"));
      parts.forEach((h, i) => {
        const checks = groups[i];
        h.classList.toggle("is-done", all || (checks.length > 0 && checks.every((c) => c.classList.contains("is-done"))));
      });
    };

    let frame = 0;
    const fill = () => {
      frame = 0;
      const top = wrap.getBoundingClientRect().top;
      // the line starts at the first circle's centre, 0.75rem under the box's top (18-question.css)
      const start = parts[0].getBoundingClientRect().top - top + 0.75 * parseFloat(getComputedStyle(document.documentElement).fontSize);
      const line = readY(), y = line - top;
      wrap.style.setProperty("--qp-fill", `${Math.max(0, Math.round(y - start))}px`);
      parts.forEach((h) => h.classList.toggle("is-passed", h.getBoundingClientRect().top <= line));
    };
    const later = () => { if (!frame) frame = requestAnimationFrame(fill); };

    solved();
    fill();
    document.addEventListener("dvq-marks", solved);
    groups.flat().forEach((c) => new MutationObserver(solved).observe(c, { attributes: true, attributeFilter: ["class"] }));
    window.addEventListener("scroll", later, { passive: true });
    window.addEventListener("resize", later, { passive: true });
    // details opening and closing move the parts below them
    wrap.addEventListener("toggle", later, true);
    if (!quiet) requestAnimationFrame(() => wrap.classList.add("is-live"));   // no transition on load
  };

  document.addEventListener("DOMContentLoaded", () => document.querySelectorAll(".qp-parts").forEach(timeline));
})();
