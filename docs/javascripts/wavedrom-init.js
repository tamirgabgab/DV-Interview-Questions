// Render ```wavedrom fenced blocks (emitted as <pre class="wavedrom">) as timing diagrams,
// then give each diagram the waveform viewer's two buttons (wave-viewer.js, session 31).
// WaveDrom numbers its diagrams in document order (WaveDrom_Display_0, _1, ...), the order
// of the sources kept here.
document.addEventListener("DOMContentLoaded", () => {
  const blocks = document.querySelectorAll("pre.wavedrom");
  if (!blocks.length || typeof WaveDrom === "undefined") return;
  const sources = [];
  blocks.forEach((pre) => {
    const script = document.createElement("script");
    script.type = "WaveDrom";
    script.textContent = pre.textContent;
    sources.push(pre.textContent);
    pre.replaceWith(script);
  });
  WaveDrom.ProcessAll();
  if (!window.dvqWaveViewer) return;
  sources.forEach((text, i) => window.dvqWaveViewer.attach(document.getElementById(`WaveDrom_Display_${i}`), text));
});
