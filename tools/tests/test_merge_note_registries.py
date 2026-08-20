# ABOUTME: Tests for the one-off registry merge script that heals the
# ABOUTME: split between data/notes and the abandoned content/data/notes registries.
import json
from pathlib import Path

from merge_note_registries import merge_registries, sweep_notes_dir


def test_union_prefers_active_on_conflict(tmp_path):
    old = {"https://a.example/1": "2024-01-01T00:00:00", "https://a.example/2": "2024-01-02T00:00:00"}
    active = {"https://a.example/2": "2025-06-01T00:00:00", "https://a.example/3": "2025-06-02T00:00:00"}
    merged = merge_registries(old, active)
    assert merged["https://a.example/1"] == "2024-01-01T00:00:00"
    assert merged["https://a.example/2"] == "2025-06-01T00:00:00"  # active wins
    assert merged["https://a.example/3"] == "2025-06-02T00:00:00"
    assert len(merged) == 3


def test_merge_is_idempotent(tmp_path):
    old = {"https://a.example/1": "2024-01-01T00:00:00"}
    active = {"https://a.example/2": "2025-01-01T00:00:00"}
    once = merge_registries(old, active)
    twice = merge_registries(once, active)
    assert once == twice == {**old, **active}


def test_sweep_adds_missing_url(tmp_path):
    """sweep_notes_dir adds a note's original_url when it is absent from the registry."""
    note_dir = tmp_path / "notes" / "2024-03-01_abc123_some-note"
    note_dir.mkdir(parents=True)
    index = note_dir / "index.md"
    index.write_text(
        "---\n"
        "date: 2024-03-01T00:00:00\n"
        "original_url: https://harper.micro.blog/2024/03/01/some-note.html\n"
        "title: 'Note #700'\n"
        "draft: false\n"
        "---\n\nSome note content.\n"
    )
    url_registry = {}
    additions = sweep_notes_dir(tmp_path / "notes", url_registry)
    assert "https://harper.micro.blog/2024/03/01/some-note.html" in additions
    assert len(additions) == 1


def test_sweep_skips_already_registered(tmp_path):
    """sweep_notes_dir skips notes whose URL is already in the registry."""
    note_dir = tmp_path / "notes" / "2024-03-01_abc123_some-note"
    note_dir.mkdir(parents=True)
    index = note_dir / "index.md"
    index.write_text(
        "---\n"
        "date: 2024-03-01T00:00:00\n"
        "original_url: https://harper.micro.blog/2024/03/01/some-note.html\n"
        "title: 'Note #700'\n"
        "draft: false\n"
        "---\n\nSome note content.\n"
    )
    # URL already registered (normalized form — no trailing slash, lowercase)
    url_registry = {"https://harper.micro.blog/2024/03/01/some-note.html": "2024-03-01T00:00:00"}
    additions = sweep_notes_dir(tmp_path / "notes", url_registry)
    assert len(additions) == 0
