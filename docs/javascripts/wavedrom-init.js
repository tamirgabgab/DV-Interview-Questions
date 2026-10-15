// Render ```wavedrom fenced blocks (emitted as <pre class="wavedrom">) as timing diagrams.
document.addEventListener("DOMContentLoaded", () => {
  const blocks = document.querySelectorAll("pre.wavedrom");
  if (!blocks.length || typeof WaveDrom === "undefined") return;
  blocks.forEach((pre) => {
    const script = document.createElement("script");
    script.type = "WaveDrom";
    script.textContent = pre.textContent;
    pre.replaceWith(script);
  });
  WaveDrom.ProcessAll();
});
