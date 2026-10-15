// "Run" panels on question pages: the page's Python code plus an editable demo run in a
// Pyodide web worker. The worker is created on the first click and reused afterwards.
(() => {
  const workerUrl = new URL("py-worker.js", document.currentScript.src).href;
  let worker = null;

  const setup = (panel) => {
    const pageCode = JSON.parse(panel.querySelector(".py-page-code").textContent);
    const editor = panel.querySelector(".py-editor");
    const output = panel.querySelector(".py-output");
    const status = panel.querySelector(".py-status");
    const runBtn = panel.querySelector(".py-run");
    const stopBtn = panel.querySelector(".py-stop");
    const original = editor.value;

    const finish = (text) => {
      status.textContent = text;
      runBtn.disabled = false;
      stopBtn.disabled = true;
    };

    runBtn.addEventListener("click", () => {
      output.textContent = "";
      output.classList.remove("py-failed");
      runBtn.disabled = true;
      stopBtn.disabled = false;
      status.textContent = worker ? "מריץ…" : "טוען Python לדפדפן…";
      if (!worker) worker = new Worker(workerUrl);
      worker.onmessage = ({ data }) => {
        if (data.type === "out" || data.type === "err") {
          status.textContent = "מריץ…";
          output.textContent += data.text;
        } else if (data.type === "done") {
          finish(`הסתיים (${Math.round(data.ms)} ms)`);
        } else if (data.type === "error") {
          output.textContent += data.text;
          output.classList.add("py-failed");
          finish("שגיאה");
        }
      };
      worker.onerror = (e) => {
        output.textContent += String(e.message || "Failed to load Python") + "\n";
        output.classList.add("py-failed");
        worker = null;
        finish("שגיאה בטעינה");
      };
      worker.postMessage({ solution: pageCode, code: editor.value });
    });

    stopBtn.addEventListener("click", () => {
      if (worker) worker.terminate();
      worker = null;                          // the next run loads a fresh interpreter
      finish("נעצר");
    });

    panel.querySelector(".py-reset").addEventListener("click", () => {
      editor.value = original;
      output.textContent = "";
      status.textContent = "";
    });

    // Tab inserts spaces instead of leaving the editor
    editor.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const { selectionStart: s, selectionEnd: t } = editor;
        editor.setRangeText("    ", s, t, "end");
      }
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".py-runner").forEach(setup);
  });
})();
