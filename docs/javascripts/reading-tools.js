// Reading aids on question pages:
// - figure lightbox: every inline SVG figure or chart gets an "enlarge" button that opens it
//   full screen, with pinch / wheel zoom, drag to pan, double tap to zoom and Esc to close;
// - tap tooltips: on a touch screen, tapping a mark that has an SVG <title> shows the title
//   (there is no hover on phones);
// - part bar: on a page with two or more parts ("### סעיף ..."), a sticky row of chips that
//   jumps to a part and marks the part being read.
// window.dvqDecorate(root, selector?) adds the enlarge buttons to figures drawn later
// (explorer.js passes its own selector for the live figures of a box).
(() => {
  const FIGURES = "svg.figure, svg.perf-chart";

  // --- lightbox --------------------------------------------------------------------------

  let box = null, stage = null, lastFocus = null;
  const view = { scale: 1, x: 0, y: 0 };
  const apply = () => {
    stage.style.transform = `translate(${view.x}px, ${view.y}px) scale(${view.scale})`;
  };
  const zoomTo = (scale, cx = 0, cy = 0) => {
    const s = Math.min(6, Math.max(1, scale));
    view.x = cx - (cx - view.x) * (s / view.scale);
    view.y = cy - (cy - view.y) * (s / view.scale);
    view.scale = s;
    if (s === 1) { view.x = 0; view.y = 0; }
    apply();
  };

  const build = () => {
    box = document.createElement("div");
    box.className = "fig-lightbox";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "איור מוגדל");
    box.innerHTML =
      '<div class="fig-lightbox__bar">' +
      '<button type="button" class="fig-lb-close" aria-label="סגירה">✕</button>' +
      '<button type="button" class="fig-lb-in" aria-label="הגדלה">+</button>' +
      '<button type="button" class="fig-lb-out" aria-label="הקטנה">−</button>' +
      '<button type="button" class="fig-lb-reset" aria-label="גודל מקורי">1:1</button>' +
      '<span class="fig-lightbox__hint">צביטה או גלגלת להגדלה, גרירה להזזה</span></div>' +
      '<div class="fig-lightbox__view md-typeset"><div class="fig-lightbox__stage"></div></div>';
    document.body.append(box);
    stage = box.querySelector(".fig-lightbox__stage");
    const area = box.querySelector(".fig-lightbox__view");
    box.querySelector(".fig-lb-close").addEventListener("click", close);
    box.querySelector(".fig-lb-in").addEventListener("click", () => zoomTo(view.scale * 1.5));
    box.querySelector(".fig-lb-out").addEventListener("click", () => zoomTo(view.scale / 1.5));
    box.querySelector(".fig-lb-reset").addEventListener("click", () => zoomTo(1));
    box.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
      if (e.key === "+" || e.key === "=") zoomTo(view.scale * 1.5);
      if (e.key === "-") zoomTo(view.scale / 1.5);
    });
    area.addEventListener("wheel", (e) => {
      e.preventDefault();
      const r = area.getBoundingClientRect();
      zoomTo(view.scale * (e.deltaY < 0 ? 1.2 : 1 / 1.2), e.clientX - r.left - r.width / 2, e.clientY - r.top - r.height / 2);
    }, { passive: false });
    // pointers: one drags, two pinch; a quick second tap toggles the zoom
    const pts = new Map();
    let pinch = null, lastTap = 0;
    area.addEventListener("pointerdown", (e) => {
      area.setPointerCapture(e.pointerId);
      pts.set(e.pointerId, [e.clientX, e.clientY]);
      if (pts.size === 2) {
        const [a, b] = [...pts.values()];
        pinch = { d: Math.hypot(a[0] - b[0], a[1] - b[1]), scale: view.scale };
      }
      const now = Date.now();
      if (pts.size === 1 && now - lastTap < 300) zoomTo(view.scale > 1 ? 1 : 2.5);
      lastTap = now;
    });
    area.addEventListener("pointermove", (e) => {
      if (!pts.has(e.pointerId)) return;
      const prev = pts.get(e.pointerId);
      pts.set(e.pointerId, [e.clientX, e.clientY]);
      if (pts.size === 2 && pinch) {
        const [a, b] = [...pts.values()];
        zoomTo(pinch.scale * Math.hypot(a[0] - b[0], a[1] - b[1]) / pinch.d);
      } else if (pts.size === 1 && view.scale > 1) {
        view.x += e.clientX - prev[0];
        view.y += e.clientY - prev[1];
        apply();
      }
    });
    const up = (e) => { pts.delete(e.pointerId); if (pts.size < 2) pinch = null; };
    area.addEventListener("pointerup", up);
    area.addEventListener("pointercancel", up);
  };

  const open = (svg) => {
    if (!box) build();
    lastFocus = document.activeElement;
    const copy = svg.cloneNode(true);
    copy.removeAttribute("style");          // the page copy may carry a max-width
    stage.replaceChildren(copy);
    view.scale = 1; view.x = 0; view.y = 0;
    apply();
    box.classList.add("is-open");
    document.documentElement.classList.add("fig-lightbox-open");
    box.querySelector(".fig-lb-close").focus();
  };
  function close() {
    box.classList.remove("is-open");
    document.documentElement.classList.remove("fig-lightbox-open");
    stage.replaceChildren();
    if (lastFocus) lastFocus.focus();
  }

  const decorate = (root, selector = FIGURES) => {
    root.querySelectorAll(selector).forEach((svg) => {
      if (svg.closest(".fig-wrap") || svg.closest(".fig-lightbox")) return;
      const wrap = document.createElement("div");
      wrap.className = "fig-wrap";
      svg.replaceWith(wrap);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "fig-enlarge";
      btn.setAttribute("aria-label", "הגדלת האיור");
      btn.title = "הגדלת האיור";
      btn.textContent = "⤢";
      btn.addEventListener("click", () => open(svg));
      wrap.append(svg, btn);
    });
  };
  window.dvqDecorate = decorate;

  // --- tap tooltips ----------------------------------------------------------------------

  let tip = null, tipTimer = null;
  const hideTip = () => { if (tip) tip.hidden = true; clearTimeout(tipTimer); };
  document.addEventListener("pointerup", (e) => {
    if (e.pointerType === "mouse") return;
    const mark = e.target.closest && e.target.closest("svg *");
    const title = mark && (mark.querySelector(":scope > title") || (mark.parentElement && mark.parentElement.matches("g") && mark.parentElement.querySelector(":scope > title")));
    if (!title || !mark.closest(FIGURES)) { hideTip(); return; }
    if (!tip) {
      tip = document.createElement("div");
      tip.className = "fig-tip";
      tip.setAttribute("role", "status");
      document.body.append(tip);
    }
    tip.textContent = title.textContent;
    tip.hidden = false;
    const x = Math.min(window.innerWidth - tip.offsetWidth - 8, Math.max(8, e.clientX - tip.offsetWidth / 2));
    tip.style.left = `${x}px`;
    tip.style.top = `${Math.max(8, e.clientY - tip.offsetHeight - 14)}px`;
    clearTimeout(tipTimer);
    tipTimer = setTimeout(hideTip, 3500);
  });
  window.addEventListener("scroll", hideTip, { passive: true });

  // --- part bar ----------------------------------------------------------------------------

  const partBar = (article) => {
    const parts = Array.from(article.querySelectorAll("h3[id]")).filter((h) => /^סעיף/.test(h.textContent.trim()));
    if (parts.length < 2) return;
    const nav = document.createElement("nav");
    nav.className = "part-nav";
    nav.setAttribute("aria-label", "סעיפי השאלה");
    nav.setAttribute("data-search-exclude", "");
    const links = parts.map((h) => {
      const a = document.createElement("a");
      a.href = `#${h.id}`;
      a.className = "part-nav__chip";
      a.textContent = h.textContent.replace("¶", "").split("–")[0].trim();
      a.title = h.textContent.replace("¶", "").trim();
      nav.append(a);
      return a;
    });
    const h2 = Array.from(article.querySelectorAll("h2[id]"));
    const end = h2.find((h) => h.compareDocumentPosition(parts[parts.length - 1]) & Node.DOCUMENT_POSITION_PRECEDING);
    const anchor = article.querySelector(".path-nav") || article.querySelector(".question-tools");
    if (anchor) anchor.after(nav); else article.prepend(nav);
    const mark = () => {
      const y = 140;
      let current = -1;
      parts.forEach((h, i) => { if (h.getBoundingClientRect().top <= y) current = i; });
      if (end && end.getBoundingClientRect().top <= y) current = -1;   // past the last part
      links.forEach((a, i) => {
        a.classList.toggle("is-current", i === current);
        if (i === current) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
    };
    window.addEventListener("scroll", mark, { passive: true });
    mark();
  };

  document.addEventListener("DOMContentLoaded", () => {
    decorate(document);
    document.querySelectorAll("article.md-content__inner").forEach(partBar);
  });
})();
