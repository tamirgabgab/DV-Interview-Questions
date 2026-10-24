// Reading aids on question pages:
// - figure lightbox: every inline SVG figure or chart gets an "enlarge" button that opens it
//   full screen, with pinch / wheel zoom, drag to pan, double tap to zoom and Esc to close;
// - tap tooltips: on a touch screen, tapping a mark that has an SVG <title> shows the title
//   (there is no hover on phones);
// - part bar: on a page with two or more parts ("### סעיף ..."), a sticky row of chips that
//   jumps to a part and marks the part being read;
// - solution blocks: each labelled block of a solution (idea, steps, code, proof, cost) is
//   wrapped for its colour and side rail, and a solution with two or more blocks gets a
//   sticky map of chips that jumps to a block and marks the block being read;
// - figure text on narrow screens: SVG text that would render under 9 px is enlarged and
//   crowded tick rows thinned (window.dvqFitText(root) refits on demand);
// - tables: a table of five or more columns that does not fit becomes cards on a phone,
//   and a long table that fits keeps its header row in view while it scrolls.
// window.dvqDecorate(root, selector?) adds the enlarge buttons to figures drawn later
// (explorer/core.js passes its own selector for the live figures of a box).
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
    unfit(copy);                             // the phone text sizes (D194) are not needed here
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

  // --- figure text on narrow screens (D194) ---------------------------------------------------

  // A figure drawn for a 640-unit viewBox shrinks with the column, and on a phone its labels
  // fall to 5-7 px. Every SVG text that would render under MIN_PX gets a font size (in the
  // figure's units) that renders at FIT_PX, at most MAX_GROW times its own; a row of tick
  // labels (class tick or coord) that then overlaps is thinned, every k-th label kept (the first and the last
  // always), the smallest k with no overlap. Redone when a figure comes into view, on
  // resize, and when an explorer box redraws; the lightbox copy gets the original sizes.
  const MIN_PX = 9, FIT_PX = 9.5, MAX_GROW = 1.8;
  const FIT_SVGS = ".md-content svg:not(mjx-container svg):not(.mermaid svg)";

  const unfit = (root) => {
    root.querySelectorAll("text[data-fit-base]").forEach((t) => {
      t.style.fontSize = t.dataset.fitBase;
      t.removeAttribute("data-fit-base");
    });
    root.querySelectorAll("text[data-fit-shift]").forEach((t) => {
      t.removeAttribute("transform");
      t.removeAttribute("data-fit-shift");
    });
    root.querySelectorAll("text.fit-hidden").forEach((t) => t.classList.remove("fit-hidden"));
  };

  // A grown label must stay inside the figure: one wider than the viewBox shrinks back to
  // fit, one past an edge moves inward (labels that carry their own transform stay).
  const keepInside = (svg, t) => {
    const vb = svg.viewBox && svg.viewBox.baseVal;
    if (!vb || !vb.width) return;
    let b = t.getBBox();
    if (b.width > vb.width - 4) {
      t.style.fontSize = `${(parseFloat(t.style.fontSize) * (vb.width - 4) / b.width).toFixed(2)}px`;
      b = t.getBBox();
    }
    if (t.hasAttribute("transform")) return;
    const lo = vb.x + 1, hi = vb.x + vb.width - 1;
    const dx = b.x < lo ? lo - b.x : b.x + b.width > hi ? hi - b.x - b.width : 0;
    if (Math.abs(dx) < 0.5) return;
    t.setAttribute("transform", `translate(${dx.toFixed(1)} 0)`);
    t.dataset.fitShift = "";
  };

  const thinRow = (row) => {
    row.sort((a, b) => a.box.x - b.box.x);
    const overlaps = (keep) => keep.some((t, i) => i && t.box.x < keep[i - 1].box.x + keep[i - 1].box.width + 2);
    for (let k = 1; k <= row.length; k++) {
      const keep = row.filter((t, i) => i % k === 0 || i === row.length - 1);
      if (k > 1 && keep.length > 1 && (row.length - 1) % k !== 0) keep.splice(-2, 1);   // the last kept, its left neighbour not
      if (!overlaps(keep) || keep.length <= 2) {
        row.forEach((t) => t.el.classList.toggle("fit-hidden", !keep.includes(t)));
        return;
      }
    }
  };

  const fitSvg = (svg) => {
    if (svg.parentElement && svg.parentElement.closest("svg")) return;
    unfit(svg);
    if (!svg.getBoundingClientRect().width) return;
    for (const t of svg.querySelectorAll("text")) {
      const m = t.getScreenCTM();
      const scale = m ? Math.hypot(m.a, m.b) : 0;
      if (!scale || !t.textContent.trim()) continue;
      const size = parseFloat(getComputedStyle(t).fontSize);
      if (size * scale >= MIN_PX) continue;
      t.dataset.fitBase = t.style.fontSize;
      t.style.fontSize = `${Math.min(FIT_PX / scale, size * MAX_GROW).toFixed(2)}px`;
    }
    const rows = new Map();
    for (const t of svg.querySelectorAll("text.tick, text.coord")) {
      if (t.getAttribute("text-anchor") !== "middle" || !t.textContent.trim()) continue;
      const key = `${t.getAttribute("class")}|${t.parentNode === svg ? "" : "g"}${Math.round(parseFloat(t.getAttribute("y")) || 0)}`;
      if (!rows.has(key)) rows.set(key, []);
      rows.get(key).push({ el: t, box: t.getBBox() });
    }
    rows.forEach((row) => { if (row.length > 2) thinRow(row); });
    svg.querySelectorAll("text[data-fit-base]:not(.fit-hidden)").forEach((t) => keepInside(svg, t));
  };

  // A figure is fitted whenever its rendered size changes: when it is first laid out, when
  // a closed solution or a tab that holds it opens, and on resize.
  const fitObserver = "ResizeObserver" in window
    ? new ResizeObserver((entries) => entries.forEach((e) => fitSvg(e.target)))
    : null;
  const watchFigures = (root) => {
    root.querySelectorAll(FIT_SVGS).forEach((svg) => {
      if (svg.dvqFitWatched || (svg.parentElement && svg.parentElement.closest("svg"))) return;
      svg.dvqFitWatched = true;
      if (fitObserver) fitObserver.observe(svg); else fitSvg(svg);
    });
  };
  window.dvqFitText = (root) => root.querySelectorAll(FIT_SVGS).forEach(fitSvg);
  window.dvqUnfitText = unfit;

  // An explorer box redraws its figures: refit the box once per frame.
  const dirtyBoxes = new Set();
  let fitFrame = 0;
  const boxObserver = new MutationObserver((records) => {
    for (const r of records) {
      const box = r.target.closest && r.target.closest(".explorer");
      if (box) dirtyBoxes.add(box);
    }
    if (!fitFrame) fitFrame = requestAnimationFrame(() => {
      fitFrame = 0;
      dirtyBoxes.forEach((box) => { watchFigures(box); box.querySelectorAll(FIT_SVGS).forEach(fitSvg); });
      dirtyBoxes.clear();
    });
  });

  // --- tables (C192) --------------------------------------------------------------------------

  // A content table of CARD_COLS or more columns and CARD_ROWS or more rows that does not
  // fit its column becomes cards on a phone: every cell gets its column's name
  // (data-label), shown before the value by the CSS. A long table that fits its column keeps
  // its header row in view while it scrolls (the scroll wrapper would otherwise hold the
  // sticky header). Data attributes, not classes: Material styles only tables without one.
  const CARD_COLS = 5, CARD_ROWS = 3, STICKY_ROWS = 8;
  const tables = (root) => {
    const wide = [], long = [];
    root.querySelectorAll(".md-content .md-typeset__table > table:not([class])").forEach((table) => {
      if (table.closest(".questions-wrap, .explorer")) return;
      const heads = Array.from(table.querySelectorAll("thead th")).map((th) => th.textContent.trim());
      const rows = table.querySelectorAll("tbody tr");
      if (heads.length >= CARD_COLS && rows.length >= CARD_ROWS) {   // a row-per-value table stays a table
        rows.forEach((tr) => Array.from(tr.children).forEach((td, i) => {
          if (heads[i]) td.dataset.label = heads[i];
        }));
        wide.push(table);
      }
      if (rows.length >= STICKY_ROWS) { table.dataset.long = ""; long.push(table); }
    });
    // Cards only where the table does not fit its column (measured as a table), and a
    // sticky header only where it does.
    const layout = () => {
      wide.forEach((table) => {
        const wrap = table.closest(".md-typeset__scrollwrap");
        delete table.dataset.cards;
        if (wrap && wrap.clientWidth && table.offsetWidth > wrap.clientWidth + 1) table.dataset.cards = "";
      });
      long.forEach((table) => {
        const wrap = table.closest(".md-typeset__scrollwrap");
        if (!wrap) return;
        wrap.classList.remove("table-fits");
        wrap.classList.toggle("table-fits", "cards" in table.dataset ? false : table.offsetWidth <= wrap.clientWidth + 1);
      });
    };
    layout();
    window.addEventListener("resize", layout, { passive: true });
    document.addEventListener("toggle", layout, true);
    document.addEventListener("change", (e) => { if (e.target.closest && e.target.closest(".tabbed-set")) layout(); });
  };

  // --- solution blocks and map --------------------------------------------------------------

  // Every "#### ... { .sol-* }" label and what follows it, up to the next label, goes into a
  // <div class="sol-block sol-block--idea"> (C191: a colour and a side rail per kind). A
  // solution with two or more blocks gets a sticky row of chips above its first block that
  // jumps to a block and marks the block being read (A181).
  const SOL_KINDS = ["idea", "steps", "code", "proof", "cost"];
  const solKind = (el) => el.tagName === "H4" && SOL_KINDS.find((k) => el.classList.contains(`sol-${k}`));

  const solutionBlocks = (sol) => {
    const blocks = [];
    for (const h of Array.from(sol.children).filter(solKind)) {
      const block = document.createElement("div");
      block.className = `sol-block sol-block--${solKind(h)}`;
      h.before(block);
      let el = h;
      while (el && !(el !== h && solKind(el))) {
        const next = el.nextElementSibling;
        block.append(el);
        el = next;
      }
      blocks.push(block);
    }
    return blocks;
  };

  const solutionMap = (sol, blocks) => {
    if (blocks.length < 2) return;
    const nav = document.createElement("nav");
    nav.className = "sol-map";
    nav.setAttribute("aria-label", "חלקי הפתרון");
    nav.setAttribute("data-search-exclude", "");
    const links = blocks.map((block, i) => {
      const h = block.firstElementChild;
      if (!h.id) h.id = `${sol.id || "sol"}-block-${i}`;
      const a = document.createElement("a");
      a.href = `#${h.id}`;
      a.className = `sol-map__chip sol-map__chip--${solKind(h)}`;
      a.textContent = h.textContent.replace("¶", "").trim();
      nav.append(a);
      return a;
    });
    blocks[0].before(nav);
    const mark = () => {
      if (!sol.open) return;
      const y = nav.getBoundingClientRect().bottom + 24;
      let current = 0;
      blocks.forEach((b, i) => { if (b.getBoundingClientRect().top <= y) current = i; });
      if (links[current].classList.contains("is-current")) return;
      links.forEach((a, i) => {
        a.classList.toggle("is-current", i === current);
        if (i === current) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
      // On a phone the row scrolls sideways: keep the current chip in it.
      const a = links[current], n = nav.getBoundingClientRect(), r = a.getBoundingClientRect();
      if (r.left < n.left || r.right > n.right) nav.scrollLeft += r.left < n.left ? r.left - n.left - 8 : r.right - n.right + 8;
    };
    window.addEventListener("scroll", mark, { passive: true });
    sol.addEventListener("toggle", mark);
    mark();
  };

  // The sticky solution map sits under the part bar when the page has one.
  const partBarHeight = () => {
    const bar = document.querySelector(".part-nav");
    document.documentElement.style.setProperty("--part-nav-h", bar ? `${bar.offsetHeight}px` : "0px");
  };

  document.addEventListener("DOMContentLoaded", () => {
    decorate(document);
    document.querySelectorAll("article.md-content__inner").forEach(partBar);
    document.querySelectorAll("article.md-content__inner details.success").forEach((sol) => {
      solutionMap(sol, solutionBlocks(sol));
    });
    partBarHeight();
    tables(document);
    watchFigures(document);
    document.querySelectorAll(".md-content .explorer").forEach((box) =>
      boxObserver.observe(box, { childList: true, subtree: true, characterData: true }));
    window.addEventListener("resize", partBarHeight, { passive: true });
  });
})();
