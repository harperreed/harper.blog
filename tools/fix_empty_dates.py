# ABOUTME: One-time script to fix empty dates in book frontmatter.
# ABOUTME: Infers the date from the directory name when frontmatter date is empty.

import glob
import os
import re

import frontmatter

from book_files import write_frontmatter_file

content_dir = os.path.join(os.path.dirname(__file__), "..", "content", "books")

fixed = 0
for f in sorted(glob.glob(os.path.join(content_dir, "*", "index.md"))):
    post = frontmatter.load(f)
    if post.get("date") == "" or post.get("date") is None:
        dirname = os.path.basename(os.path.dirname(f))
        m = re.match(r"^(\d{4}-\d{2}-\d{2})-", dirname)
        if m:
            date_str = m.group(1) + "T00:00:00-08:00"
            post["date"] = date_str
            write_frontmatter_file(post, f)
            fixed += 1

print(f"Fixed {fixed} entries")
