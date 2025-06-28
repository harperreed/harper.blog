from __future__ import print_function

import datetime
from openai import OpenAI
from pydantic import BaseModel
from typing import List
import json
import os
import requests
import logging
import yaml
import shutil
from slugify import slugify
from dotenv import load_dotenv
import xmltodict
from pprint import pprint
import frontmatter
from goodreads import review
from json import loads, dumps
from api_security import validate_api_key, safe_log_api_error, setup_secure_logging, mask_key_in_logs

load_dotenv()

# Setup secure logging
logger = setup_secure_logging(__name__)

# Suppress noisy third-party logging
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("oauthlib.oauth1.rfc5849").setLevel(logging.WARNING)

class BookSummary(BaseModel):
    Summary: str
    Tagline: str
    Description: str



def get_book_summary(book_metadata):
    logger.debug("Starting get_book_summary")
    try:
        openai_api_key = validate_api_key('OPENAI_API_KEY')
        client = OpenAI(api_key=openai_api_key)
        logger.debug("OpenAI client initialized")
    except ValueError as e:
        safe_log_api_error(logger, "Failed to validate OpenAI API key", {"error": str(e)})
        raise

    logger.info("Preparing to send request to OpenAI API")

    prompt = f"Return a summary, a tagline, and a longer full description (including info about the book, author, and ratings) based on the metadata provided: {json.dumps(book_metadata)} as json. do not include any links, or anythign that would be considered promotional. It should be written in the style of Harper Reed (technologist)."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "schema": BookSummary.model_json_schema(),
                    "name": "BookSummary",
                    "description": "A summary of the book",
                },
            },
            messages=[
                {
                    "role": "system",
                    "content": "You are a librarian and you are curating a book description.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        # {
                        #     "type": "image_url",
                        #     "image_url": {
                        #         "url": book_metadata['image_url'],
                        #     },
                        # },
                    ],
                },
            ],
        )
        logger.info("Successfully received response from OpenAI API")
        logger.debug(f"Full API response: {response}")
    except Exception as e:
        safe_log_api_error(logger, "Error occurred while calling OpenAI API", {"error": str(e)})
        raise

    logger.info("Extracting tags from API response")
    print(response.choices[0].message.content)
    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        safe_log_api_error(logger, "Failed to parse JSON from API response", {"error": str(e)})
        raise
    except AttributeError as e:
        safe_log_api_error(logger, "Unexpected API response structure", {"error": str(e)})
        raise
    except IndexError:
        logger.error("API response does not contain any choices")
        raise
    except Exception as e:
        safe_log_api_error(logger, "Unexpected error while processing API response", {"error": str(e)})
        raise

    if not isinstance(result, dict):
        logger.error(f"Unexpected result type: {type(result)}")
        raise TypeError("API response is not a dictionary")

    required_keys = ["Summary", "Tagline", "Description"]
    for key in required_keys:
        if key not in result:
            logger.error(f"Missing required key in API response: {key}")
            raise KeyError(f"API response is missing required key: {key}")

    logger.info("Successfully parsed and validated API response")
    logger.debug(f"Extracted result: {result}")

    logger.info("get_image_tags function completed successfully")
    return result


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
    logger.debug(f"Attempting to download image for book: {book['title']}")

    # Available Amazon image size variations
    sizes = ["_SCRM_", "_SCLZZZZZZZ"]

    for size in sizes:
        try:
            if asin:
                image_url = f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01.{size}.jpg"
                logger.debug(f"Trying Amazon URL: {image_url}")
            else:
                image_url = book.get("image_url")
                if not image_url:
                    logger.warning("No image URL available for book")
                    return
                logger.debug(f"Using fallback URL: {image_url}")

            if os.path.isfile(image_filename):
                logger.debug(f"Image already exists at {image_filename}")
                return

            response = requests.head(image_url, allow_redirects=True, timeout=10)

            # Validate response and content length
            if not response.ok:
                logger.warning(
                    f"Bad response from {image_url}: {response.status_code}"
                )
                continue

            content_length = int(response.headers.get("Content-Length", 0))
            if content_length <= 43:  # Amazon's minimum valid image size
                logger.warning(
                    f"Image too small ({content_length} bytes) for size {size}"
                )
                continue

            logger.info(f"Downloading image for {book['title']}, size {size}")

            with requests.get(image_url, stream=True, timeout=10) as r:
                r.raise_for_status()
                with open(image_filename, "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            logger.debug(f"Successfully saved image to {image_filename}")
            return  # Exit after successful download

        except requests.exceptions.RequestException as e:
            safe_log_api_error(logger, "Failed to download image", {"error": str(e)})
            continue
        except IOError as e:
            safe_log_api_error(logger, "Failed to save image file", {"error": str(e)})
            continue
        except Exception as e:
            safe_log_api_error(logger, "Unexpected error downloading image", {"error": str(e)})
            continue

    logger.warning(f"Failed to download image for {book['title']} in any size")


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
    logger.debug(f"Attempting to parse date string: {date_string}")

    if not date_string:
        logger.debug("Empty date string provided, returning empty string")
        return ""

    try:
        d = datetime.datetime.strptime(date_string, "%a %b %d %H:%M:%S %z %Y")
        iso_date = d.isoformat()
        logger.debug(f"Successfully converted date to ISO format: {iso_date}")
        return iso_date
    except ValueError as e:
        safe_log_api_error(logger, f"Failed to parse date string '{date_string}'", {"error": str(e)})
        return ""


def get_goodreads_book(id: str) -> dict:
    """
    Fetches a single book's metadata from the Goodreads API.

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
    logger.debug(f"Fetching book with ID: {id} from Goodreads API")

    try:
        consumer_key = validate_api_key("GOODREADS_KEY")
        logger.debug(f"Using Goodreads API key: {mask_key_in_logs(consumer_key)}")
    except ValueError as e:
        safe_log_api_error(logger, "Failed to validate Goodreads API key", {"error": str(e)})
        raise

    url = "https://www.goodreads.com/book/show.xml"
    params = {"key": consumer_key, "id": id}
    headers = {"User-Agent": "Harper Books 1.0", "Accept": "application/xml"}

    try:
        logger.debug(f"Making GET request to {url}")
        resp = requests.get(url=url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise
    except requests.exceptions.RequestException as e:
        safe_log_api_error(logger, "Request failed", {"error": str(e)})
        logger.debug(
            f"Response content: {resp.content[:500] if resp else 'No response'}"
        )
        raise

    try:
        logger.debug("Parsing XML response")
        res = xmltodict.parse(resp.content)
        if "GoodreadsResponse" not in res:
            raise KeyError("Missing GoodreadsResponse in API response")
        if "book" not in res["GoodreadsResponse"]:
            raise KeyError("Missing book data in API response")

        book = to_dict(res["GoodreadsResponse"]["book"])
        logger.info(f"Successfully fetched book: {book.get('title', 'Unknown Title')}")
        return book

    except (xmltodict.expat.ExpatError, KeyError) as e:
        safe_log_api_error(logger, "Failed to parse API response", {"error": str(e)})
        raise


def get_goodreads_books(limit: int = 200) -> list:
    """
    Fetches books directly from Goodreads API with their review data.

    Args:
        limit (int, optional): Maximum number of books to fetch. Defaults to 200.

    Returns:
        list: List of dictionaries containing book data with review information.

    Raises:
        ValueError: If GOODREADS_KEY environment variable is missing
        requests.exceptions.RequestException: If API request fails
        KeyError: If expected data is missing from API response
        xmltodict.expat.ExpatError: If XML parsing fails
    """
    logger.debug(f"Starting to fetch {limit} books from Goodreads API")

    try:
        consumer_key = validate_api_key("GOODREADS_KEY")
        logger.debug(f"Using Goodreads API key: {mask_key_in_logs(consumer_key)}")
    except ValueError as e:
        safe_log_api_error(logger, "Failed to validate Goodreads API key", {"error": str(e)})
        raise

    params = {
        "shelf": "read",
        "v": "2",
        "sort": "date_read",
        "per_page": str(limit),
        "page": "1",
        "key": consumer_key,
    }

    url = "https://www.goodreads.com/review/list/37082.xml"

    try:
        logger.debug(f"Making GET request to {url}")
        resp = requests.get(
            url=url,
            params=params,
            headers={"User-Agent": "Harper Books 1.0"},
            timeout=10,
        )
        resp.raise_for_status()

    except requests.exceptions.Timeout:
        logger.error("Request to Goodreads API timed out")
        raise
    except requests.exceptions.RequestException as e:
        safe_log_api_error(logger, "Failed to fetch books from Goodreads", {"error": str(e)})
        logger.debug(
            f"Response content: {resp.content[:500] if resp else 'No response'}"
        )
        raise

    try:
        logger.debug("Parsing XML response")
        res = xmltodict.parse(resp.content)
        if "GoodreadsResponse" not in res:
            raise KeyError("Missing GoodreadsResponse in API response")
        if "reviews" not in res["GoodreadsResponse"]:
            raise KeyError("Missing reviews data in API response")

        res = res["GoodreadsResponse"]
        reviews = [review.GoodreadsReview(r) for r in res["reviews"]["review"]]

    except (xmltodict.expat.ExpatError, KeyError) as e:
        safe_log_api_error(logger, "Failed to parse API response", {"error": str(e)})
        raise

    logger.info(f"Successfully fetched {len(reviews)} reviews")
    books = []

    for r in reviews:
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
                logger.warning(
                    f"Book missing ID: {book.get('title', 'Unknown Title')}"
                )
                continue

            # Store full book data as JSON string
            book["json"] = json.dumps(book)

            # Convert all date fields
            for date_field in ["date", "started_at", "read_at"]:
                book[date_field] = (
                    fix_date(book[date_field]) if book[date_field] else ""
                )

            books.append(book)

        except Exception as e:
            safe_log_api_error(logger, "Error processing book review", {"error": str(e)})
            continue

    logger.info(f"Successfully processed {len(books)} books")
    return books


def create_post_metadata(book_data, book, summary, asin, author):
    """
    Creates metadata dictionary for the frontmatter post
    """

    return {
        "title": book_data["title"],
        "translationKey": f"{book_data['title']}-{asin}",
        "title_without_series": book.get("title_without_series", ""),
        "date": book["read_at"],
        "num_pages": book.get("num_pages", 0),
        "review_rating": book["review_rating"],
        "average_rating": book["average_rating"],
        "goodreads_link": book["link"],
        "started_at": book["started_at"],
        "image_url": f"https://images-na.ssl-images-amazon.com/images/P/{asin}.01._SCLZZZZZZZ.jpg",
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
    Now uses frontmatter library for post creation.
    """
    logger.info("Starting main processing")

    hugo_data_dir = "../data/books/"
    hugo_book_dir = "../content/books/"

    # Ensure directories exist
    os.makedirs(hugo_data_dir, exist_ok=True)
    os.makedirs(hugo_book_dir, exist_ok=True)

    logger.info("Fetching books from Goodreads API")
    try:
        books = get_goodreads_books(limit=15)
    except Exception as e:
        safe_log_api_error(logger, "Failed to get books from Goodreads", {"error": str(e)})
        raise

    for book in books:
        logger.debug(f"Processing book: {book['title']}")
  
        
        # date = datetime.fromisoformat(book['date'])\
        date_pattern = "%Y-%m-%dT%H:%M:%S%z"
        datetime_object = datetime.datetime.strptime(book['date'], date_pattern)
        date_str = datetime_object.strftime("%Y-%m-%d")
        
        content_filename = f"{date_str} {book['title']}"

        post_directory = os.path.join(hugo_book_dir, slugify(content_filename))
        os.makedirs(post_directory, exist_ok=True)

        data_filename = os.path.join(hugo_data_dir, f"{slugify(content_filename)}.yaml")
        book_data = {}

        # Get or load book data
        if not os.path.isfile(data_filename):
            logger.info(f"Fetching new book data for {book['title']}")
            try:
                book_data = get_goodreads_book(book["id"])
                book_data.update(book)

                with open(data_filename, "w", encoding="utf-8") as f:
                    yaml.safe_dump(book_data, f, default_flow_style=False)
            except Exception as e:
                safe_log_api_error(logger, f"Failed processing book data for {book['title']}", {"error": str(e)})
                continue
        else:
            logger.debug(f"Loading existing book data from {data_filename}")
            try:
                with open(data_filename, "r", encoding="utf-8") as stream:
                    book_data = yaml.safe_load(stream)
            except Exception as e:
                safe_log_api_error(logger, f"Failed loading book data from {data_filename}", {"error": str(e)})
                continue

        # Determine ASIN
        asin = (
            book_data.get("asin", "")
            or book_data.get("kindle_asin", "")
            or book_data.get("isbn", "")
        )

        # Generate blog post
        post_filename = os.path.join(post_directory, "index.md")
        if not os.path.isfile(post_filename):
            logger.info(f"Creating new post for {book['title']}")

            try:
                author = book["authors"]["author"]["name"]
                
                if book_data:
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
                safe_log_api_error(logger, f"Failed creating post for {book['title']}", {"error": str(e)})
                continue

        # Download cover image
        if asin:
            image_filename = os.path.join(post_directory, f"{asin}.jpg")
            if not os.path.isfile(image_filename):
                logger.info(f"Downloading cover image for {book['title']}")
                try:
                    downloadAmazonImage(asin, book_data, "", image_filename)
                except Exception as e:
                    safe_log_api_error(logger, f"Failed downloading image for {book['title']}", {"error": str(e)})

    logger.info("Main processing completed")

if __name__ == "__main__":
    main()
