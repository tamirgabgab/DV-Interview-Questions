// The quick jump (session 30): a small window that finds a question by its number, its
// title or a topic and opens it. Ctrl+K (Cmd+K on a Mac) and "/" open it from any page,
// as do the button beside the header's search, the hero's large field and its ready
// searches. The site search over the whole text stays where it was; the last row of the
// list sends the typed words there. The list comes from questions.json
// (dvqInterview.loadIndex, interview.js); the matching is dvqInterview.match.
(() => {
  const NB = " ";
  const MAX = 8;
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const editable = (el) => el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName));
  const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
  const KEYS = isMac ? "⌘K" : "Ctrl K";

  let box = null, input = null, list = null, rows = [], sel = 0, back = null, data = null, failed = false;

  // the site search, with the words typed in (the same way the hero's field used to open it)
  const siteSearch = (q) => {
    const toggle = document.getElementById("__search"), field = document.querySelector(".md-search__input");
    if (toggle && !toggle.checked) { toggle.checked = true; toggle.dispatchEvent(new Event("change")); }
    if (!field) return;
    field.focus();
    if (q) {
      field.value = q;
      field.dispatchEvent(new Event("input", { bubbles: true }));
      field.dispatchEvent(new KeyboardEvent("keyup", { bubbles: true }));
    }
  };

  const build = () => {
    box = document.createElement("div");
    box.className = "qj";
    box.hidden = true;
    box.setAttribute("data-search-exclude", "");
    box.innerHTML =
      '<div class="qj-panel" role="dialog" aria-modal="true" aria-labelledby="qj-title">' +
      `<p class="qj-title" id="qj-title">קפיצה לשאלה</p>` +
      '<div class="qj-field"><svg class="qj-ico" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14"/></svg>' +
      '<input class="qj-input" id="qj-input" type="text" role="combobox" aria-expanded="true" aria-controls="qj-list" aria-autocomplete="list" ' +
      'autocomplete="off" spellcheck="false" placeholder="מספר, שם או נושא, למשל 59 או FIFO" aria-label="מספר, שם או נושא של שאלה">' +
      '<button type="button" class="qj-close" aria-label="Esc, סגירה">Esc</button></div>' +
      '<ul class="qj-list" id="qj-list" role="listbox" aria-label="שאלות שמתאימות"></ul>' +
      `<p class="qj-foot" aria-hidden="true"><span><kbd>↑</kbd> <kbd>↓</kbd> לבחירה</span><span><kbd>Enter</kbd> לפתיחה</span><span><kbd>Esc</kbd> לסגירה</span><span><kbd>${KEYS}</kbd> מכל דף</span></p>` +
      "</div>";
    document.body.append(box);
    input = box.querySelector(".qj-input");
    list = box.querySelector(".qj-list");
    input.addEventListener("input", render);
    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
      else if (e.key === "Home" && rows.length && !input.value) { e.preventDefault(); move(-sel); }
      else if (e.key === "Enter") { e.preventDefault(); go(sel); }
    });
    box.addEventListener("keydown", (e) => {
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); }
      if (e.key === "Tab") {                       // keep the focus inside: the field and the close button
        const close_ = box.querySelector(".qj-close");
        e.preventDefault();
        (document.activeElement === input ? close_ : input).focus();
      }
    });
    box.querySelector(".qj-close").addEventListener("click", close);
    box.addEventListener("mousedown", (e) => { if (e.target === box) close(); });
    list.addEventListener("click", (e) => {
      const li = e.target.closest("li[role=option]");
      if (li) go(Number(li.dataset.i));
    });
    list.addEventListener("mousemove", (e) => {
      const li = e.target.closest("li[role=option]");
      if (li && Number(li.dataset.i) !== sel) { sel = Number(li.dataset.i); paintSel(); }
    });
  };

  const I = () => window.dvqInterview;

  // the rows: matching questions, then "search the whole text"; with nothing typed, the
  // last question opened in this browser
  const render = () => {
    const q = input.value.trim();
    rows = [];
    if (data && q) I().match(data.qs, q, MAX).forEach((r) => rows.push({ kind: "q", r }));
    if (!q) {
      let lastOpen = null;
      try { lastOpen = JSON.parse(localStorage.getItem("dvq-last") || "null"); } catch (e) { /* none */ }
      if (lastOpen && lastOpen.url) rows.push({ kind: "last", last: lastOpen });
    } else rows.push({ kind: "search", q });
    sel = 0;
    const lower = q.toLowerCase();
    const mark = (title) => {
      const at = lower ? title.toLowerCase().indexOf(lower) : -1;
      if (at < 0) return esc(title);
      return esc(title.slice(0, at)) + "<mark>" + esc(title.slice(at, at + q.length)) + "</mark>" + esc(title.slice(at + q.length));
    };
    let html = rows.map((row, i) => {
      if (row.kind === "q") {
        const r = row.r, L = data.levels[r[I().LEVEL]], D = data.diffs[r[I().DIFF]];
        const topics = r[I().TAGS].slice(0, 3).join(", ");
        return `<li role="option" id="qj-o${i}" data-i="${i}" aria-selected="false" class="qj-q">` +
          `<span class="qj-id">${esc(r[I().ID])}</span><span class="qj-text"><span class="qj-name">${mark(r[I().TITLE])}</span>` +
          `<span class="qj-meta">${esc(L)}, ${esc(D)}${topics ? `. ${esc(topics)}` : ""}</span></span></li>`;
      }
      if (row.kind === "last") {
        return `<li role="option" id="qj-o${i}" data-i="${i}" aria-selected="false" class="qj-q">` +
          `<span class="qj-id">${esc(row.last.id || "")}</span><span class="qj-text"><span class="qj-name">${esc(row.last.title || "")}</span>` +
          `<span class="qj-meta">השאלה האחרונה שפתחתם</span></span></li>`;
      }
      return `<li role="option" id="qj-o${i}" data-i="${i}" aria-selected="false" class="qj-all">` +
        `<span class="qj-id" aria-hidden="true">…</span><span class="qj-text"><span class="qj-name">לחפש את "${esc(row.q)}" בכל הטקסט של האתר</span></span></li>`;
    }).join("");
    if (q && rows.length === 1) {
      html = `<li class="qj-none" role="presentation">${failed ? "רשימת השאלות לא נטענה. אפשר לחפש בכל הטקסט." : `אין שאלה עם המספר, השם או הנושא האלה${NB}: נסו מילה אחרת.`}</li>` + html;
    }
    if (!q && !rows.length) html = `<li class="qj-none" role="presentation">הקלידו מספר שאלה, מילה מהשם שלה או נושא.</li>`;
    list.innerHTML = html;
    paintSel();
  };
  const paintSel = () => {
    list.querySelectorAll("li[role=option]").forEach((li) => li.setAttribute("aria-selected", String(Number(li.dataset.i) === sel)));
    const cur = list.querySelector(`#qj-o${sel}`);
    input.setAttribute("aria-activedescendant", cur ? cur.id : "");
    if (cur) cur.scrollIntoView({ block: "nearest" });
  };
  const move = (d) => {
    if (!rows.length) return;
    sel = (sel + d + rows.length) % rows.length;
    paintSel();
  };
  const go = (i) => {
    const row = rows[i];
    if (!row) return;
    if (row.kind === "search") { close(false); siteSearch(row.q); return; }
    const url = row.kind === "q" ? I().siteUrl(row.r[I().URL]) : row.last.url;
    close(false);
    window.location.href = url;
  };

  const open = (text = "") => {
    if (!box) build();
    if (box.hidden) back = document.activeElement;
    box.hidden = false;
    document.documentElement.classList.add("qj-open");
    input.value = text;
    render();
    input.focus();
    if (!data && I()) {
      I().loadIndex().then((d) => { data = d; failed = false; if (!box.hidden) render(); })
        .catch(() => { failed = true; if (!box.hidden) render(); });
    }
  };
  const close = (restore = true) => {
    if (!box || box.hidden) return;
    box.hidden = true;
    document.documentElement.classList.remove("qj-open");
    if (restore && back && back.focus) back.focus();
  };
  window.dvqQuickJump = { open, close };

  // Ctrl/Cmd+K anywhere, and "/" outside a text field (before Material's own "/" key,
  // which focuses the site search: this listener runs first, on the window's capture)
  window.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && !e.altKey && !e.shiftKey && (e.key === "k" || e.key === "K" || e.code === "KeyK")) {
      e.preventDefault();
      e.stopImmediatePropagation();
      if (box && !box.hidden) close(); else open();
      return;
    }
    if (e.key === "/" && !e.ctrlKey && !e.metaKey && !e.altKey && !editable(e.target) && !(box && !box.hidden)) {
      const search = document.getElementById("__search");
      if (search && search.checked) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      open();
    }
  }, true);

  // a button beside the header's search
  document.addEventListener("DOMContentLoaded", () => {
    const anchor = document.querySelector('.md-header__inner label.md-header__button[for="__search"]');
    if (!anchor) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "md-header__button md-icon qj-btn";
    btn.setAttribute("aria-label", `קפיצה לשאלה (${KEYS})`);
    btn.title = `קפיצה לשאלה (${KEYS})`;
    btn.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 3h2l-.6 4h4l.6-4h2l-.6 4H18v2h-3.9l-.6 4H17v2h-3.8l-.6 4h-2l.6-4h-4l-.6 4h-2l.6-4H2.5v-2h3.9l.6-4H4v-2h3.4zm1.1 6-.6 4h4l.6-4z"/></svg>';
    btn.addEventListener("click", () => open());
    anchor.before(btn);
  });
})();
