# ABOUTME: One-time script to remove is_reread frontmatter from all book entries.
# ABOUTME: The is_reread flag was based on crowd-sourced data; related_reads is the accurate signal.

import glob
import os

import frontmatter


def strip_is_reread(content_dir: str) -> int:
    """Remove is_reread from all book entry frontmatter. Returns count of files updated."""
    count = 0
    for index_file in sorted(glob.glob(os.path.join(content_dir, "*", "index.md"))):
        post = frontmatter.load(index_file)
        if "is_reread" in post.metadata:
            del post.metadata["is_reread"]
            with open(index_file, "wb") as f:
                frontmatter.dump(post, f)
            count += 1
    return count


if __name__ == "__main__":
    content_dir = os.path.join(os.path.dirname(__file__), "..", "content", "books")
    content_dir = os.path.realpath(content_dir)
    count = strip_is_reread(content_dir)
    print(f"Stripped is_reread from {count} files")
