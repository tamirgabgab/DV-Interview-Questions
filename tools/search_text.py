"""The text of a question page for the site search: the statement and the statement of
each part, without hints, solutions, code, figures, boxes or traps, and with the math
written in plain symbols ("O(n)", "a < b", "2ⁿ − 1") instead of its TeX source.

    statement_sections(html) -> [(anchor, title, text_html), ...]
    tex_to_text(r"\\frac{n}{2} \\le k") -> "n/2 ≤ k"

hooks/questions.py calls both while it builds the search index (on_post_page, on_post_build).
"""
from __future__ import annotations

import html
import re
from html.parser import HTMLParser

# --- TeX to plain symbols ------------------------------------------------------------------

SYMBOLS = {
    "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "ne": "≠", "neq": "≠", "lt": "<", "gt": ">",
    "times": "×", "cdot": "·", "div": "÷", "pm": "±", "mp": "∓", "ast": "∗", "star": "⋆",
    "circ": "∘", "bullet": "•", "oplus": "⊕", "otimes": "⊗", "land": "∧", "wedge": "∧",
    "lor": "∨", "vee": "∨", "neg": "¬", "lnot": "¬", "to": "→", "rightarrow": "→",
    "Rightarrow": "⇒", "implies": "⇒", "leftarrow": "←", "Leftarrow": "⇐", "gets": "←",
    "leftrightarrow": "↔", "Leftrightarrow": "⇔", "iff": "⇔", "mapsto": "↦", "uparrow": "↑",
    "downarrow": "↓", "approx": "≈", "equiv": "≡", "sim": "~", "simeq": "≃", "cong": "≅",
    "propto": "∝", "infty": "∞", "partial": "∂", "nabla": "∇", "sum": "Σ", "prod": "Π",
    "int": "∫", "in": "∈", "notin": "∉", "ni": "∋", "subset": "⊂", "subseteq": "⊆",
    "supset": "⊃", "supseteq": "⊇", "cup": "∪", "cap": "∩", "setminus": "∖", "emptyset": "∅",
    "varnothing": "∅", "forall": "∀", "exists": "∃", "lfloor": "⌊", "rfloor": "⌋",
    "lceil": "⌈", "rceil": "⌉", "langle": "⟨", "rangle": "⟩", "mid": "|", "vert": "|",
    "lvert": "|", "rvert": "|", "Vert": "‖", "lVert": "‖", "rVert": "‖", "parallel": "∥",
    "perp": "⊥", "angle": "∠", "triangle": "△", "ldots": "…", "dots": "…", "cdots": "⋯",
    "vdots": "⋮", "ddots": "⋱", "prime": "′", "degree": "°", "%": "%", "#": "#", "&": "&",
    "_": "_", "$": "$", "{": "{", "}": "}", "|": "‖", "lbrace": "{", "rbrace": "}",
    "backslash": "\\", "ell": "ℓ", "hbar": "ℏ", "Re": "ℜ", "Im": "ℑ", "aleph": "ℵ",
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε", "varepsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "ϑ", "iota": "ι", "kappa": "κ",
    "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π", "varpi": "ϖ", "rho": "ρ",
    "varrho": "ϱ", "sigma": "σ", "varsigma": "ς", "tau": "τ", "upsilon": "υ", "phi": "φ",
    "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω", "Gamma": "Γ", "Delta": "Δ",
    "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ",
    "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω", "ll": "≪", "gg": "≫", "blacksquare": "∎",
    "square": "□", "qed": "∎", "checkmark": "✓",
}
# words that keep their name: \log n -> "log n"
NAMED = {"log", "ln", "lg", "exp", "min", "max", "sup", "inf", "lim", "gcd", "lcm", "deg",
         "det", "dim", "ker", "arg", "sin", "cos", "tan", "cot", "sec", "csc", "Pr", "mod",
         "bmod", "liminf", "limsup", "argmin", "argmax"}
SPACES = {",": " ", ";": " ", ":": " ", "!": "", " ": " ", "quad": " ", "qquad": " ",
          "enspace": " ", "thinspace": " ", "medspace": " ", "thickspace": " "}
# commands whose argument is shown as is
TEXT_ARG = {"text", "textrm", "textbf", "textit", "texttt", "textsf", "mathrm", "mathbf",
            "mathit", "mathtt", "mathsf", "mathcal", "mathscr", "boldsymbol", "bm",
            "operatorname", "mbox", "hbox", "overline", "underline", "bar", "hat", "widehat",
            "tilde", "widetilde", "vec", "dot", "ddot", "overbrace", "underbrace", "boxed",
            "displaystyle", "textstyle", "scriptstyle", "color", "mathbb", "mathbin", "mathrel", "mathop"}
BLACKBOARD = {"N": "ℕ", "Z": "ℤ", "Q": "ℚ", "R": "ℝ", "C": "ℂ", "P": "ℙ", "E": "𝔼"}
DROP = {"left", "right", "big", "Big", "bigg", "Bigg", "bigl", "bigr", "Bigl", "Bigr",
        "biggl", "biggr", "nonumber", "notag", "limits", "nolimits", "displaystyle",
        "textstyle", "middle", "phantom", "label", "not"}
SUP = dict(zip("0123456789+-−=()nikmxyjtpTabcdeor", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻⁼⁽⁾ⁿⁱᵏᵐˣʸʲᵗᵖᵀᵃᵇᶜᵈᵉᵒʳ"))
SUB = dict(zip("0123456789+-−=()ijkmnxtpaeor", "₀₁₂₃₄₅₆₇₈₉₊₋₋₌₍₎ᵢⱼₖₘₙₓₜₚₐₑₒᵣ"))


def _group(s: str, i: int) -> tuple[str, int]:
    """The argument at s[i]: a {...} group (nested), or one character or command."""
    while i < len(s) and s[i] == " ":
        i += 1
    if i >= len(s):
        return "", i
    if s[i] == "{":
        depth, j = 0, i
        while j < len(s):
            if s[j] == "\\":
                j += 2
                continue
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    return s[i + 1:j], j + 1
            j += 1
        return s[i + 1:], len(s)
    if s[i] == "\\":
        m = re.match(r"\\([A-Za-z]+|.)", s[i:])
        return m.group(0), i + len(m.group(0))
    return s[i], i + 1


def _atom(t: str) -> bool:
    """A short value that needs no parentheses around it (n, 2k, x_1, (a+b))."""
    return bool(re.fullmatch(r"[\w.′ⁿ⁰-⁹₀-₉]+|\(.*\)|\[.*\]|\{.*\}|\|.*\|", t))


def _script(t: str, table: dict, mark: str) -> str:
    if t and all(c in table for c in t):
        return "".join(table[c] for c in t)
    return mark + (t if len(t) == 1 or _atom(t) else f"({t})")


def _convert(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            name, i = m.group(1), i + len(m.group(0))
            if name == "\\":                       # a line break of aligned
                out.append("; ")
            elif name in SPACES:
                out.append(SPACES[name])
            elif name in ("frac", "dfrac", "tfrac", "cfrac"):
                a, i = _group(s, i)
                b, i = _group(s, i)
                a, b = _convert(a).strip(), _convert(b).strip()
                out.append(f"{a if _atom(a) else '(' + a + ')'}/{b if _atom(b) else '(' + b + ')'}")
            elif name in ("binom", "dbinom", "tbinom", "choose"):
                a, i = _group(s, i)
                b, i = _group(s, i)
                out.append(f"C({_convert(a).strip()}, {_convert(b).strip()})")
            elif name == "sqrt":
                root = ""
                if i < len(s) and s[i] == "[":
                    j = s.index("]", i)
                    root, i = _convert(s[i + 1:j]), j + 1
                a, i = _group(s, i)
                a = _convert(a).strip()
                out.append((_script(root, SUP, "") if root else "") + "√" + (a if _atom(a) else f"({a})"))
            elif name == "pmod":
                a, i = _group(s, i)
                out.append(f" (mod {_convert(a).strip()})")
            elif name == "mathbb":
                a, i = _group(s, i)
                out.append("".join(BLACKBOARD.get(ch, ch) for ch in a))
            elif name in ("color", "textcolor"):
                _, i = _group(s, i)                 # the colour name
                if name == "textcolor":
                    a, i = _group(s, i)
                    out.append(_convert(a))
            elif name in ("begin", "end"):
                _, i = _group(s, i)
                if i < len(s) and s[i] == "{" and name == "begin":   # array column spec
                    _, i = _group(s, i)
            elif name in TEXT_ARG:
                a, i = _group(s, i)
                out.append(_convert(a) if name not in ("text", "textrm", "mbox", "hbox", "texttt")
                           else re.sub(r"\\([%#&_${}])", r"\1", a))
            elif name in DROP:
                pass
            elif name in NAMED:
                out.append(("mod" if name == "bmod" else name) + " ")
            elif name in SYMBOLS:
                out.append(SYMBOLS[name])
            else:                                   # unknown: its name, never a backslash
                out.append(name)
        elif c in "^_":
            a, i = _group(s, i + 1)
            a = _convert(a).strip()
            out.append(_script(a, SUP if c == "^" else SUB, c))
        elif c in "{}":
            i += 1
        elif c == "&":
            out.append(" ")
            i += 1
        elif c == "~":
            out.append(" ")
            i += 1
        elif c == "-":
            out.append("−")
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def tex_to_text(tex: str) -> str:
    """TeX math (with or without its \\( \\) or \\[ \\] delimiters) in plain symbols."""
    tex = tex.strip()
    tex = re.sub(r"^\\[(\[]|\\[)\]]$", "", tex).strip()
    text = _convert(tex)
    text = re.sub(r"\s*([=<>≤≥≠≈≡→⇒⇔+×÷±−])\s*", r" \1 ", text)   # even spacing around operators
    text = re.sub(r"(^|[(\[{]|[,;=<>≤≥≠] )\s*− ", r"\1−", text)       # a unary minus stays close
    text = re.sub(r"\b(%s)\s+([₀-₉]+)" % "|".join(sorted(NAMED)), r"\1\2", text)   # log₂ n
    text = re.sub(r"\s+([,;.)\]}⌋⌉])", r"\1", text)
    text = re.sub(r"([(\[{⌊⌈])\s+", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


# --- the statement of a page ---------------------------------------------------------------

SKIP_TAGS = {"details", "pre", "svg", "figure", "script", "style", "nav", "button", "form",
             "input", "select", "textarea", "template", "noscript", "iframe"}
SKIP_CLASSES = {"admonition", "highlight", "tabbed-set", "explorer", "headerlink",
                "question-header", "question-tools", "path-nav", "part-nav", "viz-legend",
                "md-source-file", "fig-wrap", "sol-map"}
BLOCK = {"p", "li", "tr", "h2", "h3", "h4", "div", "ul", "ol", "table", "blockquote", "dd", "dt"}
VOID = {"br", "img", "input", "hr", "meta", "link", "wbr", "source", "col", "area", "base"}
STATEMENT = "השאלה"
PART = re.compile(r"^סעיף\b")


class _Statement(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.skip_at: int | None = None      # stack depth of the element being skipped
        self.math_at: int | None = None
        self.math: list[str] = []
        self.heading: dict | None = None     # {"tag", "id", "text"} while inside h2/h3
        self.sections: list[dict] = []       # {"id", "title", "paras": [[(kind, text)]]}
        self.state = "before"                # before, in, after

    def _para(self):
        if self.state == "in" and self.sections and self.sections[-1]["paras"][-1]:
            self.sections[-1]["paras"].append([])

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            if tag == "br":
                self._para()
            return
        self.stack.append(tag)
        if self.skip_at is not None or self.state == "after":
            return
        a = dict(attrs)
        classes = set((a.get("class") or "").split())
        if tag in ("h2", "h3"):
            self.heading = {"tag": tag, "id": a.get("id", ""), "text": ""}
            return
        if self.state != "in":
            return
        if tag in SKIP_TAGS or classes & SKIP_CLASSES or "data-search-exclude" in a:
            self.skip_at = len(self.stack)
        elif "arithmatex" in classes:
            self.math_at, self.math = len(self.stack), []
        elif tag in BLOCK:
            self._para()

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack:
            return
        depth = len(self.stack)
        while self.stack and self.stack.pop() != tag:   # tolerate a missing end tag
            depth -= 1
        if self.skip_at is not None:
            if depth <= self.skip_at:
                self.skip_at = None
            return
        if self.math_at is not None and depth <= self.math_at:
            self.math_at = None
            self._emit("math", tex_to_text("".join(self.math)))
            return
        if self.heading and tag == self.heading["tag"]:
            h, self.heading = self.heading, None
            title = re.sub(r"\s+", " ", h["text"]).strip().rstrip("¶").strip()
            if h["tag"] == "h2":
                if title == STATEMENT and self.state == "before":
                    self.state = "in"
                elif self.state == "in":
                    self.state = "after"
                    return
            if self.state == "in" and (title == STATEMENT or (h["tag"] == "h3" and PART.match(title))):
                self.sections.append({"id": h["id"], "title": title, "paras": [[]]})
            return
        if self.state == "in" and tag in BLOCK:
            self._para()

    def _emit(self, kind, text):
        if self.state == "in" and self.sections and text:
            self.sections[-1]["paras"][-1].append((kind, text))

    def handle_data(self, data):
        if self.skip_at is not None:
            return
        if self.heading is not None:
            self.heading["text"] += data
        elif self.math_at is not None:
            self.math.append(data)
        else:
            self._emit("text", data)


def _render(paras: list[list[tuple[str, str]]]) -> str:
    out = []
    for para in paras:
        parts = []
        for kind, text in para:
            if kind == "math":
                # left to right in an isolate: the search results drop markup like <bdi>
                parts.append(f"\u2066{html.escape(text, quote=False)}\u2069")
            else:
                parts.append(html.escape(re.sub(r"\s+", " ", text), quote=False))
        line = re.sub(r"\s+", " ", "".join(parts)).strip()
        if line:
            out.append(f"<p>{line}</p>")
    return "".join(out)


def statement_sections(page_html: str) -> list[tuple[str, str, str]]:
    """The statement ("השאלה") and each part ("סעיף ...") of a built question page as
    (anchor, title, text as HTML paragraphs); hints, solutions, code, figures, boxes and
    everything from the next h2 on are left out."""
    p = _Statement()
    p.feed(page_html)
    p.close()
    return [(s["id"], s["title"], _render(s["paras"])) for s in p.sections]
