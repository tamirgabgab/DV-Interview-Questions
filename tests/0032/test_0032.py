"""Question 0032: checks of the page's numbers (to write) and of the generated blocks."""


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(32)
