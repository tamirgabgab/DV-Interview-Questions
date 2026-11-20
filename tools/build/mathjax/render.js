// Math rendered at build time (N9.1): hooks/questions.py sends every formula of the built site
// to this script and puts the HTML it returns into the pages, so the browser loads no MathJax
// and lays out nothing after the load. It runs the npm package mathjax@3.2.2, the same
// components the site loaded from the CDN before (TeX input with autoload, CHTML output), from
// tools/build/mathjax/node_modules (npm ci there) or from the copy in .cache/cdn/mathjax.
// Screen readers (N11.1): the assistive MathML copy of every formula doubled its elements (a
// quarter of a math-heavy page), so a formula is one image with a spoken label instead
// (role="img", aria-label from speak() below), its drawn glyphs hidden from the reader.
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

// The label a screen reader says for a formula: its TeX made readable (fractions as a / b, the
// common symbols as their characters, commands without the backslash, no braces).
const SYMBOLS = {
  cdot: "·", times: "×", div: "÷", pm: "±", le: "≤", leq: "≤", ge: "≥", geq: "≥", ne: "≠", neq: "≠",
  approx: "≈", equiv: "≡", to: "→", rightarrow: "→", leftarrow: "←", Rightarrow: "⇒", iff: "⇔",
  infty: "∞", in: "∈", notin: "∉", subseteq: "⊆", cup: "∪", cap: "∩", sum: "sum", prod: "product",
  lfloor: "floor(", rfloor: ")", lceil: "ceiling(", rceil: ")", ldots: "…", dots: "…", cdots: "…",
  oplus: "xor", land: "and", lor: "or", neg: "not", mid: "divides", bmod: "mod", log: "log", ln: "ln",
  alpha: "alpha", beta: "beta", gamma: "gamma", delta: "delta", epsilon: "epsilon", lambda: "lambda",
  mu: "mu", pi: "pi", sigma: "sigma", theta: "theta", phi: "phi", omega: "omega", Delta: "Delta",
  "{": "{", "}": "}", "%": "%", "#": "#", "&": "and", ",": " ", ";": " ", ":": " ", "!": "", " ": " ",
  quad: " ", qquad: " ", left: "", right: "", big: "", Big: "", bigl: "", bigr: "", displaystyle: "",
};
const group = (s, i) => {   // the {...} group starting at s[i] (or one character): [text, next index]
  while (s[i] === " ") i++;
  if (s[i] !== "{") return [s[i] || "", i + 1];
  let depth = 0;
  for (let j = i; j < s.length; j++) {
    if (s[j] === "{" && s[j - 1] !== "\\") depth++;
    else if (s[j] === "}" && s[j - 1] !== "\\" && --depth === 0) return [s.slice(i + 1, j), j + 1];
  }
  return [s.slice(i + 1), s.length];
};
const wrap = (t) => (/^[\w.]+$/.test(t) ? t : `(${t})`);
function speak(tex) {
  let out = "";
  for (let i = 0; i < tex.length;) {
    const c = tex[i];
    if (c === "\\") {
      const m = /^\\([A-Za-z]+|[\s\S]?)/.exec(tex.slice(i));   // a backslash before a line break, or at the end
      const name = m[1];
      i += m[0].length;
      if (name === "frac" || name === "dfrac" || name === "tfrac" || name === "binom") {
        const [a, j] = group(tex, i); const [b, k] = group(tex, j); i = k;
        out += name === "binom" ? ` C(${speak(a)}, ${speak(b)}) ` : ` ${wrap(speak(a))} / ${wrap(speak(b))} `;
      } else if (name === "sqrt") {
        const [a, j] = group(tex, i); i = j; out += ` √${wrap(speak(a))} `;
      } else if (["text", "mathrm", "mathbf", "mathit", "mathtt", "operatorname", "textbf", "mbox", "boldsymbol"].includes(name)) {
        const [a, j] = group(tex, i); i = j; out += ` ${name.startsWith("text") || name === "mbox" ? a : speak(a)} `;
      } else if (name === "pmod") {
        const [a, j] = group(tex, i); i = j; out += ` (mod ${speak(a)}) `;
      } else if (name in SYMBOLS) out += ` ${SYMBOLS[name]} `;
      else out += ` ${name} `;
    } else if (c === "^" || c === "_") {
      const [a, j] = group(tex, i + 1); i = j;
      out += `${c}${wrap(speak(a))}`;
    } else if (c === "{" || c === "}" || c === "&") { out += " "; i++; }
    else { out += c; i++; }
  }
  return out.replace(/\s+/g, " ").replace(/\( /g, "(").replace(/ \)/g, ")").trim();
}

const input = JSON.parse(fs.readFileSync(0, "utf8"));
require(path.join(home, "es5", "node-main.js")).init({
  loader: { paths: { mathjax: path.join(home, "es5") }, load: ["input/tex", "output/chtml"] },
  // the site's options (docs/javascripts/mathjax.js before N9.1); the fonts stay on the CDN
  tex: { processEscapes: true, processEnvironments: true },
  chtml: { fontURL: "https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/output/chtml/fonts/woff-v2" },
  startup: { typeset: false },
}).then(async (MathJax) => {
  const adaptor = MathJax.startup.adaptor;
  const html = [];
  const errors = {};
  for (const [i, [tex, display]] of input.entries()) {
    const node = await MathJax.tex2chtmlPromise(tex, { display });
    adaptor.setAttribute(node, "role", "img");
    adaptor.setAttribute(node, "aria-label", speak(tex));
    adaptor.setAttribute(adaptor.firstChild(node), "aria-hidden", "true");
    const out = adaptor.outerHTML(node);
    // a TeX error, or a macro TeX does not know (drawn in red, as the browser drew it)
    // (the macro's name is the red text: one mjx-c per character, its code point in the class)
    const error = /data-mjx-error="([^"]*)"/.exec(out);
    const red = /<mjx-mtext[^>]*style="color: red;">(.*?)<\/mjx-mtext>/.exec(out);
    if (error) errors[i] = error[1];
    else if (red) {
      const name = [...red[1].matchAll(/mjx-c([0-9A-F]+)/g)].map((m) => String.fromCodePoint(parseInt(m[1], 16))).join("");
      if (name.startsWith("\\")) errors[i] = `Undefined control sequence ${name}`;
    }
    html.push(out);
  }
  if (process.env.DVQ_SPEAK) for (const [tex] of input) process.stderr.write(`${tex}  =>  ${speak(tex)}\n`);
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
