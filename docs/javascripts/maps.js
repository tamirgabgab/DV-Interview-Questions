// The study-path metro map and the tag graph (16-maps.css).
// Both are drawn at build time by hooks/questions.py (maps_metro, maps_tag_graph) and work
// as plain links without this file. Here, the metro map gets the reader's solved marks
// (marks.js; the stations fill, the legend counts them), a tooltip with the question's id
// and title on hover or focus, and the line of a hovered legend entry or station picked
// out; the tag graph picks out a hovered or focused topic and its neighbours, and a click
// on a topic filters the tag lists below to it (the "show all" button brings them back).
(() => {
  const solved = (id) => Boolean(window.dvqMarks && window.dvqMarks.has(id, "solved"));

  const metro = (box) => {
    const scroll = box.querySelector(".mm-scroll");
    const tip = box.querySelector(".mm-tip");
    const svg = box.querySelector(".mm-svg");
    if (!scroll || !tip || !svg) return;

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

    const show = (st) => {
      const name = st.dataset.name || st.getAttribute("aria-label");
      tip.textContent = name;
      tip.hidden = false;
      const dot = st.querySelector("circle").getBoundingClientRect();
      const host = box.getBoundingClientRect();
      const w = tip.offsetWidth;
      const x = Math.min(Math.max(dot.left + dot.width / 2 - host.left - w / 2, 4), host.width - w - 4);
      tip.style.left = `${x}px`;
      const above = dot.top - host.top - tip.offsetHeight - 8;
      tip.style.top = `${above >= 0 ? above : dot.bottom - host.top + 8}px`;
      pick((st.dataset.lines || "").split(" ").filter(Boolean));
    };
    const hide = () => {
      tip.hidden = true;
      pick([]);
    };

    box.querySelectorAll(".mm-st").forEach((st) => {
      st.addEventListener("pointerenter", () => show(st));
      st.addEventListener("pointerleave", hide);
      st.addEventListener("focus", () => show(st));
      st.addEventListener("blur", hide);
    });
    box.querySelectorAll(".mm-key, .mm-badge").forEach((key) => {
      const on = () => pick([key.dataset.line]);
      key.addEventListener("pointerenter", on);
      key.addEventListener("focus", on);
      key.addEventListener("pointerleave", hide);
      key.addEventListener("blur", hide);
    });
    scroll.addEventListener("scroll", () => { tip.hidden = true; }, { passive: true });

    marks();
    document.addEventListener("dvq-marks", marks);
    window.addEventListener("storage", marks);
  };

  const graph = (box) => {
    const status = box.querySelector(".tg-status");
    const text = box.querySelector(".tg-status-text");
    const reset = box.querySelector(".tg-reset");
    const grid = document.querySelector(".tag-grid");
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
      if (grid) grid.hidden = Boolean(tag);
      box.querySelectorAll(".tg-node").forEach((n) => {
        if (n.dataset.tag === tag) n.setAttribute("aria-current", "true"); else n.removeAttribute("aria-current");
      });
      status.hidden = !tag;
      if (shown) {
        const name = shown.querySelector("summary .md-tag");
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
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
