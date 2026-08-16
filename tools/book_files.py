# ABOUTME: Shared writer for book index.md files across the goodreads tools.
# ABOUTME: Serializes before opening so a failed dump never truncates or leaves a zero-byte file.

import frontmatter


def write_frontmatter_file(post, path):
    """Serialize post, then write it to path in text mode.

    python-frontmatter >= 1.2 writes str to file objects, so binary-mode
    handles raise TypeError after open() has already truncated the file.
    Serializing before opening means a failing dump can't leave an empty
    or half-written index.md behind.
    """
    text = frontmatter.dumps(post)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
