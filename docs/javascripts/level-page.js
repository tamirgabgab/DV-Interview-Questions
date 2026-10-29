// The level pages (17-lists.css): the header band with the reader's progress and the table rows.
// The band (hooks/questions.py, _lists_band) is complete without this script: it shows the
// count, the difficulty mix and a calm "nothing marked yet" line. Here the line becomes
// "solved n of m" with a bar once the reader has marked a question of the page solved
// (marks.js keeps the marks), and the favourites are counted beside it. The band's
// background rolls slowly only when motion is welcome and the browser is not automated.
(() => {
  const NB = " ";
  const quiet = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;

  const paint = () => {
    const marks = window.dvqMarks;
    if (!marks) return;
    document.querySelectorAll(".list-band .lb-progress").forEach((box) => {
      const ids = (box.dataset.ids || "").split(" ").filter(Boolean);
      if (!ids.length) return;
      const done = ids.filter((id) => marks.has(id, "solved")).length;
      const stars = ids.filter((id) => marks.has(id, "star")).length;
      const text = box.querySelector(".lb-ptext");
      box.classList.toggle("is-empty", done === 0);
      box.classList.toggle("is-done", done === ids.length);
      box.querySelector(".lb-pbar i").style.width = `${(100 * done) / ids.length}%`;
      let line = done === 0 ? "עוד לא סימנת שאלות כפתורות"
        : done === ids.length ? `פתרת את כל ${ids.length} השאלות` : `פתרת ${done} מתוך ${ids.length}`;
      if (stars) line += ` · ${stars}${NB}★ במועדפים`;
      text.textContent = line;
    });
  };

  const live = () => {
    if (quiet) return;
    document.querySelectorAll(".list-band").forEach((band) => {
      band.classList.add("is-live");
      if (!("IntersectionObserver" in window)) return;
      new IntersectionObserver(([e]) => band.classList.toggle("is-paused", !e.isIntersecting)).observe(band);
    });
  };

  document.addEventListener("dvq-marks", paint);
  document.addEventListener("DOMContentLoaded", () => { paint(); live(); });
})();
