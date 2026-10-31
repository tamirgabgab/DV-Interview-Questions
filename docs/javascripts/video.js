// The tutorial video of a question page (V3, VIDEOS.md). The hook writes a "סרטון הסבר"
// page tool and a "לפרק בסרטון" link at the top of each part's solution, both with
// data-video (the YouTube id) and data-video-chapters ([letter, start] pairs); a link also
// has data-video-start and data-video-part. A click opens a modal <dialog> above the page:
// a navy poster with the question's title and a play button, and nothing from YouTube
// until the reader presses it (no request, no cookie). Play puts the youtube-nocookie.com
// player in its place at the chosen chapter, with the Hebrew captions on; the chapter
// buttons start it again at another part. Closing (the button, Esc or a click on the
// backdrop) removes the player, which stops it, and gives the focus back to the button
// that opened the dialog. Tab cycles inside the dialog.
(() => {
  const EMBED = "https://www.youtube-nocookie.com/embed/";
  const PARAMS = "hl=he&rel=0&modestbranding=1&autoplay=1";   // captions: YouTube's own, off by default (the owner, 2026-10-31)
  const NB = " ";

  const clock = (s) => {
    const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
    const pad = (n) => String(n).padStart(2, "0");
    return h ? `${h}:${pad(m)}:${pad(sec)}` : `${m}:${pad(sec)}`;
  };
  const el = (tag, cls, text) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text) e.textContent = text;
    return e;
  };
  const time = (s) => {
    const t = el("span", "vd-time", clock(s));
    t.dir = "ltr";
    return t;
  };

  let dialog = null, opener = null;
  const state = { id: "", chapters: [], start: 0, part: "" };

  const title = () => {
    const h = document.querySelector(".question-header h1");
    return h ? h.textContent.trim() : document.title;
  };
  const qid = () => {
    const t = document.querySelector(".question-tools[data-qid]");
    return t ? t.dataset.qid : "";
  };

  // the poster: what the reader sees before choosing to watch
  const poster = () => {
    const btn = el("button", "vd-poster");
    btn.type = "button";
    const kicker = el("span", "vd-kicker", `שאלה ${qid()} · סרטון הסבר`);
    const name = el("span", "vd-name", title());
    const disc = el("span", "vd-disc");
    disc.setAttribute("aria-hidden", "true");
    const from = el("span", "vd-from");
    if (state.part) from.append(`הפעלה מסעיף ${state.part} · `, time(state.start));
    else if (state.start) from.append("הפעלה מ-", time(state.start));
    else from.append("הפעלה מההתחלה");
    btn.append(kicker, name, disc, from);
    btn.addEventListener("click", play);
    return btn;
  };

  const stage = () => dialog.querySelector(".vd-stage");

  const play = () => {
    const frame = el("iframe", "vd-frame");
    frame.src = `${EMBED}${encodeURIComponent(state.id)}?start=${state.start}&${PARAMS}`;
    frame.title = `סרטון הסבר${NB}: ${title()}`;
    frame.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    frame.allowFullscreen = true;
    frame.referrerPolicy = "strict-origin-when-cross-origin";
    stage().replaceChildren(frame);
    dialog.classList.add("is-playing");
    frame.focus();
  };

  const mark = () => dialog.querySelectorAll(".vd-chapter").forEach((b) => {
    b.setAttribute("aria-pressed", String(Number(b.dataset.start) === state.start));
  });

  // jump to a part: a new player at its start once playing, a new poster before
  const jump = (letter, start) => {
    state.part = letter;
    state.start = start;
    mark();
    if (dialog.classList.contains("is-playing")) play();
    else stage().replaceChildren(poster());
  };

  const build = () => {
    dialog = el("dialog", "vd");
    dialog.setAttribute("aria-labelledby", "vd-title");
    dialog.setAttribute("data-search-exclude", "");
    const head = el("div", "vd-head");
    const h = el("h2", "vd-title");
    h.id = "vd-title";
    const close = el("button", "vd-close");
    close.type = "button";
    close.setAttribute("aria-label", "סגירת הסרטון");
    close.dataset.tip = "סגירה (Esc)";
    close.textContent = "×";
    close.addEventListener("click", () => dialog.close());
    head.append(h, close);
    const chapters = el("div", "vd-chapters");
    chapters.setAttribute("role", "group");
    chapters.setAttribute("aria-label", "פרקי הסרטון");
    const note = el("p", "vd-note", "הסרטון נטען מ-YouTube רק אחרי הלחיצה על הפעלה.");
    dialog.append(head, chapters, el("div", "vd-stage"), note);
    dialog.addEventListener("close", () => {
      stage().replaceChildren();                      // the player goes, and the sound with it
      dialog.classList.remove("is-playing");
      document.documentElement.classList.remove("vd-open");
      if (opener && opener.isConnected) opener.focus();
      opener = null;
    });
    dialog.addEventListener("click", (e) => { if (e.target === dialog) dialog.close(); });   // the backdrop
    dialog.addEventListener("keydown", (e) => {
      if (e.key !== "Tab") return;
      const stops = Array.from(dialog.querySelectorAll("button, iframe")).filter((b) => b.offsetParent !== null);
      if (!stops.length) return;
      const first = stops[0], last = stops[stops.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    document.body.append(dialog);
  };

  const open = (from) => {
    if (!dialog) build();
    opener = from;
    state.id = from.dataset.video;
    try { state.chapters = JSON.parse(from.dataset.videoChapters || "[]"); } catch (e) { state.chapters = []; }
    state.start = Number(from.dataset.videoStart || 0);
    state.part = from.dataset.videoPart || "";
    dialog.querySelector(".vd-title").textContent = `סרטון הסבר${NB}: ${title()}`;
    const row = dialog.querySelector(".vd-chapters");
    row.replaceChildren(...(state.chapters.length > 1 ? state.chapters.map(([letter, start]) => {
      const b = el("button", "vd-chapter");
      b.type = "button";
      b.dataset.start = start;
      b.append(`סעיף ${letter} `, time(start));
      b.addEventListener("click", () => jump(letter, start));
      return b;
    }) : []));
    row.hidden = state.chapters.length < 2;
    dialog.classList.remove("is-playing");
    stage().replaceChildren(poster());
    mark();
    document.documentElement.classList.add("vd-open");
    dialog.showModal();
    dialog.querySelector(".vd-poster").focus();
  };

  document.addEventListener("click", (e) => {
    const from = e.target.closest && e.target.closest("[data-video]");
    if (!from || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    if (typeof HTMLDialogElement !== "function") {    // no dialog: the link goes to YouTube itself
      if (from.tagName !== "A") window.open(`https://www.youtube.com/watch?v=${encodeURIComponent(from.dataset.video)}`, "_blank", "noopener");
      return;
    }
    e.preventDefault();
    open(from);
  });
})();
