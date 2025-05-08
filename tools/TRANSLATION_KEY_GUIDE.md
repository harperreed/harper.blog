# Translation Key Guide

The `add_translation_keys.py` script helps manage translationKeys in your Hugo content files for multilingual support.

## What are Translation Keys?

Translation keys allow Hugo to link content across different languages. When a page in one language has the same `translationKey` as a page in another language, Hugo recognizes them as translations of each other.

## Usage

Basic usage:

```bash
uv run tools/add_translation_keys.py /path/to/content/directory
```

This will recursively process all `.md` files in the directory and add a `translationKey` to each one if missing.

## Options

- Process recursively (default): The script will find all markdown files in subdirectories by default
- Disable recursive mode: `--no-recursive`
- Use UUIDs for keys: `--uuid` (generates random UUIDs instead of using titles)
- Don't use titles: `--no-title` (use date-slug or UUID instead of title)
- Dry-run mode: `--dry-run` (show what would be done without making changes)

## Examples

Process all files in the content/posts directory:
```bash
uv run tools/add_translation_keys.py ../content/posts
```

Preview changes without modifying files:
```bash
uv run tools/add_translation_keys.py --dry-run ../content/posts
```

Generate UUID-based keys instead of using titles:
```bash
uv run tools/add_translation_keys.py --uuid ../content/posts
```

## Translation Key Strategy

By default, the script uses the following strategy for generating translation keys:

1. If a translationKey already exists, it keeps it unchanged
2. If the title is available, it uses the title as the key
3. If no title is available, it uses a date-slug combination
4. As a last resort, it generates a UUID

## Report Summary

The script provides a summary at the end of the run showing:
- Total files processed
- Number of keys added (green)
- Number of keys unchanged (yellow)
- Number of keys updated (green)

## Help

For all available options:

```bash
uv run tools/add_translation_keys.py --help
```