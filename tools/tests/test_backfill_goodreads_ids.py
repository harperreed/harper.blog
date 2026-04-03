# ABOUTME: Tests for the one-time backfill script that adds goodreads_work_id to book frontmatter.
# ABOUTME: Covers work ID extraction from YAML data files and frontmatter updates.

import os
import tempfile
import yaml
import frontmatter
import pytest

from backfill_goodreads_ids import get_work_id_from_data_file, backfill_work_ids


def test_get_work_id_from_data_file():
    """Extracts work.id from a YAML data file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.safe_dump({"work": {"id": "50700"}, "title": "Old Man's War"}, f)
        f.flush()
        result = get_work_id_from_data_file(f.name)
    os.unlink(f.name)
    assert result == "50700"


def test_get_work_id_from_data_file_missing_work():
    """Returns None when work field is missing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.safe_dump({"title": "No Work Field"}, f)
        f.flush()
        result = get_work_id_from_data_file(f.name)
    os.unlink(f.name)
    assert result is None


def test_backfill_work_ids_writes_goodreads_work_id(tmp_path):
    """Writes goodreads_work_id into content frontmatter from data YAML."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "2025-02-25-some-book.yaml"
    yaml.safe_dump({"work": {"id": "12345"}, "title": "Some Book"}, data_file.open("w"))

    content_dir = tmp_path / "content" / "books" / "2025-02-25-some-book"
    content_dir.mkdir(parents=True)
    post = frontmatter.Post(content="A book description.", title="Some Book", date="2025-02-25")
    with open(content_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    stats = backfill_work_ids(
        data_dir=str(data_dir),
        content_dir=str(tmp_path / "content" / "books"),
    )

    updated = frontmatter.load(str(content_dir / "index.md"))
    assert updated["goodreads_work_id"] == "12345"
    assert stats["updated"] == 1
    assert stats["skipped"] == 0


def test_backfill_work_ids_skips_already_set(tmp_path):
    """Skips entries that already have goodreads_work_id."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "2025-02-25-some-book.yaml"
    yaml.safe_dump({"work": {"id": "12345"}, "title": "Some Book"}, data_file.open("w"))

    content_dir = tmp_path / "content" / "books" / "2025-02-25-some-book"
    content_dir.mkdir(parents=True)
    post = frontmatter.Post(
        content="A book description.",
        title="Some Book",
        goodreads_work_id="12345",
    )
    with open(content_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    stats = backfill_work_ids(
        data_dir=str(data_dir),
        content_dir=str(tmp_path / "content" / "books"),
    )

    assert stats["updated"] == 0
    assert stats["skipped"] == 1
