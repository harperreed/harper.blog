# ABOUTME: Corrupt registries must abort the run (exit non-zero), never
# ABOUTME: silently reset to empty — an empty registry recreates all notes.
import pytest

import grab_micro_posts_fixed as gm


def test_missing_registry_returns_empty(tmp_path):
    assert gm.load_url_registry(str(tmp_path)) == {}
    assert gm.load_content_registry(str(tmp_path)) == {}


def test_corrupt_url_registry_raises(tmp_path):
    (tmp_path / gm.URL_REGISTRY_FILENAME).write_text("{truncated")
    with pytest.raises(gm.RegistryCorruptError):
        gm.load_url_registry(str(tmp_path))


def test_corrupt_content_registry_raises(tmp_path):
    (tmp_path / gm.CONTENT_REGISTRY_FILENAME).write_text("not json at all")
    with pytest.raises(gm.RegistryCorruptError):
        gm.load_content_registry(str(tmp_path))
