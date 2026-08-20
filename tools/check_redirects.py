# ABOUTME: Validates Netlify _redirects rules against a built Hugo site: checks that
# ABOUTME: redirect targets exist, and that sources don't shadow real content pages.

"""Usage: uv run check_redirects.py <built-site-dir> [redirects-file]

Parses static/_redirects (or a supplied path) and verifies each rule:
  - Target must exist in the built site (as page dir/index.html or exact file)
    OR be an external URL (http-prefixed).
  - Splat rules: the target pattern's base section must exist.
  - Non-splat source must NOT also exist as a built page (shadowing = bug).

Exits 1 with one line per violation, 0 when all rules are clean.
"""

import sys
from pathlib import Path

# Repo root is two levels up from this file (tools/check_redirects.py).
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_REDIRECTS = _REPO_ROOT / "static" / "_redirects"


def _page_exists(site_dir: Path, url_path: str) -> bool:
    """Return True if url_path resolves to a page or file in site_dir.

    Accepts:
      - <site_dir><url_path>/index.html  (directory pages)
      - <site_dir><url_path>             (exact files like index.xml)
    """
    stripped = url_path.lstrip("/")
    candidate_dir = site_dir / stripped / "index.html"
    candidate_file = site_dir / stripped
    return candidate_dir.exists() or (candidate_file.exists() and candidate_file.is_file())


def _splat_base(target_pattern: str) -> str:
    """Return the directory that must exist as a built page for a splat target.

    '/es/media/books/:splat'    →  '/es/media/books/'
    '/media/books/page/:splat'  →  '/media/books/'  (Hugo emits no bare
        /page/ index — the section root is what must survive)
    '/:splat'                   →  '/'
    """
    without_splat = target_pattern.replace(":splat", "").rstrip("/")
    if without_splat.endswith("/page"):
        without_splat = without_splat[: -len("/page")]
    return without_splat + "/"


def check_rules(site_dir: Path, redirects_path: Path) -> list[str]:
    """Parse redirects_path and check each rule; return violation strings."""
    violations: list[str] = []

    text = redirects_path.read_text(encoding="utf-8")
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) < 2:
            violations.append(f"{redirects_path}:{lineno}: malformed rule: {line!r}")
            continue

        source, target = parts[0], parts[1]
        is_splat = ":splat" in target or "*" in source

        # External targets are always valid — Netlify handles them.
        if target.startswith("http"):
            continue

        if is_splat:
            # For splat rules, verify that the target's base section exists.
            base = _splat_base(target)
            if not _page_exists(site_dir, base):
                violations.append(
                    f"{redirects_path}:{lineno}: splat target base missing: "
                    f"{base!r} (rule: {source} → {target})"
                )
        else:
            # For exact rules, target must exist as a page or file.
            if not _page_exists(site_dir, target):
                violations.append(
                    f"{redirects_path}:{lineno}: target not found in built site: "
                    f"{target!r} (rule: {source} → {target})"
                )

            # Source must NOT shadow a real built page.
            if _page_exists(site_dir, source):
                violations.append(
                    f"{redirects_path}:{lineno}: source shadows real content: "
                    f"{source!r} exists as a built page (rule: {source} → {target})"
                )

    return violations


def main(argv: list[str]) -> int:
    """Check _redirects rules against built site; return 0 = clean, 1 = problems."""
    if not argv:
        print("usage: check_redirects.py <built-site-dir> [redirects-file]", file=sys.stderr)
        return 1

    site_dir = Path(argv[0])
    redirects_path = Path(argv[1]) if len(argv) > 1 else _DEFAULT_REDIRECTS

    if not redirects_path.exists():
        print(f"ERROR: _redirects not found: {redirects_path}", file=sys.stderr)
        return 1

    violations = check_rules(site_dir, redirects_path)

    for v in violations:
        print(v)

    if violations:
        print(f"\n{len(violations)} redirect violation(s).", file=sys.stderr)
        return 1

    print(f"redirects clean: {redirects_path} — all rules valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
