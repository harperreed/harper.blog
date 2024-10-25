# Welcome to the Tools Repository! 🚀

This repository contains a suite of powerful tools designed to help you manage and process micro posts and starred links seamlessly. Created by [harperreed](https://github.com/harperreed), these tools allow you to convert, store, and manipulate data from various sources. Let's dive in! 🌟

## 📖 Summary of Project

This project comprises two primary scripts:

1. **grab_micro_posts.py**: This script downloads JSON feeds, converts HTML content to Markdown, and processes any images associated with the posts to ensure a smooth integration into a Hugo blog.
2. **grab_starred_links.py**: This script fetches RSS feeds of starred links and converts them into Markdown format suitable for Hugo.

Additionally, the repository includes configuration files (like `requirements.txt` and `pyproject.toml`) to manage dependencies and environment setup effectively.

## 🔧 How to Use

### Prerequisites

Before using the tools, ensure you have the following installed:

- Python 3.12 or higher
- Dependencies defined in `requirements.txt` or `pyproject.toml`.

### Setup

1. **Install Dependencies**

   Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   or if using poetry:

   ```bash
   poetry install
   ```

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
   python grab_micro_posts.py
   ```

   To fetch starred links and convert them to Markdown, run:

   ```bash
   python grab_starred_links.py
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

- **Directory Structure**:
  ```
  tools/
  ├── README.md
  ├── grab_micro_posts.py       # Script to fetch and process micro posts
  ├── grab_starred_links.py     # Script to fetch and process starred links
  ├── pyproject.toml            # Configuration file for project dependencies
  ├── requirements.txt          # List of dependencies
  ```

---

This README is your starting point for exploring the repository. If you have any questions or suggestions, feel free to reach out! Happy coding! 🎉
