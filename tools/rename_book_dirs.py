# ABOUTME: One-time script to rename 2025-02-25-* book directories to match corrected frontmatter dates.
# ABOUTME: Also renames matching data/books/*.yaml files.

import os
import glob
import datetime
import logging
import shutil
import frontmatter

logger = logging.getLogger(__name__)


def rename_book_dirs(content_dir: str, data_dir: str) -> dict:
    """
    Renames content/books/2025-02-25-* directories and matching data files
    to use the corrected frontmatter date.

    Returns:
        Dict with counts: {"renamed": int, "skipped": int, "errors": int}
    """
    stats = {"renamed": 0, "skipped": 0, "errors": 0}

    for index_file in sorted(glob.glob(os.path.join(content_dir, "2025-02-25-*", "index.md"))):
        content_path = os.path.dirname(index_file)
        old_slug = os.path.basename(content_path)
        book_name = old_slug.replace("2025-02-25-", "", 1)

        post = frontmatter.load(index_file)
        date_val = post.get("date", "")
        if not date_val:
            logger.warning(f"No date in {old_slug}, skipping")
            stats["skipped"] += 1
            continue

        try:
            dt = datetime.datetime.fromisoformat(str(date_val))
            new_date = dt.strftime("%Y-%m-%d")
        except (ValueError, TypeError) as e:
            logger.error(f"Bad date in {old_slug}: {e}")
            stats["errors"] += 1
            continue

        if new_date == "2025-02-25":
            logger.warning(f"Date still 2025-02-25 in {old_slug}, skipping")
            stats["skipped"] += 1
            continue

        new_slug = f"{new_date}-{book_name}"
        new_content_path = os.path.join(content_dir, new_slug)

        if os.path.exists(new_content_path):
            logger.warning(f"Target already exists: {new_slug}, skipping")
            stats["skipped"] += 1
            continue

        # Rename content directory
        os.rename(content_path, new_content_path)
        logger.info(f"Renamed content: {old_slug} -> {new_slug}")

        # Rename data file if it exists
        old_data = os.path.join(data_dir, f"{old_slug}.yaml")
        new_data = os.path.join(data_dir, f"{new_slug}.yaml")
        if os.path.isfile(old_data):
            os.rename(old_data, new_data)
            logger.info(f"Renamed data: {old_slug}.yaml -> {new_slug}.yaml")

        # Update related_reads references in other files that point to the old slug
        for other_file in glob.glob(os.path.join(content_dir, "*", "index.md")):
            try:
                other_post = frontmatter.load(other_file)
                related = other_post.get("related_reads", [])
                if old_slug in related:
                    related = [new_slug if s == old_slug else s for s in related]
                    other_post["related_reads"] = related
                    with open(other_file, "wb") as f:
                        frontmatter.dump(other_post, f)
                    logger.info(f"Updated related_reads ref in {os.path.basename(os.path.dirname(other_file))}")
            except Exception:
                pass

        stats["renamed"] += 1

    return stats


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Rename 2025-02-25 book directories to match corrected dates.")
    parser.add_argument("--content-dir", default=os.path.join(os.path.dirname(__file__), "..", "content", "books"))
    parser.add_argument("--data-dir", default=os.path.join(os.path.dirname(__file__), "..", "data", "books"))
    args = parser.parse_args()

    stats = rename_book_dirs(
        content_dir=os.path.realpath(args.content_dir),
        data_dir=os.path.realpath(args.data_dir),
    )
    print(f"Done. Renamed: {stats['renamed']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")
