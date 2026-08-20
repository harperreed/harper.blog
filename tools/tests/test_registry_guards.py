# ABOUTME: Corrupt registries must abort the run (exit non-zero), never
# ABOUTME: silently reset to empty — an empty registry recreates all notes.
import sys

import pytest

import grab_micro_posts_fixed as gm


def test_missing_url_registry_returns_empty(tmp_path):
    assert gm.load_url_registry(str(tmp_path)) == {}


def test_missing_content_registry_returns_empty(tmp_path):
    assert gm.load_content_registry(str(tmp_path)) == {}


def test_corrupt_url_registry_raises(tmp_path):
    (tmp_path / gm.URL_REGISTRY_FILENAME).write_text("{truncated")
    with pytest.raises(gm.RegistryCorruptError):
        gm.load_url_registry(str(tmp_path))


def test_corrupt_content_registry_raises(tmp_path):
    (tmp_path / gm.CONTENT_REGISTRY_FILENAME).write_text("not json at all")
    with pytest.raises(gm.RegistryCorruptError):
        gm.load_content_registry(str(tmp_path))


def test_corrupt_registry_main_returns_1(tmp_path, monkeypatch):
    """main() must return 1 cleanly (no traceback) when a registry is corrupt."""
    monkeypatch.setattr(sys, "argv", ["grab_micro_posts_fixed.py"])
    monkeypatch.setenv("NOTES_JSON_FEED_URL", "https://example.com/feed.json")
    monkeypatch.setenv("NOTES_HUGO_CONTENT_DIR", str(tmp_path / "content"))
    monkeypatch.setenv("NOTES_HUGO_DATA_DIR", str(tmp_path / "data"))
    (tmp_path / "data").mkdir(parents=True)
    (tmp_path / "data" / gm.URL_REGISTRY_FILENAME).write_text("{bad json")

    result = gm.main()
    assert result == 1
