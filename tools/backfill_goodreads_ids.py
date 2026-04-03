# ABOUTME: One-time backfill script that adds goodreads_work_id to book entry frontmatter.
# ABOUTME: Reads work.id from data/books/*.yaml and writes it into content/books/*/index.md.

import os
import logging
import yaml
import frontmatter
import glob
from collections import defaultdict

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


def check_is_reread(data_file_path: str) -> bool:
    """
    Reads popular_shelves.shelf from a data/books/*.yaml file and returns True
    if any shelf entry has @name equal to 're-read'.

    Args:
        data_file_path: Path to the YAML data file.

    Returns:
        True if the re-read shelf is present, False otherwise.
    """
    with open(data_file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    popular_shelves = data.get("popular_shelves")
    if not popular_shelves or not isinstance(popular_shelves, dict):
        return False

    shelves = popular_shelves.get("shelf")
    if not shelves or not isinstance(shelves, list):
        return False

    return any(shelf.get("@name") == "re-read" for shelf in shelves)


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

        needs_update = False

        if not post.get("goodreads_work_id"):
            post["goodreads_work_id"] = work_id
            needs_update = True

        if not post.get("is_reread") and check_is_reread(data_file):
            post["is_reread"] = True
            logger.info(f"Marked {slug} as re-read")
            needs_update = True

        if needs_update:
            with open(content_file, "wb") as f:
                frontmatter.dump(post, f)
            logger.info(f"Updated {slug}")
            stats["updated"] += 1
        else:
            logger.debug(f"Already up to date: {slug}")
            stats["skipped"] += 1

    return stats


def detect_and_link_rereads(content_dir: str) -> int:
    """
    Scans all book entries for shared goodreads_work_id values and
    populates related_reads on entries that share the same work ID.

    Args:
        content_dir: Path to content/books/ directory.

    Returns:
        Number of entries updated with new related_reads links.
    """
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


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Backfill goodreads_work_id into book content frontmatter."
    )
    parser.add_argument(
        "--data-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "books"),
        help="Path to data/books/ directory",
    )
    parser.add_argument(
        "--content-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "content", "books"),
        help="Path to content/books/ directory",
    )
    args = parser.parse_args()

    stats = backfill_work_ids(
        data_dir=os.path.realpath(args.data_dir),
        content_dir=os.path.realpath(args.content_dir),
    )
    print(
        f"Done. Updated: {stats['updated']}, Skipped: {stats['skipped']}, Missing: {stats['missing']}"
    )

    logging.info("Step 2: Detecting and linking re-reads...")
    linked = detect_and_link_rereads(content_dir=os.path.realpath(args.content_dir))
    print(f"Linked {linked} entries as re-reads")
