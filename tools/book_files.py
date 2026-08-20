# ABOUTME: Shared writer for book index.md files across the goodreads tools.
# ABOUTME: Serializes before opening so a failed dump never truncates or leaves a zero-byte file.

import frontmatter
import os
import tempfile


def write_frontmatter_file(post, path):
    """Serialize post, then write it atomically via temp file + os.replace.

    Serializing before opening means a failing dump can't leave an empty or
    half-written file behind. The temp-file + os.replace pattern means a
    concurrent reader always sees either the old file or the new one — never
    a partial write.
    """
    text = frontmatter.dumps(post)
    dir_ = os.path.dirname(os.path.abspath(path))
    fd, tmp_path = tempfile.mkstemp(dir=dir_)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp_path, path)
    except Exception:
        os.unlink(tmp_path)
        raise
