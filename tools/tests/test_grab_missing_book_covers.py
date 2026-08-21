# ABOUTME: Tests for grab_missing_book_covers — backfill tool for missing local book cover images.
# ABOUTME: Covers bundle detection, image validation, filename derivation, and dry-run flag logic.

import frontmatter as fm

import grab_missing_book_covers as gmc


# ---------------------------------------------------------------------------
# find_missing_cover_bundles
# ---------------------------------------------------------------------------


def test_find_missing_cover_bundles_detects_dir_without_image(tmp_path):
    """A bundle with index.md but no image file is reported as missing."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(content="body", title="Project Hail Mary", asin="B0DWVVNLC9", book_author="Andy Weir")
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert len(result) == 1
    assert result[0]["slug"] == "2021-05-13-project-hail-mary"


def test_find_missing_cover_bundles_skips_dir_with_jpg(tmp_path):
    """A bundle that already has a .jpg file is skipped."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(content="body", title="Project Hail Mary", asin="B0DWVVNLC9", book_author="Andy Weir")
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")
    (d / "B0DWVVNLC9.jpg").write_bytes(b"\xff\xd8\xff" + b"\x00" * 3000)

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert result == []


def test_find_missing_cover_bundles_skips_dir_with_png(tmp_path):
    """A bundle that has a .png file is also skipped."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(content="body", title="Project Hail Mary", asin="B0DWVVNLC9", book_author="Andy Weir")
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")
    (d / "cover.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 3000)

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert result == []


def test_find_missing_cover_bundles_returns_metadata_fields(tmp_path):
    """Each returned bundle dict contains title, book_author, asin, and dir."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(
        content="body",
        title="Project Hail Mary",
        asin="B0DWVVNLC9",
        book_author="Andy Weir",
    )
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    b = result[0]
    assert b["title"] == "Project Hail Mary"
    assert b["book_author"] == "Andy Weir"
    assert b["asin"] == "B0DWVVNLC9"
    assert b["dir"] == str(d)


def test_find_missing_cover_bundles_ignores_dirs_without_index(tmp_path):
    """Directories that have no index.md are ignored entirely."""
    d = tmp_path / "not-a-bundle"
    d.mkdir()
    # No index.md, no image

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert result == []


def test_find_missing_cover_bundles_handles_multiple(tmp_path):
    """Multiple missing bundles are all returned."""
    for slug, title in [
        ("2006-11-05-fahrenheit-451", "Fahrenheit 451"),
        ("2021-05-13-project-hail-mary", "Project Hail Mary"),
    ]:
        d = tmp_path / slug
        d.mkdir()
        post = fm.Post(content="body", title=title, asin="ASIN123", book_author="Author")
        (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert len(result) == 2


# ---------------------------------------------------------------------------
# cover_target_path
# ---------------------------------------------------------------------------


def test_cover_target_path_uses_asin(tmp_path):
    """Target path is <bundle_dir>/<ASIN>.jpg."""
    bundle = {
        "dir": str(tmp_path / "2021-05-13-project-hail-mary"),
        "asin": "B0DWVVNLC9",
    }
    expected = str(tmp_path / "2021-05-13-project-hail-mary" / "B0DWVVNLC9.jpg")
    assert gmc.cover_target_path(bundle) == expected


def test_cover_target_path_falls_back_to_cover_when_no_asin(tmp_path):
    """When asin is empty, target filename is cover.jpg."""
    bundle = {
        "dir": str(tmp_path / "2021-05-13-project-hail-mary"),
        "asin": "",
    }
    result = gmc.cover_target_path(bundle)
    assert result.endswith("cover.jpg")


# ---------------------------------------------------------------------------
# is_valid_image
# ---------------------------------------------------------------------------


def test_is_valid_image_accepts_valid_jpeg():
    """JPEG magic bytes + adequate size pass validation."""
    data = b"\xff\xd8\xff" + b"\x00" * 3000
    assert gmc.is_valid_image(data) is True


def test_is_valid_image_accepts_valid_png():
    """PNG magic bytes + adequate size pass validation."""
    data = b"\x89PNG\r\n\x1a\n" + b"\x00" * 3000
    assert gmc.is_valid_image(data) is True


def test_is_valid_image_rejects_too_small():
    """Data below MIN_IMAGE_BYTES is rejected even with valid magic."""
    data = b"\xff\xd8\xff" + b"\x00" * 10
    assert gmc.is_valid_image(data) is False


def test_is_valid_image_rejects_gif_magic():
    """GIF magic bytes (Amazon blank) are rejected."""
    data = b"GIF89a" + b"\x00" * 3000
    assert gmc.is_valid_image(data) is False


def test_is_valid_image_rejects_html():
    """HTML content is rejected even if large enough."""
    data = b"<html>" + b"x" * 3000
    assert gmc.is_valid_image(data) is False


def test_is_valid_image_rejects_empty():
    """Empty bytes are rejected."""
    assert gmc.is_valid_image(b"") is False


def test_is_valid_image_rejects_43_byte_amazon_blank():
    """Amazon's 43-byte blank GIF is rejected."""
    # Real Amazon blank: GIF89a magic
    data = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x00\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    assert len(data) == 43
    assert gmc.is_valid_image(data) is False


# ---------------------------------------------------------------------------
# min image constant exists and is sane
# ---------------------------------------------------------------------------


def test_min_image_bytes_constant_is_sane():
    """MIN_IMAGE_BYTES is at least 2048 (rejects Amazon 43-byte blank with margin)."""
    assert gmc.MIN_IMAGE_BYTES >= 2048


# ---------------------------------------------------------------------------
# HTTP timeout constant exists
# ---------------------------------------------------------------------------


def test_http_timeout_constant_exists():
    """HTTP_TIMEOUT module constant is defined and positive."""
    assert gmc.HTTP_TIMEOUT > 0


# ---------------------------------------------------------------------------
# every requests.get call in source carries timeout
# ---------------------------------------------------------------------------


def test_every_requests_get_has_timeout():
    """All requests.get call sites in the module pass a timeout argument."""
    import inspect
    src = inspect.getsource(gmc)
    calls = [line.strip() for line in src.splitlines() if "requests.get(" in line]
    assert calls, "expected at least one requests.get call"
    missing = [c for c in calls if "timeout" not in c]
    assert not missing, f"requests.get calls missing timeout: {missing}"


# ---------------------------------------------------------------------------
# main() returns int
# ---------------------------------------------------------------------------


def test_main_returns_int(monkeypatch):
    """main() returns an int (contract for sys.exit)."""
    # Patch find_missing_cover_bundles to return empty list — no network calls.
    monkeypatch.setattr(gmc, "find_missing_cover_bundles", lambda _: [])
    result = gmc.main(books_dir="/nonexistent", dry_run=True)
    assert isinstance(result, int)
