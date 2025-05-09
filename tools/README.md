# Welcome to the Tools Repository! 🚀

This repository contains a suite of powerful tools designed to help you manage and process micro posts and starred links seamlessly. Created by [harperreed](https://github.com/harperreed), these tools allow you to convert, store, and manipulate data from various sources. Let's dive in! 🌟

## 📖 Summary of Project

This project comprises three primary scripts:

1. **grab_micro_posts.py**: This script downloads JSON feeds, converts HTML content to Markdown, and processes any images associated with the posts to ensure a smooth integration into a Hugo blog.
2. **grab_starred_links.py**: This script fetches RSS feeds of starred links and converts them into Markdown format suitable for Hugo.
3. **convert_posts_to_page_bundles.py**: This script converts posts in the `content/post` directory into page bundle directories, processes images in the markdown content, and updates the image paths.
4. **add_translation_keys.py**: This script adds or updates the translationKey in the frontmatter of Hugo content files, which is essential for multilingual content.

Additionally, the repository includes configuration files (like `pyproject.toml`) to manage dependencies and environment setup effectively.

## 🔧 How to Use

### Prerequisites

Before using the tools, ensure you have the following installed:

- Python 3.12 or higher
- Dependencies defined in `pyproject.toml`.

### Setup

1. **Dependencies**

   All dependencies are specified in the `pyproject.toml` file and managed with uv.
   No additional installation steps are needed as scripts are run directly with `uv run`.

2. **Environment Variables**

   Create a `.env` file in your project directory to store your environment variables:

   ```
   NOTES_JSON_FEED_URL=your_json_feed_url_here
   NOTES_HUGO_CONTENT_DIR=your_hugo_content_directory_here
   LINKS_RSS_URL=your_rss_feed_url_here
   LINKS_HUGO_CONTENT_DIR=your_hugo_content_directory_here
   ```

3. **Run the Scripts**

   To fetch micro posts and convert them to Markdown, run:

   ```bash
   uv run tools/grab_micro_posts.py
   ```

   To fetch starred links and convert them to Markdown, run:

   ```bash
   uv run tools/grab_starred_links.py
   ```

   To convert posts to page bundles, run:

   ```bash
   uv run tools/convert_posts_to_page_bundles.py
   ```
   
   To add translation keys to Hugo content files, run:
   
   ```bash
   uv run tools/add_translation_keys.py /path/to/content/directory
   
   # Directories are processed recursively by default. To disable recursive processing:
   uv run tools/add_translation_keys.py --no-recursive /path/to/content/directory
   
   # To use UUIDs instead of titles for translation keys:
   uv run tools/add_translation_keys.py --uuid /path/to/content/directory
   
   # To run in dry-run mode (no changes):
   uv run tools/add_translation_keys.py --dry-run /path/to/content/directory
   ```

## 🛠️ Tech Info

- **Languages and Frameworks**: Python
- **Key Libraries**:
  - `requests`: For HTTP requests to fetch feeds.
  - `feedparser`: To parse RSS feeds.
  - `html2text`: To convert HTML to Markdown.
  - `python-dotenv`: For loading environment variables from the `.env` file.
  - `python-frontmatter`: For handling front matter in Markdown files.
  - `python-slugify`: To create URL-friendly slugs.
  - `logging`: For centralized logging configuration and error handling.

- **Directory Structure**:
  ```
  tools/
  ├── README.md
  ├── grab_micro_posts.py       # Script to fetch and process micro posts
  ├── grab_starred_links.py     # Script to fetch and process starred links
  ├── convert_posts_to_page_bundles.py # Script to convert posts to page bundles
  ├── add_translation_keys.py   # Script to add translation keys to Hugo content
  ├── pyproject.toml            # Configuration file for project dependencies
  ```

## 📝 Logging and Error Handling

All scripts in this repository use the `logging` module for logging instead of print statements. A centralized logging configuration is set up at the beginning of each script. Errors are logged with appropriate severity levels (e.g., `logging.error`, `logging.warning`).

Comprehensive error handling is implemented in all scripts. Exceptions are caught and logged with detailed error messages. Retry mechanisms are added where appropriate to handle transient errors.

---

This README is your starting point for exploring the repository. If you have any questions or suggestions, feel free to reach out! Happy coding! 🎉
