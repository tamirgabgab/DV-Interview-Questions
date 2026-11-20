// Reading aids on question pages:
// - figure lightbox: every inline SVG figure or chart gets an "enlarge" button that opens it
//   full screen, with pinch / wheel zoom, drag to pan, double tap to zoom and Esc to close
//   (the button moves above a drawing that has text in its corner);
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
    box.classList.remove("is-closing");
    stage.replaceChildren(copy);
    view.scale = 1; view.x = 0; view.y = 0;
    apply();
    box.classList.add("is-open");
    document.documentElement.classList.add("fig-lightbox-open");
    box.querySelector(".fig-lb-close").focus();
  };
  // A closing run (session 33, 26-ui-round.css): .is-closing plays the exit animation, and
  // done() hides the element when it ends; at once under reduced motion, in an automated
  // browser (the page checks) or without the Web Animations API.
  const exitRun = (el, done) => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches || navigator.webdriver || !el.getAnimations) { done(); return; }
    el.classList.add("is-closing");
    const runs = el.getAnimations({ subtree: true }).filter((a) => a.playState !== "finished");
    const end = () => { el.classList.remove("is-closing"); done(); };
    if (!runs.length) { end(); return; }
    Promise.all(runs.map((a) => a.finished)).then(end, end);
  };
  function close() {
    if (!box.classList.contains("is-open") || box.classList.contains("is-closing")) return;
    document.documentElement.classList.remove("fig-lightbox-open");
    if (lastFocus) lastFocus.focus();
    exitRun(box, () => { box.classList.remove("is-open"); stage.replaceChildren(); });
  }

  // The button covers the top inline-start corner of the drawing. When SVG text is drawn
  // there (a value label, an axis end), the wrap gets fig-wrap--above and the button moves
  // to a strip above the drawing. The decision is taken once the wrap is laid out (a figure
  // in a closed tab has no size yet), again after the phone fit enlarged the figure's text
  // (fitSvg below), and again when the window changes width. A live figure
  // that a box redraws gets a new wrap each time; the decision is kept on its container
  // (data-fig-above), so the figure does not jump between the two layouts while playing. A
  // container marked data-fig-strip always has the strip: a live figure whose labels reach
  // the corner only at some steps (the 0039 zoom) would otherwise move down once.
  const ABOVE = "fig-wrap--above";
  const covers = (wrap, which = false) => {
    const btn = wrap.querySelector(":scope > .fig-enlarge"), svg = wrap.querySelector("svg");
    if (!btn || !svg) return null;
    const b = btn.getBoundingClientRect();
    if (!b.width || !b.height) return null;                   // not laid out yet
    const pad = 2;
    for (const t of svg.querySelectorAll("text")) {
      if (t.closest("defs") || !t.textContent.trim()) continue;
      const r = t.getBoundingClientRect();
      if (!r.width || !r.height) continue;
      if (r.left < b.right + pad && r.right > b.left - pad && r.top < b.bottom + pad && r.bottom > b.top - pad) return which ? t.textContent.trim() : true;
    }
    return false;
  };
  // The container remembers the decision per figure (its index among the container's
  // figures, since a container may hold several).
  const slot = (wrap) => {
    const host = wrap.parentElement;
    if (!host) return null;
    const i = [...host.children].filter((c) => c.classList.contains("fig-wrap")).indexOf(wrap);
    return { host, key: ` ${i} `, list: () => ` ${host.dataset.figAbove || ""} ` };
  };
  const decide = (wrap) => {
    if (wrap.parentElement && wrap.parentElement.hasAttribute("data-fig-strip")) { wrap.classList.add(ABOVE); return true; }
    const at = slot(wrap);
    if (at && at.list().includes(at.key)) { wrap.classList.add(ABOVE); return true; }
    wrap.classList.remove(ABOVE);
    const hit = covers(wrap);
    if (hit === null) return false;
    if (hit) { wrap.classList.add(ABOVE); if (at) at.host.dataset.figAbove = (at.list() + at.key).trim().replace(/\s+/g, " "); }
    return true;
  };
  const sized = typeof ResizeObserver === "function" ? new ResizeObserver((entries) => {
    entries.forEach((e) => { if (decide(e.target)) sized.unobserve(e.target); });
  }) : null;
  window.dvqFigCovers = covers;                                // the phone check reads it
  let refit = 0;
  window.addEventListener("resize", () => {
    clearTimeout(refit);
    refit = setTimeout(() => {
      document.querySelectorAll("[data-fig-above]").forEach((h) => delete h.dataset.figAbove);
      document.querySelectorAll(".fig-wrap").forEach((w) => { if (!decide(w) && sized) sized.observe(w); });
    }, 150);
  }, { passive: true });

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
      if (sized) sized.observe(wrap); else decide(wrap);     // decided once the wrap is laid out
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

  // The sticky bar (UI325): on a question page, the part chips (two parts or more), and
  // once the header has scrolled away the solved toggle (it presses the header's own
  // button, and mirrors it; the site header shows the title by then), with a
  // reading-progress line along its bottom. With parts it is sticky in the flow under the header; without
  // them it is fixed under the site header and slides in only after the header.
  // The row with parts is in the built page (the hook's part_row), so nothing moves when
  // this script runs: it is only wired here, and built here when the page has none.
  const partBar = (article) => {
    const header = article.querySelector(".question-header");
    const parts = Array.from(article.querySelectorAll("h3[id]")).filter((h) => /^סעיף/.test(h.textContent.trim()));
    if (!header && parts.length < 2) return;
    const fixed = parts.length < 2;
    const ready = article.querySelector("nav.part-nav");
    if (ready && fixed) ready.remove();
    const built = Boolean(ready) && !fixed;
    const nav = built ? ready : document.createElement("nav");
    const part = (cls, tag = "span") => {
      let el = nav.querySelector(`:scope > .${cls}`);
      if (!el) { el = document.createElement(tag); el.className = cls; nav.append(el); }
      return el;
    };
    nav.className = `part-nav${fixed ? " pn-fixed" : ""}`;
    nav.setAttribute("aria-label", fixed ? "השאלה" : "סעיפי השאלה");
    nav.setAttribute("data-search-exclude", "");
    const h1 = header && header.querySelector("h1");
    const chips = part("pn-chips");
    const links = (fixed ? [] : parts).map((h, k) => {
      const a = chips.children[k] || chips.appendChild(document.createElement("a"));
      a.href = `#${h.id}`;
      a.className = "part-nav__chip";
      a.textContent = h.textContent.replace("¶", "").split("–")[0].trim();
      a.title = h.textContent.replace("¶", "").trim();
      return a;
    });
    while (chips.children.length > links.length) chips.lastElementChild.remove();
    // W347: the map of the solution being read shows here, so one sticky row remains
    const slot = part("pn-sol");
    const progress = part("pn-progress");
    if (!progress.firstElementChild) progress.innerHTML = "<i></i>";
    const own = header && header.querySelector(".qt-solved");
    if (own) {
      const solved = own.cloneNode(true);
      solved.classList.remove("qt-mark", "qt-solved");
      solved.classList.add("pn-solved");
      solved.addEventListener("click", () => own.click());
      const mirror = () => {
        ["aria-pressed", "aria-label", "data-tip", "class"].forEach((at) => {
          if (at === "class") solved.classList.toggle("is-active", own.classList.contains("is-active"));
          else solved.setAttribute(at, own.getAttribute(at));
        });
        solved.querySelector(".ui-ico").className = own.querySelector(".ui-ico").className;
      };
      new MutationObserver(mirror).observe(own, { attributes: true, subtree: true });
      mirror();
      progress.before(solved);
    }
    const h2 = Array.from(article.querySelectorAll("h2[id]"));
    const end = parts.length ? h2.find((h) => h.compareDocumentPosition(parts[parts.length - 1]) & Node.DOCUMENT_POSITION_PRECEDING) : null;
    if (fixed) article.append(nav);
    else if (!built) {
      const anchor = article.querySelector(".path-nav") || header;
      if (anchor) anchor.after(nav); else article.prepend(nav);
    }
    const place = () => {                     // the fixed bar spans the article's column, under the site header
      if (!fixed) return;
      const r = article.getBoundingClientRect(), site = document.querySelector(".md-header");
      nav.style.left = `${r.left}px`;
      nav.style.width = `${r.width}px`;
      if (site) nav.style.top = `${site.getBoundingClientRect().bottom}px`;
    };
    const mark = () => {
      const y = spyLine();                      // the one reading line (the TOC's too, tocSpy)
      let current = -1;
      parts.forEach((h, i) => { if (h.getBoundingClientRect().top <= y) current = i; });
      if (end && end.getBoundingClientRect().top <= y) current = -1;   // past the last part
      links.forEach((a, i) => {
        a.classList.toggle("is-current", i === current);
        if (i === current) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
      const stuck = Boolean(h1) && h1.getBoundingClientRect().bottom < 60;
      if (stuck !== nav.classList.contains("is-stuck")) { nav.classList.toggle("is-stuck", stuck); place(); }
      const r = article.getBoundingClientRect();
      const read = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - window.innerHeight)));
      nav.style.setProperty("--pn-read", `${(read * 100).toFixed(1)}%`);
    };
    window.addEventListener("scroll", mark, { passive: true });
    window.addEventListener("resize", () => { place(); mark(); fades(chips); }, { passive: true });
    chips.addEventListener("scroll", () => fades(chips), { passive: true });
    slot.addEventListener("scroll", () => fades(slot), { passive: true });
    place();
    mark();
    fades(chips);
  };

  // A row of chips that scrolls sideways fades out at an edge with more chips beyond it,
  // so a chip cut by the edge reads as "more this way" (the mask in 10-rounds-w.css).
  const fades = (row) => {
    if (!row) return;
    const max = row.scrollWidth - row.clientWidth, pos = Math.abs(row.scrollLeft);
    row.classList.toggle("fade-s", max > 1 && pos > 1);         // the start (right) edge
    row.classList.toggle("fade-e", max > 1 && pos < max - 1);   // the end (left) edge
  };

  // --- figure text on narrow screens (D194) ---------------------------------------------------

  // A figure drawn for a 640-unit viewBox shrinks with the column, and on a phone its labels
  // fall to 5-7 px. Every SVG text that would render under MIN_PX gets a font size (in the
  // figure's units) that renders at FIT_PX, at most MAX_GROW times its own (a label marked
  // data-fit-drop that still renders under MIN_PX is hidden, its tooltip stays); a row of tick
  // labels (class tick or coord) that then overlaps is thinned, every k-th label kept (the first and the last
  // always), the smallest k with no overlap, and so is a column of them (a y axis, labels
  // anchored at their end). Tick and coord labels, which thinning keeps apart, and legend
  // labels (the names of a chart's lines, such as "T ≈ 0.333") render at TICK_PX at least
  // (round 9: the axes of 0028 and 0044; round 10: the legends, at 11 px on a phone); a lone
  // one that then overlaps another (the values over a bar chart's bars) is hidden, the
  // higher kept. Redone when a figure comes into view, on resize, and when an explorer box
  // redraws; the lightbox copy gets the original sizes.
  const MIN_PX = 9, FIT_PX = 9.5, TICK_PX = 11, MAX_GROW = 2;
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
    t.dataset.fitShift = dx.toFixed(1);
  };

  // a row along x, or with col a column along y (a digit fills about 0.7 of its box's height)
  const thinRow = (row, col = false) => {
    const lo = (b) => (col ? b.y : b.x), end = (b) => (col ? b.y + 0.7 * b.height : b.x + b.width + 2);
    row.sort((a, b) => lo(a.box) - lo(b.box));
    const overlaps = (keep) => keep.some((t, i) => i && lo(t.box) < end(keep[i - 1].box));
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
      const tick = t.matches(".tick, .coord, .legend"), min = tick ? TICK_PX : MIN_PX;
      if (size * scale >= min) continue;
      t.dataset.fitBase = t.style.fontSize;
      const grown = Math.min((tick ? TICK_PX : FIT_PX) / scale, size * MAX_GROW);
      t.style.fontSize = `${grown.toFixed(2)}px`;
      if (t.hasAttribute("data-fit-drop") && grown * scale < MIN_PX) t.classList.add("fit-hidden");
    }
    const rows = new Map(), cols = new Map();
    const group = (map, key, t) => { if (!map.has(key)) map.set(key, []); map.get(key).push({ el: t, box: t.getBBox() }); };
    const at = (t, k) => `${t.getAttribute("class")}|${t.parentNode === svg ? "" : "g"}${Math.round(parseFloat(t.getAttribute(k)) || 0)}`;
    const labels = [...svg.querySelectorAll("text.tick, text.coord")].filter((t) => t.textContent.trim());
    labels.forEach((t) => { if (t.getAttribute("text-anchor") === "middle") group(rows, at(t, "y"), t); });
    // a column: labels anchored at their end on one x, but for one on an x axis's row (the axis's name)
    const axisRows = new Set([...rows].filter(([, r]) => r.length > 2).map(([k]) => k.split("|").pop()));
    labels.forEach((t) => {
      if (t.getAttribute("text-anchor") === "end" && !axisRows.has(at(t, "y").split("|").pop())) group(cols, at(t, "x"), t);
    });
    rows.forEach((row) => { if (row.length > 2) thinRow(row); });
    cols.forEach((col) => { if (col.length > 2) thinRow(col, true); });
    // the lone ones (a bar's value): the highest first, each hidden when it overlaps one kept
    const lone = [...rows.values()].filter((r) => r.length <= 2).flat().sort((a, b) => a.box.y - b.box.y), kept = [];
    lone.forEach((t) => {
      const b = t.box, hit = kept.some((k) => b.x < k.x + k.width && k.x < b.x + b.width && b.y < k.y + 0.7 * k.height && k.y < b.y + 0.7 * b.height);
      t.el.classList.toggle("fit-hidden", hit);
      if (!hit) kept.push(b);
    });
    // an axis's name (anchored at its end on the row of the x axis's labels, at a corner of
    // the chart) wins over the labels it now covers: the 0 of the y axis, the first of the x axis
    svg.querySelectorAll("text[data-fit-base]:not(.fit-hidden)").forEach((t) => keepInside(svg, t));
    const shifted = (t) => { const b = t.getBBox(); return { x: b.x + (parseFloat(t.dataset.fitShift) || 0), y: b.y, width: b.width, height: b.height }; };
    const named = labels.filter((t) => t.getAttribute("text-anchor") === "end" && axisRows.has(at(t, "y").split("|").pop()));
    named.forEach((n) => {
      const a = shifted(n);
      labels.forEach((t) => {
        if (t === n || named.includes(t) || t.classList.contains("fit-hidden")) return;
        const b = shifted(t);
        if (a.x < b.x + b.width && b.x < a.x + a.width && a.y < b.y + 0.7 * b.height && b.y < a.y + 0.7 * a.height) t.classList.add("fit-hidden");
      });
    });
    const wrap = svg.parentElement;
    if (wrap && wrap.classList.contains("fig-wrap")) decide(wrap);   // the enlarged text may reach the button
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
  // (data-label), shown before the value by the CSS. A table of short values (a trace, or
  // rows named in the first column) is a grid instead (Y394): it stays a table, tighter,
  // and when it still does not fit it scrolls sideways with its first column in place
  // (data-scrolls). A long table that fits its column keeps its header row in view while
  // it scrolls (the scroll wrapper would otherwise hold the sticky header). Data
  // attributes, not classes: Material styles only tables without one.
  const CARD_COLS = 5, CARD_ROWS = 3, STICKY_ROWS = 8, GRID_CELL = 14;
  const tables = (root) => {
    const wide = [], long = [], grids = [];
    root.querySelectorAll(".md-content .md-typeset__table > table:not([class])").forEach((table) => {
      if (table.closest(".questions-wrap, .explorer")) return;
      const heads = Array.from(table.querySelectorAll("thead th")).map((th) => th.textContent.trim());
      const rows = table.querySelectorAll("tbody tr");
      const values = Array.from(rows).flatMap((tr) => Array.from(tr.children).slice(1).map((td) => td.textContent.trim().length));
      if (heads.length >= CARD_COLS && Math.max(0, ...values, ...heads.slice(1).map((h) => h.length)) <= GRID_CELL) {
        table.dataset.grid = "";
        grids.push(table);
      } else if (heads.length >= CARD_COLS && rows.length >= CARD_ROWS) {   // a row-per-value table stays a table
        rows.forEach((tr) => Array.from(tr.children).forEach((td, i) => {
          if (heads[i]) td.dataset.label = heads[i];
        }));
        wide.push(table);
      }
      if (rows.length >= STICKY_ROWS) { table.dataset.long = ""; long.push(table); }
    });
    // Cards only where the table does not fit its column (measured as a table), and a
    // sticky header only where it does. "Fits" is the scroll box's own overflow, which
    // counts the theme's padding around the table (a table 1 px narrower than the box
    // could still stick out by that padding), measured again once the fonts are in.
    const overflows = (wrap) => wrap && wrap.clientWidth && wrap.scrollWidth > wrap.clientWidth + 1;
    // Each group is reset, then measured, then marked (N11.1): a measure between two changes
    // makes the browser lay out the whole page again, once per table on a long page.
    const wrapOf = (table) => table.closest(".md-typeset__scrollwrap");
    const layout = () => {
      grids.forEach((table) => { delete table.dataset.scrolls; });
      grids.map((table) => overflows(wrapOf(table)))
        .forEach((over, i) => { if (over) grids[i].dataset.scrolls = ""; });
      wide.forEach((table) => { delete table.dataset.cards; });
      wide.map((table) => overflows(wrapOf(table)))
        .forEach((over, i) => { if (over) wide[i].dataset.cards = ""; });
      const wraps = long.map(wrapOf);
      wraps.forEach((wrap) => { if (wrap) wrap.classList.remove("table-fits"); });
      wraps.map((wrap, i) => wrap && ("cards" in long[i].dataset ? false : !overflows(wrap)))
        .forEach((fits, i) => { if (wraps[i]) wraps[i].classList.toggle("table-fits", fits); });
    };
    layout();
    if (document.fonts) document.fonts.ready.then(layout);
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

  // The solution map (A181) is a row of chips at the top of a solution, one per block. While
  // the reader is inside an open solution whose own row has scrolled away, a copy of it
  // sits in the part bar (W347: one sticky row, not two), the current block marked.
  const maps = [];
  // On a short screen (a phone on its side, a page zoomed to 200%) the part bar does not
  // stick (32-access.css): it scrolls away with the page, so nothing hangs from it.
  const shortScreen = window.matchMedia("(max-height: 30em)");
  const readingLine = () => {
    const bar = document.querySelector(".part-nav");
    if (bar && !shortScreen.matches && (!bar.classList.contains("pn-fixed") || bar.classList.contains("is-stuck"))) {
      return bar.getBoundingClientRect().bottom;
    }
    const site = document.querySelector(".md-header");
    return site ? site.getBoundingClientRect().bottom : 0;
  };
  // The line a heading or a block has to pass to count as the one being read: under the
  // part bar and the solution row hanging from it, the same for the part bar, the solution
  // maps and the table of contents (one scroll-spy, so they never disagree).
  const spyLine = () => {
    const bar = document.querySelector(".part-nav");
    const slot = bar && bar.classList.contains("has-sol") && bar.querySelector(".pn-sol");
    const line = readingLine();
    return (slot ? Math.max(line, slot.getBoundingClientRect().bottom) : line) + 24;
  };
  let shown = null;
  const syncSlot = () => {
    const bar = document.querySelector(".part-nav");
    const slot = bar && bar.querySelector(".pn-sol");
    if (!slot) return;
    const line = readingLine();
    const active = !shortScreen.matches && maps.find((m) => m.sol.open && m.nav.getBoundingClientRect().bottom < line
      && m.sol.getBoundingClientRect().bottom > line + 40) || null;
    if (active !== shown) {
      shown = active;
      slot.replaceChildren(...(active ? active.links.map((a) => a.cloneNode(true)) : []));
      bar.classList.toggle("has-sol", Boolean(active));
      fades(slot);
    }
    if (!active) return;
    Array.from(slot.children).forEach((c, i) => {
      const on = active.links[i].classList.contains("is-current");
      c.classList.toggle("is-current", on);
      if (on) {
        c.setAttribute("aria-current", "true");
        const n = slot.getBoundingClientRect(), r = c.getBoundingClientRect();
        if (r.left < n.left || r.right > n.right) slot.scrollLeft += r.left < n.left ? r.left - n.left - 8 : r.right - n.right + 8;
      } else c.removeAttribute("aria-current");
    });
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
    maps.push({ sol, nav, links });
    const mark = () => {
      if (!sol.open) return;
      const y = spyLine();
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
    sol.addEventListener("toggle", () => { mark(); syncSlot(); });
    mark();
  };

  // A one-line title that does not fit its box: drop whole words from its end and add an
  // ellipsis. The CSS ellipsis alone cuts inside a word, and in a Hebrew line with English
  // words it cut the English one in the middle ("PCIe" read "Cle"). Takes [text, box] pairs
  // and works in rounds, one dropped word a round: every width is read before any title is
  // written, so a round is one layout however many titles there are (one title at a time
  // was a layout per title and word, about 800 on a page's load).
  const fitWords = (pairs) => {
    let todo = pairs.filter(([text, box]) => text && box).map(([text, box]) => ({ text, box, words: null }));
    while (todo.length) {
      todo = todo.filter((t) => t.box.clientWidth && t.box.scrollWidth > t.box.clientWidth + 1);   // read
      todo = todo.filter((t) => {                                                                   // write
        if (!t.words) t.words = t.text.textContent.trim().split(/\s+/);
        if (t.words.length <= 1) return false;
        t.words.pop();
        while (t.words.length > 1 && /^[–\-·•:]+$/.test(t.words[t.words.length - 1])) t.words.pop();   // no dangling dash
        t.text.textContent = `${t.words.join(" ").replace(/[,;:]$/, "")} …`;
        return true;
      });
    }
  };

  // An inline formula wider than its line (a long chain, or the text enlarged by the phone)
  // scrolls on its own instead of widening the page: marked .is-wide, and focusable so the
  // keyboard can scroll it. Measured once the fonts are in (the math is in the page from the
  // build) and again on a resize.
  const wideMath = () => {
    document.querySelectorAll(".md-typeset mjx-container:not([display='true'])").forEach((m) => {
      const box = m.parentElement && m.parentElement.closest("p, li, td, th, dd, div, span.arithmatex");
      const line = box && box.matches("span.arithmatex") ? box.parentElement : box;
      if (!line) return;
      m.classList.remove("is-wide");
      // past the line's content box on either side (an RTL line overflows to the left)
      const r = m.getBoundingClientRect(), l = line.getBoundingClientRect(), cs = getComputedStyle(line);
      const left = l.left + parseFloat(cs.paddingLeft) + parseFloat(cs.borderLeftWidth);
      const right = l.right - parseFloat(cs.paddingRight) - parseFloat(cs.borderRightWidth);
      if (r.width && (r.left < left - 0.5 || r.right > right + 0.5)) {
        m.classList.add("is-wide");
        m.tabIndex = 0;
      } else if (m.tabIndex === 0 && !m.classList.contains("is-wide")) m.removeAttribute("tabindex");
    });
  };
  let wideTimer = null;
  const wideLater = () => { clearTimeout(wideTimer); wideTimer = setTimeout(wideMath, 150); };

  // A link to a closed fold (the tags page's lists, Y398) opens it and shows it.
  const openTarget = () => {
    let target = null;
    try { target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { return; }
    if (target && target.matches("details") && !target.open) {
      target.open = true;
      target.scrollIntoView();
    }
  };

  // The sticky solution map sits under the part bar when the page has one.
  const partBarHeight = () => {
    const bar = document.querySelector(".part-nav");
    document.documentElement.style.setProperty("--part-nav-h", bar && !shortScreen.matches ? `${bar.offsetHeight}px` : "0px");
  };

  // The table of contents follows the same reading line as the part bar (spyLine): its
  // link of the heading being read gets .is-spy, which 13-motion.css colours and the TOC
  // marker (motion.js) follows; Material's own --active class used a higher line, so the
  // part bar said ג while the contents still said ב.
  const tocSpy = () => {
    const nav = document.querySelector(".md-sidebar--secondary .md-nav--secondary");
    if (!nav) return;
    const pairs = Array.from(nav.querySelectorAll("a.md-nav__link[href^='#']")).map((a) => {
      let id = a.getAttribute("href").slice(1);
      try { id = decodeURIComponent(id); } catch (e) { /* keep it */ }
      return [a, document.getElementById(id)];
    }).filter(([, h]) => h);
    if (!pairs.length) return;
    nav.classList.add("has-spy");
    let on = null, frame = 0;
    const mark = () => {
      frame = 0;
      const y = spyLine();
      let cur = null;
      pairs.forEach((p) => { if (p[1].getBoundingClientRect().top <= y) cur = p[0]; });
      const doc = document.documentElement;
      if (window.innerHeight + window.scrollY >= doc.scrollHeight - 2) cur = pairs[pairs.length - 1][0];   // the end of the page
      if (cur === on) return;
      if (on) { on.classList.remove("is-spy"); on.removeAttribute("aria-current"); }
      on = cur;
      if (on) { on.classList.add("is-spy"); on.setAttribute("aria-current", "location"); }
    };
    const later = () => { if (!frame) frame = requestAnimationFrame(mark); };
    window.addEventListener("scroll", later, { passive: true });
    window.addEventListener("resize", later, { passive: true });
    document.addEventListener("toggle", later, true);
    mark();
  };

  document.addEventListener("DOMContentLoaded", () => {
    decorate(document);
    document.querySelectorAll("article.md-content__inner").forEach(partBar);
    document.querySelectorAll("article.md-content__inner details.success").forEach((sol) => {
      solutionMap(sol, solutionBlocks(sol));
    });
    partBarHeight();
    const pbar = document.querySelector(".part-nav");
    if (pbar && "ResizeObserver" in window) new ResizeObserver(partBarHeight).observe(pbar);
    window.addEventListener("scroll", syncSlot, { passive: true });
    syncSlot();
    tocSpy();
    tables(document);
    watchFigures(document);
    document.querySelectorAll(".md-content .explorer").forEach((box) =>
      boxObserver.observe(box, { childList: true, subtree: true, characterData: true }));
    window.addEventListener("resize", () => { partBarHeight(); syncSlot(); }, { passive: true });
    openTarget();
    window.addEventListener("hashchange", openTarget);
    // a side navigation title (S421) and a path step's title (S419) that do not fit lose
    // whole words from their end, the full title stays as the link's tooltip; fitted again
    // from the whole title when the column changes width (a grip, a resize, the fold button)
    // or a section of it opens. Under Material's breakpoint the navigation is a drawer:
    // nothing is measured until it opens.
    const drawerNav = window.matchMedia("(max-width: 76.234375em)");
    const drawerBox = document.getElementById("__drawer");
    const fitNav = () => {
      if (drawerNav.matches && !(drawerBox && drawerBox.checked)) return;
      const pairs = [];
      document.querySelectorAll(".md-sidebar--primary .md-nav__link .md-ellipsis").forEach((span) => {
        const link = span.closest("a");
        if (!link || link.classList.contains("md-nav__link--active")) return;
        if (!span.dataset.full) span.dataset.full = span.textContent.trim();
        if (!link.title) link.title = span.dataset.full;
        if (span.textContent !== span.dataset.full) span.textContent = span.dataset.full;
        pairs.push([span, span]);
      });
      fitWords(pairs);
    };
    let navFrame = 0;
    const fitNavLater = () => { cancelAnimationFrame(navFrame); navFrame = requestAnimationFrame(fitNav); };
    requestAnimationFrame(fitNav);   // after layout.js has put back a remembered column width
    window.addEventListener("resize", fitNavLater, { passive: true });
    if (drawerBox) drawerBox.addEventListener("change", fitNavLater);
    const sideNav = document.querySelector(".md-sidebar--primary");
    if (sideNav) sideNav.addEventListener("change", fitNavLater);
    fitWords([...document.querySelectorAll(".path-nav .pn-title")].map((t) => [t, t.closest("a")]));
    wideMath();
    if (document.fonts) document.fonts.ready.then(wideMath, wideMath);
    document.addEventListener("toggle", wideLater, true);           // a solution opened: its math is laid out now
    window.addEventListener("resize", wideLater, { passive: true });
  });
})();
