# ABOUTME: Tests for check_redirects.py: valid, broken, and shadowing redirect rules.
# ABOUTME: Exercises main(argv) with tmp site dirs and tmp _redirects fixture files.

import textwrap
from pathlib import Path


def _write_redirects(tmp_path: Path, content: str) -> Path:
    """Write a _redirects fixture file and return its path."""
    p = tmp_path / "_redirects"
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


def _make_site_page(site_dir: Path, url_path: str) -> None:
    """Create a built-site page (index.html under url_path) in site_dir."""
    page = site_dir / url_path.lstrip("/")
    page.mkdir(parents=True, exist_ok=True)
    (page / "index.html").write_text("<html></html>", encoding="utf-8")


def _make_site_file(site_dir: Path, rel: str) -> None:
    """Create an exact file in site_dir (e.g. index.xml)."""
    f = site_dir / rel.lstrip("/")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("data", encoding="utf-8")


# ---------------------------------------------------------------------------
# main() contract: valid rule → exit 0
# ---------------------------------------------------------------------------

def test_valid_rule_exits_0(tmp_path):
    """A redirect whose target exists in the built site must exit 0."""
    import check_redirects

    site_dir = tmp_path / "site"
    _make_site_page(site_dir, "/media/books/")

    redirects = _write_redirects(tmp_path, """\
        /books/ /media/books/ 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0


def test_external_target_exits_0(tmp_path):
    """A redirect to an http(s) URL must exit 0 (no local file check)."""
    import check_redirects

    site_dir = tmp_path / "site"
    site_dir.mkdir()

    redirects = _write_redirects(tmp_path, """\
        /old/ https://external.example.com/new/ 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0


def test_missing_target_exits_1(tmp_path):
    """A redirect whose target page is absent from the built site must exit 1."""
    import check_redirects

    site_dir = tmp_path / "site"
    site_dir.mkdir()

    redirects = _write_redirects(tmp_path, """\
        /old/ /new-missing/ 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 1


def test_shadowing_rule_exits_1(tmp_path):
    """A redirect whose source URL also exists as a real page must exit 1."""
    import check_redirects

    site_dir = tmp_path / "site"
    # Source /books/ exists as a built page AND as a redirect source.
    _make_site_page(site_dir, "/books/")
    _make_site_page(site_dir, "/media/books/")

    redirects = _write_redirects(tmp_path, """\
        /books/ /media/books/ 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 1


def test_blank_lines_and_comments_ignored(tmp_path):
    """Blank lines and # comment lines must be skipped without error."""
    import check_redirects

    site_dir = tmp_path / "site"
    _make_site_page(site_dir, "/media/books/")

    redirects = _write_redirects(tmp_path, """\
        # This is a comment

        /books/ /media/books/ 301

    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0


def test_splat_rule_valid_when_section_exists(tmp_path):
    """A splat rule is valid when its target base section exists in the built site."""
    import check_redirects

    site_dir = tmp_path / "site"
    _make_site_page(site_dir, "/media/books/")

    redirects = _write_redirects(tmp_path, """\
        /books/page/* /media/books/page/:splat 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0


def test_splat_rule_direct_section_valid(tmp_path):
    """A /section/:splat rule verifies the section itself exists."""
    import check_redirects

    site_dir = tmp_path / "site"
    _make_site_page(site_dir, "/media/books/")

    redirects = _write_redirects(tmp_path, """\
        /old/* /media/books/:splat 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0


def test_splat_rule_direct_section_missing_exits_1(tmp_path):
    """A /section/:splat rule must fail when the section is gone, even if its parent exists."""
    import check_redirects

    site_dir = tmp_path / "site"
    # Parent /media/ exists; the actual target section /media/books/ does not.
    _make_site_page(site_dir, "/media/")

    redirects = _write_redirects(tmp_path, """\
        /old/* /media/books/:splat 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 1


def test_splat_rule_invalid_when_section_missing(tmp_path):
    """A splat rule whose target base section is absent from the built site must exit 1."""
    import check_redirects

    site_dir = tmp_path / "site"
    site_dir.mkdir()

    redirects = _write_redirects(tmp_path, """\
        /old/page/* /nonexistent/page/:splat 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 1


def test_missing_redirects_file_exits_1(tmp_path):
    """main() must return 1 when the _redirects file does not exist."""
    import check_redirects

    site_dir = tmp_path / "site"
    site_dir.mkdir()

    result = check_redirects.main([str(site_dir), str(tmp_path / "no_such_file")])
    assert result == 1


def test_missing_site_arg_exits_1():
    """main([]) with no args must return 1 with a usage message."""
    import check_redirects

    result = check_redirects.main([])
    assert result == 1


def test_exact_file_target(tmp_path):
    """A redirect to an exact file (e.g. index.xml) must exit 0 when file exists."""
    import check_redirects

    site_dir = tmp_path / "site"
    _make_site_file(site_dir, "/media/books/index.xml")

    redirects = _write_redirects(tmp_path, """\
        /books/index.xml /media/books/index.xml 301
    """)

    result = check_redirects.main([str(site_dir), str(redirects)])
    assert result == 0
