// Web worker that runs Python with Pyodide, so a long or endless run never freezes the page.
// The panel creates it when it opens (W350), so the interpreter is downloading while the
// reader reads; it reports "stage" messages, then runs each request through py_run.py (the
// same file the tests run): the page code as the module `solution`, the reader's code, and
// the check of every commented print().
const PYODIDE = "https://cdn.jsdelivr.net/npm/pyodide@0.26.4/";

postMessage({ type: "stage", stage: "download" });
importScripts(PYODIDE + "pyodide.js");

const ready = Promise.all([
  loadPyodide({ indexURL: PYODIDE }),
  fetch(new URL("py_run.py", self.location.href)).then((r) => {
    if (!r.ok) throw new Error(`py_run.py: HTTP ${r.status}`);
    return r.text();
  }),
]).then(([py, source]) => {
  py.setStdout({ batched: (text) => postMessage({ type: "out", text: text + "\n" }) });
  py.setStderr({ batched: (text) => postMessage({ type: "err", text: text + "\n" }) });
  const ns = py.globals.get("dict")();
  py.runPython(source, { globals: ns, filename: "py_run.py" });
  postMessage({ type: "stage", stage: "ready" });
  return { py, run: ns.get("run") };
});
ready.catch((err) => postMessage({ type: "error", text: String(err.message || err) + "\n", load: true }));

// Keep only the user's part of a traceback (drop Pyodide's and py_run.py's frames).
const cleanTraceback = (text) => {
  const lines = text.split("\n");
  const first = lines.findIndex((l) => /File "(solution|your_code)\.py"/.test(l));
  return first < 0 ? text : ["Traceback (most recent call last):", ...lines.slice(first)].join("\n");
};

onmessage = async (event) => {
  const { py, run } = await ready;
  postMessage({ type: "stage", stage: "run" });
  const start = performance.now();
  try {
    const result = run(event.data.solution, event.data.code);
    const checks = result.toJs({ dict_converter: Object.fromEntries });
    result.destroy();
    postMessage({ type: "done", ms: performance.now() - start, checks });
  } catch (err) {
    postMessage({ type: "error", text: cleanTraceback(String(err.message || err)), ms: performance.now() - start });
  }
  py.runPython("import gc; gc.collect()");
};
