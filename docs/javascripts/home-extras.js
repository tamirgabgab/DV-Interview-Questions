// The home page (15-home.css): the dark band, the live level cards and the question of the day.
// The band's pulses run while it is on screen (.is-live) and the level cards' pictures move
// on hover and focus (.is-motion), never under reduced motion or in an automated browser
// (the page checks see a still page). The question of the day is the same for every reader:
// day d since the epoch (the reader's local date) picks (d * stride) mod n in the list the
// hook put in the page; the page already holds the pick of the build day, in the same place
// and the same height, so nothing moves when it changes or when the script does not run.
(() => {
  const band = document.querySelector(".home-band");
  if (!band) return;
  const quiet = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;

  if (!quiet) {
    band.classList.add("is-motion");
    if ("IntersectionObserver" in window) {
      new IntersectionObserver((entries) => entries.forEach((e) => band.classList.toggle("is-live", e.isIntersecting)))
        .observe(band);
    }
  }

  const card = band.querySelector(".daily-card");
  const dataEl = card && card.querySelector(".dc-data");
  if (!dataEl) return;
  let data;
  try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

  const today = new Date();
  const [ey, em, ed] = data.epoch.split("-").map(Number);
  const day = Math.round((Date.UTC(today.getFullYear(), today.getMonth(), today.getDate()) - Date.UTC(ey, em - 1, ed)) / 864e5);
  const n = data.qs.length;
  const pick = data.qs[(((day * data.stride) % n) + n) % n];

  // the same markup as the hook's _home_daily_inner
  const render = ([id, title, level, diff, kind, teaser, href, interactive]) => {
    const box = interactive ? '<span class="dc-box">תיבה אינטראקטיבית</span>' : "";
    const inner =
      `<div class="dc-art">${data.icons[kind]}${box}</div>` +
      '<div class="dc-body">' +
      '<p class="dc-label"><span class="dc-kicker">שאלת היום</span><span class="dc-date"></span><span class="dc-solved" hidden>✓ פתרת</span></p>' +
      `<p class="dc-title"><span class="dc-id">${id}</span> <a href="${esc(href)}">${esc(title)}</a></p>` +
      `<p class="dc-chips"><span class="chip chip-level">${data.levels[level]}</span>` +
      `<span class="chip chip-diff chip-diff-${diff}">${data.diffs[diff]}</span>` +
      `<span class="chip chip-kind chip-kind-${kind}">${data.icons[kind]}${data.kinds[kind]}</span></p>` +
      `<p class="dc-teaser">${esc(teaser)}</p>` +
      "</div>" +
      `<a class="md-button md-button--primary dc-go" href="${esc(href)}">לפתור עכשיו</a>`;
    [...card.children].forEach((el) => { if (el !== dataEl) el.remove(); });
    card.insertAdjacentHTML("afterbegin", inner);
    card.dataset.id = id;
  };
  if (pick && pick[0] !== card.dataset.id) render(pick);

  const date = card.querySelector(".dc-date");
  try {
    date.textContent = today.toLocaleDateString("he-IL", { weekday: "long", day: "numeric", month: "long" });
  } catch (e) { /* an old browser: the label stays without the date */ }

  // personal progress: "✓ פתרת" once this browser marked the day's question solved
  const solved = () => {
    const mark = card.querySelector(".dc-solved");
    if (mark) mark.hidden = !(window.dvqMarks && window.dvqMarks.has(card.dataset.id, "solved"));
  };
  solved();
  document.addEventListener("dvq-marks", solved);
})();
