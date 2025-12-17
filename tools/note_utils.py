# ABOUTME: Shared utilities for note/micro-post processing across tools.
# ABOUTME: Contains content normalization, hashing, and note ID extraction.

import re
import hashlib


def normalize_content(content):
    """
    Normalize content for comparison by stripping HTML, removing URLs, and
    normalizing whitespace.

    Used for duplicate detection across grab_micro_posts_fixed.py and
    deduplicate_notes.py. Changes here affect both scripts.

    Args:
        content (str): Content to normalize

    Returns:
        str: Normalized content
    """
    # Strip all HTML tags first
    normalized = re.sub(r'<[^>]+>', ' ', content)
    # Remove image markdown syntax ![alt](url)
    normalized = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', normalized)
    # Remove URLs (both absolute and common relative patterns like uploads/)
    normalized = re.sub(r'https?://\S+', '', normalized)
    normalized = re.sub(r'uploads/\S+', '', normalized)
    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized.strip())
    return normalized


def generate_content_hash(content, truncate=True):
    """
    Generate a SHA-1 hash of normalized content for duplicate detection.

    Args:
        content (str): Content to hash (will be normalized first)
        truncate (bool): If True, return 12-char hash; otherwise full 40-char

    Returns:
        str: SHA-1 hash of the normalized content
    """
    normalized = normalize_content(content)
    sha1 = hashlib.sha1()
    sha1.update(normalized.encode('utf-8'))
    if truncate:
        return sha1.hexdigest()[:12]
    return sha1.hexdigest()


def get_note_id_from_title(title):
    """
    Extract note ID from a title like "Note #123".

    Args:
        title (str): Title string

    Returns:
        int or None: Extracted note ID or None if not found
    """
    if not title:
        return None

    match = re.search(r'Note\s*#(\d+)', title)
    if match:
        return int(match.group(1))
    return None
