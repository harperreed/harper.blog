# ABOUTME: Audits Hugo layouts/ for inline style= attributes and <style> blocks that
# ABOUTME: production CSP (style-src 'self') silently kills — these are dead on Netlify.

"""Usage: uv run check_inline_styles.py

Scans layouts/**/*.html for:
  - style="..." attributes
  - <style> blocks

Skips content inside Go template comments ({{/* ... */}}).

Exits 1 with file:line hits, 0 when all templates are clean.
"""

import re
import sys
from pathlib import Path

# Repo root is two levels up from this file (tools/check_inline_styles.py).
_REPO_ROOT = Path(__file__).resolve().parent.parent
_LAYOUTS_ROOT = _REPO_ROOT / "layouts"

# Match Go template block comments: {{/* ... */}} — may span multiple lines.
_GO_COMMENT_RE = re.compile(r"\{\{/\*.*?\*/\}\}", re.DOTALL)

# Patterns that signal a CSP-blocked inline style.
_STYLE_ATTR_RE = re.compile(r'\bstyle\s*=\s*["\']', re.IGNORECASE)
_STYLE_TAG_RE = re.compile(r"<style[\s>]", re.IGNORECASE)


def scan_layouts(layouts_root: Path) -> list[str]:
    """Scan layouts_root/**/*.html for inline styles; return 'file:line: snippet' strings."""
    hits: list[str] = []

    for html_file in sorted(layouts_root.rglob("*.html")):
        text = html_file.read_text(encoding="utf-8")

        # Strip Go template comments so their content doesn't trigger false positives.
        cleaned = _GO_COMMENT_RE.sub("", text)

        for lineno, line in enumerate(cleaned.splitlines(), start=1):
            if _STYLE_ATTR_RE.search(line) or _STYLE_TAG_RE.search(line):
                snippet = line.strip()[:100]
                hits.append(f"{html_file}:{lineno}: {snippet}")

    return hits


def main() -> int:
    """Scan real layouts/ for inline styles; return 0 = clean, 1 = hits found."""
    hits = scan_layouts(_LAYOUTS_ROOT)

    for hit in hits:
        print(hit)

    if hits:
        print(f"\n{len(hits)} inline-style hit(s) — blocked by production CSP.", file=sys.stderr)
        return 1

    print("inline styles clean: no style= attributes or <style> blocks in layouts/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
