// Question page tools: open / close every collapsible block, practice mode (solutions
// hidden, with a stopwatch) and the hint ladder (hint n+1 appears once hint n is open).
// Practice mode is remembered across pages in localStorage; the stopwatch is per page.
(() => {
  const KEY = "dvq-practice";
  const SOLUTION = "details.success";

  const pad = (n) => String(n).padStart(2, "0");
  const fmt = (ms) => {
    const s = Math.floor(ms / 1000);
    return `${pad(Math.floor(s / 60))}:${pad(s % 60)}`;
  };

  const setup = (bar) => {
    const article = bar.closest("article") || document;
    const details = () => Array.from(article.querySelectorAll("details"));
    const solutions = () => Array.from(article.querySelectorAll(SOLUTION));
    const practiceBtn = bar.querySelector(".qt-practice");
    const clock = bar.querySelector(".qt-clock");
    let start = null, timer = null;

    const setPractice = (on, remember = true) => {
      document.body.classList.toggle("practice-mode", on);
      practiceBtn.classList.toggle("is-active", on);
      practiceBtn.textContent = on ? "הצג פתרונות" : "מצב תרגול";
      solutions().forEach((d) => { d.hidden = on; if (on) d.open = false; });
      if (remember) {
        try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* private mode */ }
      }
      clearInterval(timer);
      if (on) {
        start = Date.now();
        clock.hidden = false;
        clock.textContent = "⏱ 00:00";
        timer = setInterval(() => { clock.textContent = "⏱ " + fmt(Date.now() - start); }, 1000);
      } else if (start) {
        clock.textContent = "⏱ " + fmt(Date.now() - start) + " · הפתרונות גלויים";
      }
    };

    bar.querySelector(".qt-open").addEventListener("click", () => {
      details().forEach((d) => { if (!d.hidden) d.open = true; });
    });
    bar.querySelector(".qt-close").addEventListener("click", () => {
      details().forEach((d) => (d.open = false));
    });
    practiceBtn.addEventListener("click", () => setPractice(!document.body.classList.contains("practice-mode")));

    let remembered = false;
    try { remembered = localStorage.getItem(KEY) === "1"; } catch (e) { /* ignore */ }
    if (remembered) setPractice(true, false);
  };

  // Hint ladder: consecutive hint blocks (details.tip whose title starts with "רמז")
  // stay hidden until the previous hint has been opened.
  const ladder = (article) => {
    const hints = Array.from(article.querySelectorAll("details.tip")).filter((d) => {
      const s = d.querySelector("summary");
      return s && s.textContent.trim().startsWith("רמז");
    });
    hints.forEach((h, i) => {
      const next = hints[i + 1];
      if (!next || next.previousElementSibling !== h) return;   // only direct neighbours
      next.classList.add("hint-locked");
      const unlock = () => { if (h.open) next.classList.remove("hint-locked"); };
      h.addEventListener("toggle", unlock);
      unlock();
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".question-tools").forEach(setup);
    document.querySelectorAll("article").forEach(ladder);
  });
})();
