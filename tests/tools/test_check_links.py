"""tools/checks/check_links.py: the external check retries a server error, leaves out the
site's own links and fetches one edit link for all of them."""

import http.server
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "checks"))
import check_links  # noqa: E402


class Flaky(http.server.BaseHTTPRequestHandler):
    """Answers 503 to the first `fails` requests of a path, then 200."""
    fails: dict[str, int] = {}
    seen: dict[str, int] = {}

    def answer(self, body: bool):
        n = Flaky.seen[self.path] = Flaky.seen.get(self.path, 0) + 1
        code = 503 if n <= Flaky.fails.get(self.path, 0) else 200
        self.send_response(code)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_HEAD(self):
        self.answer(False)

    def do_GET(self):
        self.answer(True)

    def log_message(self, *args):
        pass


def serve():
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Flaky)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def test_a_passing_server_error_is_tried_again():
    server, base = serve()
    try:
        Flaky.fails, Flaky.seen = {"/once": 2, "/always": 99}, {}
        # a 503 on HEAD is the answer of that try (only 403, 404, 405, 429, 500, 501 go on to GET)
        assert check_links.fetch(base + "/once", pauses=(0, 0))[1] == 200
        assert check_links.fetch(base + "/always", pauses=(0, 0))[1] == 503
        assert Flaky.seen["/always"] == 3          # three tries
        assert check_links.fetch(base + "/always", pauses=())[1] == 503
    finally:
        server.shutdown()


def test_a_missing_page_is_not_tried_again():
    server, base = serve()
    try:
        Flaky.fails, Flaky.seen = {}, {}
        original = Flaky.answer
        Flaky.answer = lambda self, body: (self.send_response(404), self.send_header("Content-Length", "0"), self.end_headers())
        assert check_links.fetch(base + "/gone", pauses=(0, 0))[1] == 404
    finally:
        Flaky.answer = original
        server.shutdown()


def test_own_links_and_extra_edit_links_are_left_out(tmp_path):
    own = "https://example.github.io/Site/"
    edit = "https://github.com/someone/Site/edit/main/docs/"
    a, b = check_links.Collector(), check_links.Collector()
    a.feed(f'<a href="{own}questions/x/">x</a><a href="{edit}a.md">e</a>'
           '<a href="https://example.com/page#top">ext</a>')
    b.feed(f'<a href="{edit}b.md">e</a><a href="{edit}a.md">e</a><a href="https://example.com/page">ext</a>')
    pages = {tmp_path / "a.html": a, tmp_path / "b.html": b}
    where, own_count, edits = check_links.external_links(pages, tmp_path, own)
    assert sorted(where) == sorted([edit + "a.md", "https://example.com/page"])
    assert (own_count, edits) == (1, 1)
    assert where["https://example.com/page"].startswith("a.html:")


def test_site_url_comes_from_the_home_page(tmp_path):
    (tmp_path / "index.html").write_text('<link rel="canonical" href="https://example.github.io/Site/">')
    assert check_links.site_url(tmp_path) == "https://example.github.io/Site/"
    assert check_links.site_prefix(tmp_path) == "/Site/"
    assert check_links.site_url(tmp_path / "missing") == ""
    assert check_links.site_prefix(tmp_path / "missing") == "/"
