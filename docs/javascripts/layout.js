// The desktop layout (14-layout.css): the list of a level's questions in the side navigation
// folded to the current question behind a button with the count, and the three columns
// (navigation, the page, the table of contents) resized by dragging the grip between them.
// Both are remembered in localStorage; a double click on a grip (or Home on a focused grip)
// gives the column back its default width. Neither runs on a phone or a tablet, where
// the navigation is a drawer and the table of contents is hidden; there the closed drawer
// and the closed search are taken out of the Tab order instead (hiddenChrome).
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
    // the section of the study paths lists paths, not questions
    const first = list.querySelector("a.md-nav__link[href]");
    const paths = !!first && /(^|\/)paths\//.test(new URL(first.getAttribute("href"), location.href).pathname);
    const all = paths ? "כל המסלולים" : "כל השאלות במשרה";
    btn.innerHTML = `<span class="nav-fold__text">${all}</span> <span class="nav-fold__n">${items.length}</span><span class="nav-fold__arrow" aria-hidden="true"></span>`;
    const set = (open) => {
      nav.classList.toggle("is-folded", !open);
      btn.setAttribute("aria-expanded", String(open));
      btn.title = open ? (paths ? "לקפל את הרשימה למסלול הנוכחי" : "לקפל את הרשימה לשאלה הנוכחית")
        : (paths ? "לפרוס את כל המסלולים" : "לפרוס את כל השאלות של המשרה");
    };
    set(store.get(FOLD_KEY) === "1");
    btn.addEventListener("click", () => {
      const open = nav.classList.contains("is-folded");
      store.set(FOLD_KEY, open ? "1" : null);
      set(open);
      window.dispatchEvent(new Event("resize"));   // the titles now shown are fitted to the column
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
    // a saved width that no longer fits (a smaller window) is pulled back in, on load too
    const fit = () => {
      Object.entries(sides).forEach(([which, side]) => {
        if (!side || !store.get(WIDTH_KEY[which]) || !side.offsetParent) return;
        const w = side.getBoundingClientRect().width, c = clamp(which, w);
        if (Math.abs(c - w) > 1) apply(which, c);
      });
    };
    fit();
    window.addEventListener("resize", fit, { passive: true });
  };

  // On a phone the closed drawer and the closed search are off the screen but were still in
  // the Tab order, so Tab walked into links nobody could see. The drawer is inert while it
  // is closed; the search's field and result list leave the Tab order (tabindex -1, so
  // Material can still focus the field when the search opens).
  const hiddenChrome = () => {
    const drawer = document.getElementById("__drawer"), search = document.getElementById("__search");
    const side = document.querySelector(".md-sidebar--primary");
    const narrowNav = window.matchMedia("(max-width: 76.234375em)");      // Material's drawer
    const narrowSearch = window.matchMedia("(max-width: 59.984375em)");   // the field folded into an icon
    const sync = () => {
      if (side && drawer) {
        const hide = narrowNav.matches && !drawer.checked;
        if (hide) side.setAttribute("inert", ""); else side.removeAttribute("inert");
      }
      if (search) {
        const closed = !search.checked;
        document.querySelectorAll(".md-search__scrollwrap").forEach((el) => el.setAttribute("tabindex", closed ? "-1" : "0"));
        document.querySelectorAll(".md-search__input, .md-search__options :is(a, button)").forEach((el) => {
          if (closed && narrowSearch.matches) el.setAttribute("tabindex", "-1"); else el.removeAttribute("tabindex");
        });
      }
    };
    const later = () => requestAnimationFrame(sync);
    [drawer, search].forEach((t) => t && t.addEventListener("change", later));
    document.addEventListener("click", later, true);    // Material also sets the toggles without a change event
    document.addEventListener("keyup", later, true);
    narrowNav.addEventListener("change", sync);
    narrowSearch.addEventListener("change", sync);
    sync();
  };

  document.addEventListener("DOMContentLoaded", () => {
    foldLevel();
    grips();
    hiddenChrome();
  });
})();
