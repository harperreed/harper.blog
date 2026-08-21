# ABOUTME: Backfill tool for missing local book cover images in content/books/.
# ABOUTME: Queries OpenLibrary first, then falls back to Goodreads og:image, validates, and saves.

import argparse
import glob
import logging
import os
import re
import sys
import tempfile
import time

import frontmatter
import requests

logger = logging.getLogger(__name__)

HTTP_TIMEOUT = 20
MIN_IMAGE_BYTES = 2048

JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

OPENLIBRARY_SEARCH_URL = "https://openlibrary.org/search.json"
OPENLIBRARY_COVERS_URL = "https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

RATE_LIMIT_SECONDS = 0.5
GOODREADS_RATE_LIMIT_SECONDS = 1.5

# Browser-ish User-Agent; still honest (identifies as a bot via the path component).
GOODREADS_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0 Safari/537.36 harper-blog-cover-backfill/1.0"
)

# Matches: <meta property="og:image" content="..." />
# Only the content attribute value is captured.
_OG_IMAGE_RE = re.compile(
    r'<meta\s[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_OG_IMAGE_RE_ALT = re.compile(
    r'<meta\s[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:image["\']',
    re.IGNORECASE,
)


def parse_og_image(html: str) -> str | None:
    """Extract the og:image URL from an HTML string.

    Returns the URL string when found and it starts with 'https:', else None.
    Accepts both attribute orderings of the meta tag.
    """
    for pattern in (_OG_IMAGE_RE, _OG_IMAGE_RE_ALT):
        m = pattern.search(html)
        if m:
            url = m.group(1).strip()
            if url.startswith("https:"):
                return url
    return None


def fetch_goodreads_cover_bytes(goodreads_link: str) -> bytes | None:
    """Fetch the book's cover image via the Goodreads og:image tag.

    Fetches the Goodreads page, parses only the og:image meta tag, then
    downloads the image URL found there. Returns raw bytes or None.
    Never writes the intermediate HTML to disk.
    Backs off politely (GOODREADS_RATE_LIMIT_SECONDS) after each page fetch.
    """
    if not goodreads_link:
        return None

    headers = {"User-Agent": GOODREADS_USER_AGENT}
    try:
        resp = requests.get(goodreads_link, headers=headers, timeout=HTTP_TIMEOUT)
    except requests.RequestException as e:
        logger.warning(f"Goodreads fetch failed for {goodreads_link}: {e}")
        return None

    time.sleep(GOODREADS_RATE_LIMIT_SECONDS)

    if resp.status_code in (403, 429):
        logger.warning(
            f"Goodreads blocked request (HTTP {resp.status_code}) for {goodreads_link} — skipping"
        )
        return None

    if resp.status_code != 200:
        logger.warning(f"Goodreads returned HTTP {resp.status_code} for {goodreads_link}")
        return None

    # Detect CAPTCHA / block pages heuristically — no og:image means nothing to do.
    html = resp.text
    image_url = parse_og_image(html)
    if not image_url:
        logger.info(f"No og:image found on Goodreads page: {goodreads_link}")
        return None

    logger.debug(f"Goodreads og:image URL: {image_url}")

    try:
        img_resp = requests.get(image_url, headers=headers, timeout=HTTP_TIMEOUT, stream=True)
        img_resp.raise_for_status()

        chunks = []
        total = 0
        max_bytes = 10 * 1024 * 1024
        for chunk in img_resp.iter_content(chunk_size=65536):
            total += len(chunk)
            if total > max_bytes:
                logger.warning(f"Goodreads cover too large (>{max_bytes} B) at {image_url}")
                img_resp.close()
                return None
            chunks.append(chunk)

        return b"".join(chunks)
    except requests.RequestException as e:
        logger.warning(f"Failed to download Goodreads cover from {image_url}: {e}")
        return None


def find_missing_cover_bundles(books_dir: str) -> list[dict]:
    """Return bundles under books_dir that have index.md but no image file.

    Each returned dict has: dir, slug, title, book_author, asin, goodreads_link.
    """
    image_exts = {".jpg", ".jpeg", ".png", ".webp"}
    missing = []

    for index_file in sorted(glob.glob(os.path.join(books_dir, "*", "index.md"))):
        bundle_dir = os.path.dirname(index_file)
        slug = os.path.basename(bundle_dir)

        contents = os.listdir(bundle_dir)
        has_image = any(
            os.path.splitext(f)[1].lower() in image_exts for f in contents
        )
        if has_image:
            continue

        try:
            post = frontmatter.load(index_file)
        except Exception as e:
            logger.warning(f"Could not parse {index_file}: {e}")
            continue

        missing.append(
            {
                "dir": bundle_dir,
                "slug": slug,
                "title": post.get("title", ""),
                "book_author": post.get("book_author", ""),
                "asin": post.get("asin", ""),
                "goodreads_link": post.get("goodreads_link", ""),
            }
        )

    return missing


def cover_target_path(bundle: dict) -> str:
    """Return the absolute path where the cover image should be saved."""
    asin = bundle.get("asin", "")
    filename = f"{asin}.jpg" if asin else "cover.jpg"
    return os.path.join(bundle["dir"], filename)


def is_valid_image(data: bytes) -> bool:
    """Return True if data looks like a real JPEG or PNG of adequate size."""
    if len(data) < MIN_IMAGE_BYTES:
        return False
    if data[:3] == JPEG_MAGIC:
        return True
    if data[:8] == PNG_MAGIC:
        return True
    return False


def fetch_openlibrary_cover_id(title: str, author: str) -> int | None:
    """Search OpenLibrary for a book and return the cover_i, or None if not found."""
    params = {
        "title": title,
        "author": author,
        "fields": "title,author_name,cover_i",
        "limit": "5",
    }
    try:
        resp = requests.get(OPENLIBRARY_SEARCH_URL, params=params, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.warning(f"OpenLibrary search failed for '{title}': {e}")
        return None
    except ValueError as e:
        logger.warning(f"OpenLibrary returned non-JSON for '{title}': {e}")
        return None

    docs = data.get("docs", [])
    for doc in docs:
        cover_id = doc.get("cover_i")
        if cover_id and isinstance(cover_id, int) and cover_id > 0:
            logger.debug(
                f"Found OpenLibrary cover_i={cover_id} for '{doc.get('title')}'"
            )
            return cover_id

    logger.info(f"No cover found on OpenLibrary for '{title}' by '{author}'")
    return None


def download_cover_bytes(cover_id: int) -> bytes | None:
    """Download the large cover image from OpenLibrary. Returns raw bytes or None."""
    url = OPENLIBRARY_COVERS_URL.format(cover_id=cover_id)
    try:
        resp = requests.get(url, timeout=HTTP_TIMEOUT, stream=True)
        resp.raise_for_status()

        chunks = []
        total = 0
        max_bytes = 10 * 1024 * 1024  # 10 MB ceiling
        for chunk in resp.iter_content(chunk_size=65536):
            total += len(chunk)
            if total > max_bytes:
                logger.warning(f"Cover too large (>{max_bytes} B) at {url}, skipping")
                resp.close()
                return None
            chunks.append(chunk)

        return b"".join(chunks)
    except requests.RequestException as e:
        logger.warning(f"Failed to download cover from {url}: {e}")
        return None


def save_cover(data: bytes, target_path: str) -> bool:
    """Write cover bytes to target_path atomically. Returns True on success."""
    target_dir = os.path.dirname(os.path.abspath(target_path))
    tmp_path = None
    try:
        fd, tmp_path = tempfile.mkstemp(dir=target_dir, suffix=".tmp")
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp_path, target_path)
        tmp_path = None
        return True
    except OSError as e:
        logger.error(f"Failed to save cover to {target_path}: {e}")
        return False
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)


def process_bundle(bundle: dict, dry_run: bool) -> str:
    """Attempt to fetch and save a cover for one bundle.

    Tries OpenLibrary first; falls back to Goodreads og:image when that yields nothing.
    Returns a status string: 'fetched', 'no_cover', 'failed', or 'skipped'.
    """
    title = bundle["title"]
    author = bundle["book_author"]
    goodreads_link = bundle.get("goodreads_link", "")
    target = cover_target_path(bundle)

    if os.path.exists(target):
        logger.info(f"Already exists, skipping: {target}")
        return "skipped"

    logger.info(f"Looking up cover for '{title}' by '{author}'")
    cover_id = fetch_openlibrary_cover_id(title, author)

    data: bytes | None = None
    any_source_failed = False  # True when a source returned bytes that failed validation

    if cover_id is not None:
        data = download_cover_bytes(cover_id)
        if data is not None and not is_valid_image(data):
            logger.warning(
                f"OpenLibrary image validation failed for '{title}': {len(data)} bytes, "
                f"magic={data[:8].hex() if data else 'empty'}"
            )
            any_source_failed = True
            data = None

    if data is None:
        if goodreads_link:
            logger.info(f"Trying Goodreads fallback for '{title}'")
            raw = fetch_goodreads_cover_bytes(goodreads_link)
            if raw is not None:
                if is_valid_image(raw):
                    data = raw
                else:
                    logger.warning(
                        f"Goodreads image validation failed for '{title}': {len(raw)} bytes, "
                        f"magic={raw[:8].hex() if raw else 'empty'}"
                    )
                    any_source_failed = True
        else:
            logger.info(f"No Goodreads link for '{title}', cannot try fallback")

    if data is None:
        if any_source_failed:
            logger.warning(f"All cover sources failed for '{title}'")
            return "failed"
        logger.info(f"No cover found for '{title}'")
        return "no_cover"

    if dry_run:
        logger.info(f"[dry-run] Would save {len(data)} bytes to {target}")
        return "fetched"

    if save_cover(data, target):
        logger.info(f"Saved cover to {target} ({len(data)} bytes)")
        return "fetched"
    else:
        return "failed"


def main(books_dir: str | None = None, dry_run: bool = False) -> int:
    """Backfill missing book covers. Returns 0 on clean run, 1 on run-level failure."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)-24s %(levelname)-8s %(message)s",
    )

    if books_dir is None:
        here = os.path.dirname(os.path.abspath(__file__))
        books_dir = os.path.join(here, "..", "content", "books")

    books_dir = os.path.abspath(books_dir)

    if not os.path.isdir(books_dir):
        logger.error(f"Books directory not found: {books_dir}")
        return 1

    bundles = find_missing_cover_bundles(books_dir)
    logger.info(f"Found {len(bundles)} bundle(s) missing a cover image")

    counts = {"fetched": 0, "no_cover": 0, "failed": 0, "skipped": 0}

    for i, bundle in enumerate(bundles, 1):
        logger.info(
            f"[{i}/{len(bundles)}] {bundle['slug']}"
        )
        status = process_bundle(bundle, dry_run=dry_run)
        counts[status] = counts.get(status, 0) + 1

        if i < len(bundles):
            time.sleep(RATE_LIMIT_SECONDS)

    logger.info(
        f"Done. fetched={counts['fetched']} no_cover={counts['no_cover']} "
        f"failed={counts['failed']} skipped={counts['skipped']}"
    )
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backfill missing book cover images from OpenLibrary."
    )
    parser.add_argument(
        "--books-dir",
        default=None,
        help="Path to content/books/ directory (default: ../content/books/ relative to this script)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fetched without writing any files.",
    )
    args = parser.parse_args()
    sys.exit(main(books_dir=args.books_dir, dry_run=args.dry_run))
