# Book Re-Read Tracking Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Detect when a book has been read multiple times and cross-link the entries so each book page shows a subtle note pointing to other reads of the same book.

**Architecture:** Each book entry gets two new frontmatter fields: `goodreads_work_id` (the Goodreads "work" ID that groups editions) and `related_reads` (list of slugs for other reads of the same book). The ingestion script detects re-reads by scanning existing entries for matching work IDs. A one-time backfill script populates `goodreads_work_id` across all 827 existing entries. The Hugo template renders a subtle "Previously read in..." or "Re-read in..." note with a link.

**Tech Stack:** Python (frontmatter, PyYAML, python-slugify), Hugo Go templates

**Key discovery:** Goodreads book `id` differs between editions (51964 vs 640474 for Old Man's War). The `work.id` field (50700 for both) is the correct canonical identifier. All 841 data files have this field.

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `tools/backfill_goodreads_ids.py` | Create | One-time script: reads `data/books/*.yaml`, writes `goodreads_work_id` into `content/books/*/index.md` frontmatter, detects and cross-links re-reads |
| `tools/tests/test_backfill_goodreads_ids.py` | Create | Tests for backfill script |
| `tools/grab_read_books.py` | Modify | Add `goodreads_work_id` to `create_post_metadata()`, add re-read detection and cross-linking in `main()` |
| `tools/tests/test_grab_read_books.py` | Create | Tests for new re-read detection logic |
| `layouts/books/single.html` | Modify | Render related reads note |

---

### Task 1: Backfill Script — Write `goodreads_work_id` into Existing Entries

**Files:**
- Create: `tools/backfill_goodreads_ids.py`
- Create: `tools/tests/__init__.py`
- Create: `tools/tests/test_backfill_goodreads_ids.py`

This task creates the backfill script that reads `work.id` from each `data/books/*.yaml` file and writes it as `goodreads_work_id` into the corresponding `content/books/*/index.md` frontmatter.

- [ ] **Step 1: Write the failing test for `get_work_id_from_data_file`**

Create `tools/tests/__init__.py` (empty file).

Create `tools/tests/test_backfill_goodreads_ids.py`:

```python
# ABOUTME: Tests for the one-time backfill script that adds goodreads_work_id to book frontmatter.
# ABOUTME: Covers work ID extraction from YAML data files and frontmatter updates.

import os
import tempfile
import yaml
import frontmatter
import pytest

from backfill_goodreads_ids import get_work_id_from_data_file


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backfill_goodreads_ids'`

- [ ] **Step 3: Write `get_work_id_from_data_file` implementation**

Create `tools/backfill_goodreads_ids.py`:

```python
# ABOUTME: One-time backfill script that adds goodreads_work_id to book entry frontmatter.
# ABOUTME: Reads work.id from data/books/*.yaml and writes it into content/books/*/index.md.

import os
import logging
import yaml
import frontmatter
import glob

logger = logging.getLogger(__name__)


def get_work_id_from_data_file(data_file_path: str) -> str | None:
    """
    Reads a data/books/*.yaml file and extracts the work.id field.

    Args:
        data_file_path: Path to the YAML data file.

    Returns:
        The work ID as a string, or None if not found.
    """
    with open(data_file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    work = data.get("work")
    if not work or not isinstance(work, dict):
        return None

    work_id = work.get("id")
    return str(work_id) if work_id is not None else None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Write the failing test for `backfill_work_ids`**

Append to `tools/tests/test_backfill_goodreads_ids.py`:

```python
from backfill_goodreads_ids import backfill_work_ids


def test_backfill_work_ids_writes_goodreads_work_id(tmp_path):
    """Writes goodreads_work_id into content frontmatter from data YAML."""
    # Set up data dir with one book
    data_dir = tmp_path / "data" / "books"
    data_dir.mkdir(parents=True)
    data_file = data_dir / "2025-02-25-some-book.yaml"
    yaml.safe_dump({"work": {"id": "12345"}, "title": "Some Book"}, data_file.open("w"))

    # Set up content dir with matching book
    content_dir = tmp_path / "content" / "books" / "2025-02-25-some-book"
    content_dir.mkdir(parents=True)
    post = frontmatter.Post(content="A book description.", title="Some Book", date="2025-02-25")
    with open(content_dir / "index.md", "wb") as f:
        frontmatter.dump(post, f)

    stats = backfill_work_ids(
        data_dir=str(data_dir),
        content_dir=str(tmp_path / "content" / "books"),
    )

    # Verify frontmatter was updated
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
```

- [ ] **Step 6: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py::test_backfill_work_ids_writes_goodreads_work_id -v`
Expected: FAIL with `ImportError: cannot import name 'backfill_work_ids'`

- [ ] **Step 7: Write `backfill_work_ids` implementation**

Add to `tools/backfill_goodreads_ids.py`:

```python
def backfill_work_ids(data_dir: str, content_dir: str) -> dict:
    """
    Reads work.id from each data/books/*.yaml and writes goodreads_work_id
    into the matching content/books/*/index.md frontmatter.

    Args:
        data_dir: Path to data/books/ directory containing YAML files.
        content_dir: Path to content/books/ directory containing book entries.

    Returns:
        Dict with counts: {"updated": int, "skipped": int, "missing": int}
    """
    stats = {"updated": 0, "skipped": 0, "missing": 0}

    data_files = glob.glob(os.path.join(data_dir, "*.yaml"))
    for data_file in sorted(data_files):
        slug = os.path.splitext(os.path.basename(data_file))[0]
        content_file = os.path.join(content_dir, slug, "index.md")

        if not os.path.isfile(content_file):
            logger.warning(f"No content file for {slug}")
            stats["missing"] += 1
            continue

        work_id = get_work_id_from_data_file(data_file)
        if not work_id:
            logger.warning(f"No work ID in {data_file}")
            stats["missing"] += 1
            continue

        post = frontmatter.load(content_file)
        if post.get("goodreads_work_id"):
            logger.debug(f"Already has work ID: {slug}")
            stats["skipped"] += 1
            continue

        post["goodreads_work_id"] = work_id
        with open(content_file, "wb") as f:
            frontmatter.dump(post, f)

        logger.info(f"Updated {slug} with work ID {work_id}")
        stats["updated"] += 1

    return stats
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py -v`
Expected: PASS (4 tests)

- [ ] **Step 9: Commit**

```bash
git add tools/backfill_goodreads_ids.py tools/tests/__init__.py tools/tests/test_backfill_goodreads_ids.py
git commit -m "feat: add backfill script for goodreads_work_id in book frontmatter"
```

---

### Task 2: Backfill Script — Detect and Cross-Link Re-Reads

**Files:**
- Modify: `tools/backfill_goodreads_ids.py`
- Modify: `tools/tests/test_backfill_goodreads_ids.py`

This task adds re-read detection and cross-linking to the backfill script. After all entries have `goodreads_work_id`, the script scans for entries sharing the same work ID and populates `related_reads` on each.

- [ ] **Step 1: Write the failing test for `detect_and_link_rereads`**

Append to `tools/tests/test_backfill_goodreads_ids.py`:

```python
from backfill_goodreads_ids import detect_and_link_rereads


def test_detect_and_link_rereads(tmp_path):
    """Detects two entries with same goodreads_work_id and cross-links them."""
    content_dir = tmp_path / "content" / "books"

    # Create first read
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

    # Create second read (re-read)
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

    # Create unrelated book
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

    # Verify cross-linking
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py::test_detect_and_link_rereads -v`
Expected: FAIL with `ImportError: cannot import name 'detect_and_link_rereads'`

- [ ] **Step 3: Write `detect_and_link_rereads` implementation**

Add to `tools/backfill_goodreads_ids.py`:

```python
from collections import defaultdict


def detect_and_link_rereads(content_dir: str) -> int:
    """
    Scans all book entries for shared goodreads_work_id values and
    populates related_reads on entries that share the same work ID.

    Args:
        content_dir: Path to content/books/ directory.

    Returns:
        Number of entries updated with new related_reads links.
    """
    # Build map: work_id -> list of (slug, content_file_path)
    work_id_map = defaultdict(list)
    entry_dirs = sorted(glob.glob(os.path.join(content_dir, "*", "index.md")))

    for content_file in entry_dirs:
        slug = os.path.basename(os.path.dirname(content_file))
        post = frontmatter.load(content_file)
        work_id = post.get("goodreads_work_id")
        if work_id:
            work_id_map[work_id].append((slug, content_file))

    updated_count = 0

    for work_id, entries in work_id_map.items():
        if len(entries) < 2:
            continue

        all_slugs = [slug for slug, _ in entries]

        for slug, content_file in entries:
            post = frontmatter.load(content_file)
            existing = post.get("related_reads", [])
            sibling_slugs = [s for s in all_slugs if s != slug]

            new_slugs = [s for s in sibling_slugs if s not in existing]
            if not new_slugs:
                continue

            post["related_reads"] = existing + new_slugs
            with open(content_file, "wb") as f:
                frontmatter.dump(post, f)

            logger.info(f"Linked {slug} to {new_slugs}")
            updated_count += 1

    return updated_count
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Add `__main__` block to backfill script**

Add to the bottom of `tools/backfill_goodreads_ids.py`:

```python
def main():
    """Run the full backfill: add work IDs, then detect and link re-reads."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    )

    data_dir = os.path.join(os.path.dirname(__file__), "..", "data", "books")
    content_dir = os.path.join(os.path.dirname(__file__), "..", "content", "books")

    logger.info("Step 1: Backfilling goodreads_work_id into frontmatter...")
    stats = backfill_work_ids(data_dir=data_dir, content_dir=content_dir)
    logger.info(f"Backfill complete: {stats}")

    logger.info("Step 2: Detecting and linking re-reads...")
    linked = detect_and_link_rereads(content_dir=content_dir)
    logger.info(f"Linked {linked} entries")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: Run full test suite**

Run: `cd tools && uv run pytest tests/test_backfill_goodreads_ids.py -v`
Expected: PASS (6 tests)

- [ ] **Step 7: Commit**

```bash
git add tools/backfill_goodreads_ids.py tools/tests/test_backfill_goodreads_ids.py
git commit -m "feat: add re-read detection and cross-linking to backfill script"
```

---

### Task 3: Run Backfill on Real Data

**Files:**
- Modify: `content/books/*/index.md` (all 827 entries get `goodreads_work_id`; Old Man's War entries get `related_reads`)

This task runs the backfill script against the actual book data.

- [ ] **Step 1: Run the backfill script**

Run: `cd tools && uv run backfill_goodreads_ids.py`

Expected output:
- ~827 entries updated with `goodreads_work_id`
- 2 entries linked (the two Old Man's War reads)

- [ ] **Step 2: Verify Old Man's War entries are cross-linked**

Run: `grep -A2 "related_reads" ../content/books/2006-11-26-old-man-s-war-old-man-s-war-1/index.md ../content/books/2025-02-25-old-man-s-war-old-man-s-war-1/index.md`

Expected: Both files show `related_reads` containing the other's slug.

- [ ] **Step 3: Verify a random non-reread entry has `goodreads_work_id` but no `related_reads`**

Run: `head -25 ../content/books/2025-05-06-void-star/index.md`

Expected: `goodreads_work_id: '50329713'` present, no `related_reads` field.

- [ ] **Step 4: Verify Hugo builds cleanly**

Run (from repo root): `hugo --quiet`

Expected: Build succeeds with no errors.

- [ ] **Step 5: Commit the backfilled content**

```bash
git add content/books/
git commit -m "chore: backfill goodreads_work_id across all book entries"
```

---

### Task 4: Modify Ingestion Script — Surface `goodreads_work_id` and Detect Re-Reads

**Files:**
- Modify: `tools/grab_read_books.py:409-434` (`create_post_metadata` function)
- Modify: `tools/grab_read_books.py:436-540` (`main` function)
- Create: `tools/tests/test_grab_read_books.py`

This task modifies the ingestion script so new books get `goodreads_work_id` in their frontmatter, and re-reads are automatically detected and cross-linked.

- [ ] **Step 1: Write the failing test for `create_post_metadata` including `goodreads_work_id`**

Create `tools/tests/test_grab_read_books.py`:

```python
# ABOUTME: Tests for re-read detection and goodreads_work_id surfacing in the book ingestion script.
# ABOUTME: Covers metadata creation and re-read scanning logic.

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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py::test_create_post_metadata_includes_goodreads_work_id -v`
Expected: FAIL with `AssertionError` (key missing from returned dict)

- [ ] **Step 3: Add `goodreads_work_id` to `create_post_metadata`**

In `tools/grab_read_books.py`, modify `create_post_metadata` (line ~409). Add after the `"book_author": author` line:

```python
        "book_author": author,
        "goodreads_work_id": str(book_data.get("work", {}).get("id", "") or ""),
```

(Note: also add trailing comma to the `"book_author": author` line.)

- [ ] **Step 4: Run test to verify it passes**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py -v`
Expected: PASS (2 tests)

- [ ] **Step 5: Write the failing test for `find_existing_reads`**

Append to `tools/tests/test_grab_read_books.py`:

```python
import os
import tempfile
import frontmatter as fm

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
```

- [ ] **Step 6: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py::test_find_existing_reads_finds_match -v`
Expected: FAIL with `ImportError: cannot import name 'find_existing_reads'`

- [ ] **Step 7: Write `find_existing_reads` function**

Add to `tools/grab_read_books.py`, before `create_post_metadata`:

First, add `import glob` to the top-level imports in `tools/grab_read_books.py` (after the existing `import os` line):

```python
import glob
```

Then add the function before `create_post_metadata`:

```python
def find_existing_reads(content_dir: str, work_id: str) -> list[str]:
    """
    Scans content/books/ for entries with a matching goodreads_work_id.

    Args:
        content_dir: Path to content/books/ directory.
        work_id: The Goodreads work ID to match.

    Returns:
        List of directory slugs (e.g. "2006-11-26-old-mans-war") that match.
    """
    if not work_id:
        return []

    matches = []
    for index_file in glob.glob(os.path.join(content_dir, "*", "index.md")):
        post = frontmatter.load(index_file)
        if str(post.get("goodreads_work_id", "")) == str(work_id):
            slug = os.path.basename(os.path.dirname(index_file))
            matches.append(slug)

    return sorted(matches)
```

- [ ] **Step 8: Run tests to verify they pass**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py -v`
Expected: PASS (4 tests)

- [ ] **Step 9: Write the failing test for `link_related_reads`**

Append to `tools/tests/test_grab_read_books.py`:

```python
from grab_read_books import link_related_reads


def test_link_related_reads_updates_both_entries(tmp_path):
    """Cross-links new entry and existing entry."""
    # Existing entry
    dir1 = tmp_path / "2006-11-26-old-mans-war"
    dir1.mkdir()
    post1 = fm.Post(content="First read.", goodreads_work_id="50700", title="OMW")
    with open(dir1 / "index.md", "wb") as f:
        fm.dump(post1, f)

    # New entry
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
```

- [ ] **Step 10: Run test to verify it fails**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py::test_link_related_reads_updates_both_entries -v`
Expected: FAIL with `ImportError: cannot import name 'link_related_reads'`

- [ ] **Step 11: Write `link_related_reads` function**

Add to `tools/grab_read_books.py`, after `find_existing_reads`:

```python
def link_related_reads(content_dir: str, new_slug: str, existing_slugs: list[str]) -> None:
    """
    Cross-links a new book entry with its existing reads.

    Adds related_reads to the new entry listing existing slugs, and updates
    each existing entry to include the new slug.

    Args:
        content_dir: Path to content/books/ directory.
        new_slug: Directory slug of the newly created entry.
        existing_slugs: List of directory slugs for existing reads of the same book.
    """
    # Update new entry with all existing slugs
    new_file = os.path.join(content_dir, new_slug, "index.md")
    if os.path.isfile(new_file):
        post = frontmatter.load(new_file)
        related = post.get("related_reads", [])
        for slug in existing_slugs:
            if slug not in related:
                related.append(slug)
        post["related_reads"] = related
        with open(new_file, "wb") as f:
            frontmatter.dump(post, f)

    # Update each existing entry to include new slug
    for slug in existing_slugs:
        existing_file = os.path.join(content_dir, slug, "index.md")
        if not os.path.isfile(existing_file):
            continue
        post = frontmatter.load(existing_file)
        related = post.get("related_reads", [])
        if new_slug not in related:
            related.append(new_slug)
            post["related_reads"] = related
            with open(existing_file, "wb") as f:
                frontmatter.dump(post, f)
```

- [ ] **Step 12: Run tests to verify they pass**

Run: `cd tools && uv run pytest tests/test_grab_read_books.py -v`
Expected: PASS (5 tests)

- [ ] **Step 13: Wire re-read detection into `main()`**

In `tools/grab_read_books.py`, modify the `main()` function. After the line that creates the post (around line 521, after `frontmatter.dump(post, file)`), add the re-read detection and linking:

```python
                    # Write the post to file
                    with open(post_filename, "wb") as file:
                        frontmatter.dump(post, file, encoding="utf-8")

                    # Detect and link re-reads
                    work_id = str(book_data.get("work", {}).get("id", "") or "")
                    new_slug = os.path.basename(post_directory)
                    if work_id:
                        existing = find_existing_reads(hugo_book_dir, work_id)
                        # Exclude self from the list
                        existing = [s for s in existing if s != new_slug]
                        if existing:
                            logging.info(f"Re-read detected for {book['title']}: linking to {existing}")
                            link_related_reads(hugo_book_dir, new_slug, existing)
```

- [ ] **Step 14: Run full test suite**

Run: `cd tools && uv run pytest tests/ -v`
Expected: PASS (all tests)

- [ ] **Step 15: Commit**

```bash
git add tools/grab_read_books.py tools/tests/test_grab_read_books.py
git commit -m "feat: add goodreads_work_id to ingestion, detect and link re-reads"
```

---

### Task 5: Hugo Template — Render Related Reads Note

**Files:**
- Modify: `layouts/books/single.html`

This task adds the subtle "Previously read in..." / "Re-read in..." note to the single book page template.

- [ ] **Step 1: Add related reads block to `layouts/books/single.html`**

In `layouts/books/single.html`, add the following block after the closing `</ul>` tag (after line 27) and before the Amazon link (line 28):

Note: The 2025 Old Man's War entry has `date: ''` (empty), which Hugo treats as zero time. The template guards against this with `.Date.IsZero` checks.

```html
{{ with .Params.related_reads }}
<p class="related-reads">
    {{ $currentDate := $.Date }}
    {{ range . }}
        {{ $relatedPage := $.Site.GetPage (printf "/books/%s" .) }}
        {{ if $relatedPage }}
            {{ if or $relatedPage.Date.IsZero $currentDate.IsZero }}
                <em>Also read:</em>
                <a href="{{ $relatedPage.RelPermalink }}">{{ $relatedPage.Title }}</a>
            {{ else if $relatedPage.Date.Before $currentDate }}
                <em>Previously read in {{ $relatedPage.Date.Format "January 2006" }}:</em>
                <a href="{{ $relatedPage.RelPermalink }}">{{ $relatedPage.Date.Format "January 2, 2006" }}</a>
            {{ else }}
                <em>Re-read in {{ $relatedPage.Date.Format "January 2006" }}:</em>
                <a href="{{ $relatedPage.RelPermalink }}">{{ $relatedPage.Date.Format "January 2, 2006" }}</a>
            {{ end }}
            <br>
        {{ end }}
    {{ end }}
</p>
{{ end }}
```

- [ ] **Step 2: Verify Hugo builds cleanly**

Run (from repo root): `hugo --quiet`

Expected: Build succeeds with no errors.

- [ ] **Step 3: Verify the template renders on Old Man's War pages**

Run: `hugo serve --buildDrafts --buildFuture`

Check both URLs in a browser:
- The 2006 Old Man's War entry should show "Re-read in February 2025" with a link
- The 2025 Old Man's War entry should show "Previously read in November 2006" with a link

Non-reread books should show no related reads section.

- [ ] **Step 4: Commit**

```bash
git add layouts/books/single.html
git commit -m "feat: render related reads note on book pages"
```

---

### Task 6: Integration Verification

**Files:** None (verification only)

- [ ] **Step 1: Run full test suite**

Run: `cd tools && uv run pytest tests/ -v`

Expected: All tests pass.

- [ ] **Step 2: Run Hugo build with full flags**

Run: `hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info`

Expected: Clean build, no errors or warnings related to books.

- [ ] **Step 3: Spot-check frontmatter integrity**

Run: `grep -c "goodreads_work_id" content/books/*/index.md | grep ":0$" | head -5`

Expected: No output (all entries have the field). If some show `:0`, they have no matching data file — acceptable if count is very small.

- [ ] **Step 4: Verify no unintended related_reads**

Run: `grep -l "related_reads" content/books/*/index.md`

Expected: Only the two Old Man's War entries (unless more re-reads exist in the data).

- [ ] **Step 5: Final commit if any cleanup needed**

Only if adjustments were made during verification. Otherwise, skip this step.
