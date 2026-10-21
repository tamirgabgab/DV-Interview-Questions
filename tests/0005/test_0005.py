from extract_code import load_python

ns = load_python(5)
bfs, enum = ns["smallest_01_multiple"], ns["by_enumeration"]


def test_page_examples():
    assert bfs(7) == "1001"
    assert bfs(9) == "111111111"
    assert bfs(1) == "1"
    assert len(bfs(9999)) == 36


def test_bfs_is_a_01_multiple():
    for x in range(1, 2000):
        y = bfs(x)
        assert set(y) <= {"0", "1"} and y[0] == "1" and int(y) % x == 0, x


def test_bfs_is_minimal():
    # The enumeration is minimal by construction; compare where it is fast enough.
    for x in range(1, 300):
        y = bfs(x)
        if len(y) <= 16:
            assert y == enum(x), x


def test_chart_steps_match_page_code():
    """The step counts behind the chart: the generator's BFS equals the page code, and the
    other two counts follow from the answer (y / x multiples, y read as binary)."""
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0005

    for x in q0005.XS:
        y = bfs(x)
        assert q0005.smallest_01_multiple(x)[0] == y
        assert q0005.steps(x)[:2] == (int(y) // x, int(y, 2))
    assert [q0005.steps(x)[2] for x in q0005.XS] == [4, 8, 89, 899, 8999]   # the page table


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(5)
