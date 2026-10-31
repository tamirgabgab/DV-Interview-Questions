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

// My map (session 30): a square per question, a row per level (the hook draws them as
// links), painted from this browser: solved and favourite marks (marks.js), and started
// (a self-check answered, or an interview done, interview mode). Hidden until there is
// something to show. One square is in the tab order; the arrows move between squares
// (left is forward on this page), up and down between the levels, Home and End.
(() => {
  const map = document.querySelector(".my-map");
  if (!map) return;
  const cells = Array.from(map.querySelectorAll(".mm-cell"));
  const rows = Array.from(map.querySelectorAll(".mm-cells")).map((r) => Array.from(r.children));
  const peek = map.querySelector(".mm-peek"), stats = map.querySelector(".mm-stats");
  const keys = () => {
    const out = [];
    try { for (let i = 0; i < localStorage.length; i++) out.push(localStorage.key(i)); } catch (e) { /* storage off */ }
    return out;
  };
  const state = (cell, all) => {
    const id = cell.dataset.id, path = new URL(cell.href).pathname;
    const marks = window.dvqMarks;
    if (marks && marks.has(id, "solved")) return "solved";
    if (all.some((k) => k === `dvq-interview:${id}` || k.startsWith(`dvq-check:${path}:`))) return "started";
    return "";
  };
  const say = { solved: "פתרתם", started: "התחלתם", "": "עוד לא" };
  const paint = () => {
    const all = keys();
    let solved = 0, started = 0, starred = 0;
    cells.forEach((c) => {
      const s = state(c, all), star = Boolean(window.dvqMarks && window.dvqMarks.has(c.dataset.id, "star"));
      c.dataset.state = s;
      c.classList.toggle("is-solved", s === "solved");
      c.classList.toggle("is-started", s === "started");
      c.classList.toggle("is-star", star);
      solved += s === "solved"; started += s === "started"; starred += star;
    });
    map.hidden = !(solved || started || starred);
    stats.textContent = `פתרתם ${solved} מתוך ${cells.length} שאלות` + (started ? `, והתחלתם עוד ${started}.` : ".");
  };
  const show = (c) => {
    const [id, ...title] = c.getAttribute("aria-label").split(" ");
    peek.textContent = `${id} ${title.join(" ")}. ${say[c.dataset.state || ""]}${c.classList.contains("is-star") ? ", במועדפים" : ""}.`;
  };
  if (cells.length) cells[0].tabIndex = 0;
  const focus = (c) => { cells.forEach((x) => { x.tabIndex = x === c ? 0 : -1; }); c.focus(); show(c); };
  map.addEventListener("keydown", (e) => {
    const c = e.target.closest(".mm-cell");
    if (!c) return;
    const r = rows.findIndex((row) => row.includes(c)), i = rows[r].indexOf(c);
    let to = null;
    if (e.key === "ArrowLeft") to = rows[r][i + 1] || (rows[r + 1] && rows[r + 1][0]);
    else if (e.key === "ArrowRight") to = rows[r][i - 1] || (rows[r - 1] && rows[r - 1][rows[r - 1].length - 1]);
    else if (e.key === "ArrowDown" && rows[r + 1]) to = rows[r + 1][Math.min(i, rows[r + 1].length - 1)];
    else if (e.key === "ArrowUp" && rows[r - 1]) to = rows[r - 1][Math.min(i, rows[r - 1].length - 1)];
    else if (e.key === "Home") to = cells[0];
    else if (e.key === "End") to = cells[cells.length - 1];
    if (to) { e.preventDefault(); focus(to); }
  });
  map.addEventListener("focusin", (e) => { const c = e.target.closest(".mm-cell"); if (c) show(c); });
  map.addEventListener("mouseover", (e) => { const c = e.target.closest(".mm-cell"); if (c) show(c); });
  document.addEventListener("dvq-marks", paint);
  document.addEventListener("DOMContentLoaded", paint);
  if (document.readyState !== "loading") paint();
})();
