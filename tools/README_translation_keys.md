# Translation Key Collision Checker

This tool checks Hugo content files for translation key collisions, particularly focusing on when different posts share the same `translationKey` but have different dates.

## Purpose

In Hugo multilingual sites, `translationKey` is used to connect content across different languages. However, when different posts (especially ones with different dates) share the same `translationKey`, it can lead to unexpected linking behavior. This script identifies such collisions to help maintain proper translation relationships.

## Installation

The script is already in your tools directory. It requires PyYAML to run, which can be installed with:

```bash
cd tools
uv add --script check_translation_keys.py pyyaml
```

## Usage

Always run the script using `uv run` as specified in the project guidelines:

```bash
# Basic usage - check a directory
uv run tools/check_translation_keys.py content/

# Check multiple directories
uv run tools/check_translation_keys.py content/ content.ja/ content.ko/

# Get verbose output with more details
uv run tools/check_translation_keys.py --verbose content/

# Get suggested fixes for each collision
uv run tools/check_translation_keys.py --suggest content/

# Check specific files (rather than entire directories)
uv run tools/check_translation_keys.py --files content/music/file1.md content/music/file2.md
```

## Options

- `--verbose`, `-v`: Enable verbose output with more details about skipped files and general suggestions
- `--suggest`, `-s`: Provide specific suggestions for each colliding file
- `--fix`: Automatically fix collisions by adding date-based suffixes to translation keys
- `--dry-run`, `-d`: Only report issues without making changes (this is the default behavior)
- `--files`, `-f`: Treat all provided paths as individual files rather than directories

## Output

The script reports:
1. Files that share the same `translationKey` but have different dates
2. Suggestions for how to make the keys unique (typically by appending the date)
3. A summary of findings

## Example Output

### Check mode:
```
================================================================================
Found 1 translationKey collision(s) with differing dates:
--------------------------------------------------------------------------------
1. Key: 'Pink Moon'
   Date: 2022-02-22
      - content/music/20220222-pink-moon-e087c2.md
   Date: 2023-03-12
      - content/music/20230312-pink-moon-5f4775.md
--------------------------------------------------------------------------------

Summary:
  • Found translation key collisions that need to be resolved
  • Run with --suggest for specific suggestions for each file
  • Run with --fix to automatically apply suggested changes
```

### Suggest mode:
```
================================================================================
Found 1 translationKey collision(s) with differing dates:
--------------------------------------------------------------------------------
1. Key: 'Pink Moon'
   Date: 2022-02-22
      - content/music/20220222-pink-moon-e087c2.md
        Suggested key: 'Pink Moon-20220222'
   Date: 2023-03-12
      - content/music/20230312-pink-moon-5f4775.md
        Suggested key: 'Pink Moon-20230312'
--------------------------------------------------------------------------------

Summary:
  • Found translation key collisions that need to be resolved
  • Run with --suggest for specific suggestions for each file
  • Run with --fix to automatically apply suggested changes
```

### Fix mode:
```
================================================================================
Found 1 translationKey collision(s) with differing dates:
--------------------------------------------------------------------------------
1. Key: 'Pink Moon'
   Date: 2022-02-22
      - content/music/20220222-pink-moon-e087c2.md
        Suggested key: 'Pink Moon-20220222'
        ✅ Fixed: translationKey updated to 'Pink Moon-20220222'
   Date: 2023-03-12
      - content/music/20230312-pink-moon-5f4775.md
        Suggested key: 'Pink Moon-20230312'
        ✅ Fixed: translationKey updated to 'Pink Moon-20230312'
--------------------------------------------------------------------------------

Fixed 2 out of 2 files with collisions
```

## How to Fix Collisions

You have three options for fixing collisions:

### 1. Automatic fixing (recommended for bulk fixes):

```bash
uv run tools/check_translation_keys.py --fix content/
```

This will automatically add date-based suffixes to translation keys to make them unique.

### 2. Manual fixing after reviewing suggestions:

```bash
uv run tools/check_translation_keys.py --suggest content/
```

1. Determine if the posts should truly be linked as translations
   - If they're the same content in different languages → keep the same key
   - If they're different posts that happen to have the same title/key → make keys unique

2. For posts that should have unique keys, edit the frontmatter and modify the `translationKey` field:
   - Consider adding a date suffix as suggested: `Original Title` → `Original Title-20250216`
   - Or add another unique identifier that makes sense for your content

### 3. Selective fixing (for specific files):

```bash
uv run tools/check_translation_keys.py --files --fix specific-file1.md specific-file2.md
```

This allows you to fix only specific files that you've identified.

## Note

By default, the script only reports issues and doesn't modify files. Use the `--fix` option to apply changes automatically.