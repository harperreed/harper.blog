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

load_dotenv()



logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("oauthlib.oauth1.rfc5849").setLevel(logging.WARNING)

class BookSummary(BaseModel):
    Summary: str
    Tagline: str
    Description: str



def get_book_summary(book_metadata):
    logging.debug("Starting get_book_summary")
    client = OpenAI()
    logging.debug("OpenAI client initialized")

    logging.info("Preparing to send request to OpenAI API")

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
        logging.info("Successfully received response from OpenAI API")
        logging.debug(f"Full API response: {response}")
    except Exception as e:
        logging.error(f"Error occurred while calling OpenAI API: {str(e)}")
        raise

    logging.info("Extracting tags from API response")
    print(response.choices[0].message.content)
    try:
        result = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON from API response: {str(e)}")
        raise
    except AttributeError as e:
        logging.error(f"Unexpected API response structure: {str(e)}")
        raise
    except IndexError:
        logging.error("API response does not contain any choices")
        raise
    except Exception as e:
        logging.error(f"Unexpected error while processing API response: {str(e)}")
        raise

    if not isinstance(result, dict):
        logging.error(f"Unexpected result type: {type(result)}")
        raise TypeError("API response is not a dictionary")

    required_keys = ["Summary", "Tagline", "Description"]
    for key in required_keys:
        if key not in result:
            logging.error(f"Missing required key in API response: {key}")
            raise KeyError(f"API response is missing required key: {key}")

    logging.info("Successfully parsed and validated API response")
    logging.debug(f"Extracted result: {result}")

    logging.info("get_image_tags function completed successfully")
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
        logging.error(f"Failed to parse date string '{date_string}': {str(e)}")
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
    logging.debug(f"Fetching book with ID: {id} from Goodreads API")

    consumer_key = os.getenv("GOODREADS_KEY")
    if not consumer_key:
        logging.error("GOODREADS_KEY environment variable not found")
        raise ValueError("Missing GOODREADS_KEY in environment variables")

    url = "https://www.goodreads.com/book/show.xml"
    params = {"key": consumer_key, "id": id}
    headers = {"User-Agent": "Harper Books 1.0", "Accept": "application/xml"}

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
            f"Response content: {resp.content[:500] if resp else 'No response'}"
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
    logging.debug(f"Starting to fetch {limit} books from Goodreads API")

    consumer_key = os.getenv("GOODREADS_KEY")
    if not consumer_key:
        logging.error("GOODREADS_KEY environment variable not found")
        raise ValueError("Missing GOODREADS_KEY in environment variables")

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
        logging.debug(f"Making GET request to {url}")
        resp = requests.get(
            url=url,
            params=params,
            headers={"User-Agent": "Harper Books 1.0"},
            timeout=10,
        )
        resp.raise_for_status()

    except requests.exceptions.Timeout:
        logging.error("Request to Goodreads API timed out")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch books from Goodreads: {str(e)}")
        logging.debug(
            f"Response content: {resp.content[:500] if resp else 'No response'}"
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
        reviews = [review.GoodreadsReview(r) for r in res["reviews"]["review"]]

    except (xmltodict.expat.ExpatError, KeyError) as e:
        logging.error(f"Failed to parse API response: {str(e)}")
        raise

    logging.info(f"Successfully fetched {len(reviews)} reviews")
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
                logging.warning(
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
            logging.error(f"Error processing book review: {str(e)}")
            continue

    logging.info(f"Successfully processed {len(books)} books")
    return books


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
    logging.info("Starting main processing")

    hugo_data_dir = "../data/books/"
    hugo_book_dir = "../content/books/"

    # Ensure directories exist
    os.makedirs(hugo_data_dir, exist_ok=True)
    os.makedirs(hugo_book_dir, exist_ok=True)

    logging.info("Fetching books from Goodreads API")
    try:
        books = get_goodreads_books(limit=15)
    except Exception as e:
        logging.error(f"Failed to get books from Goodreads: {str(e)}")
        raise

    for book in books:
        logging.debug(f"Processing book: {book['title']}")

        post_directory = os.path.join(hugo_book_dir, slugify(book["title"]))
        os.makedirs(post_directory, exist_ok=True)

        data_filename = os.path.join(hugo_data_dir, f"{slugify(book['title'])}.yaml")
        book_data = {}

        # Get or load book data
        if not os.path.isfile(data_filename):
            logging.info(f"Fetching new book data for {book['title']}")
            try:
                book_data = get_goodreads_book(book["id"])
                book_data.update(book)

                with open(data_filename, "w", encoding="utf-8") as f:
                    yaml.safe_dump(book_data, f, default_flow_style=False)
            except Exception as e:
                logging.error(f"Failed processing book data for {book['title']}: {str(e)}")
                continue
        else:
            logging.debug(f"Loading existing book data from {data_filename}")
            try:
                with open(data_filename, "r", encoding="utf-8") as stream:
                    book_data = yaml.safe_load(stream)
            except Exception as e:
                logging.error(f"Failed loading book data from {data_filename}: {str(e)}")
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
            logging.info(f"Creating new post for {book['title']}")

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
                logging.error(f"Failed creating post for {book['title']}: {str(e)}")
                continue

        # Download cover image
        if asin:
            image_filename = os.path.join(post_directory, f"{asin}.jpg")
            if not os.path.isfile(image_filename):
                logging.info(f"Downloading cover image for {book['title']}")
                try:
                    downloadAmazonImage(asin, book_data, "", image_filename)
                except Exception as e:
                    logging.error(f"Failed downloading image for {book['title']}: {str(e)}")

    logging.info("Main processing completed")

if __name__ == "__main__":
    main()
