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
    parser.add_argument("--dry-run", action="store_true", help="Don't write any files")
    args = parser.parse_args()

    if args.dry_run:
        logging.info("Dry run mode — no files will be written")

    stats = backfill_work_ids(
        data_dir=os.path.realpath(args.data_dir),
        content_dir=os.path.realpath(args.content_dir),
    )
    print(
        f"Done. Updated: {stats['updated']}, Skipped: {stats['skipped']}, Missing: {stats['missing']}"
    )
