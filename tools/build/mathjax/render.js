// Math rendered at build time (N9.1): hooks/questions.py sends every formula of the built site
// to this script and puts the HTML it returns into the pages, so the browser loads no MathJax
// and lays out nothing after the load. It runs the npm package mathjax@3.2.2, the same
// components the site loaded from the CDN before (TeX input with autoload, CHTML output, the
// assistive MathML for screen readers), from tools/build/mathjax/node_modules (npm ci there)
// or from the copy in .cache/cdn/mathjax.
//
// stdin: JSON [[tex, display], ...]; stdout: JSON {"html": [the mjx-container of each], "css": the
// stylesheet of every character used}. A formula that fails (a TeX error, or a macro TeX does not
// know) is returned as its error's text in "errors" (index -> message), and the hook stops the
// build.
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../../..");
const places = [path.join(__dirname, "node_modules", "mathjax"), path.join(root, ".cache", "cdn", "mathjax")];
const home = places.find((p) => fs.existsSync(path.join(p, "es5", "node-main.js")));
if (!home) {
  process.stderr.write(`render.js: no mathjax@3.2.2 in ${places.join(" or ")}; run npm ci in tools/build/mathjax\n`);
  process.exit(2);
}
const version = JSON.parse(fs.readFileSync(path.join(home, "package.json"), "utf8")).version;
if (version !== "3.2.2") {
  process.stderr.write(`render.js: mathjax ${version} in ${home}, the site renders with 3.2.2\n`);
  process.exit(2);
}

const input = JSON.parse(fs.readFileSync(0, "utf8"));
require(path.join(home, "es5", "node-main.js")).init({
  loader: { paths: { mathjax: path.join(home, "es5") }, load: ["input/tex", "output/chtml", "a11y/assistive-mml"] },
  // the site's options (docs/javascripts/mathjax.js before N9.1); the fonts stay on the CDN
  tex: { processEscapes: true, processEnvironments: true },
  chtml: { fontURL: "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/output/chtml/fonts/woff-v2" },
  startup: { typeset: false },
}).then(async (MathJax) => {
  const adaptor = MathJax.startup.adaptor;
  const html = [];
  const errors = {};
  for (const [i, [tex, display]] of input.entries()) {
    const out = adaptor.outerHTML(await MathJax.tex2chtmlPromise(tex, { display }));
    // a TeX error, or a macro TeX does not know (drawn in red, as the browser drew it)
    const error = /data-mjx-error="([^"]*)"/.exec(out) || /<mtext mathcolor="red">(\\[^<]*)<\/mtext>/.exec(out);
    if (error) errors[i] = error[0].startsWith("<mtext") ? `Undefined control sequence ${error[1]}` : error[1];
    html.push(out);
  }
  let css = adaptor.textContent(MathJax.chtmlStylesheet());
  // The script box rule belongs to msubsup (and munderover drawn as one), but its selector also
  // pads the script of every plain msub and msup, outside the width MathJax computed for them.
  // In the browser it reached only the pages that hold such an element (21 of 108); one
  // stylesheet for the whole site keeps it to its own elements. (MathJax writes the rule only
  // when an msubsup was rendered.)
  css = css.replace("\nmjx-script {\n", "\nmjx-msubsup > mjx-script, mjx-munderover > mjx-script {\n");
  // In the browser MathJax scaled every formula to the x-height of the text around it, Rubik's
  // over TeX's: 123.4% in every context of the site (all 108 pages with math, both widths; only
  // formulas hidden while the page loaded got 113.1%, a measuring fallback). Nothing is measured
  // here, so the scale is one rule.
  css += '\nmjx-container[jax="CHTML"] {font-size: 123.4%}\n';
  process.stdout.write(JSON.stringify({ html, css, errors }));
}).catch((e) => {
  process.stderr.write(`render.js: ${e && e.stack || e}\n`);
  process.exit(1);
});
