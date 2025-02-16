import os
import re
import requests
import logging
from pathlib import Path
from urllib.parse import urlparse

# Centralized logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
def download_image(url: str, output_path: Path) -> bool:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        logging.exception("Failed to download image from %s", url)
        return False
def process_images(content: str, post_dir: Path) -> str:
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    img_matches = img_pattern.findall(content)

    for i, (alt_text, img_url) in enumerate(img_matches):
        if not img_url.startswith(('http://', 'https://')):
            logging.warning("Skipping invalid URL: %s", img_url)
            continue
        parsed_url = urlparse(img_url)
        file_extension = os.path.splitext(parsed_url.path)[1]
        if not file_extension:
            file_extension = '.jpg'  # Default to .jpg if no extension is found
        local_img_path = f'image_{i + 1}{file_extension}'
        full_img_path = os.path.join(post_dir, local_img_path)
        if download_image(img_url, full_img_path):
            content = content.replace(f'![{alt_text}]({img_url})', f'![{alt_text}]({local_img_path})')

    return content
def convert_posts_to_page_bundles(content_dir: Path) -> None:
    content_dir = Path(content_dir)
    for md_file in content_dir.glob("*.md"):
        try:
            post_name = md_file.stem
            post_dir = content_dir / post_name
            post_dir.mkdir(exist_ok=True)

            with open(md_file, 'r') as f:
                content = f.read()

            content = process_images(content, post_dir)

            index_md_path = post_dir / "index.md"
            with open(index_md_path, 'w') as f:
                f.write(content)

            md_file.unlink()
            logging.info("Converted %s to page bundle %s", md_file, post_dir)
        except Exception:
            logging.exception("Failed to convert %s", md_file)
if __name__ == "__main__":
    content_dir = "../content/post"
    convert_posts_to_page_bundles(content_dir)
