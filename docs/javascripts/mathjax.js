window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
    // no contextual menu: with it every formula is a tab stop (hundreds on a page), and the
    // menu is English; the assistive MathML for screen readers stays (S425)
    enableMenu: false,
  },
};
