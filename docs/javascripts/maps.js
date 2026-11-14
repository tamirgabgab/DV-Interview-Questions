// The study-path metro map and the tag graph (16-maps.css).
// Both are drawn at build time by hooks/questions.py (maps_metro, maps_tag_graph) and work
// as plain links without this file. Here, the metro map gets the reader's solved marks
// (marks.js; the stations fill, the legend counts them), a card of the question on hover,
// focus or a tap, the line of a hovered legend entry or station picked out, and a fade
// with a "the map goes on" button while the map is wider than its box; the rows of the
// paths page get the reader's progress; the tag graph picks out a hovered or focused topic
// and its neighbours, and a click on a topic filters the tag lists below to it (the "show
// all" button brings them back).
(() => {
  const solved = (id) => Boolean(window.dvqMarks && window.dvqMarks.has(id, "solved"));

  const reduced = () => window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  };

  const metro = (box) => {
    const scroll = box.querySelector(".mm-scroll");
    const card = box.querySelector(".mm-card");
    const svg = box.querySelector(".mm-svg");
    if (!scroll || !card || !svg) return;
    let words = {};
    try { words = JSON.parse(box.dataset.names || "{}"); } catch (e) { /* the card shows no names */ }

    const marks = () => {
      box.querySelectorAll(".mm-st").forEach((st) => {
        const on = solved(st.dataset.id);
        st.classList.toggle("is-solved", on);
        const name = st.dataset.name || (st.dataset.name = st.getAttribute("aria-label"));
        st.setAttribute("aria-label", on ? `${name} (פתורה)` : name);
      });
      box.querySelectorAll(".mm-count").forEach((c) => {
        const ids = (c.dataset.ids || "").split(" ").filter(Boolean);
        const done = ids.filter(solved).length;
        c.textContent = done ? `${done} מתוך ${ids.length} פתורות` : `${ids.length} שאלות`;
        c.classList.toggle("is-done", done === ids.length);
      });
    };

    // pick out the given lines (numbers as strings); none: every line as it is
    const pick = (lines) => {
      box.classList.toggle("is-hl", lines.length > 0);
      box.querySelectorAll("[data-line]").forEach((el) => el.classList.toggle("is-on", lines.includes(el.dataset.line)));
      box.querySelectorAll(".mm-st").forEach((st) => {
        st.classList.toggle("is-on", (st.dataset.lines || "").split(" ").some((n) => lines.includes(n)));
      });
    };

    // The station card: one element, filled for the station under the pointer, the focus
    // or a tap. With a mouse or the keyboard the station stays the link and the card is
    // only read (pointer-events: none, aria-describedby); after a tap the card stays and
    // carries the link to the question (.is-touch), and a tap elsewhere puts it away.
    let shown = null;      // the station the card shows
    let pointer = "";      // the kind of the last pointer pressed ("" for the keyboard)
    const linesOf = (st) => (st.dataset.lines || "").split(" ").filter(Boolean);

    const fill = (st, tapped) => {
      const d = st.dataset;
      const cut = (d.title || "").indexOf(" – ");
      const title = cut < 0 ? d.title || "" : d.title.slice(0, cut);
      const sub = cut < 0 ? "" : d.title.slice(cut + 3);
      const top = el("div", "mm-card-top");
      top.append(el("span", "mm-card-id", d.id));
      const kind = el("span", "mm-card-kind");
      const ico = el("i", `kind-ico kind-ico-${d.kind}`);
      ico.setAttribute("aria-hidden", "true");
      kind.append(ico, (words.kind || {})[d.kind] || "");
      top.append(kind);
      const lines = el("span", "mm-card-lines");
      lines.setAttribute("role", "img");
      lines.setAttribute("aria-label", `מסלולים : ${linesOf(st).join(", ")}`);
      linesOf(st).forEach((n) => {
        const key = box.querySelector(`.mm-key[data-line="${n}"] .mm-num`);
        lines.append(el("i", key ? key.className : "mm-num", n));
      });
      top.append(lines);
      const meta = el("div", "mm-card-meta");
      meta.append(el("span", "chip chip-level", (words.level || {})[d.level] || ""),
        el("span", `chip chip-diff chip-diff-${d.diff}`, (words.diff || {})[d.diff] || ""));
      if (solved(d.id)) meta.append(el("span", "mm-card-solved", "פתורה ✓"));
      if (tapped) {
        const go = el("a", "mm-card-go", "לשאלה ←");
        go.href = st.getAttribute("href");
        meta.append(go);
      }
      card.replaceChildren(top, el("p", "mm-card-title", title));
      if (sub) card.append(el("p", "mm-card-sub", sub));
      card.append(meta);
      card.classList.toggle("is-touch", Boolean(tapped));
    };

    const place = () => {
      if (!shown) return;
      const dot = shown.querySelector("circle").getBoundingClientRect();
      const host = box.getBoundingClientRect();
      const w = card.offsetWidth, h = card.offsetHeight;
      const cx = dot.left + dot.width / 2 - host.left;
      const x = Math.min(Math.max(cx - w / 2, 8), host.width - w - 8);
      card.style.left = `${x}px`;
      card.style.setProperty("--mm-ax", `${Math.min(Math.max(cx - x, 16), w - 16)}px`);
      const below = dot.bottom - host.top + 12, above = dot.top - host.top - h - 12;
      const under = below + h <= host.height - 6 || above < 6;      // under the station unless only above has room
      card.classList.toggle("is-above", !under);
      card.style.top = `${under ? below : above}px`;
    };

    const hide = () => {
      if (shown) shown.removeAttribute("aria-describedby");
      shown = null;
      card.hidden = true;
      pick([]);
    };
    const show = (st, tapped) => {
      if (shown && shown !== st) shown.removeAttribute("aria-describedby");
      shown = st;
      fill(st, tapped);
      card.hidden = false;
      st.setAttribute("aria-describedby", card.id);
      place();
      pick(linesOf(st));
    };
    const tapped = () => !card.hidden && card.classList.contains("is-touch");

    box.querySelectorAll(".mm-st").forEach((st) => {
      st.addEventListener("pointerenter", (ev) => { if (ev.pointerType === "mouse" && !tapped()) show(st, false); });
      st.addEventListener("pointerleave", (ev) => { if (ev.pointerType === "mouse" && !tapped()) hide(); });
      st.addEventListener("focus", () => { if (!(tapped() && shown === st)) show(st, false); });
      st.addEventListener("blur", () => { if (!tapped()) hide(); });
      // a tap shows the card with its link; a second tap on the station follows it
      st.addEventListener("click", (ev) => {
        if (pointer !== "touch" && pointer !== "pen") return;
        if (tapped() && shown === st) return;
        ev.preventDefault();
        show(st, true);
      });
    });
    document.addEventListener("pointerdown", (ev) => {
      pointer = ev.pointerType;
      if (tapped() && !card.contains(ev.target) && !(shown && shown.contains(ev.target))) hide();
    }, true);
    document.addEventListener("keydown", (ev) => {
      pointer = "";
      if (ev.key === "Escape" && !card.hidden) hide();
    }, true);
    box.querySelectorAll(".mm-key, .mm-badge").forEach((key) => {
      const on = () => { if (card.hidden) pick([key.dataset.line]); };
      const off = () => { if (card.hidden) pick([]); };
      key.addEventListener("pointerenter", on);
      key.addEventListener("focus", on);
      key.addEventListener("pointerleave", off);
      key.addEventListener("blur", off);
    });

    // The map wider than its box: a fade on each cut edge and, while it goes on towards
    // the end, a button that scrolls one screen; the scroller takes the keyboard's arrows.
    const more = box.querySelector(".mm-more");
    const fadeStart = box.querySelector(".mm-fade-start"), fadeEnd = box.querySelector(".mm-fade-end");
    const edges = () => {
      const max = scroll.scrollWidth - scroll.clientWidth;
      const at = Math.abs(scroll.scrollLeft);
      const wide = max > 1, onward = wide && at < max - 1;
      box.classList.toggle("is-wide", wide);
      if (wide) {
        scroll.tabIndex = 0;
        scroll.setAttribute("role", "region");
        scroll.setAttribute("aria-label", "המפה, נגללת לצדדים");
      } else {
        scroll.removeAttribute("tabindex");
        scroll.removeAttribute("role");
        scroll.removeAttribute("aria-label");
      }
      if (fadeStart) fadeStart.hidden = !(wide && at > 1);
      if (fadeEnd) fadeEnd.hidden = !onward;
      if (more) {
        if (!onward && document.activeElement === more) scroll.focus({ preventScroll: true });
        more.hidden = !onward;
      }
    };
    if (more) {
      more.addEventListener("click", () => {
        const dir = getComputedStyle(scroll).direction === "rtl" ? -1 : 1;
        scroll.scrollBy({ left: dir * scroll.clientWidth * 0.8, behavior: reduced() ? "auto" : "smooth" });
      });
    }
    scroll.addEventListener("scroll", () => {
      edges();
      if (shown && document.activeElement === shown && !tapped()) place();   // the focus brought it into view
      else if (shown) hide();
    }, { passive: true });
    window.addEventListener("resize", () => { edges(); place(); }, { passive: true });
    if ("ResizeObserver" in window) new ResizeObserver(edges).observe(scroll);
    edges();

    marks();
    document.addEventListener("dvq-marks", marks);
    window.addEventListener("storage", marks);
  };

  // The rows of the paths page: the reader's progress in each path (a thin bar and "n/m")
  // and the link to its first question still unsolved, from the solved marks.
  const rows = () => {
    document.querySelectorAll(".pr-progress").forEach((p) => {
      const ids = (p.dataset.ids || "").split(" ").filter(Boolean);
      const hrefs = (p.dataset.hrefs || "").split(" ").filter(Boolean);
      const bar = p.querySelector(".pr-bar"), n = p.querySelector(".pr-n");
      const go = p.querySelector(".pr-go"), all = p.querySelector(".pr-done");
      if (!ids.length || !bar || !n || !go || !all) return;
      const done = ids.filter(solved).length;
      const next = ids.findIndex((id) => !solved(id));
      p.classList.toggle("is-empty", done === 0);
      bar.hidden = n.hidden = false;
      bar.querySelector("i").style.setProperty("--p", done / ids.length);
      const ltr = el("span", "", `${done}/${ids.length}`);
      ltr.dir = "ltr";
      n.replaceChildren(ltr);
      n.setAttribute("role", "img");
      n.setAttribute("aria-label", `פתרת ${done} מתוך ${ids.length}`);
      go.hidden = next < 0;
      all.hidden = next >= 0;
      if (next >= 0) {
        if (hrefs[next]) go.href = hrefs[next];
        go.firstChild.textContent = done ? "להמשיך" : "להתחיל";
        go.setAttribute("aria-label", done ? `להמשיך במסלול ${p.dataset.name}` : `להתחיל את המסלול ${p.dataset.name}`);
      }
    });
  };

  const graph = (box) => {
    const status = box.querySelector(".tg-status");
    const text = box.querySelector(".tg-status-text");
    const reset = box.querySelector(".tg-reset");
    const index = document.querySelector(".tag-index");
    const sections = [...document.querySelectorAll(".tag-section")];
    if (!sections.length) return;

    const light = (node) => {
      box.querySelectorAll(".tg-svg").forEach((svg) => {
        const tag = node && node.dataset.tag;
        const nb = node ? (node.dataset.nb || "").split(" ") : [];
        svg.classList.toggle("is-hl", Boolean(node));
        svg.querySelectorAll(".tg-node").forEach((n) => {
          n.classList.toggle("is-focus", n.dataset.tag === tag);
          n.classList.toggle("is-on", n.dataset.tag === tag || nb.includes(n.dataset.tag));
        });
        svg.querySelectorAll(".tg-edge").forEach((e) => e.classList.toggle("is-on", e.dataset.a === tag || e.dataset.b === tag));
      });
    };

    const filter = (tag) => {
      let shown = null;
      sections.forEach((s) => {
        const on = !tag || s.id === `tag:${tag}`;
        s.hidden = !on;
        if (tag && on) { s.open = true; shown = s; }
      });
      if (index) index.classList.toggle("is-filtered", Boolean(tag));   // the level row and the headings step aside
      box.querySelectorAll(".tg-node").forEach((n) => {
        if (n.dataset.tag === tag) n.setAttribute("aria-current", "true"); else n.removeAttribute("aria-current");
      });
      status.hidden = !tag;
      if (shown) {
        const name = shown.querySelector("summary .tr-name");
        const count = shown.querySelectorAll(".tag-list > li").length;
        text.textContent = `מוצגות ${count} השאלות בנושא ${name ? name.textContent.trim() : tag}.`;
      }
    };

    box.querySelectorAll(".tg-node").forEach((node) => {
      node.addEventListener("pointerenter", () => light(node));
      node.addEventListener("pointerleave", () => light(null));
      node.addEventListener("focus", () => light(node));
      node.addEventListener("blur", () => light(null));
      node.addEventListener("click", (ev) => {
        ev.preventDefault();
        const again = node.getAttribute("aria-current") === "true";
        filter(again ? null : node.dataset.tag);
        if (!again) status.scrollIntoView({ block: "nearest" });
      });
    });
    reset.addEventListener("click", () => {
      const was = [...box.querySelectorAll('.tg-node[aria-current="true"]')].find((n) => n.getBoundingClientRect().width);
      filter(null);
      if (was) was.focus({ preventScroll: true });
    });
  };

  const init = () => {
    document.querySelectorAll(".metro").forEach(metro);
    document.querySelectorAll(".tag-graph").forEach(graph);
    if (document.querySelector(".pr-progress")) {
      rows();
      document.addEventListener("dvq-marks", rows);
      window.addEventListener("storage", rows);
    }
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
