// Home page touches: the hero's numbers count up from zero the first time they come into
// view (W339), and the sections and cards under the hero rise into view once (W344, a 40 ms
// stagger along a row of cards). The real numbers and the content are in the page; without
// the script, under reduced motion or in an automated browser (the page checks), nothing
// moves or hides. Round M adds the hero's live example (M2): the machine of 0055 part a
// reads numbers bit by bit (the page holds its last frame for 27), and the waves and the
// example stop while the hero is off screen.
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

  // M2: a number's bits, MSB first, through r -> (2r + b) mod 3: the edge taken and the
  // bit read light up, the state moves; at the end the verdict stays for a moment.
  const FSM_NUMBERS = [27, 10, 21, 14, 6, 13];
  const STEP_MS = 750, HOLD_MS = 2000;
  const NB = " ";
  const fsmDemo = (hero) => {
    const panel = hero.querySelector(".hh-fsm");
    if (!panel) return null;
    const nodes = [...panel.querySelectorAll(".hf-node")], edges = [...panel.querySelectorAll(".hf-edge")];
    const bitsEl = panel.querySelector(".hf-bits"), read = panel.querySelector(".hf-read");
    let k = 0, n = 0, bits = [], i = 0, r = 0, timer = 0;
    const show = () => nodes.forEach((el) => el.classList.toggle("is-now", Number(el.dataset.r) === r));
    const begin = () => {
      n = FSM_NUMBERS[k];
      bits = [...n.toString(2)].map(Number);
      i = 0; r = 0;
      bitsEl.innerHTML = bits.map((b) => `<span class="hf-bit">${b}</span>`).join("");
      edges.forEach((el) => el.classList.remove("is-taken"));
      panel.classList.remove("is-yes", "is-no");
      read.textContent = `מתחילים בשארית 0`;
      show();
    };
    const tick = () => {
      if (i < bits.length) {
        const b = bits[i];
        edges.forEach((el) => el.classList.toggle("is-taken", el.dataset.e === `${r}${b}`));
        r = (2 * r + b) % 3;
        [...bitsEl.children].forEach((el, j) => { el.classList.toggle("is-read", j < i); el.classList.toggle("is-now", j === i); });
        i += 1;
        const prefix = bits.slice(0, i).join("");
        read.innerHTML = `עד עכשיו <bdi dir="ltr">${prefix}</bdi> = ${parseInt(prefix, 2)}, שארית${NB}: ${r}`;
        show();
        timer = setTimeout(tick, STEP_MS);
        return;
      }
      [...bitsEl.children].forEach((el) => { el.classList.add("is-read"); el.classList.remove("is-now"); });
      panel.classList.add(r === 0 ? "is-yes" : "is-no");
      read.innerHTML = r === 0 ? `המספר <bdi dir="ltr">${n}</bdi> מתחלק ב-3 ✓`
        : `המספר <bdi dir="ltr">${n}</bdi> לא מתחלק ב-3 (שארית ${r})`;
      timer = setTimeout(() => { k = (k + 1) % FSM_NUMBERS.length; begin(); timer = setTimeout(tick, STEP_MS); }, HOLD_MS);
    };
    let started = false;
    return {
      play() {
        if (timer) return;
        if (!started) { started = true; begin(); }
        timer = setTimeout(tick, STEP_MS);
      },
      pause() { clearTimeout(timer); timer = 0; },
    };
  };

  document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".home-hero");
    if (!hero || !("IntersectionObserver" in window)) return;
    const demo = reduce || navigator.webdriver ? null : fsmDemo(hero);
    // the hero's rolling waves and the example run only while it is on screen
    new IntersectionObserver((entries) => {
      const on = entries.some((e) => e.isIntersecting);
      hero.classList.toggle("is-paused", !on);
      if (demo) { if (on) demo.play(); else demo.pause(); }
    }).observe(hero);
  });

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
