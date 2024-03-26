import os
import re

# Set the directory where your Hugo posts are stored
directory = 'path/to/your/hugo/posts'

# URL replacement
old_url = 'http://nata2.info'
new_url = 'https://web.archive.org/web/20030814003134/http://www.nata2.info/'

def replace_url_in_file(filepath):
    """
    Replaces occurrences of the specified old URL with the new URL in the given file.
    """
    with open(filepath, 'r') as file:
        content = file.read()

    # Replace old URL with new URL
    updated_content = content.replace(old_url, new_url)

    # Write changes back to file if any replacements were made
    if updated_content != content:
        with open(filepath, 'w') as file:
            file.write(updated_content)

def update_urls_in_posts(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".md"):  # Assuming Hugo posts are Markdown files
            filepath = os.path.join(directory, filename)
            replace_url_in_file(filepath)

# Replace 'path/to/your/hugo/posts' with the actual path to your Hugo posts
update_urls_in_posts('content/archives')
