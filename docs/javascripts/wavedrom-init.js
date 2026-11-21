// Render ```wavedrom fenced blocks (emitted as <pre class="wavedrom">) as timing diagrams,
// then give each diagram the waveform viewer's two buttons (wave-viewer.js, session 31).
// WaveDrom numbers its diagrams in document order (WaveDrom_Display_0, _1, ...), the order
// of the sources kept here.

// The site's look for the diagrams (round 11.1). The CDN's default skin draws black lines and
// blue names in Helvetica on an inline white rectangle, so in the dark scheme a diagram was a
// white slab, and its <style> (text{...}, .s1{...}) reached every svg of the page, the site's
// own figures included. Before the diagrams render, its shapes' classes get a "wd-" prefix and
// its style is replaced by rules drawn from the figure palette (02-pages.css, 08-explorers.css),
// so they follow both schemes. The text is the site's at 13 px: WaveDrom sizes the names'
// column from Helvetica's widths at 11pt, which a wider face (the code font) overflows. The shapes are drawn through <use>, whose copies have no
// ancestor in the page, so their rules match the class alone; the rest is scoped to a diagram.
(function siteSkin() {
  const skin = window.WaveSkin && window.WaveSkin.default;
  if (!skin || skin[2][0] !== "style") return;
  const d = '[id^="svgcontent_"]';
  const prefix = (el) => {
    if (!Array.isArray(el)) return;
    const attrs = el[1];
    if (attrs && typeof attrs === "object" && !Array.isArray(attrs)) {
      if (/^s\d+$/.test(attrs.class || "")) attrs.class = `wd-${attrs.class}`;
      if (el[0] === "marker") attrs.style = "fill:var(--viz-s1)";
    }
    el.forEach(prefix);
  };
  prefix(skin[3]);
  const line = "fill:none;stroke:var(--viz-ink);stroke-linecap:round;stroke-linejoin:miter";
  const tint = (v) => `fill:color-mix(in srgb,var(${v}) 24%,transparent);stroke:none`;
  skin[2][2] = [
    `${d} text{font-family:var(--md-text-font-family),sans-serif;font-size:13px;fill:var(--viz-ink)}`,
    `${d} .info{fill:var(--viz-ink);font-weight:600}`,
    `${d} .muted{fill:var(--viz-text)}`,
    `.wd-s1,.wd-s4{${line};stroke-width:1.25}`,
    `.wd-s2{${line};stroke-width:0.6}`,
    `.wd-s3{${line};stroke-width:1;stroke-dasharray:1,3}`,
    ".wd-s5{fill:var(--md-default-bg-color);stroke:none}",
    ".wd-s6{fill:var(--viz-ink);stroke:none}",
    ".wd-s7{fill:var(--site-primary-soft);stroke:none}",
    `.wd-s8,.wd-s9{${tint("--viz-s2")}}`, `.wd-s10,.wd-s11{${tint("--viz-s1")}}`,
    `.wd-s12{${tint("--viz-s3")}}`, `.wd-s13{${tint("--viz-s4")}}`, `.wd-s14{${tint("--viz-s5")}}`,
    ".wd-s15{fill:var(--viz-s1);stroke:none}", ".wd-s16{fill:none;stroke:var(--viz-s1)}",
    // the white rectangle under each diagram and the grid's grey dots are inline styles
    `${d} [id^="waves_"]>rect:first-child{fill:none!important}`,
    `${d} [id^="gmarks_"]>g{stroke:var(--viz-text)!important;stroke-opacity:0.55}`,
  ].join("");
})();

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
