// Site-wide motion (round M, 13-motion.css): the site mark drawn on the first page of a
// visit (M3; the pointer draws it again by CSS alone), a marker that slides along the table
// of contents to the section being read (M4), and the question title carried from a list
// into the question page by a cross-document view transition (M6, the CSS declares the
// transition itself). Nothing here hides content: under reduced motion or in an automated
// browser (the page checks) the mark is drawn from the start and the marker sits still.
(() => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const quiet = reduce || navigator.webdriver;
  const LOGO_KEY = "dvq-logo-drawn";

  // M3: draw the mark in the header once per visit (sessionStorage: a new tab or a new
  // visit draws it again); the class goes when the check mark is done.
  const drawLogo = () => {
    if (quiet) return;
    try {
      if (sessionStorage.getItem(LOGO_KEY)) return;
      sessionStorage.setItem(LOGO_KEY, "1");
    } catch (e) { return; }
    const logo = document.querySelector(".md-header .dvq-logo");
    if (!logo) return;
    logo.classList.add("is-drawing");
    logo.querySelector(".lg-v").addEventListener("animationend", () => logo.classList.remove("is-drawing"), { once: true });
  };

  // M4: one bar beside the table of contents, moved to the link Material marks active.
  const tocMarker = () => {
    const nav = document.querySelector(".md-sidebar--secondary .md-nav--secondary");
    const list = nav && nav.querySelector(":scope > .md-nav__list");
    if (!list) return;
    const bar = document.createElement("span");
    bar.className = "toc-marker";
    bar.setAttribute("aria-hidden", "true");
    nav.append(bar);
    let frame = 0;
    const place = () => {
      frame = 0;
      const links = list.querySelectorAll(".md-nav__link--active");
      const link = links[links.length - 1];
      const box = link && link.getBoundingClientRect();
      if (!box || !box.height) { bar.classList.remove("is-on"); return; }
      const top = box.top - nav.getBoundingClientRect().top;
      bar.style.transform = `translateY(${top}px)`;
      bar.style.height = `${box.height}px`;
      bar.classList.add("is-on");
    };
    const later = () => { if (!frame) frame = requestAnimationFrame(place); };
    new MutationObserver(later).observe(list, { subtree: true, attributes: true, attributeFilter: ["class"] });
    window.addEventListener("resize", later, { passive: true });
    place();
    if (!quiet) requestAnimationFrame(() => bar.classList.add("is-moving"));   // no slide in from the top on load
  };

  // M6: the link to a question that was followed takes the title's transition name, so the
  // browser carries it into the page's title; one name at a time, or the transition fails.
  const QUESTION = /\/questions\/[a-z]+\/\d{4}-[^/]+\/?$/;
  const nameTitles = () => {
    if (quiet || !("onpagereveal" in window)) return;
    let named = null;
    document.addEventListener("click", (e) => {
      const a = e.target.closest && e.target.closest(".md-content a[href]");
      if (!a || a.closest(".question-header") || !QUESTION.test(new URL(a.href, location.href).pathname)) return;
      if (named) named.style.viewTransitionName = "";
      a.style.viewTransitionName = "dvq-title";
      named = a;
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    drawLogo();
    tocMarker();
    nameTitles();
  });
})();
