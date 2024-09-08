import requests
import json
import os
import re
from datetime import datetime
import html2text
import frontmatter
from slugify import slugify
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

def download_json_feed(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to download JSON feed. Status code: {response.status_code}")

def html_to_markdown(html_content):
    h = html2text.HTML2Text()
    h.wrap_links = False
    h.body_width = 0  # Disable line wrapping
    return h.handle(html_content)

def download_image(url, output_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def process_images(content, post_dir):
    img_pattern = re.compile(r'<img[^>]+src="([^">]+)"')
    img_matches = img_pattern.findall(content)
    for i, img_url in enumerate(img_matches):
        parsed_url = urlparse(img_url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        if not file_extension:
            file_extension = '.jpg'  # Default to .jpg if no extension is found
        local_img_path = f'image_{i + 1}{file_extension}'
        full_img_path = os.path.join(post_dir, local_img_path)
        if download_image(img_url, full_img_path):
            content = content.replace(img_url, local_img_path)
    return content

def create_hugo_content(entry, output_dir):
    title = entry.get('title', 'Untitled')
    content = entry.get('content_html') or entry.get('content_text', '')
    date_str = entry.get('date_published', datetime.now().isoformat())
    post_url = entry.get('url', '')

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()

    slug = slugify(title)

    # Use the full timestamp in the filename
    base_filename = f"{date.strftime('%Y-%m-%d-%H-%M-%S')}-{slug}"

    img_pattern = re.compile(r'<img[^>]+src="[^">]+"')
    has_images = bool(img_pattern.search(content))

    if has_images:
        post_dir = os.path.join(output_dir, base_filename)
        if os.path.exists(post_dir):
            print(f"Post already exists (with images): {post_dir}")
            return
        os.makedirs(post_dir, exist_ok=True)
        content = process_images(content, post_dir)
        file_path = os.path.join(post_dir, "index.md")
    else:
        file_path = os.path.join(output_dir, f"{base_filename}.md")
        if os.path.exists(file_path):
            print(f"Post already exists: {file_path}")
            return

    content = html_to_markdown(content)
    post = frontmatter.loads(content)
    post['title'] = title
    post['date'] = date
    post['draft'] = False
    post['url'] = post_url

    with open(file_path, 'w') as f:
        f.write(frontmatter.dumps(post))

    print(f"Created new post: {file_path}")

def main():
    json_feed_url = os.getenv('JSON_FEED_URL', 'https://example.com/feed.json')
    hugo_content_dir = os.getenv('HUGO_CONTENT_DIR', 'path/to/hugo/content/notes')

    os.makedirs(hugo_content_dir, exist_ok=True)

    feed_data = download_json_feed(json_feed_url)

    for entry in feed_data.get('items', []):
        create_hugo_content(entry, hugo_content_dir)

    print(f"Processed {len(feed_data.get('items', []))} entries.")

if __name__ == "__main__":
    main()
