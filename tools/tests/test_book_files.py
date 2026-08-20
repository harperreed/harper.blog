# ABOUTME: Tests for book_files.write_frontmatter_file, the shared frontmatter writer.
# ABOUTME: Covers round-tripping and that failed serialization never truncates or creates files.

import os

import frontmatter as fm
import pytest

from book_files import write_frontmatter_file


def test_writes_parseable_file(tmp_path):
    """A written post round-trips through frontmatter.load."""
    path = tmp_path / "index.md"
    post = fm.Post(content="A book.", title="Old Man's War", review_rating="5")

    write_frontmatter_file(post, str(path))

    loaded = fm.load(str(path))
    assert loaded.content == "A book."
    assert loaded["title"] == "Old Man's War"
    assert os.path.getsize(path) > 0


def test_failed_serialization_creates_no_file(tmp_path):
    """A post whose metadata can't serialize leaves no zero-byte corpse behind."""
    path = tmp_path / "index.md"
    post = fm.Post(content="body", bad=object())

    with pytest.raises(Exception):
        write_frontmatter_file(post, str(path))

    assert not path.exists()


def test_write_frontmatter_file_is_atomic(tmp_path):
    import inspect, book_files
    src = inspect.getsource(book_files.write_frontmatter_file)
    assert "os.replace(" in src  # temp-file + rename, no in-place open("w")


def test_write_frontmatter_file_roundtrips_and_leaves_no_tmp(tmp_path):
    """Write via write_frontmatter_file, round-trip with frontmatter.load, no *.tmp* residue."""
    path = tmp_path / "index.md"
    post = fm.Post(content="Great book.", title="Atomic Write Test", review_rating="5")

    write_frontmatter_file(post, str(path))

    loaded = fm.load(str(path))
    assert loaded.content == "Great book."
    assert loaded["title"] == "Atomic Write Test"
    tmp_residue = list(tmp_path.glob("*.tmp*")) + list(tmp_path.glob("*tmp*"))
    assert tmp_residue == [], f"Leftover temp files: {tmp_residue}"


def test_failed_serialization_keeps_existing_content(tmp_path):
    """A failed rewrite must not truncate the existing file."""
    path = tmp_path / "index.md"
    write_frontmatter_file(fm.Post(content="First read.", title="OMW"), str(path))
    original = path.read_text(encoding="utf-8")

    with pytest.raises(Exception):
        write_frontmatter_file(fm.Post(content="x", bad=object()), str(path))

    assert path.read_text(encoding="utf-8") == original
