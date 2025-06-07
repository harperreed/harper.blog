from __future__ import print_function

import datetime
import json
import os
import requests
import logging
import yaml
import shutil
import time
from slugify import slugify
from dotenv import load_dotenv
import xmltodict
import frontmatter
from goodreads import review
from json import loads, dumps
from diskcache import Cache
from typing import List, Dict, Any, Optional
import argparse

load_dotenv()

# Set up logging
logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Suppress verbose logging from libraries
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("oauthlib.oauth1.rfc5849").setLevel(logging.WARNING)

# Initialize disk cache
cache = Cache("./book_cache")

def to_dict(input_ordered_dict):
    """
    Converts an OrderedDict to a dictionary.
    """
    return loads(dumps(input_ordered_dict))

def fix_date(date_string: str) -> str:
    """
    Converts a date string from Goodreads format to ISO format.

    Args:
        date_string (str): Date string in format "%a %b %d %H:%M:%S %z %Y"
            (e.g. "Wed Jan 01 12:00:00 +0000 2020")

    Returns:
        str: ISO formatted date string (e.g. "2020-01-01T12:00:00+00:00")
            or empty string if input is empty/invalid

    Raises:
        ValueError: If date_string is in invalid format
    """
    logging.debug(f"Attempting to parse date string: {date_string}")

    if not date_string:
        logging.debug("Empty date string provided, returning empty string")
        return ""

    try:
        d = datetime.datetime.strptime(date_string, "%a %b %d %H:%M:%S %z %Y")
        iso_date = d.isoformat()
        logging.debug(f"Successfully converted date to ISO format: {iso_date}")
        return iso_date
    except ValueError as e:
        logging.warning(f"Failed to parse date string '{date_string}': {str(e)}")
        return date_string  # Return original on error

@cache.memoize(expire=604800)  # Cache for one week
def get_goodreads_book(id: str) -> dict:
    """
    Fetches a single book's metadata from the Goodreads API with caching.

    Args:
        id (str): The Goodreads book ID to fetch

    Returns:
        dict: Book metadata including title, author, description etc.

    Raises:
        ValueError: If GOODREADS_KEY environment variable is missing
        requests.exceptions.RequestException: If API request fails
        KeyError: If expected data is missing from API response
        xmltodict.expat.ExpatError: If XML parsing fails
    """
    logging.debug(f"Fetching book with ID: {id} from Goodreads API or cache")

    consumer_key = os.getenv("GOODREADS_KEY")
    if not consumer_key:
        logging.error("GOODREADS_KEY environment variable not found")
        raise ValueError("Missing GOODREADS_KEY in environment variables")

    url = "https://www.goodreads.com/book/show.xml"
    params = {"key": consumer_key, "id": id}
    headers = {"User-Agent": "Harper Books Historical Backfill 1.0", "Accept": "application/xml"}

    try:
        logging.debug(f"Making GET request to {url}")
        resp = requests.get(url=url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()

    except requests.exceptions.Timeout:
        logging.error("Request timed out")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        logging.debug(
            f"Response content: {resp.content[:500] if 'resp' in locals() else 'No response'}"
        )
        raise

    try:
        logging.debug("Parsing XML response")
        res = xmltodict.parse(resp.content)
        if "GoodreadsResponse" not in res:
            raise KeyError("Missing GoodreadsResponse in API response")
        if "book" not in res["GoodreadsResponse"]:
            raise KeyError("Missing book data in API response")

        book = to_dict(res["GoodreadsResponse"]["book"])
        logging.info(f"Successfully fetched book: {book.get('title', 'Unknown Title')}")
        return book

    except (xmltodict.expat.ExpatError, KeyError) as e:
        logging.error(f"Failed to parse API response: {str(e)}")
        raise

def get_goodreads_reviews_page(page: int, limit: int = 200) -> List[Dict]:
    """
    Fetches a page of book reviews from Goodreads API.

    Args:
        page (int): Page number to fetch
        limit (int): Number of reviews per page

    Returns:
        List[Dict]: List of review objects

    Raises:
        Various exceptions on failure
    """
    cache_key = f"goodreads_reviews_page_{page}_{limit}"
    cached_data = cache.get(cache_key)
    
    if cached_data is not None:
        logging.info(f"Using cached data for page {page}")
        return cached_data
    
    logging.info(f"Fetching page {page} of reviews from Goodreads API")
    
    consumer_key = os.getenv("GOODREADS_KEY")
    if not consumer_key:
        logging.error("GOODREADS_KEY environment variable not found")
        raise ValueError("Missing GOODREADS_KEY in environment variables")

    params = {
        "shelf": "read",
        "v": "2",
        "sort": "date_read",
        "per_page": str(limit),
        "page": str(page),
        "key": consumer_key,
    }

    url = "https://www.goodreads.com/review/list/37082.xml"

    try:
        logging.debug(f"Making GET request to {url} for page {page}")
        resp = requests.get(
            url=url,
            params=params,
            headers={"User-Agent": "Harper Books Historical Backfill 1.0"},
            timeout=10,
        )
        resp.raise_for_status()

    except requests.exceptions.Timeout:
        logging.error(f"Request to Goodreads API timed out for page {page}")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch reviews from Goodreads for page {page}: {str(e)}")
        logging.debug(
            f"Response content: {resp.content[:500] if 'resp' in locals() else 'No response'}"
        )
        raise

    try:
        logging.debug("Parsing XML response")
        res = xmltodict.parse(resp.content)
        if "GoodreadsResponse" not in res:
            raise KeyError("Missing GoodreadsResponse in API response")
        if "reviews" not in res["GoodreadsResponse"]:
            raise KeyError("Missing reviews data in API response")

        res = res["GoodreadsResponse"]
        reviews_data = res["reviews"]["review"]
        
        # Process reviews
        reviews = [process_review(review.GoodreadsReview(r)) for r in reviews_data]
        
        # Store in cache for one week
        cache.set(cache_key, reviews, expire=604800)
        
        # Get total number of reviews and pages if available
        total = int(res["reviews"].get("@total", "0"))
        logging.info(f"Total reviews available: {total}")
        
        return reviews

    except (xmltodict.expat.ExpatError, KeyError) as e:
        logging.error(f"Failed to parse API response for page {page}: {str(e)}")
        raise

def process_review(r) -> Dict:
    """
    Process a single review into a book dictionary.
    
    Args:
        r: A GoodreadsReview object
        
    Returns:
        Dict: Processed book data
    """
    try:
        book = to_dict(r.book)

        # Add review data to book dict
        book.update(
            {
                "review_rating": r.rating,
                "owned": r.owned,
                "review_url": r.url,
                "read_at": str(r.read_at) if r.read_at else "",
                "started_at": str(r.started_at) if r.started_at else "",
                "date": str(r.read_at)
                if r.read_at
                else (str(r.started_at) if r.started_at else ""),
            }
        )

        # Extract ID from nested structure
        book["id"] = book.get("id", {}).get("#text", "")
        if not book["id"]:
            logging.warning(
                f"Book missing ID: {book.get('title', 'Unknown Title')}"
            )
            return None

        # Store full book data as JSON string
        book["json"] = json.dumps(book)

        # Convert all date fields
        for date_field in ["date", "started_at", "read_at"]:
            book[date_field] = (
                fix_date(book[date_field]) if book[date_field] else ""
            )

        return book

    except Exception as e:
        logging.error(f"Error processing book review: {str(e)}")
        return None

def get_all_goodreads_books(max_pages: int = 10) -> List[Dict]:
    """
    Fetches all books across multiple pages.
    
    Args:
        max_pages (int): Maximum number of pages to fetch
        
    Returns:
        List[Dict]: All books fetched from all pages
    """
    all_books = []
    page = 1
    
    while page <= max_pages:
        try:
            logging.info(f"Fetching page {page} of {max_pages}")
            books = get_goodreads_reviews_page(page)
            
            if not books:
                logging.info(f"No more books found on page {page}")
                break
                
            all_books.extend([b for b in books if b is not None])
            logging.info(f"Retrieved {len(books)} books from page {page}")
            
            # Be nice to the API
            time.sleep(1)
            
            page += 1
            
        except Exception as e:
            logging.error(f"Error fetching page {page}: {e}")
            break
    
    logging.info(f"Retrieved a total of {len(all_books)} books")
    return all_books

def downloadAmazonImage(asin: str, book: dict, url: str, image_filename: str) -> None:
    """
    Downloads book cover images from Amazon or falls back to provided image URL.

    Args:
        asin (str): Amazon ASIN identifier for the book
        book (dict): Dictionary containing book metadata including title and image_url
        url (str): Fallback URL if Amazon image not available
        image_filename (str): Path where image should be saved

    Raises:
        requests.exceptions.RequestException: If image download fails
        IOError: If file cannot be written
    """
    logging.debug(f"Attempting to download image for book: {book['title']}")

    # Available Amazon image size variations
    sizes = ["_SCRM_", "_SCLZZZZZZZ"]

    for size in sizes:
        try:
            if asin:
                image_url = f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.{size}.jpg"
                logging.debug(f"Trying Amazon URL: {image_url}")
            else:
                image_url = book.get("image_url")
                if not image_url:
                    logging.warning("No image URL available for book")
                    return
                logging.debug(f"Using fallback URL: {image_url}")

            if os.path.isfile(image_filename):
                logging.debug(f"Image already exists at {image_filename}")
                return

            response = requests.head(image_url, allow_redirects=True, timeout=10)

            # Validate response and content length
            if not response.ok:
                logging.warning(
                    f"Bad response from {image_url}: {response.status_code}"
                )
                continue

            content_length = int(response.headers.get("Content-Length", 0))
            if content_length <= 43:  # Amazon's minimum valid image size
                logging.warning(
                    f"Image too small ({content_length} bytes) for size {size}"
                )
                continue

            logging.info(f"Downloading image for {book['title']}, size {size}")

            with requests.get(image_url, stream=True, timeout=10) as r:
                r.raise_for_status()
                with open(image_filename, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            logging.debug(f"Successfully saved image to {image_filename}")
            return  # Exit after successful download

        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download image: {str(e)}")
            continue
        except IOError as e:
            logging.error(f"Failed to save image file: {str(e)}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error downloading image: {str(e)}")
            continue

    logging.warning(f"Failed to download image for {book['title']} in any size")

def get_book_summary(book_metadata: Dict) -> Dict:
    """
    Create a simple summary from book metadata without relying on OpenAI.
    
    Args:
        book_metadata: Dictionary with book metadata
        
    Returns:
        Dict: Summary dictionary with Summary, Tagline, and Description fields
    """
    title = book_metadata.get("title", "Unknown Title")
    author = book_metadata.get("authors", {}).get("author", {}).get("name", "Unknown Author")
    avg_rating = book_metadata.get("average_rating", "0")
    num_pages = book_metadata.get("num_pages", "Unknown")
    
    # Generate simple summary fields
    tagline = f"A {num_pages}-page book by {author}"
    
    summary = f"{title} by {author} - rated {avg_rating}/5 on Goodreads"
    
    # Use description from book or generate a placeholder
    description = book_metadata.get("description", "")
    if not description:
        description = f"This is {title} by {author}. The book has {num_pages} pages and an average rating of {avg_rating}/5 on Goodreads."
    
    return {
        "Summary": summary,
        "Tagline": tagline,
        "Description": description
    }

def create_post_metadata(book_data, book, summary, asin, author):
    """
    Creates metadata dictionary for the frontmatter post
    """
    return {
        "title": book_data["title"],
        "title_without_series": book.get("title_without_series", ""),
        "date": book["read_at"],
        "num_pages": book.get("num_pages", 0),
        "review_rating": book["review_rating"],
        "average_rating": book["average_rating"],
        "goodreads_link": book["link"],
        "started_at": book["started_at"],
        "image_url": f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SCLZZZZZZZ.jpg" if asin else "",
        "draft": False,
        "tagline": summary["Tagline"],
        "summary": summary["Summary"],
        "tags": [author],
        "layout": "book",
        "image": [asin + ".jpg"] if asin else [],
        "asin": asin,
        "yaml": slugify(book_data["title"]),
        "book_author": author
    }

def main():
    """
    Main function to process books from Goodreads API and generate Hugo blog posts.
    """
    parser = argparse.ArgumentParser(description='Backfill historical books from Goodreads')
    parser.add_argument('--pages', type=int, default=10, help='Maximum number of pages to fetch')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between book processing in seconds')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--retry', action='store_true', help='Retry failed books')
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logging.info(f"Starting historical book backfill, processing up to {args.pages} pages")

    hugo_data_dir = "../data/books/"
    hugo_book_dir = "../content/books/"

    # Ensure directories exist
    os.makedirs(hugo_data_dir, exist_ok=True)
    os.makedirs(hugo_book_dir, exist_ok=True)
    os.makedirs("./book_cache", exist_ok=True)

    logging.info("Fetching books from Goodreads API")
    try:
        books = get_all_goodreads_books(max_pages=args.pages)
    except Exception as e:
        logging.error(f"Failed to get books from Goodreads: {str(e)}")
        raise

    processed_count = 0
    skipped_count = 0
    failed_count = 0
    
    # Track processed books to avoid duplicates
    processed_ids = set()

    for book in books:
        book_id = book.get("id")
        
        # Skip duplicate books
        if book_id in processed_ids:
            logging.debug(f"Skipping duplicate book: {book['title']} (ID: {book_id})")
            continue
            
        processed_ids.add(book_id)
        
        logging.info(f"Processing book: {book['title']} (ID: {book_id})")
        
        try:
            # Parse date or use current date as fallback
            if book.get('date'):
                try:
                    date_pattern = "%Y-%m-%dT%H:%M:%S%z"
                    datetime_object = datetime.datetime.strptime(book['date'], date_pattern)
                    date_str = datetime_object.strftime("%Y-%m-%d")
                except ValueError:
                    # Fallback if date format is unexpected
                    logging.warning(f"Could not parse date: {book['date']}, using today's date")
                    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            else:
                # If no date at all, use current date
                date_str = datetime.datetime.now().strftime("%Y-%m-%d")
            
            content_filename = f"{date_str} {book['title']}"
            post_directory = os.path.join(hugo_book_dir, slugify(content_filename))
            data_filename = os.path.join(hugo_data_dir, f"{slugify(content_filename)}.yaml")
            
            # Skip if already processed and not in retry mode
            if os.path.isfile(data_filename) and os.path.isfile(os.path.join(post_directory, "index.md")) and not args.retry:
                logging.info(f"Skipping existing book: {book['title']}")
                skipped_count += 1
                continue
                
            os.makedirs(post_directory, exist_ok=True)
            
            # Get or load book data
            book_data = {}
            if not os.path.isfile(data_filename) or args.retry:
                logging.info(f"Fetching new book data for {book['title']}")
                try:
                    book_data = get_goodreads_book(book["id"])
                    book_data.update(book)

                    with open(data_filename, "w", encoding="utf-8") as f:
                        yaml.safe_dump(book_data, f, default_flow_style=False)
                except Exception as e:
                    logging.error(f"Failed processing book data for {book['title']}: {str(e)}")
                    failed_count += 1
                    continue
            else:
                logging.debug(f"Loading existing book data from {data_filename}")
                try:
                    with open(data_filename, "r", encoding="utf-8") as stream:
                        book_data = yaml.safe_load(stream)
                except Exception as e:
                    logging.error(f"Failed loading book data from {data_filename}: {str(e)}")
                    failed_count += 1
                    continue

            # Determine ASIN
            asin = (
                book_data.get("asin", "")
                or book_data.get("kindle_asin", "")
                or book_data.get("isbn", "")
            )

            # Generate blog post
            post_filename = os.path.join(post_directory, "index.md")
            if not os.path.isfile(post_filename) or args.retry:
                logging.info(f"Creating new post for {book['title']}")

                try:
                    author = book_data.get("authors", {}).get("author", {}).get("name", "Unknown Author")
                    
                    summary = get_book_summary(book_data)
                    
                    # Create post using frontmatter
                    post = frontmatter.Post(
                        content=summary.get("Description", ""),
                        **create_post_metadata(book_data, book, summary, asin, author)
                    )

                    # Write the post to file
                    with open(post_filename, "wb") as file:
                        frontmatter.dump(post, file, encoding="utf-8")

                except Exception as e:
                    logging.error(f"Failed creating post for {book['title']}: {str(e)}")
                    failed_count += 1
                    continue

            # Download cover image
            if asin:
                image_filename = os.path.join(post_directory, f"{asin}.jpg")
                if not os.path.isfile(image_filename) or args.retry:
                    logging.info(f"Downloading cover image for {book['title']}")
                    try:
                        downloadAmazonImage(asin, book_data, "", image_filename)
                    except Exception as e:
                        logging.error(f"Failed downloading image for {book['title']}: {str(e)}")

            processed_count += 1
            logging.info(f"Successfully processed book: {book['title']}")
            
            # Add delay between processing to be nice to APIs
            time.sleep(args.delay)
            
        except Exception as e:
            logging.error(f"Unexpected error processing book {book.get('title', 'Unknown')}: {str(e)}")
            failed_count += 1
            continue

    logging.info(f"Historical book backfill completed. Processed: {processed_count}, Skipped: {skipped_count}, Failed: {failed_count}")
    logging.info(f"Books data directory: {hugo_data_dir}")
    logging.info(f"Books content directory: {hugo_book_dir}")
    
    # Print cache stats
    logging.info(f"Cache statistics: {cache.stats()}")

if __name__ == "__main__":
    main()
