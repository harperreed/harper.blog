# ABOUTME: One-time script to fix 116 book entries with wrong 2025-02-25 dates.
# ABOUTME: Fetches date_added from Goodreads API and updates frontmatter.

import argparse
import datetime
import glob
import logging
import os

import frontmatter
import requests
import xmltodict
import yaml

logger = logging.getLogger(__name__)


def fetch_all_reviews(api_key: str) -> list[dict]:
    """
    Paginates through the Goodreads review list API and returns all raw review dicts.

    Args:
        api_key: Goodreads API key.

    Returns:
        List of raw review dicts from the API response.
    """
    url = "https://www.goodreads.com/review/list/37082.xml"
    per_page = 200
    page = 1
    all_reviews = []

    while True:
        params = {
            "shelf": "read",
            "v": "2",
            "sort": "date_read",
            "per_page": str(per_page),
            "page": str(page),
            "key": api_key,
        }
        headers = {"User-Agent": "Harper Books 1.0"}

        logger.info(f"Fetching page {page} from Goodreads review list API")
        resp = requests.get(url=url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()

        res = xmltodict.parse(resp.content)
        reviews = res["GoodreadsResponse"]["reviews"]["review"]

        # xmltodict returns a dict (not list) when there is only one result
        if isinstance(reviews, dict):
            reviews = [reviews]

        all_reviews.extend(reviews)
        logger.info(f"Fetched {len(reviews)} reviews on page {page}")

        if len(reviews) < per_page:
            break

        page += 1

    logger.info(f"Total reviews fetched: {len(all_reviews)}")
    return all_reviews


def _extract_book_id(review: dict) -> str | None:
    """
    Extracts the Goodreads book ID from a review dict.

    The book.id field may be a plain string or a nested dict
    like {"@type": "integer", "#text": "12345"}.

    Args:
        review: Raw review dict from the Goodreads API.

    Returns:
        Book ID as a string, or None if not found.
    """
    book_id = review.get("book", {}).get("id")
    if book_id is None:
        return None
    if isinstance(book_id, dict):
        return book_id.get("#text")
    return str(book_id)


def build_date_added_map(reviews: list[dict]) -> dict[str, str]:
    """
    Maps Goodreads book ID to ISO-formatted date_added from review dicts.

    Args:
        reviews: List of raw review dicts from the Goodreads API.

    Returns:
        Dict mapping book ID string → ISO 8601 date string.
    """
    date_map = {}

    for review in reviews:
        book_id = _extract_book_id(review)
        if not book_id:
            logger.debug("Skipping review with no book ID")
            continue

        date_added = review.get("date_added")
        if not date_added:
            logger.debug(f"Skipping book {book_id}: empty date_added")
            continue

        try:
            parsed = datetime.datetime.strptime(date_added, "%a %b %d %H:%M:%S %z %Y")
            date_map[book_id] = parsed.isoformat()
        except ValueError as e:
            logger.warning(f"Could not parse date_added '{date_added}' for book {book_id}: {e}")

    return date_map


def get_book_id_from_data_file(data_file: str) -> str | None:
    """
    Reads a data/books/*.yaml file and returns the book's Goodreads ID.

    Args:
        data_file: Path to the YAML data file.

    Returns:
        Book ID as a string, or None if not found.
    """
    with open(data_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    book_id = data.get("id")
    if book_id is None:
        return None

    # Handle nested dict format (unlikely in data files but defensive)
    if isinstance(book_id, dict):
        return book_id.get("#text")

    return str(book_id)


def fix_dates(content_dir: str, data_dir: str, date_map: dict[str, str]) -> dict:
    """
    Scans content_dir for 2025-02-25-* book directories and updates their
    frontmatter date field using values from date_map.

    Args:
        content_dir: Path to content/books/ directory.
        data_dir: Path to data/books/ directory.
        date_map: Dict mapping Goodreads book ID → ISO date string.

    Returns:
        Stats dict with keys: "fixed", "no_match", "skipped".
    """
    stats = {"fixed": 0, "no_match": 0, "skipped": 0}

    pattern = os.path.join(content_dir, "2025-02-25-*")
    candidate_dirs = sorted(glob.glob(pattern))

    for book_dir in candidate_dirs:
        if not os.path.isdir(book_dir):
            continue

        slug = os.path.basename(book_dir)
        content_file = os.path.join(book_dir, "index.md")

        if not os.path.isfile(content_file):
            logger.warning(f"No index.md in {book_dir}")
            stats["skipped"] += 1
            continue

        data_file = os.path.join(data_dir, f"{slug}.yaml")
        if not os.path.isfile(data_file):
            logger.warning(f"No data file for {slug}")
            stats["skipped"] += 1
            continue

        book_id = get_book_id_from_data_file(data_file)
        if not book_id:
            logger.warning(f"No book ID in data file for {slug}")
            stats["skipped"] += 1
            continue

        new_date = date_map.get(book_id)
        if not new_date:
            logger.info(f"No date_added in map for book {book_id} ({slug})")
            stats["no_match"] += 1
            continue

        post = frontmatter.load(content_file)
        post["date"] = new_date

        with open(content_file, "wb") as f:
            frontmatter.dump(post, f)

        logger.info(f"Fixed {slug}: {new_date}")
        stats["fixed"] += 1

    return stats


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(
        description="Fix 116 book entries with wrong 2025-02-25 dates using Goodreads date_added."
    )
    parser.add_argument(
        "--content-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "content", "books"),
        help="Path to content/books/ directory",
    )
    parser.add_argument(
        "--data-dir",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "books"),
        help="Path to data/books/ directory",
    )
    args = parser.parse_args()

    api_key = os.environ.get("GOODREADS_KEY")
    if not api_key:
        raise ValueError("GOODREADS_KEY environment variable is required")

    content_dir = os.path.realpath(args.content_dir)
    data_dir = os.path.realpath(args.data_dir)

    logger.info("Fetching all reviews from Goodreads API...")
    reviews = fetch_all_reviews(api_key)

    logger.info("Building date_added map...")
    date_map = build_date_added_map(reviews)
    logger.info(f"Built date map with {len(date_map)} entries")

    logger.info("Fixing book dates...")
    stats = fix_dates(content_dir, data_dir, date_map)

    print(
        f"Done. Fixed: {stats['fixed']}, No match: {stats['no_match']}, Skipped: {stats['skipped']}"
    )


if __name__ == "__main__":
    main()
