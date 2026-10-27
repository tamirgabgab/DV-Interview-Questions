// "Run" panels on question pages: the page's Python code plus an editable demo run in a
// Pyodide web worker (py-worker.js). Opening a panel starts the worker, so Python is
// downloading while the reader reads (W350), and loads the code editor (W349: CodeMirror,
// bundled in vendor/codemirror.min.js; the textarea stays when it cannot load). The output
// reads like a terminal with a copy button and line links in a traceback (W351), every
// commented print() gets a ✓ or ✗ (W352), and the code tabs of the solution get a "run"
// button that opens the panel (W353).
(() => {
  const base = document.currentScript.src;
  const workerUrl = new URL("py-worker.js", base).href;
  const editorUrl = new URL("vendor/codemirror.min.js", base).href;
  let worker = null;
  let workerReady = false;
  let current = null;                 // the panel whose run the worker is doing
  let editorScript = null;

  const loadEditor = () => {
    if (!editorScript) {
      editorScript = new Promise((resolve, reject) => {
        const s = document.createElement("script");
        s.src = editorUrl;
        s.onload = () => (window.dvqEditor ? resolve(window.dvqEditor) : reject(new Error("no editor")));
        s.onerror = reject;
        document.head.appendChild(s);
      });
    }
    return editorScript;
  };

  // One worker for the page; a stop or a failed load drops it, and the next run starts anew.
  const startWorker = () => {
    if (worker) return worker;
    workerReady = false;
    worker = new Worker(workerUrl);
    worker.onmessage = ({ data }) => {
      if (data.type === "stage" && data.stage === "ready") workerReady = true;
      if (current) current.receive(data);
      if (data.load) { worker.terminate(); worker = null; }
    };
    worker.onerror = (e) => {
      if (current) current.receive({ type: "error", text: String(e.message || "Failed to load Python") + "\n", load: true });
      worker = null;
    };
    return worker;
  };

  const setup = (panel) => {
    const pageCode = JSON.parse(panel.querySelector(".py-page-code").textContent);
    const textarea = panel.querySelector(".py-editor");
    const wrap = panel.querySelector(".py-editor-wrap");
    const outWrap = panel.querySelector(".py-output-wrap");
    const output = panel.querySelector(".py-output");
    const status = panel.querySelector(".py-status");
    const stages = panel.querySelector(".py-stages");
    const checksBox = panel.querySelector(".py-checks");
    const runBtn = panel.querySelector(".py-run");
    const stopBtn = panel.querySelector(".py-stop");
    const copyBtn = panel.querySelector(".py-copy");
    const original = textarea.value;
    let editor = null;                  // the CodeMirror wrapper once it has loaded
    let text = "";                      // the plain output, for the copy button

    const code = () => (editor ? editor.value : textarea.value);
    const setStatus = (label, kind, ltr) => {
      status.textContent = label;
      if (ltr) {                                    // a time like "28 ms", kept left to right
        const b = document.createElement("bdi");
        b.dir = "ltr";
        b.textContent = ltr;
        status.append(" ", b);
      }
      status.className = "py-status" + (kind ? ` is-${kind}` : "");
    };
    const setStage = (stage) => {
      const order = ["download", "run"];
      const at = order.indexOf(stage);
      stages.hidden = false;
      stages.querySelectorAll("li").forEach((li, i) => {
        li.classList.toggle("is-done", i < at || (stage === "done" && i === at));
        li.classList.toggle("is-now", i === at && stage !== "done");
      });
    };

    // the output as text, a traceback's "your_code.py", line N as a link to that line
    const write = (chunk, failed) => {
      text += chunk;
      outWrap.hidden = false;
      const re = /File "your_code\.py", line (\d+)/g;
      let last = 0, m;
      const frag = document.createDocumentFragment();
      const span = (s) => {
        const el = document.createElement("span");
        if (failed) el.className = "py-err";
        el.textContent = s;
        return el;
      };
      while ((m = re.exec(chunk))) {
        if (m.index > last) frag.appendChild(span(chunk.slice(last, m.index)));
        const a = document.createElement("button");
        a.type = "button";
        a.className = "py-line-link";
        a.textContent = m[0];
        const line = Number(m[1]);
        a.addEventListener("click", () => (editor ? editor.goToLine(line) : selectLine(line)));
        frag.appendChild(a);
        last = m.index + m[0].length;
      }
      if (last < chunk.length) frag.appendChild(span(chunk.slice(last)));
      output.appendChild(frag);
    };
    const selectLine = (n) => {
      const lines = textarea.value.split("\n");
      if (n < 1 || n > lines.length) return;
      const from = lines.slice(0, n - 1).join("\n").length + (n > 1 ? 1 : 0);
      textarea.focus();
      textarea.setSelectionRange(from, from + lines[n - 1].length);
    };

    const showChecks = (checks) => {
      checksBox.replaceChildren();
      if (editor) editor.setMarks(checks.map((c) => ({ line: c.line, ok: c.ok,
        title: c.ok ? `תואם\u00a0: ${c.expected}` : `התקבל ${c.got}, צפוי ${c.expected}` })));
      if (!checks.length) { checksBox.hidden = true; return; }
      const good = checks.filter((c) => c.ok).length;
      const head = document.createElement("p");
      head.className = "py-checks-head " + (good === checks.length ? "is-ok" : "is-bad");
      head.textContent = good === checks.length
        ? `בדיקת פלט : כל ${checks.length} השורות תואמות לערך שבהערה ✓`
        : `בדיקת פלט : ${good} מתוך ${checks.length} שורות תואמות לערך שבהערה`;
      checksBox.appendChild(head);
      const list = document.createElement("ul");
      checks.filter((c) => !c.ok).forEach((c) => {
        const li = document.createElement("li");
        const ltr = (s) => { const b = document.createElement("code"); b.textContent = s; return b; };
        li.append(`✗ שורה ${c.line} : התקבל `, ltr(c.got), " · צפוי ", ltr(c.expected));
        list.appendChild(li);
      });
      if (list.children.length) checksBox.appendChild(list);
      checksBox.hidden = false;
    };

    const finish = () => {
      runBtn.disabled = false;
      stopBtn.disabled = true;
      if (current === api) current = null;
    };

    const api = {
      receive(data) {
        if (data.type === "stage") {
          if (data.stage === "download" && !workerReady) { setStage("download"); setStatus("מוריד את Python…", "busy"); }
          if (data.stage === "run") { setStage("run"); setStatus("מריץ…", "busy"); }
        } else if (data.type === "out" || data.type === "err") {
          write(data.text, data.type === "err");
        } else if (data.type === "done") {
          stages.hidden = true;
          setStatus("הסתיים ✓", "ok", `${Math.round(data.ms)} ms`);
          showChecks(data.checks || []);
          finish();
        } else if (data.type === "error") {
          write(data.text, true);
          outWrap.classList.add("py-failed");
          stages.hidden = true;
          setStatus(data.load ? "שגיאה בטעינת Python" : "שגיאה", "bad");
          finish();
        }
      },
    };

    const run = () => {
      if (runBtn.disabled) return;
      if (current && current !== api) return;              // another panel is running
      output.replaceChildren();
      text = "";
      outWrap.hidden = true;
      outWrap.classList.remove("py-failed");
      checksBox.hidden = true;
      if (editor) editor.setMarks([]);
      runBtn.disabled = true;
      stopBtn.disabled = false;
      current = api;
      const w = startWorker();
      if (workerReady) { setStage("run"); setStatus("מריץ…", "busy"); }
      else { setStage("download"); setStatus("מוריד את Python…", "busy"); }
      w.postMessage({ solution: pageCode, code: code() });
    };

    runBtn.addEventListener("click", run);
    stopBtn.addEventListener("click", () => {
      if (worker) worker.terminate();
      worker = null;                          // the next run loads a fresh interpreter
      workerReady = false;
      stages.hidden = true;
      setStatus("נעצר", "bad");
      finish();
    });
    panel.querySelector(".py-reset").addEventListener("click", () => {
      if (editor) { editor.value = original; editor.setMarks([]); } else textarea.value = original;
      output.replaceChildren();
      text = "";
      outWrap.hidden = true;
      checksBox.hidden = true;
      stages.hidden = true;
      setStatus("");
    });
    copyBtn.addEventListener("click", () => {
      navigator.clipboard?.writeText(text).then(() => {
        copyBtn.classList.add("is-copied");
        setTimeout(() => copyBtn.classList.remove("is-copied"), 1200);
      }).catch(() => {});
    });

    // the textarea until the editor loads: Tab inserts spaces, Ctrl+Enter runs
    textarea.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const { selectionStart: s, selectionEnd: t } = textarea;
        textarea.setRangeText("    ", s, t, "end");
      } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        run();
      }
    });

    // opening the panel swaps in the editor; a reader's own opening (a click or a key on
    // the summary, or a run button) also starts the download, while "open all" and the
    // page checks open it without fetching Python
    panel.querySelector("summary").addEventListener("click", (e) => {
      if (e.isTrusted && !panel.open) startWorker();
    });
    const opened = () => {
      if (!panel.open) return;
      if (editor || panel.dataset.editor) return;
      panel.dataset.editor = "loading";
      loadEditor().then((cm) => {
        editor = cm.create(wrap, textarea.value, { label: textarea.getAttribute("aria-label"), onRun: run });
        textarea.hidden = true;
        panel.dataset.editor = "ready";
      }).catch(() => { panel.dataset.editor = "textarea"; });
    };
    panel.addEventListener("toggle", opened);
    opened();
    return { panel, open: () => { startWorker(); panel.open = true; opened(); } };
  };

  // W353: a "run" button under each Python and SystemVerilog tab of a solution's code (the
  // statement's signatures get none).
  const runButtons = (target) => {
    document.querySelectorAll(".md-typeset details.success .tabbed-set").forEach((set) => {
      const labels = [...set.querySelectorAll(":scope > .tabbed-labels > label")];
      const blocks = [...set.querySelectorAll(":scope > .tabbed-content > .tabbed-block")];
      labels.forEach((label, i) => {
        const lang = label.textContent.trim();
        const block = blocks[i];
        if (!block || !/^(Python|SystemVerilog)$/.test(lang) || !block.querySelector("pre")) return;
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "py-from-code";
        btn.textContent = lang === "Python" ? "▶ להרצה בדפדפן" : "▶ להרצה (גרסת ה-Python)";
        btn.title = lang === "Python"
          ? "פותח את פאנל ההרצה בסוף העמוד, עם קוד השאלה טעון"
          : "SystemVerilog לא רץ בדפדפן (הוא נבדק ב-Verilator); הפאנל מריץ את גרסת ה-Python";
        btn.addEventListener("click", () => {
          target.open();
          target.panel.scrollIntoView({ behavior: "smooth", block: "start" });
          if (lang !== "Python") {
            const note = target.panel.querySelector(".py-runner-note:last-of-type");
            note?.classList.add("is-flash");
            setTimeout(() => note?.classList.remove("is-flash"), 1600);
          }
        });
        block.appendChild(btn);
      });
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    const panels = [...document.querySelectorAll(".py-runner")].map(setup);
    if (panels.length) runButtons(panels[0]);
  });
})();
