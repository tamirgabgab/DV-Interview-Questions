"""The search text of a question (tools/search_text.py): TeX in plain symbols, and only the
statement and the parts' statements of a page."""

import re

import pytest

import search_text
from extract_code import ROOT

LRI, PDI = "\u2066", "\u2069"


@pytest.mark.parametrize("tex, text", [
    (r"\( a < b \)", "a < b"),
    (r"\( O(n \log n) \)", "O(n log n)"),
    (r"\( 2^n - 1 \)", "2ⁿ − 1"),
    (r"\( \frac{n}{2} \le k \)", "n/2 ≤ k"),
    (r"\( \frac{n(n+1)}{2} \)", "(n(n + 1))/2"),
    (r"\( \binom{n}{k} \)", "C(n, k)"),
    (r"\( m \times n \)", "m × n"),
    (r"\( x_{i+1} = x_i \oplus 1 \)", "xᵢ₊₁ = xᵢ ⊕ 1"),
    (r"\( \lfloor \log_2 n \rfloor + 1 \)", "⌊log₂ n⌋ + 1"),
    (r"\( 2^{L-1-z} \)", "2^(L − 1 − z)"),
    (r"\( f(-1, -2) \)", "f(−1, −2)"),
    (r"\( a \equiv b \pmod{m} \)", "a ≡ b (mod m)"),
    (r"\( d \in \{0, 1\} \)", "d ∈ {0, 1}"),
    (r"\( \text{rate}_{w} \)", "rate_w"),
    (r"\[ \sum_{i=1}^{n} i \]", "Σᵢ₌₁ⁿ i"),
])
def test_tex_to_text(tex, text):
    assert search_text.tex_to_text(tex) == text


PAGE = """<div class="question-header"><h1>T</h1><div class="qh-top">0001 קל</div></div>
<h2 id="_1">השאלה<a class="headerlink" href="#_1">&para;</a></h2>
<p>נתון מערך של <span class="arithmatex">\\( n \\)</span> מספרים<strong>שלמים</strong>.</p>
<ul><li>סעיף א : הראשון</li><li>סעיף ב : השני</li></ul>
<div class="highlight"><pre><code>int f();</code></pre></div>
<details class="interviewer"><summary>מה המראיין בודק</summary><p>סוד</p></details>
<h3 id="_2">סעיף א – פשוט<a class="headerlink" href="#_2">&para;</a></h3>
<p>כתבו פתרון בזמן <span class="arithmatex">\\( O(n^2) \\)</span>.</p>
<details class="tip"><summary>רמז 1</summary><p>רמז סודי</p></details>
<details class="success"><summary>פתרון</summary><h4>הרעיון</h4><p>פתרון סודי</p></details>
<h2 id="_9">נקודות חשובות ושאלות המשך</h2><p>מלכודת סודית</p>
"""


def test_statement_sections_keep_only_the_statements():
    sections = search_text.statement_sections(PAGE)
    assert [(a, t) for a, t, _ in sections] == [("_1", "השאלה"), ("_2", "סעיף א – פשוט")]
    statement, part = sections[0][2], sections[1][2]
    assert f"של {LRI}n{PDI} מספרים" in statement
    assert "<p>סעיף א : הראשון</p><p>סעיף ב : השני</p>" in statement
    assert part == f"<p>כתבו פתרון בזמן {LRI}O(n²){PDI}.</p>"
    text = "".join(t for _, _, t in sections)
    assert "סוד" not in text and "int f" not in text and "0001" not in text


def test_every_page_has_a_statement_without_tex():
    pages = sorted((ROOT / "site" / "questions").glob("*/*/index.html"))
    if not pages:
        pytest.skip("no built site")
    for page in pages:
        sections = search_text.statement_sections(page.read_text(encoding="utf-8"))
        assert sections and sections[0][1] == "השאלה" and sections[0][2], page
        for _, _, text in sections:
            assert not re.search(r"\\[A-Za-z(\[]", text), (page, text)
