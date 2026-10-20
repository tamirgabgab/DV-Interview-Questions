"""Question 0032: tests of the page's Python code (it runs as published)."""

from extract_code import load_python


def test_page_code_loads():
    ns = load_python(32)
    assert ns, "the page has no Python block yet"
