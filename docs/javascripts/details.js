// Details (19-details.css): the success pulse and the box loading wave.
// V15: a calm green pulse where the reader marks a question solved (the "solved" button of
// the page tools, question-tools.js, and its copy in the part bar, reading-tools.js) and where
// a self-check answer is right (selfcheck.js). It only listens: a click that has turned the
// button on (aria-pressed), or a check that has left the reply marked right (.is-ok), gets
// an overlay fixed over the page, which removes itself. Nothing moves under reduced motion
// or in an automated browser (the page checks), where the state change is the whole answer.
// V17: in an automated browser the root gets .dt-still, which stops the boxes' loading wave.
(() => {
  const quiet = window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver;
  if (navigator.webdriver) document.documentElement.classList.add("dt-still");
  if (quiet) return;

  // the ring takes the shape of the anchor (a pill button, a field) and spreads
  // from its edge; the mark rises from the anchor's icon
  const pulse = (anchor, icon) => {
    const r = anchor.getBoundingClientRect(), c = (icon || anchor).getBoundingClientRect();
    if (!r.width && !r.height) return;
    const el = document.createElement("div");
    el.className = "dt-pulse";
    el.setAttribute("aria-hidden", "true");
    el.style.left = `${r.left}px`;
    el.style.top = `${r.top}px`;
    el.style.width = `${r.width}px`;
    el.style.height = `${r.height}px`;
    el.style.setProperty("--r", getComputedStyle(anchor).borderRadius || "50%");
    el.style.setProperty("--mx", `${c.left + c.width / 2 - r.left}px`);
    el.style.setProperty("--my", `${c.top + c.height / 2 - r.top}px`);
    el.innerHTML = '<i class="dt-ring"></i><i class="dt-ring"></i><i class="dt-mark"></i>';
    document.body.append(el);
    setTimeout(() => el.remove(), 1200);
  };

  // A click on a "solved" button, after its own handler: the part bar's copy passes the
  // click on to the header's button by script (not trusted), so only the button the reader
  // pressed pulses.
  document.addEventListener("click", (e) => {
    if (!e.isTrusted) return;
    const btn = e.target.closest && e.target.closest(".qt-solved, .pn-solved");
    if (btn) {
      // the part bar's copy follows the header's button through a MutationObserver
      setTimeout(() => { if (btn.getAttribute("aria-pressed") === "true") pulse(btn, btn.querySelector(".ui-ico")); }, 0);
      return;
    }
    const go = e.target.closest && e.target.closest(".selfcheck__go");
    if (go) checked(go.closest(".selfcheck"));
  });
  document.addEventListener("keydown", (e) => {
    if (e.key !== "Enter" || !e.target.closest) return;
    const input = e.target.closest(".selfcheck__in");
    if (input) checked(input.closest(".selfcheck"));
  });
  const checked = (box) => {
    const msg = box && box.querySelector(".selfcheck__msg");
    // the ring around the field the answer was typed in, the mark from the reply's check mark
    if (msg && msg.classList.contains("is-ok")) pulse(box.querySelector(".selfcheck__in") || msg, msg.querySelector(".selfcheck__tick"));
  };
})();
