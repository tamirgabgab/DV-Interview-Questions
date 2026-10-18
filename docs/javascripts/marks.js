// Solved / favourite marks, kept only in this browser (localStorage), and the "solved n of
// m" progress bars that hooks/questions.py places on level cards, path cards and path pages
// (div.mark-progress with data-ids). Other scripts use window.dvqMarks and listen for the
// "dvq-marks" event on document.
(() => {
  const KEY = "dvq-marks";

  const load = () => {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; }
  };
  let marks = load();

  const save = () => {
    try { localStorage.setItem(KEY, JSON.stringify(marks)); } catch (e) { /* private mode */ }
    document.dispatchEvent(new CustomEvent("dvq-marks"));
  };

  window.dvqMarks = {
    has: (id, mark) => Boolean(marks[id] && marks[id][mark]),
    toggle: (id, mark) => {
      const m = marks[id] || (marks[id] = {});
      if (m[mark]) delete m[mark]; else m[mark] = 1;
      if (!Object.keys(m).length) delete marks[id];
      save();
      return Boolean(m[mark]);
    },
  };

  const progress = () => {
    document.querySelectorAll(".mark-progress").forEach((box) => {
      const ids = (box.dataset.ids || "").split(" ").filter(Boolean);
      if (!ids.length) return;
      const done = ids.filter((id) => window.dvqMarks.has(id, "solved")).length;
      box.hidden = false;
      box.classList.toggle("is-empty", done === 0);
      box.querySelector(".mp-bar i").style.width = `${(100 * done) / ids.length}%`;
      box.querySelector(".mp-text").textContent =
        done === ids.length ? `פתרת את כל ${ids.length} השאלות` : `פתרת ${done} מתוך ${ids.length}`;
    });
    document.querySelectorAll(".path-step").forEach((li) => {
      const id = li.dataset.id;
      li.classList.toggle("is-solved", window.dvqMarks.has(id, "solved"));
      const slot = li.querySelector(".ps-mark");
      if (slot) slot.textContent = (window.dvqMarks.has(id, "solved") ? "✓" : "") + (window.dvqMarks.has(id, "star") ? "★" : "");
    });
  };

  // Another tab changed the marks
  window.addEventListener("storage", (e) => {
    if (e.key === KEY) { marks = load(); document.dispatchEvent(new CustomEvent("dvq-marks")); }
  });
  document.addEventListener("dvq-marks", progress);
  document.addEventListener("DOMContentLoaded", progress);
})();
