# ABOUTME: Feed date handling must never mix naive and aware datetimes —
# ABOUTME: one malformed date_published used to TypeError the whole run.
from datetime import timezone

import grab_micro_posts_fixed as gm


def test_parse_feed_date_aware_passthrough():
    d = gm.parse_feed_date("2025-06-01T12:00:00+02:00")
    assert d.tzinfo is not None and d.year == 2025


def test_parse_feed_date_naive_becomes_utc():
    assert gm.parse_feed_date("2025-06-01T12:00:00").tzinfo == timezone.utc


def test_parse_feed_date_garbage_and_none_are_aware():
    assert gm.parse_feed_date("not a date").tzinfo is not None
    assert gm.parse_feed_date(None).tzinfo is not None


def test_mixed_entries_sort_without_typeerror():
    entries = [
        {"date_published": "2025-06-01T12:00:00+00:00"},
        {"date_published": "2025-06-01T11:00:00"},   # naive
        {"date_published": "garbage"},
    ]
    ordered = sorted(entries, key=lambda x: gm.parse_feed_date(x.get("date_published")))
    assert len(ordered) == 3
