// Solved / favourite marks, kept only in this browser (localStorage), and the "solved n of
// m" progress bars that hooks/questions.py places on level cards, path cards and path pages
// (div.mark-progress with data-ids). Other scripts use window.dvqMarks and listen for the
// "dvq-marks" event on document. It also keeps the last question opened (for the home
// page's "continue" card).
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

  // The last question this browser opened (E34): saved on every question page, shown on
  // the home page as a "continue where you left off" card with its marks.
  const LAST = "dvq-last";
  const remember = () => {
    const tools = document.querySelector(".question-tools[data-qid]");
    const h1 = document.querySelector(".question-header h1");
    if (!tools || !h1) return;
    try {
      localStorage.setItem(LAST, JSON.stringify({ id: tools.dataset.qid, title: h1.textContent.trim(), url: location.pathname, at: Date.now() }));
    } catch (e) { /* private mode */ }
  };
  const ago = (ms) => {
    const m = Math.round(ms / 60000), h = Math.round(m / 60), d = Math.round(h / 24);
    return m < 2 ? "ממש עכשיו" : m < 60 ? `לפני ${m} דקות` : h < 2 ? "לפני שעה" : h < 24 ? `לפני ${h} שעות` : d < 2 ? "אתמול" : `לפני ${d} ימים`;
  };
  const resume = () => {
    const card = document.querySelector(".continue-card");
    if (!card) return;
    let last = null;
    try { last = JSON.parse(localStorage.getItem(LAST) || "null"); } catch (e) { last = null; }
    if (!last || !last.id || !last.url) return;
    const a = document.createElement("a");
    a.className = "cc-link";
    a.href = last.url;
    a.innerHTML = '<span class="cc-label">המשך מאיפה שעצרת</span><span class="cc-title"></span><span class="cc-meta"></span>';
    a.querySelector(".cc-title").textContent = `${last.id} · ${last.title}`;
    const marksText = (window.dvqMarks.has(last.id, "solved") ? " · ✓ פתרת" : "") + (window.dvqMarks.has(last.id, "star") ? " · ★ מועדף" : "");
    a.querySelector(".cc-meta").textContent = `ביקרת ${ago(Date.now() - (last.at || Date.now()))}${marksText}`;
    card.replaceChildren(a);
    card.hidden = false;
  };

  // Another tab changed the marks
  window.addEventListener("storage", (e) => {
    if (e.key === KEY) { marks = load(); document.dispatchEvent(new CustomEvent("dvq-marks")); }
  });
  document.addEventListener("dvq-marks", progress);
  document.addEventListener("DOMContentLoaded", () => { progress(); remember(); resume(); });
})();
