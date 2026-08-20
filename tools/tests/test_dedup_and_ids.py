# ABOUTME: Tests for duplicate detection and note-ID assignment correctness.
# ABOUTME: Prefix heuristic must be gone; ID scan must happen once, not per note.
import inspect

import grab_micro_posts_fixed as gm


def test_shared_prefix_alone_is_not_duplicate(tmp_path):
    # Existing note has a short body (>50 chars) that shares its first 50 chars
    # with the new content; the overall similarity is well under 80%.
    # The prefix branch would have returned True (false positive); it must be gone.
    shared_open = "This is a shared opening that happens to be exactl"
    assert len(shared_open) == 50
    a = tmp_path / "note-a"
    a.mkdir()
    (a / "index.md").write_text("---\ntitle: a\n---\n" + shared_open + "y fine.")
    new_content = shared_open + " ZZZZ " * 100
    is_dup, _ = gm.is_duplicate_content(new_content, str(tmp_path))
    assert is_dup is False


def test_create_hugo_content_does_not_rescan_per_note():
    src = inspect.getsource(gm.create_hugo_content)
    assert "get_highest_note_id(" not in src
