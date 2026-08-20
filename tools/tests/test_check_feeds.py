# ABOUTME: Tests for the check_feeds.py feed-validity checker.
# ABOUTME: Exercises check_feed() for healthy/broken/empty XML and main() missing-feed guard.

import textwrap


HEALTHY_FEED = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Test Feed</title>
        <link>https://example.com</link>
        <lastBuildDate>Mon, 01 Jan 2024 00:00:00 +0000</lastBuildDate>
        <item>
          <title>Post One</title>
          <link>https://example.com/1</link>
          <pubDate>Mon, 01 Jan 2024 00:00:00 +0000</pubDate>
        </item>
        <item>
          <title>Post Two</title>
          <link>https://example.com/2</link>
          <pubDate>Tue, 02 Jan 2024 00:00:00 +0000</pubDate>
        </item>
      </channel>
    </rss>
""")

BROKEN_FEED = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Broken Feed</title>
        <item>
          <link>https://example.com/1</link>
    """)  # unclosed tag — not well-formed XML

EMPTY_FEED = textwrap.dedent("""\
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>Empty Feed</title>
        <link>https://example.com</link>
      </channel>
    </rss>
""")  # zero <item> elements


def test_check_feed_healthy(tmp_path):
    """A well-formed feed with 2 items and valid dates returns no problems."""
    f = tmp_path / "index.xml"
    f.write_text(HEALTHY_FEED, encoding="utf-8")

    import check_feeds
    assert check_feeds.check_feed(f) == []


def test_check_feed_broken_xml(tmp_path):
    """An unclosed tag must produce a parse-error problem string."""
    f = tmp_path / "index.xml"
    f.write_text(BROKEN_FEED, encoding="utf-8")

    import check_feeds
    problems = check_feeds.check_feed(f)
    assert len(problems) >= 1
    assert "parse" in problems[0].lower() or "xml" in problems[0].lower()


def test_check_feed_empty_items(tmp_path):
    """A feed with zero <item> elements must report an item-count problem."""
    f = tmp_path / "index.xml"
    f.write_text(EMPTY_FEED, encoding="utf-8")

    import check_feeds
    problems = check_feeds.check_feed(f)
    assert len(problems) >= 1
    assert any("item" in p.lower() for p in problems)


def test_main_fails_when_feed_missing(tmp_path):
    """main() must return 1 when any expected feed file is absent."""
    import check_feeds
    # tmp_path has no feed files at all
    result = check_feeds.main([str(tmp_path)])
    assert result == 1
