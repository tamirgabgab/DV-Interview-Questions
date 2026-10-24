// Question page tools, icon buttons at the end of the header's chip row (UI324): open or
// close every collapsible block (one toggle), practice mode (solutions hidden, with a
// stopwatch), solved / favourite marks (marks.js), a random question of the same level, and
// the hint ladder (hint n+1 appears once hint n is open). A button's name is its
// aria-label and its tooltip (data-tip); `retip` changes both, and the icon with them.
// Practice mode is remembered across pages in localStorage; the stopwatch is per page.
// Marking a question solved shows a short message with the level's progress (UI326).
(() => {
  const KEY = "dvq-practice";
  const SOLUTION = "details.success";

  const pad = (n) => String(n).padStart(2, "0");
  const fmt = (ms) => {
    const s = Math.floor(ms / 1000);
    return `${pad(Math.floor(s / 60))}:${pad(s % 60)}`;
  };

  const retip = (btn, tip, icon) => {
    btn.setAttribute("aria-label", tip);
    btn.dataset.tip = tip;
    if (icon) btn.querySelector(".ui-ico").className = `ui-ico ui-ico-${icon}`;
  };

  // Marking a question solved (UI326): a short message at the bottom of the screen with
  // the progress of its level and a link to the level's next question not solved yet; the
  // check mark pops, and solving the level's last question drops a short confetti. Taking
  // the mark off says so, with an undo. Under prefers-reduced-motion only the message shows.
  const still = () => Boolean(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  const TOAST_MS = 7000;
  let toastTimer = null;
  const toast = (fill) => {
    let t = document.querySelector(".dvq-toast");
    if (!t) {
      t = document.createElement("div");
      t.className = "dvq-toast";
      t.setAttribute("role", "status");
      t.setAttribute("data-search-exclude", "");
      t.addEventListener("mouseenter", () => clearTimeout(toastTimer));
      t.addEventListener("focusin", () => clearTimeout(toastTimer));
      t.addEventListener("mouseleave", () => { if (!t.contains(document.activeElement)) later(t); });
      t.addEventListener("focusout", (e) => { if (!t.contains(e.relatedTarget)) later(t); });
      t.addEventListener("keydown", (e) => { if (e.key === "Escape") t.hidden = true; });
      document.body.append(t);
    }
    t.replaceChildren();
    const body = document.createElement("div");
    body.className = "dt-body";
    fill(body);
    const close = document.createElement("button");
    close.type = "button";
    close.className = "dt-close";
    close.setAttribute("aria-label", "סגירת ההודעה");
    close.textContent = "×";
    close.addEventListener("click", () => { t.hidden = true; });
    t.append(body, close);
    t.hidden = false;
    t.classList.remove("is-in");
    void t.offsetWidth;                                  // restart the entrance
    t.classList.add("is-in");
    later(t);
  };
  const later = (t) => { clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, TOAST_MS); };

  const pop = () => {
    if (still()) return;
    document.querySelectorAll(".qt-solved, .pn-solved").forEach((el) => {
      el.classList.remove("is-pop");
      void el.offsetWidth;
      el.classList.add("is-pop");
      el.addEventListener("animationend", () => el.classList.remove("is-pop"), { once: true });
    });
  };

  const CONFETTI = 40;
  const confetti = () => {
    if (still()) return;
    const layer = document.createElement("div");
    layer.className = "dvq-confetti";
    layer.setAttribute("aria-hidden", "true");
    for (let i = 0; i < CONFETTI; i++) {
      const p = document.createElement("i");
      p.className = `dc-${i % 4}`;
      p.style.setProperty("--x", `${(Math.random() * 100).toFixed(1)}vw`);
      p.style.setProperty("--dx", `${(Math.random() * 16 - 8).toFixed(1)}vw`);
      p.style.setProperty("--r", `${Math.round(Math.random() * 720 - 360)}deg`);
      p.style.setProperty("--d", `${Math.round(Math.random() * 400)}ms`);
      layer.append(p);
    }
    document.body.append(layer);
    setTimeout(() => layer.remove(), 2600);
  };

  const solvedFeedback = (bar, btn, on) => {
    if (!on) {
      toast((body) => {
        body.append(Object.assign(document.createElement("p"), { className: "dt-text", textContent: "הסימון \"פתרתי\" בוטל." }));
        const undo = document.createElement("button");
        undo.type = "button";
        undo.className = "dt-action";
        undo.textContent = "ביטול";
        undo.addEventListener("click", () => btn.click());
        body.append(undo);
      });
      return;
    }
    const ids = (bar.dataset.levelIds || "").split(" ").filter(Boolean);
    const hrefs = JSON.parse(bar.dataset.levelHrefs || "[]");
    const solved = (id) => window.dvqMarks.has(id, "solved");
    const done = ids.filter(solved).length, n = ids.length;
    const all = n > 0 && done === n;
    pop();
    if (all) confetti();
    toast((body) => {
      const text = document.createElement("p");
      text.className = "dt-text";
      text.innerHTML = all
        ? `<b>כל הכבוד!</b> פתרת את כל ${n} השאלות ברמת ${bar.dataset.levelName || ""}.`
        : `<b>כל הכבוד!</b> פתרת ${done} מתוך ${n} שאלות ברמת ${bar.dataset.levelName || ""}.`;
      const meter = document.createElement("span");
      meter.className = "dt-bar";
      meter.setAttribute("aria-hidden", "true");
      meter.innerHTML = `<i style="width:${n ? (100 * done) / n : 0}%"></i>`;
      body.append(text, meter);
      // the level's next question not solved yet, after this one and around
      const at = ids.indexOf(bar.dataset.qid);
      let next = -1;
      for (let k = 1; k <= n && next < 0; k++) {
        const j = (at + k) % n;
        if (!solved(ids[j])) next = j;
      }
      const link = document.createElement("a");
      link.className = "dt-action";
      if (next >= 0) {
        link.href = hrefs[next];
        link.textContent = `לשאלה הבאה שלא פתרת (${ids[next]})`;
      } else {
        link.href = bar.dataset.levelPage || "../";
        link.textContent = `לכל שאלות ${bar.dataset.levelName || "הרמה"}`;
      }
      body.append(link);
    });
  };

  const setup = (bar) => {
    const article = bar.closest("article") || document;
    const details = () => Array.from(article.querySelectorAll("details"));
    const solutions = () => Array.from(article.querySelectorAll(SOLUTION));
    const practiceBtn = bar.querySelector(".qt-practice");
    const clock = bar.querySelector(".qt-clock");
    let start = null, timer = null;

    const setPractice = (on, remember = true) => {
      document.body.classList.toggle("practice-mode", on);
      practiceBtn.classList.toggle("is-active", on);
      practiceBtn.setAttribute("aria-pressed", String(on));
      retip(practiceBtn, on ? "יציאה ממצב תרגול : הצג פתרונות" : "מצב תרגול : הפתרונות מוסתרים ושעון רץ");
      solutions().forEach((d) => { d.hidden = on; if (on) d.open = false; });
      if (remember) {
        try { localStorage.setItem(KEY, on ? "1" : "0"); } catch (e) { /* private mode */ }
      }
      clearInterval(timer);
      if (on) {
        start = Date.now();
        clock.hidden = false;
        clock.textContent = "00:00";
        timer = setInterval(() => { clock.textContent = fmt(Date.now() - start); }, 1000);
      } else if (start) {
        clock.textContent = fmt(Date.now() - start);
      }
      fold.paint();
    };

    // one toggle for every block: it opens all while any visible block is closed
    const foldBtn = bar.querySelector(".qt-fold");
    const fold = {
      allOpen: () => details().filter((d) => !d.hidden).every((d) => d.open),
      paint: () => (fold.allOpen() ? retip(foldBtn, "סגור הכל", "unfold-less") : retip(foldBtn, "פתח הכל", "unfold-more")),
    };
    foldBtn.addEventListener("click", () => {
      const open = !fold.allOpen();
      details().forEach((d) => { if (!d.hidden) d.open = open; });
      fold.paint();
    });
    article.addEventListener("toggle", () => fold.paint(), true);
    fold.paint();
    practiceBtn.addEventListener("click", () => setPractice(!document.body.classList.contains("practice-mode")));

    // Solved / favourite marks
    const qid = bar.dataset.qid;
    const LABEL = { solved: ["סמן כפתורה", "סומנה כפתורה : לחיצה מבטלת"], star: ["הוסף למועדפים", "במועדפים : לחיצה מסירה"] };
    const ICON = { solved: ["solved", "solved-on"], star: ["star", "star-on"] };
    const paint = () => {
      bar.querySelectorAll(".qt-mark").forEach((b) => {
        const on = Boolean(window.dvqMarks && window.dvqMarks.has(qid, b.dataset.mark));
        b.setAttribute("aria-pressed", String(on));
        b.classList.toggle("is-active", on);
        retip(b, LABEL[b.dataset.mark][on ? 1 : 0], ICON[b.dataset.mark][on ? 1 : 0]);
      });
    };
    bar.querySelectorAll(".qt-mark").forEach((b) => {
      b.addEventListener("click", () => {
        if (!window.dvqMarks) return;
        const on = window.dvqMarks.toggle(qid, b.dataset.mark);
        if (b.dataset.mark === "solved") solvedFeedback(bar, b, on);
      });
    });
    document.addEventListener("dvq-marks", paint);
    paint();

    // Random question of the same level (links computed by the hook, relative to this page)
    const random = bar.querySelector(".qt-random");
    if (random) {
      random.addEventListener("click", () => {
        const hrefs = JSON.parse(random.dataset.hrefs || "[]");
        if (hrefs.length) window.location.href = hrefs[Math.floor(Math.random() * hrefs.length)];
      });
    }

    let remembered = false;
    try { remembered = localStorage.getItem(KEY) === "1"; } catch (e) { /* ignore */ }
    if (remembered) setPractice(true, false);
  };

  // Hint ladder: consecutive hint blocks (details.tip whose title starts with "רמז")
  // stay hidden until the previous hint has been opened.
  const ladder = (article) => {
    const hints = Array.from(article.querySelectorAll("details.tip")).filter((d) => {
      const s = d.querySelector("summary");
      return s && s.textContent.trim().startsWith("רמז");
    });
    hints.forEach((h, i) => {
      const next = hints[i + 1];
      if (!next || next.previousElementSibling !== h) return;   // only direct neighbours
      next.classList.add("hint-locked");
      const unlock = () => { if (h.open) next.classList.remove("hint-locked"); };
      h.addEventListener("toggle", unlock);
      unlock();
    });
  };

  // Step-through figures: frames generated by tools/figures/stepper.py, one visible at a time.
  // Each stepper gets an id (stepper-1, stepper-2, ... in page order), a link button that
  // copies a deep link to the current step (#stepper-2-step-5 opens that step), and a swipe
  // on touch screens (left = forward on this RTL page, like the arrow keys).
  const STEP_HASH = /^#(stepper-\d+)-step-(\d+)$/;
  const stepper = (box, index) => {
    const frames = Array.from(box.querySelectorAll(".stepper-frame"));
    const prev = box.querySelector(".stepper-prev");
    const next = box.querySelector(".stepper-next");
    const pos = box.querySelector(".stepper-pos");
    if (!box.id) box.id = `stepper-${index + 1}`;
    let i = 0;
    const show = (k) => {
      i = Math.max(0, Math.min(frames.length - 1, k));
      frames.forEach((f, j) => f.classList.toggle("is-active", j === i));
      prev.disabled = i === 0;
      next.disabled = i === frames.length - 1;
      pos.textContent = `צעד ${i + 1} מתוך ${frames.length}`;
    };
    prev.addEventListener("click", () => show(i - 1));
    next.addEventListener("click", () => show(i + 1));
    const link = document.createElement("button");
    link.type = "button";
    link.className = "stepper-btn stepper-link";
    link.title = "קישור לצעד הזה";
    link.setAttribute("aria-label", "העתקת קישור לצעד הזה");
    link.textContent = "🔗";
    link.addEventListener("click", () => {
      const url = `${location.origin}${location.pathname}#${box.id}-step-${i + 1}`;
      history.replaceState(null, "", `#${box.id}-step-${i + 1}`);
      const done = () => { const keep = pos.textContent; pos.textContent = "הקישור הועתק"; setTimeout(() => { pos.textContent = keep; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done, done); else done();
    });
    pos.after(link);
    let touch = null;
    box.addEventListener("pointerdown", (e) => { touch = e.pointerType === "touch" && !e.target.closest("button") ? [e.clientX, e.clientY] : null; }, { passive: true });
    box.addEventListener("pointerup", (e) => {
      if (!touch) return;
      const dx = e.clientX - touch[0], dy = e.clientY - touch[1];
      touch = null;
      if (Math.abs(dx) > 40 && Math.abs(dx) > 2 * Math.abs(dy)) show(dx < 0 ? i + 1 : i - 1);
    }, { passive: true });
    box.openStep = (k) => {
      let el = box;
      while ((el = el.parentElement)) if (el.tagName === "DETAILS") el.open = true;
      box.classList.remove("hint-locked");
      show(k - 1);
      box.scrollIntoView({ block: "center" });
    };
    box.addEventListener("keydown", (e) => {
      // RTL page: the "forward" arrow key is the left one
      if (e.key === "ArrowLeft" || e.key === " ") { e.preventDefault(); show(i + 1); }
      if (e.key === "ArrowRight") { e.preventDefault(); show(i - 1); }
      if (e.key === "Home") { e.preventDefault(); show(0); }
      if (e.key === "End") { e.preventDefault(); show(frames.length - 1); }
    });
    show(0);
  };

  // Accessibility fixes for markup the theme renders: a name on every code-annotation
  // marker (Material draws them after load, so watch the article), and keyboard access to
  // tables that scroll sideways.
  const annotationNames = (article) => {
    const label = () => article.querySelectorAll(".md-annotation__index:not([aria-label])").forEach((a) => {
      const id = a.querySelector("[data-md-annotation-id]");
      a.setAttribute("aria-label", `הערה ${id ? id.dataset.mdAnnotationId : ""}`.trim());
    });
    new MutationObserver(label).observe(article, { childList: true, subtree: true });
    label();
  };
  const scrollableTables = (article) => {
    article.querySelectorAll(".md-typeset__scrollwrap, pre > code").forEach((w) => {
      if (w.scrollWidth > w.clientWidth + 1 && !w.hasAttribute("tabindex")) {
        w.setAttribute("tabindex", "0");
        w.setAttribute("role", "region");
        w.setAttribute("aria-label", w.tagName === "CODE" ? "קוד רחב, גלילה לרוחב" : "טבלה רחבה, גלילה לרוחב");
      }
    });
  };

  // Comments (giscus): follow the site's light / dark toggle.
  const giscusTheme = () => {
    const frame = document.querySelector("iframe.giscus-frame");
    if (!frame) return;
    const theme = document.body.dataset.mdColorScheme === "slate" ? "dark" : "light";
    frame.contentWindow.postMessage({ giscus: { setConfig: { theme } } }, "https://giscus.app");
  };

  // Printing: every closed block opens (blocks hidden by practice mode stay hidden) and
  // the dark scheme prints light; both are put back afterwards. The boxes are built by
  // core.js on the same event.
  let printed = null;
  window.addEventListener("beforeprint", () => {
    if (printed) return;                               // a second beforeprint before afterprint
    const body = document.body, scheme = body.getAttribute("data-md-color-scheme");
    const opened = Array.from(document.querySelectorAll("article details:not([open])")).filter((d) => !d.hidden);
    opened.forEach((d) => { d.open = true; });
    if (scheme === "slate") body.setAttribute("data-md-color-scheme", "default");
    printed = { opened, scheme };
  });
  window.addEventListener("afterprint", () => {
    if (!printed) return;
    printed.opened.forEach((d) => { d.open = false; });
    if (printed.scheme) document.body.setAttribute("data-md-color-scheme", printed.scheme);
    printed = null;
  });

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("input[name='__palette']").forEach((i) => i.addEventListener("change", () => setTimeout(giscusTheme, 50)));
    document.querySelectorAll(".question-tools").forEach(setup);
    document.querySelectorAll("article").forEach(ladder);
    document.querySelectorAll(".stepper").forEach(stepper);
    const openStepFromHash = () => {
      const m = STEP_HASH.exec(location.hash);
      const box = m && document.getElementById(m[1]);
      if (box && box.openStep) box.openStep(Number(m[2]));
    };
    openStepFromHash();
    window.addEventListener("hashchange", openStepFromHash);
    document.querySelectorAll("article").forEach(annotationNames);
    document.querySelectorAll("article").forEach(scrollableTables);
    window.addEventListener("resize", () => document.querySelectorAll("article").forEach(scrollableTables), { passive: true });
  });
})();
