# ABOUTME: One-shot script to merge the split note deduplication registries.
# ABOUTME: Heals the split between data/notes/ (active) and content/data/notes/ (abandoned older copy).

import json
import logging
import sys
from pathlib import Path

import frontmatter

from grab_micro_posts_fixed import (
    CONTENT_REGISTRY_FILENAME,
    URL_REGISTRY_FILENAME,
    normalize_url,
    save_content_registry,
    save_url_registry,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Paths relative to project root (parent of the tools/ directory)
_REPO_ROOT = Path(__file__).parent.parent
ACTIVE_DATA_DIR = _REPO_ROOT / "data" / "notes"
OLD_DATA_DIR = _REPO_ROOT / "content" / "data" / "notes"
NOTES_CONTENT_DIR = _REPO_ROOT / "content" / "notes"


def merge_registries(old: dict, active: dict) -> dict:
    """Return a union of old and active, with active winning any key conflict."""
    return {**old, **active}


def sweep_notes_dir(notes_dir: Path, url_registry: dict) -> dict:
    """Scan notes_dir for index.md files whose original_url is absent from url_registry.

    Returns a dict of {normalized_url: date_str} for URLs that were missing.
    Does NOT mutate url_registry — caller decides whether to merge.
    """
    additions = {}
    for index_md in sorted(notes_dir.rglob("index.md")):
        try:
            with open(index_md, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
        except Exception as e:
            logging.warning(f"Could not parse {index_md}: {e}")
            continue

        raw_url = post.get("original_url", "")
        if not raw_url:
            continue

        norm = normalize_url(raw_url)
        if not norm:
            continue

        if norm in url_registry or norm in additions:
            continue

        # Use the note's own date as the registry timestamp
        date_val = post.get("date")
        if date_val is None:
            date_str = "unknown"
        else:
            date_str = str(date_val)

        additions[norm] = date_str

    return additions


def _load_json(path: Path) -> dict:
    if not path.exists():
        logging.warning(f"Registry not found, treating as empty: {path}")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logging.error(f"Could not load {path}: {e}")
        return {}


def main() -> int:
    # NOTE: OLD_DATA_DIR (content/data/notes/) was deleted after the 2026-08-20
    # merge ran; re-runs find nothing there and are no-ops by design.
    # --- Load both URL registries ---
    old_url = _load_json(OLD_DATA_DIR / URL_REGISTRY_FILENAME)
    active_url = _load_json(ACTIVE_DATA_DIR / URL_REGISTRY_FILENAME)

    old_url_count = len(old_url)
    active_url_count = len(active_url)

    # --- Load both content-hash registries ---
    old_content = _load_json(OLD_DATA_DIR / CONTENT_REGISTRY_FILENAME)
    active_content = _load_json(ACTIVE_DATA_DIR / CONTENT_REGISTRY_FILENAME)

    old_content_count = len(old_content)
    active_content_count = len(active_content)

    # --- Merge: active wins conflicts ---
    merged_url = merge_registries(old_url, active_url)
    merged_content = merge_registries(old_content, active_content)

    merged_url_count = len(merged_url)
    merged_content_count = len(merged_content)

    # --- Disk sweep: pick up any note whose URL slipped both registries ---
    sweep_additions = sweep_notes_dir(NOTES_CONTENT_DIR, merged_url)
    merged_url.update(sweep_additions)
    swept_count = len(sweep_additions)

    final_url_count = len(merged_url)

    # --- Write merged registries atomically to the ACTIVE data dir ---
    save_url_registry(merged_url, str(ACTIVE_DATA_DIR))
    save_content_registry(merged_content, str(ACTIVE_DATA_DIR))

    # --- Report ---
    logging.info(
        f"URL registry:     old={old_url_count}  active={active_url_count}  "
        f"merged={merged_url_count}  swept={swept_count}  final={final_url_count}"
    )
    logging.info(
        f"Content registry: old={old_content_count}  active={active_content_count}  "
        f"merged={merged_content_count}"
    )

    print(f"URL registry:     old={old_url_count}, active={active_url_count}, merged={merged_url_count}, swept={swept_count}, final={final_url_count}")
    print(f"Content registry: old={old_content_count}, active={active_content_count}, merged={merged_content_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
