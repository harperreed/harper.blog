# ABOUTME: Tests for check_inline_styles.py: detects style= attributes and <style blocks.
# ABOUTME: Exercises scan_layouts() with tmp layout trees and main() on the real repo.

import textwrap
from pathlib import Path


def _write_template(layouts_dir: Path, rel: str, content: str) -> Path:
    """Write a template file under layouts_dir."""
    p = layouts_dir / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(content), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# scan_layouts() unit tests (pure helper, no I/O side effects)
# ---------------------------------------------------------------------------

def test_clean_template_returns_no_hits(tmp_path):
    """A template with no inline styles must return an empty hit list."""
    import check_inline_styles

    layouts = tmp_path / "layouts"
    _write_template(layouts, "index.html", """\
        <div class="foo">
          <p>Hello world</p>
        </div>
    """)

    hits = check_inline_styles.scan_layouts(layouts)
    assert hits == []


def test_style_attribute_detected(tmp_path):
    """A template containing style="..." must appear in scan results."""
    import check_inline_styles

    layouts = tmp_path / "layouts"
    _write_template(layouts, "shortcodes/kitco.html", """\
        <iframe src="https://kit.co/embed?url=x" style="display: block; width: 100%"></iframe>
    """)

    hits = check_inline_styles.scan_layouts(layouts)
    assert len(hits) >= 1
    # hit should reference the file
    assert any("kitco.html" in h for h in hits)


def test_style_block_detected(tmp_path):
    """A template containing a <style> block must appear in scan results."""
    import check_inline_styles

    layouts = tmp_path / "layouts"
    _write_template(layouts, "partials/custom.html", """\
        <style>
          .foo { color: red; }
        </style>
        <div class="foo">hi</div>
    """)

    hits = check_inline_styles.scan_layouts(layouts)
    assert len(hits) >= 1
    assert any("custom.html" in h for h in hits)


def test_go_comment_style_not_detected(tmp_path):
    """A style= inside a Go template comment {{/* ... */}} must NOT be flagged."""
    import check_inline_styles

    layouts = tmp_path / "layouts"
    _write_template(layouts, "index.html", """\
        {{/* This is a comment with style="example" in it */}}
        <div>real content</div>
    """)

    hits = check_inline_styles.scan_layouts(layouts)
    assert hits == []


def test_multiple_files_multiple_hits(tmp_path):
    """Hits from multiple files must all be returned."""
    import check_inline_styles

    layouts = tmp_path / "layouts"
    _write_template(layouts, "a.html", '<span style="color:red">A</span>')
    _write_template(layouts, "b.html", '<span style="color:blue">B</span>')

    hits = check_inline_styles.scan_layouts(layouts)
    assert len(hits) >= 2


# ---------------------------------------------------------------------------
# main() contract
# ---------------------------------------------------------------------------

def test_main_returns_int():
    """main() must return an int (0 or 1)."""
    import check_inline_styles

    result = check_inline_styles.main()
    assert isinstance(result, int)
    assert result in (0, 1)
