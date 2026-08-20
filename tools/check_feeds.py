# ABOUTME: Validates RSS feeds in a built Hugo site: well-formed XML, item presence,
# ABOUTME: date parseability, and that every expected feed path actually exists.

"""Usage: uv run check_feeds.py <built-site-dir>

Checks each expected RSS feed for: well-formed XML, at least one <item>, every
item has <link> and a parseable <pubDate>, and channel <lastBuildDate> is
parseable when present.

Exits 1 with one line per finding, 0 when all feeds are clean.
"""

import sys
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

# The six feeds verified against a production build — missing = incident.
FEED_PATHS = [
    "index.xml",
    "photos/index.xml",
    "media/books/index.xml",
    "media/links/index.xml",
    "media/music/index.xml",
    "notes/index.xml",
]


def _parse_date(value: str) -> bool:
    """Return True if value is a parseable RFC 2822 date, False otherwise."""
    try:
        parsedate_to_datetime(value)
        return True
    except Exception:
        return False


def check_feed(path: Path) -> list[str]:
    """Check one RSS feed file; return problem strings (empty list = healthy)."""
    problems: list[str] = []

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"{path}: XML parse error: {exc}"]

    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        return [f"{path}: no <channel> element"]

    # lastBuildDate is optional but must parse when present.
    last_build = channel.findtext("lastBuildDate")
    if last_build is not None and not _parse_date(last_build):
        problems.append(f"{path}: unparseable <lastBuildDate>: {last_build!r}")

    items = channel.findall("item")
    if not items:
        problems.append(f"{path}: no <item> elements")
        return problems

    for i, item in enumerate(items):
        link = item.findtext("link")
        if not link:
            problems.append(f"{path}: item[{i}] missing <link>")

        pub_date = item.findtext("pubDate")
        if pub_date is None:
            problems.append(f"{path}: item[{i}] missing <pubDate>")
        elif not _parse_date(pub_date):
            problems.append(f"{path}: item[{i}] unparseable <pubDate>: {pub_date!r}")

    return problems


def main(argv: list[str]) -> int:
    """Check all expected feeds under the built-site directory; return 0 = clean, 1 = problems."""
    if not argv:
        print("usage: check_feeds.py <built-site-dir>", file=sys.stderr)
        return 1

    site_dir = Path(argv[0])
    all_problems: list[str] = []

    for rel in FEED_PATHS:
        feed_path = site_dir / rel
        if not feed_path.exists():
            all_problems.append(f"MISSING: {feed_path}")
        else:
            all_problems.extend(check_feed(feed_path))

    for problem in all_problems:
        print(problem)

    if all_problems:
        print(f"\n{len(all_problems)} feed problem(s).", file=sys.stderr)
        return 1

    print("feeds clean: all 6 feeds well-formed with items and valid dates.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
