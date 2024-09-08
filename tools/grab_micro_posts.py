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
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    img_matches = img_pattern.findall(content)

    for i, (alt_text, img_url) in enumerate(img_matches):
        parsed_url = urlparse(img_url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        if not file_extension:
            file_extension = '.jpg'  # Default to .jpg if no extension is found
        local_img_path = f'image_{i + 1}{file_extension}'
        full_img_path = os.path.join(post_dir, local_img_path)
        if download_image(img_url, full_img_path):
            # Remove the image from the content
            content = content.replace(f'![{alt_text}]({img_url})', '')

    # Remove any empty lines left after removing images
    content = re.sub(r'\n\s*\n', '\n\n', content)
    return content.strip()

def create_hugo_content(entry, output_dir, note_id):
    sub_title = entry.get('title', "Untitled")
    title = f"Note #{note_id}"
    content = entry.get('content_html') or entry.get('content_text', '')
    date_str = entry.get('date_published', datetime.now().isoformat())
    post_url = entry.get('url', '')

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()

    slug = slugify(title)

    # Use the full timestamp and note_id in the filename
    base_filename = f"{date.strftime('%Y-%m-%d-%H-%M-%S')}-{slugify(sub_title)}"

    post_dir = os.path.join(output_dir, base_filename)
    if os.path.exists(post_dir):
        print(f"Post already exists: {post_dir}")
        return
    os.makedirs(post_dir, exist_ok=True)

    content = html_to_markdown(content)
    content = process_images(content, post_dir)

    file_path = os.path.join(post_dir, "index.md")

    # Create a frontmatter.Post object
    post = frontmatter.loads(content)
    post['title'] = title
    post['sub_title'] = sub_title
    post['date'] = date
    post['draft'] = False
    post['original_url'] = post_url
    post['note_id'] = note_id

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    print(f"Created new post: {file_path}")

def main():
    json_feed_url = os.getenv('JSON_FEED_URL')
    hugo_content_dir = os.getenv('HUGO_CONTENT_DIR')

    if not json_feed_url or not hugo_content_dir:
        raise ValueError("JSON_FEED_URL and HUGO_CONTENT_DIR must be set in the .env file")

    os.makedirs(hugo_content_dir, exist_ok=True)

    feed_data = download_json_feed(json_feed_url)

    # Sort entries by date_published
    sorted_entries = sorted(
        feed_data.get('items', []),
        key=lambda x: datetime.fromisoformat(x.get('date_published', datetime.now().isoformat())),
        reverse=False  # Oldest first
    )

    # Get the current highest note_id
    existing_files = os.listdir(hugo_content_dir)
    highest_id = 0
    for filename in existing_files:
        match = re.search(r'-(\d{4})-', filename)
        if match:
            file_id = int(match.group(1))
            highest_id = max(highest_id, file_id)

    # Process entries
    for i, entry in enumerate(sorted_entries, start=highest_id+1):
        create_hugo_content(entry, hugo_content_dir, i)

    print(f"Processed {len(sorted_entries)} entries.")

if __name__ == "__main__":
    main()
