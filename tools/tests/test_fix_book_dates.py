# ABOUTME: Tests for the one-time fix_book_dates script that corrects wrong 2025-02-25 dates.
# ABOUTME: Covers offline functions: date map building, book ID extraction, and frontmatter updates.

import os
import yaml
import frontmatter
import pytest

from fix_book_dates import build_date_added_map, get_book_id_from_data_file, fix_dates


def test_build_date_added_map_basic():
    """Maps review dicts with plain string IDs to book_id → ISO date."""
    reviews = [
        {
            "book": {"id": "14770"},
            "date_added": "Mon Nov 05 00:00:00 -0800 2006",
        },
    ]
    result = build_date_added_map(reviews)
    assert result == {"14770": "2006-11-05T00:00:00-08:00"}


def test_build_date_added_map_handles_nested_id():
    """Maps review dicts where book.id is a nested dict with @type and #text."""
    reviews = [
        {
            "book": {"id": {"@type": "integer", "#text": "12345"}},
            "date_added": "Sat Mar 01 12:00:00 -0500 2008",
        },
    ]
    result = build_date_added_map(reviews)
    assert "12345" in result
    assert result["12345"].startswith("2008-03-01")


def test_build_date_added_map_skips_empty_date():
    """Skips reviews with missing or empty date_added."""
    reviews = [
        {"book": {"id": "99"}, "date_added": None},
        {"book": {"id": "100"}, "date_added": ""},
    ]
    result = build_date_added_map(reviews)
    assert result == {}


def test_build_date_added_map_multiple():
    """Handles multiple reviews and returns all mappings."""
    reviews = [
        {"book": {"id": "1"}, "date_added": "Mon Jan 01 00:00:00 -0800 2007"},
        {"book": {"id": "2"}, "date_added": "Tue Feb 01 00:00:00 -0800 2011"},
    ]
    result = build_date_added_map(reviews)
    assert "1" in result
    assert "2" in result
    assert result["1"].startswith("2007-01-01")
    assert result["2"].startswith("2011-02-01")


def test_get_book_id_from_data_file(tmp_path):
    """Reads the id field from a YAML data file and returns it as a string."""
    data_file = tmp_path / "some-book.yaml"
    yaml.safe_dump({"id": "14770", "title": "Some Book"}, data_file.open("w"))
    result = get_book_id_from_data_file(str(data_file))
    assert result == "14770"


def test_get_book_id_from_data_file_integer_id(tmp_path):
    """Returns the id as a string even when YAML loads it as an integer."""
    data_file = tmp_path / "some-book.yaml"
    yaml.safe_dump({"id": 14770, "title": "Some Book"}, data_file.open("w"))
    result = get_book_id_from_data_file(str(data_file))
    assert result == "14770"


def test_get_book_id_from_data_file_missing(tmp_path):
    """Returns None when the id field is absent."""
    data_file = tmp_path / "no-id.yaml"
    yaml.safe_dump({"title": "No ID Book"}, data_file.open("w"))
    result = get_book_id_from_data_file(str(data_file))
    assert result is None


def test_fix_dates_updates_frontmatter(tmp_path):
    """Updates date frontmatter for matching 2025-02-25 entries found in the date map."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)

    content_dir = tmp_path / "content" / "books"
    content_dir.mkdir(parents=True)

    # Create a data file for the book
    slug = "2025-02-25-some-book"
    data_file = data_dir / f"{slug}.yaml"
    yaml.safe_dump({"id": "14770", "title": "Some Book"}, data_file.open("w"))

    # Create the matching content directory and index.md
    book_dir = content_dir / slug
    book_dir.mkdir(parents=True)
    post = frontmatter.Post(
        content="A description.",
        title="Some Book",
        date="2025-02-25T00:00:00-08:00",
    )
    with open(book_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    date_map = {"14770": "2006-11-05T00:00:00-08:00"}
    stats = fix_dates(str(content_dir), str(data_dir), date_map)

    updated = frontmatter.load(str(book_dir / "index.md"))
    assert updated["date"] == "2006-11-05T00:00:00-08:00"
    assert stats["fixed"] == 1
    assert stats["no_match"] == 0
    assert stats["skipped"] == 0


def test_fix_dates_skips_non_matching_directories(tmp_path):
    """Ignores content directories that do not start with 2025-02-25-."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)

    content_dir = tmp_path / "content" / "books"
    content_dir.mkdir(parents=True)

    # A correctly dated entry — should be skipped
    good_slug = "2006-11-05-some-book"
    data_file = data_dir / f"{good_slug}.yaml"
    yaml.safe_dump({"id": "14770", "title": "Some Book"}, data_file.open("w"))

    book_dir = content_dir / good_slug
    book_dir.mkdir(parents=True)
    post = frontmatter.Post(
        content="A description.",
        title="Some Book",
        date="2006-11-05T00:00:00-08:00",
    )
    with open(book_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    date_map = {"14770": "2006-11-05T00:00:00-08:00"}
    stats = fix_dates(str(content_dir), str(data_dir), date_map)

    assert stats["fixed"] == 0
    assert stats["skipped"] == 0
    assert stats["no_match"] == 0


def test_fix_dates_no_match_in_map(tmp_path):
    """Records no_match when book ID is not in the date map."""
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)

    content_dir = tmp_path / "content" / "books"
    content_dir.mkdir(parents=True)

    slug = "2025-02-25-unknown-book"
    data_file = data_dir / f"{slug}.yaml"
    yaml.safe_dump({"id": "99999", "title": "Unknown Book"}, data_file.open("w"))

    book_dir = content_dir / slug
    book_dir.mkdir(parents=True)
    post = frontmatter.Post(
        content="A description.",
        title="Unknown Book",
        date="2025-02-25T00:00:00-08:00",
    )
    with open(book_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    date_map = {}  # empty map — no match
    stats = fix_dates(str(content_dir), str(data_dir), date_map)

    assert stats["fixed"] == 0
    assert stats["no_match"] == 1
    assert stats["skipped"] == 0
