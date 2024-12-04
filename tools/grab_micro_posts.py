import requests
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

def get_highest_note_id(hugo_content_dir):
    highest_note_id = 0
    for root, dirs, files in os.walk(hugo_content_dir):
        for file in files:
            if file == "index.md":
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        if 'note_id' in post.metadata:
                            current_id = post.metadata['note_id']
                            print(f"Found note_id: {current_id} in file: {file_path}")
                            if isinstance(current_id, int):
                                highest_note_id = max(highest_note_id, current_id)
                            else:
                                print(f"Warning: non-integer note_id found: {current_id} in file: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {str(e)}")

    print(f"Highest Note ID found: {highest_note_id}")
    return highest_note_id

def create_hugo_content(entry, output_dir, note_id):
    sub_title = entry.get('title', "Untitled")
    title = f"Note #{note_id}"
    content = entry.get('content_text') or entry.get('content_html', '')
    date_str = entry.get('date_published', datetime.now().isoformat())
    post_url = entry.get('url', '')

    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        date = datetime.now()

    base_filename = f"{date.strftime('%Y-%m-%d-%H-%M-%S')}-{slugify(sub_title)}"
    post_dir = os.path.join(output_dir, base_filename)
    
    if os.path.exists(post_dir):
        print(f"Post already exists: {post_dir}")
        return False

    os.makedirs(post_dir, exist_ok=True)

    content = html_to_markdown(content)
    content = process_images(content, post_dir)

    file_path = os.path.join(post_dir, "index.md")

    post = frontmatter.loads(content)
    post['title'] = title
    post['sub_title'] = sub_title
    post['description'] = create_description(content)
    post['date'] = date
    post['draft'] = False
    post['original_url'] = post_url
    post['note_id'] = note_id

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))

    print(f"Created new post: {file_path} with Note ID: {note_id}")
    return True

def create_description(content, max_length=160):
    # Strip markdown syntax
    clean_content = re.sub(r'[#*`_~\[\]\(\)!]', '', content)
    # Normalize whitespace
    clean_content = ' '.join(clean_content.split())
    # Truncate and add ellipsis if needed
    if len(clean_content) > max_length:
        return clean_content[:max_length-3] + '...'
    return clean_content

def main():
    json_feed_url = os.getenv('NOTES_JSON_FEED_URL')
    hugo_content_dir = os.getenv('NOTES_HUGO_CONTENT_DIR')

    if not json_feed_url or not hugo_content_dir:
        raise ValueError("NOTES_JSON_FEED_URL and NOTES_HUGO_CONTENT_DIR must be set in the .env file")

    os.makedirs(hugo_content_dir, exist_ok=True)

    feed_data = download_json_feed(json_feed_url)

    sorted_entries = sorted(
        feed_data.get('items', []),
        key=lambda x: datetime.fromisoformat(x.get('date_published', datetime.now().isoformat())),
        reverse=False
    )

    highest_note_id = get_highest_note_id(hugo_content_dir)
    print(f"Starting with highest Note ID: {highest_note_id}")

    new_posts_created = 0
    for entry in sorted_entries:
        new_note_id = highest_note_id + new_posts_created + 1
        print(f"Attempting to create post with Note ID: {new_note_id}")
        if create_hugo_content(entry, hugo_content_dir, new_note_id):
            new_posts_created += 1

    print(f"Processed {len(sorted_entries)} entries.")
    print(f"Created {new_posts_created} new posts.")
    print(f"New highest Note ID: {highest_note_id + new_posts_created}")

if __name__ == "__main__":
    main()
