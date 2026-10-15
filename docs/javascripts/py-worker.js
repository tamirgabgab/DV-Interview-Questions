// Web worker that runs Python with Pyodide, so a long or endless run never freezes the page.
const PYODIDE = "https://cdn.jsdelivr.net/npm/pyodide@0.26.4/";
importScripts(PYODIDE + "pyodide.js");

const ready = loadPyodide({ indexURL: PYODIDE }).then((py) => {
  py.setStdout({ batched: (text) => postMessage({ type: "out", text: text + "\n" }) });
  py.setStderr({ batched: (text) => postMessage({ type: "err", text: text + "\n" }) });
  return py;
});

// Keep only the user's part of a traceback (drop Pyodide's internal frames).
const cleanTraceback = (text) => {
  const lines = text.split("\n");
  const first = lines.findIndex((l) => /File "(solution|your_code)\.py"/.test(l));
  return first < 0 ? text : ["Traceback (most recent call last):", ...lines.slice(first)].join("\n");
};

onmessage = async (event) => {
  const py = await ready;
  const globals = py.globals.get("dict")();       // fresh namespace for every run
  const start = performance.now();
  try {
    await py.runPythonAsync(event.data.solution, { globals, filename: "solution.py" });
    await py.runPythonAsync(event.data.code, { globals, filename: "your_code.py" });
    postMessage({ type: "done", ms: performance.now() - start });
  } catch (err) {
    postMessage({ type: "error", text: cleanTraceback(String(err.message || err)), ms: performance.now() - start });
  } finally {
    globals.destroy();
  }
};
