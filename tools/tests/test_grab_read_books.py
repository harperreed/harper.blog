# ABOUTME: Tests for re-read detection and goodreads_work_id surfacing in the book ingestion script.
# ABOUTME: Covers metadata creation and re-read scanning logic.

import os
import frontmatter as fm

from grab_read_books import create_post_metadata


def test_create_post_metadata_includes_goodreads_work_id():
    """create_post_metadata includes goodreads_work_id from book_data."""
    book_data = {
        "title": "Old Man's War",
        "work": {"id": "50700"},
    }
    book = {
        "title_without_series": "Old Man's War",
        "read_at": "2025-02-25T00:00:00-08:00",
        "num_pages": "318",
        "review_rating": "5",
        "average_rating": "4.23",
        "link": "https://www.goodreads.com/book/show/51964",
        "started_at": "",
    }
    summary = {"Tagline": "A tagline", "Summary": "A summary", "Description": "Desc"}
    asin = "B000SEIK2S"
    author = "John Scalzi"

    metadata = create_post_metadata(book_data, book, summary, asin, author)

    assert metadata["goodreads_work_id"] == "50700"


def test_create_post_metadata_handles_missing_work_id():
    """create_post_metadata sets goodreads_work_id to empty string when work field is missing."""
    book_data = {"title": "No Work ID Book"}
    book = {
        "title_without_series": "No Work ID Book",
        "read_at": "2025-01-01T00:00:00-08:00",
        "num_pages": "200",
        "review_rating": "3",
        "average_rating": "3.5",
        "link": "https://goodreads.com/book/show/1",
        "started_at": "",
    }
    summary = {"Tagline": "Tag", "Summary": "Sum", "Description": "Desc"}

    metadata = create_post_metadata(book_data, book, summary, "ASIN123", "Author")

    assert metadata["goodreads_work_id"] == ""


from grab_read_books import find_existing_reads


def test_find_existing_reads_finds_match(tmp_path):
    """Finds existing entries with matching goodreads_work_id."""
    book_dir = tmp_path / "2006-11-26-old-mans-war"
    book_dir.mkdir()
    post = fm.Post(content="A book.", goodreads_work_id="50700", title="Old Man's War")
    with open(book_dir / "index.md", "wb") as f:
        fm.dump(post, f)

    results = find_existing_reads(str(tmp_path), "50700")

    assert len(results) == 1
    assert results[0] == "2006-11-26-old-mans-war"


def test_find_existing_reads_no_match(tmp_path):
    """Returns empty list when no entries match."""
    book_dir = tmp_path / "2006-11-26-other-book"
    book_dir.mkdir()
    post = fm.Post(content="A book.", goodreads_work_id="99999", title="Other")
    with open(book_dir / "index.md", "wb") as f:
        fm.dump(post, f)

    results = find_existing_reads(str(tmp_path), "50700")

    assert results == []


def test_create_post_metadata_includes_is_reread():
    """create_post_metadata sets is_reread True when re-read shelf present in popular_shelves."""
    book_data = {
        "title": "Old Man's War",
        "work": {"id": "50700"},
        "popular_shelves": {
            "shelf": [
                {"@name": "to-read", "@count": "279892"},
                {"@name": "re-read", "@count": "51"},
            ]
        },
    }
    book = {
        "title_without_series": "Old Man's War",
        "read_at": "2025-02-25T00:00:00-08:00",
        "num_pages": "318",
        "review_rating": "5",
        "average_rating": "4.23",
        "link": "https://www.goodreads.com/book/show/51964",
        "started_at": "",
    }
    summary = {"Tagline": "A tagline", "Summary": "A summary", "Description": "Desc"}
    asin = "B000SEIK2S"
    author = "John Scalzi"

    metadata = create_post_metadata(book_data, book, summary, asin, author)

    assert metadata["is_reread"] is True


def test_create_post_metadata_is_reread_false_when_no_shelf():
    """create_post_metadata sets is_reread False when re-read shelf is absent."""
    book_data = {
        "title": "Old Man's War",
        "work": {"id": "50700"},
        "popular_shelves": {
            "shelf": [
                {"@name": "to-read", "@count": "279892"},
                {"@name": "currently-reading", "@count": "1200"},
            ]
        },
    }
    book = {
        "title_without_series": "Old Man's War",
        "read_at": "2025-02-25T00:00:00-08:00",
        "num_pages": "318",
        "review_rating": "5",
        "average_rating": "4.23",
        "link": "https://www.goodreads.com/book/show/51964",
        "started_at": "",
    }
    summary = {"Tagline": "A tagline", "Summary": "A summary", "Description": "Desc"}
    asin = "B000SEIK2S"
    author = "John Scalzi"

    metadata = create_post_metadata(book_data, book, summary, asin, author)

    assert metadata["is_reread"] is False


def test_create_post_metadata_falls_back_to_date_added():
    """create_post_metadata uses date_added when read_at and started_at are both empty."""
    book_data = {"title": "Some Book", "work": {"id": "12345"}}
    book = {
        "title_without_series": "Some Book",
        "read_at": "",
        "started_at": "",
        "date_added": "2023-06-15T00:00:00-07:00",
        "num_pages": "250",
        "review_rating": "4",
        "average_rating": "3.9",
        "link": "https://www.goodreads.com/book/show/12345",
    }
    summary = {"Tagline": "A tagline", "Summary": "A summary", "Description": "Desc"}

    metadata = create_post_metadata(book_data, book, summary, "ASIN456", "Some Author")

    assert metadata["date"] == "2023-06-15T00:00:00-07:00"


from grab_read_books import link_related_reads


def test_link_related_reads_updates_both_entries(tmp_path):
    """Cross-links new entry and existing entry."""
    dir1 = tmp_path / "2006-11-26-old-mans-war"
    dir1.mkdir()
    post1 = fm.Post(content="First read.", goodreads_work_id="50700", title="OMW")
    with open(dir1 / "index.md", "wb") as f:
        fm.dump(post1, f)

    dir2 = tmp_path / "2025-02-25-old-mans-war"
    dir2.mkdir()
    post2 = fm.Post(content="Re-read.", goodreads_work_id="50700", title="OMW")
    with open(dir2 / "index.md", "wb") as f:
        fm.dump(post2, f)

    link_related_reads(
        content_dir=str(tmp_path),
        new_slug="2025-02-25-old-mans-war",
        existing_slugs=["2006-11-26-old-mans-war"],
    )

    updated1 = fm.load(str(dir1 / "index.md"))
    updated2 = fm.load(str(dir2 / "index.md"))

    assert "2025-02-25-old-mans-war" in updated1["related_reads"]
    assert "2006-11-26-old-mans-war" in updated2["related_reads"]
