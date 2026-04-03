# ABOUTME: Tests for the one-time backfill script that adds goodreads_work_id to book frontmatter.
# ABOUTME: Covers work ID extraction from YAML data files and frontmatter updates.

import os
import tempfile
import yaml
import frontmatter
import pytest

from backfill_goodreads_ids import get_work_id_from_data_file, backfill_work_ids, detect_and_link_rereads, check_is_reread


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


def test_detect_and_link_rereads(tmp_path):
    """Detects two entries with same goodreads_work_id and cross-links them."""
    content_dir = tmp_path / "content" / "books"

    dir1 = content_dir / "2006-11-26-old-mans-war"
    dir1.mkdir(parents=True)
    post1 = frontmatter.Post(
        content="First read.",
        title="Old Man's War",
        date="2006-11-26T00:00:00-08:00",
        goodreads_work_id="50700",
    )
    with open(dir1 / "index.md", "wb") as f:
        frontmatter.dump(post1, f)

    dir2 = content_dir / "2025-02-25-old-mans-war"
    dir2.mkdir(parents=True)
    post2 = frontmatter.Post(
        content="Re-read.",
        title="Old Man's War",
        date="2025-02-25T00:00:00-08:00",
        goodreads_work_id="50700",
    )
    with open(dir2 / "index.md", "wb") as f:
        frontmatter.dump(post2, f)

    dir3 = content_dir / "2025-01-01-other-book"
    dir3.mkdir(parents=True)
    post3 = frontmatter.Post(
        content="Different book.",
        title="Other Book",
        date="2025-01-01T00:00:00-08:00",
        goodreads_work_id="99999",
    )
    with open(dir3 / "index.md", "wb") as f:
        frontmatter.dump(post3, f)

    linked = detect_and_link_rereads(content_dir=str(content_dir))

    updated1 = frontmatter.load(str(dir1 / "index.md"))
    updated2 = frontmatter.load(str(dir2 / "index.md"))
    updated3 = frontmatter.load(str(dir3 / "index.md"))

    assert "2025-02-25-old-mans-war" in updated1["related_reads"]
    assert "2006-11-26-old-mans-war" in updated2["related_reads"]
    assert "related_reads" not in updated3.metadata
    assert linked == 2


def test_detect_and_link_rereads_no_duplicates(tmp_path):
    """Does not add duplicate slugs to related_reads if already linked."""
    content_dir = tmp_path / "content" / "books"

    dir1 = content_dir / "2006-11-26-old-mans-war"
    dir1.mkdir(parents=True)
    post1 = frontmatter.Post(
        content="First read.",
        title="Old Man's War",
        date="2006-11-26T00:00:00-08:00",
        goodreads_work_id="50700",
        related_reads=["2025-02-25-old-mans-war"],
    )
    with open(dir1 / "index.md", "wb") as f:
        frontmatter.dump(post1, f)

    dir2 = content_dir / "2025-02-25-old-mans-war"
    dir2.mkdir(parents=True)
    post2 = frontmatter.Post(
        content="Re-read.",
        title="Old Man's War",
        date="2025-02-25T00:00:00-08:00",
        goodreads_work_id="50700",
        related_reads=["2006-11-26-old-mans-war"],
    )
    with open(dir2 / "index.md", "wb") as f:
        frontmatter.dump(post2, f)

    linked = detect_and_link_rereads(content_dir=str(content_dir))

    updated1 = frontmatter.load(str(dir1 / "index.md"))
    assert updated1["related_reads"] == ["2025-02-25-old-mans-war"]
    assert linked == 0


def test_check_is_reread_true(tmp_path):
    """Returns True when popular_shelves contains a shelf named re-read."""
    data_file = tmp_path / "some-book.yaml"
    data = {
        "work": {"id": "50700"},
        "popular_shelves": {
            "shelf": [
                {"@name": "to-read", "@count": "279892"},
                {"@name": "re-read", "@count": "51"},
            ]
        },
    }
    with open(data_file, "w") as f:
        yaml.safe_dump(data, f)

    assert check_is_reread(str(data_file)) is True


def test_check_is_reread_false(tmp_path):
    """Returns False when popular_shelves does not contain a shelf named re-read."""
    data_file = tmp_path / "some-book.yaml"
    data = {
        "work": {"id": "50700"},
        "popular_shelves": {
            "shelf": [
                {"@name": "to-read", "@count": "279892"},
                {"@name": "currently-reading", "@count": "10"},
            ]
        },
    }
    with open(data_file, "w") as f:
        yaml.safe_dump(data, f)

    assert check_is_reread(str(data_file)) is False


def test_backfill_sets_is_reread(tmp_path):
    """backfill_work_ids writes is_reread: true when the data file has re-read shelf."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "2025-02-25-old-mans-war.yaml"
    data = {
        "work": {"id": "50700"},
        "popular_shelves": {
            "shelf": [
                {"@name": "to-read", "@count": "279892"},
                {"@name": "re-read", "@count": "51"},
            ]
        },
    }
    with open(data_file, "w") as f:
        yaml.safe_dump(data, f)

    content_dir = tmp_path / "content" / "books" / "2025-02-25-old-mans-war"
    content_dir.mkdir(parents=True)
    post = frontmatter.Post(content="Re-read.", title="Old Man's War", date="2025-02-25")
    with open(content_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    backfill_work_ids(
        data_dir=str(data_dir),
        content_dir=str(tmp_path / "content" / "books"),
    )

    updated = frontmatter.load(str(content_dir / "index.md"))
    assert updated.get("is_reread") is True
