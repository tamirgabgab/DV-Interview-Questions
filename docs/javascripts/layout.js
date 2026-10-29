// The desktop layout (14-layout.css): the list of a level's questions in the side navigation
// folded to the current question behind a button with the count, and the three columns
// (navigation, the page, the table of contents) resized by dragging the grip between them.
// Both are remembered in localStorage; a double click on a grip (or Home on a focused grip)
// gives the column back its default width. Nothing here runs on a phone or a tablet, where
// the navigation is a drawer and the table of contents is hidden.
(() => {
  const FOLD_KEY = "dvq-nav-open";
  const WIDTH_KEY = { nav: "dvq-col-nav", toc: "dvq-col-toc" };
  const VAR = { nav: "--dvq-nav-w", toc: "--dvq-toc-w" };
  const MIN_REM = 10, MAX_REM = 24, PAGE_MIN_REM = 30, STEP_REM = 0.5;
  const store = {
    get: (k) => { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: (k, v) => { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };
  const rem = () => parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;

  // The level's list: folded by default to the page's own question, the button opens it.
  const foldLevel = () => {
    const nav = document.querySelector(".md-sidebar--primary .md-nav__item--section.md-nav__item--active > nav.md-nav");
    const list = nav && nav.querySelector(":scope > .md-nav__list");
    if (!list || nav.querySelector(":scope > .nav-fold")) return;
    const items = list.querySelectorAll(":scope > .md-nav__item");
    if (items.length < 2) return;
    list.id = list.id || "dvq-level-list";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "nav-fold";
    btn.setAttribute("aria-controls", list.id);
    btn.innerHTML = `<span class="nav-fold__text">כל השאלות במשרה</span> <span class="nav-fold__n">${items.length}</span><span class="nav-fold__arrow" aria-hidden="true"></span>`;
    const set = (open) => {
      nav.classList.toggle("is-folded", !open);
      btn.setAttribute("aria-expanded", String(open));
      btn.title = open ? "לקפל את הרשימה לשאלה הנוכחית" : "לפרוס את כל השאלות של המשרה";
    };
    set(store.get(FOLD_KEY) === "1");
    btn.addEventListener("click", () => {
      const open = nav.classList.contains("is-folded");
      store.set(FOLD_KEY, open ? "1" : null);
      set(open);
    });
    list.before(btn);
  };

  // A grip on the inner edge of each sidebar; the width goes into a CSS variable.
  const grips = () => {
    const grid = document.querySelector(".md-main__inner");
    if (!grid) return;
    const sides = { nav: document.querySelector(".md-sidebar--primary"), toc: document.querySelector(".md-sidebar--secondary") };
    const apply = (which, px) => {
      if (px === null) document.documentElement.style.removeProperty(VAR[which]);
      else document.documentElement.style.setProperty(VAR[which], `${Math.round(px)}px`);
    };
    // the bounds: 10 to 24 rem, and never so wide that the page gets under 30 rem
    const bounds = (which) => {
      const r = rem(), other = which === "nav" ? "toc" : "nav";
      const otherW = sides[other] && sides[other].offsetParent ? sides[other].getBoundingClientRect().width : 0;
      const room = grid.getBoundingClientRect().width - otherW - PAGE_MIN_REM * r;
      return [MIN_REM * r, Math.max(MIN_REM * r, Math.min(MAX_REM * r, room))];
    };
    const clamp = (which, px) => { const [lo, hi] = bounds(which); return Math.min(hi, Math.max(lo, px)); };
    const relayout = () => window.dispatchEvent(new Event("resize"));
    Object.entries(sides).forEach(([which, side]) => {
      if (!side) return;
      const saved = Number(store.get(WIDTH_KEY[which]));
      if (saved > 0) apply(which, saved);
      const grip = document.createElement("div");
      grip.className = `col-grip col-grip--${which}`;
      grip.tabIndex = 0;
      grip.setAttribute("role", "separator");
      grip.setAttribute("aria-orientation", "vertical");
      grip.setAttribute("aria-label", which === "nav" ? "רוחב רשימת השאלות: גוררים או חיצים, לחיצה כפולה מחזירה" : "רוחב תוכן העניינים: גוררים או חיצים, לחיצה כפולה מחזירה");
      grip.title = "גוררים כדי לשנות את הרוחב, לחיצה כפולה מחזירה לרוחב הרגיל";
      side.append(grip);
      const width = () => side.getBoundingClientRect().width;
      const label = () => grip.setAttribute("aria-valuenow", String(Math.round(width() / rem())));
      const save = () => { store.set(WIDTH_KEY[which], String(Math.round(width()))); label(); relayout(); };
      const reset = () => { apply(which, null); store.set(WIDTH_KEY[which], null); label(); relayout(); };
      // which way is wider: the grip moving toward the middle of the page, so to the right
      // for the sidebar on the left (+1) and to the left for the one on the right (−1)
      const outward = () => {
        const s = side.getBoundingClientRect(), g = grid.getBoundingClientRect();
        return s.left + s.width / 2 < g.left + g.width / 2 ? 1 : -1;
      };
      grip.addEventListener("pointerdown", (e) => {
        if (e.button !== 0) return;
        e.preventDefault();
        grip.setPointerCapture(e.pointerId);
        const x0 = e.clientX, w0 = width(), dir = outward();
        document.documentElement.classList.add("is-col-dragging");
        const move = (ev) => apply(which, clamp(which, w0 + dir * (ev.clientX - x0)));
        const up = () => {
          grip.removeEventListener("pointermove", move);
          document.documentElement.classList.remove("is-col-dragging");
          save();
        };
        grip.addEventListener("pointermove", move);
        grip.addEventListener("pointerup", up, { once: true });
        grip.addEventListener("pointercancel", up, { once: true });
      });
      grip.addEventListener("dblclick", reset);
      grip.addEventListener("keydown", (e) => {
        const dir = outward();
        const by = e.key === "ArrowLeft" ? -1 : e.key === "ArrowRight" ? 1 : 0;
        if (e.key === "Home") { e.preventDefault(); reset(); return; }
        if (!by) return;
        e.preventDefault();
        apply(which, clamp(which, width() + by * dir * STEP_REM * rem() * (e.shiftKey ? 4 : 1)));
        save();
      });
      label();
    });
    // a saved width that no longer fits (a smaller window) is pulled back in
    window.addEventListener("resize", () => {
      Object.entries(sides).forEach(([which, side]) => {
        if (!side || !store.get(WIDTH_KEY[which]) || !side.offsetParent) return;
        const w = side.getBoundingClientRect().width, c = clamp(which, w);
        if (Math.abs(c - w) > 1) apply(which, c);
      });
    }, { passive: true });
  };

  document.addEventListener("DOMContentLoaded", () => {
    foldLevel();
    grips();
  });
})();
