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
