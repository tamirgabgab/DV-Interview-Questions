// Question page tools, icon buttons at the end of the header's chip row (UI324): open or
// close every collapsible block (one toggle), interview mode (session 30, it replaced
// practice mode: see `interview` below), solved / favourite marks (marks.js), a random
// question of the same level, and the hint ladder (hint n+1 appears once hint n is open).
// A button's name is its aria-label and its tooltip (data-tip); `retip` changes both, and
// the icon with them. Interview mode is remembered across pages in localStorage (the key
// kept its old name); the clock is per page.
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
  // check mark pops, and solving the level's last question drops a short confetti; so does
  // completing a study path, with its own message and a link to the next path. Taking
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
    // a study path whose questions are now all solved (W348): its own message and confetti
    const paths = JSON.parse(bar.dataset.paths || "[]");
    const path = paths.find((p) => p.ids.length > 1 && p.ids.every(solved));
    if (path) {
      confetti();
      toast((body) => {
        const text = document.createElement("p");
        text.className = "dt-text";
        const b = document.createElement("b");
        b.textContent = "כל הכבוד!";
        text.append(b, ` סיימת את המסלול "${path.title}"\u00a0: כל ${path.ids.length} השאלות שלו פתורות.`);
        const meter = document.createElement("span");
        meter.className = "dt-bar";
        meter.setAttribute("aria-hidden", "true");
        meter.innerHTML = '<i style="width:100%"></i>';
        body.append(text, meter);
        const link = document.createElement("a");
        link.className = "dt-action";
        link.href = path.next ? path.next.href : path.href;
        link.textContent = path.next ? `למסלול הבא\u00a0: ${path.next.title}` : "לדף המסלול";
        body.append(link);
      });
      return;
    }
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
    const iv = interview(bar, article, practiceBtn, () => fold.paint());
    // one toggle for every block: it opens all while any visible block is closed
    const foldBtn = bar.querySelector(".qt-fold");
    const fold = {
      // in interview mode a solution opens only through its confidence question
      shown: () => details().filter((d) => !d.hidden && !(iv.on() && d.matches(SOLUTION))),
      allOpen: () => fold.shown().every((d) => d.open),
      paint: () => {
        const open = fold.allOpen();
        retip(foldBtn, open ? "סגור הכל" : "פתח הכל", open ? "unfold-less" : "unfold-more");
        const name = foldBtn.querySelector(".qt-name");   // its name on a touch screen (S420)
        if (name) name.textContent = open ? "סגור הכל" : "פתח הכל";
      },
    };
    foldBtn.addEventListener("click", () => {
      const open = !fold.allOpen();
      fold.shown().forEach((d) => { d.open = open; });
      fold.paint();
    });
    article.addEventListener("toggle", () => fold.paint(), true);
    fold.paint();
    practiceBtn.addEventListener("click", () => (iv.on() ? iv.end() : iv.start(true)));

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

    // a series from the home page's interview builder, or the mode left on: start at once
    let remembered = false;
    try { remembered = localStorage.getItem(KEY) === "1"; } catch (e) { /* ignore */ }
    if (iv.inPlan() || remembered) iv.start(false);
  };

  // Interview mode (session 30): a bar at the foot of the screen with a clock against the
  // question's target time (dvqInterview.targetMinutes: by difficulty, more for every part
  // beyond the third), the hints opened and the self-checks answered right; a solution
  // opens only after "how sure are you?"; a right self-check brings the next of the page's
  // follow-up questions as the interviewer's question, its short answer folded; "end"
  // shows a summary beside the last interview of this question (kept in the browser), and
  // within a series from the home page's builder, a link to the series' next question.
  const CONF = ["מנחשים", "די בטוחים", "בטוחים"];
  const interview = (bar, article, btn, repaint) => {
    const I = window.dvqInterview;
    const qid = bar.dataset.qid;
    const target = I ? I.targetMinutes(bar.dataset.difficulty, bar.dataset.parts) : 15;
    let on = false, running = false, startAt = 0, acc = 0, ticker = null;
    let hints = new Set(), right = new Set(), conf = [], asked = new WeakSet(), fuNext = 0;
    let ui = null;
    const secs = () => Math.floor((acc + (running ? Date.now() - startAt : 0)) / 1000);
    const followups = () => {
      const f = article.querySelector("details.followup");
      return f ? Array.from(f.querySelectorAll(":scope > ul > li")) : [];
    };
    const checks = () => article.querySelectorAll(".selfcheck").length;
    const planNow = () => {
      const p = I && I.plan.get();
      if (!p || !Array.isArray(p.ids)) return null;
      const i = p.ids.indexOf(qid);
      return i < 0 ? null : { ...p, i };
    };

    const makeBar = () => {
      const el = document.createElement("div");
      el.className = "iv-bar";
      el.hidden = true;
      el.setAttribute("role", "region");
      el.setAttribute("aria-label", "מצב ראיון");
      el.setAttribute("data-search-exclude", "");
      el.innerHTML = '<div class="iv-in">' +
        '<span class="iv-step" hidden></span>' +
        '<span class="iv-clock" role="timer" aria-label="הזמן שעבר">00:00</span>' +
        '<span class="iv-gauge" aria-hidden="true"><i></i></span>' +
        `<span class="iv-stat">יעד <b>${target}</b> דקות</span>` +
        '<span class="iv-stat">רמזים <b class="iv-hints">0</b></span>' +
        `<span class="iv-stat iv-stat-right">נכונות <b class="iv-right">0</b>${checks() ? ` מתוך ${checks()}` : ""}</span>` +
        '<button type="button" class="iv-btn iv-pause">השהיה</button>' +
        '<button type="button" class="iv-btn iv-end">סיום הראיון</button></div>';
      document.body.append(el);
      el.querySelector(".iv-pause").addEventListener("click", pause);
      el.querySelector(".iv-end").addEventListener("click", end);
      return el;
    };
    const tick = () => {
      const s = secs();
      ui.querySelector(".iv-clock").textContent = I ? I.fmt(s) : String(s);
      ui.querySelector(".iv-clock").classList.toggle("is-over", s > target * 60);
      ui.querySelector(".iv-gauge i").style.transform = `scaleX(${Math.min(1, s / (target * 60))})`;
    };
    const count = () => {
      ui.querySelector(".iv-hints").textContent = hints.size;
      ui.querySelector(".iv-right").textContent = right.size;
    };
    const pause = () => {
      const b = ui.querySelector(".iv-pause");
      if (running) { acc += Date.now() - startAt; running = false; b.textContent = "להמשיך"; }
      else { startAt = Date.now(); running = true; b.textContent = "השהיה"; }
      tick();
    };
    const paintBtn = () => {
      document.body.classList.toggle("interview-mode", on);
      btn.classList.toggle("is-active", on);
      btn.setAttribute("aria-pressed", String(on));
      retip(btn, on ? "סיום הראיון : סיכום של הזמן, הרמזים והתשובות" : "מצב ראיון : שעון מול יעד, רמזים נספרים ושאלות המשך");
      repaint();
    };
    const start = (remember) => {
      if (on) return;
      if (!ui) ui = makeBar();
      on = true; running = true; startAt = Date.now(); acc = 0;
      hints = new Set(); right = new Set(); conf = []; asked = new WeakSet(); fuNext = 0;
      article.querySelectorAll(".iv-follow, .iv-conf").forEach((el) => el.remove());
      article.querySelectorAll(SOLUTION).forEach((d) => { d.open = false; });
      const p = planNow(), step = ui.querySelector(".iv-step");
      step.hidden = !p;
      if (p) step.textContent = `שאלה ${p.i + 1} מתוך ${p.ids.length}`;
      ui.querySelector(".iv-pause").textContent = "השהיה";
      ui.hidden = false;
      if (remember) { try { localStorage.setItem(KEY, "1"); } catch (e) { /* private mode */ } }
      count(); tick();
      clearInterval(ticker);
      ticker = setInterval(tick, 1000);
      paintBtn();
    };
    const plural = (n, one, many) => (n === 1 ? one : `${n} ${many}`);
    const summary = (rec, prev) => {
      const old = article.querySelector(".iv-summary");
      if (old) old.remove();
      const box = document.createElement("section");
      box.className = "iv-summary";
      box.tabIndex = -1;
      box.setAttribute("aria-labelledby", "iv-sum-title");
      box.setAttribute("data-search-exclude", "");
      const over = rec.secs > rec.target * 60;
      const confText = rec.conf.length ? rec.conf.map((c) => CONF[c] || "בלי תשובה").join(", ") : "–";
      let advice;
      if (over) advice = "עברתם את היעד. בראיון, תנו קודם תשובה חלקית שעובדת, ואחר כך שפרו אותה.";
      else if (rec.hints) advice = "בזמן, עם רמזים. בראיון, אמרו בקול מה ניסיתם לפני שאתם מבקשים רמז.";
      else advice = "בזמן ובלי רמזים. נסו עכשיו את שאלות ההמשך בסוף הדף.";
      let html = '<p class="iv-sum-title" id="iv-sum-title" role="heading" aria-level="2">סיכום הראיון</p>' +
        '<dl class="iv-sum-grid">' +
        `<div><dt>זמן</dt><dd>${I.fmt(rec.secs)}<span class="iv-of"> מתוך ${rec.target} דקות</span></dd></div>` +
        `<div><dt>רמזים</dt><dd>${rec.hints}</dd></div>` +
        `<div><dt>בדיקות נכונות</dt><dd>${rec.right}${rec.checks ? `<span class="iv-of"> מתוך ${rec.checks}</span>` : ""}</dd></div>` +
        `<div><dt>ביטחון לפני הפתרון</dt><dd class="iv-conf-list">${confText}</dd></div></dl>` +
        `<p class="iv-advice">${advice}</p>`;
      if (prev && Number.isFinite(prev.secs)) {
        const when = new Date(prev.at || Date.now()).toLocaleDateString("he-IL", { day: "numeric", month: "long" });
        html += `<p class="iv-prev">בפעם הקודמת (${when}) : ${I.fmt(prev.secs)}, ${plural(prev.hints, "רמז אחד", "רמזים")}` +
          `${prev.checks ? `, ${prev.right} מתוך ${prev.checks} נכונות` : ""}.</p>`;
      }
      const p = planNow();
      html += '<p class="iv-sum-actions">';
      if (p && p.i + 1 < p.ids.length) {
        html += `<a class="md-button md-button--primary iv-next" href="${p.urls[p.i + 1]}">לשאלה הבאה בראיון (${p.i + 2} מתוך ${p.ids.length})</a>` +
          '<button type="button" class="md-button iv-stop">לעצור את הסדרה</button>';
      } else if (p) {
        html += '<span class="iv-done">סיימתם את כל הסדרה. כל הכבוד!</span>';
        I.plan.clear();
      }
      html += '<button type="button" class="md-button iv-close">סגירת הסיכום</button></p>';
      box.innerHTML = html;
      const header = article.querySelector(".question-header");
      (header || article.firstElementChild).after(box);
      const stop = box.querySelector(".iv-stop");
      if (stop) stop.addEventListener("click", () => { I.plan.clear(); stop.closest(".iv-sum-actions").querySelector(".iv-next").remove(); stop.remove(); });
      box.querySelector(".iv-close").addEventListener("click", () => { box.remove(); btn.focus(); });
      box.focus({ preventScroll: true });
      box.scrollIntoView({ block: "start", behavior: still() ? "auto" : "smooth" });
    };
    const end = () => {
      if (!on) return;
      const rec = { at: Date.now(), secs: secs(), target, hints: hints.size, right: right.size, checks: checks(), conf };
      clearInterval(ticker);
      on = false; running = false;
      ui.hidden = true;
      article.querySelectorAll(".iv-conf").forEach((el) => el.remove());
      try { localStorage.setItem(KEY, "0"); } catch (e) { /* private mode */ }
      paintBtn();
      if (!I) return;
      const prev = I.last.get(qid);
      I.last.set(qid, rec);
      summary(rec, prev);
    };

    // hints opened while the interview runs, each once
    article.addEventListener("toggle", (e) => {
      const d = e.target;
      if (!on || !d.open || !d.matches || !d.matches("details.tip")) return;
      const s = d.querySelector("summary");
      if (s && s.textContent.trim().startsWith("רמז") && !hints.has(d)) { hints.add(d); count(); }
    }, true);

    // a solution: "how sure are you?" first
    article.addEventListener("click", (e) => {
      const summaryEl = e.target.closest("summary");
      const d = summaryEl && summaryEl.parentElement;
      if (!on || !d || !d.matches(SOLUTION) || d.open || asked.has(d)) return;
      e.preventDefault();
      if (d.previousElementSibling && d.previousElementSibling.classList.contains("iv-conf")) {
        d.previousElementSibling.querySelector("button").focus();
        return;
      }
      const ask = document.createElement("div");
      ask.className = "iv-conf";
      ask.setAttribute("role", "group");
      const id = `iv-conf-${Math.random().toString(36).slice(2, 8)}`;
      ask.setAttribute("aria-labelledby", id);
      ask.innerHTML = `<p id="${id}">לפני הפתרון : כמה אתם בטוחים בתשובה שלכם?</p><p class="iv-conf-opts">` +
        CONF.map((c, i) => `<button type="button" class="md-button" data-c="${i}">${c}</button>`).join("") +
        '<button type="button" class="md-button iv-conf-none" data-c="3">עוד אין לי תשובה</button></p>';
      d.before(ask);
      ask.querySelector("button").focus();
      ask.addEventListener("click", (ev) => {
        const b = ev.target.closest("button[data-c]");
        if (!b) return;
        conf.push(Number(b.dataset.c));
        asked.add(d);
        ask.remove();
        d.open = true;
        d.querySelector("summary").focus();
      });
    }, true);

    // a right self-check: the interviewer asks the next follow-up
    document.addEventListener("dvq-selfcheck", (e) => {
      const { box, ok } = e.detail || {};
      if (!on || !ok || !box || !article.contains(box) || right.has(box)) return;
      right.add(box);
      count();
      const items = followups();
      if (fuNext >= items.length) return;
      const li = items[fuNext++];
      const say = document.createElement("div");
      say.className = "iv-follow";
      say.setAttribute("data-search-exclude", "");
      const bubble = document.createElement("div");
      bubble.className = "iv-bubble";
      bubble.innerHTML = '<p class="iv-who-name">המראיין שואל</p>';
      Array.from(li.children).forEach((c) => bubble.append(c.cloneNode(true)));
      bubble.querySelectorAll("details").forEach((d) => { d.open = false; });
      say.innerHTML = '<span class="iv-who" aria-hidden="true">מ</span>';
      say.append(bubble);
      box.after(say);
      // math in a copy that MathJax had not reached yet (the copy of typeset math is left as it is)
      if (window.MathJax && window.MathJax.typesetPromise) window.MathJax.typesetPromise([bubble]).catch(() => {});
    });

    return { on: () => on, start, end, inPlan: () => Boolean(planNow()) };
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
    // M8: a run of two hints or more gets a row of dots above it, one per hint, filled
    // once that hint has been opened (a picture only; the hints keep their own titles).
    const runs = [];
    hints.forEach((h, i) => {
      if (i && h.previousElementSibling === hints[i - 1]) runs[runs.length - 1].push(h);
      else runs.push([h]);
    });
    runs.filter((run) => run.length > 1).forEach((run) => {
      const row = document.createElement("p");
      row.className = "hint-dots";
      row.setAttribute("aria-hidden", "true");
      row.innerHTML = `<span>רמזים</span>${run.map(() => "<i></i>").join("")}`;
      run[0].before(row);
      const dots = row.querySelectorAll("i");
      run.forEach((h, i) => {
        const fill = () => { if (h.open) dots[i].classList.add("is-on"); };
        h.addEventListener("toggle", fill);
        fill();
      });
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

  // Printing: every closed block opens (hidden blocks stay hidden) and
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
