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


# ---------------------------------------------------------------------------
# parse_og_image — Goodreads og:image extraction
# ---------------------------------------------------------------------------

_OG_IMAGE_HTML = """\
<html><head>
<meta property="og:title" content="Excession" />
<meta property="og:image" content="https://images.gr-assets.com/books/1487025510l/12345.jpg" />
</head><body></body></html>
"""

_NO_OG_IMAGE_HTML = """\
<html><head>
<meta property="og:title" content="Excession" />
</head><body></body></html>
"""

_MALFORMED_OG_IMAGE_HTML = """\
<html><head>
<meta property="og:image" content="" />
</head><body></body></html>
"""

_NON_HTTPS_OG_IMAGE_HTML = """\
<html><head>
<meta property="og:image" content="http://images.gr-assets.com/books/123.jpg" />
</head><body></body></html>
"""

_HTTP_BLOCK_HTML = """\
<html><head><title>Access Denied</title></head>
<body>Please verify you are a human.</body>
</html>
"""


def test_parse_og_image_extracts_url():
    """parse_og_image returns the og:image URL when present."""
    url = gmc.parse_og_image(_OG_IMAGE_HTML)
    assert url == "https://images.gr-assets.com/books/1487025510l/12345.jpg"


def test_parse_og_image_returns_none_when_absent():
    """parse_og_image returns None when the page has no og:image tag."""
    url = gmc.parse_og_image(_NO_OG_IMAGE_HTML)
    assert url is None


def test_parse_og_image_returns_none_for_empty_content():
    """parse_og_image returns None when og:image has an empty content attribute."""
    url = gmc.parse_og_image(_MALFORMED_OG_IMAGE_HTML)
    assert url is None


def test_parse_og_image_rejects_http_urls():
    """parse_og_image returns None for non-https image URLs."""
    url = gmc.parse_og_image(_NON_HTTPS_OG_IMAGE_HTML)
    assert url is None


def test_parse_og_image_returns_none_on_captcha_page():
    """parse_og_image returns None when page has no og:image (e.g. block page)."""
    url = gmc.parse_og_image(_HTTP_BLOCK_HTML)
    assert url is None


# ---------------------------------------------------------------------------
# find_missing_cover_bundles — goodreads_link field included
# ---------------------------------------------------------------------------


def test_find_missing_cover_bundles_includes_goodreads_link(tmp_path):
    """Returned bundle dict includes goodreads_link from frontmatter."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(
        content="body",
        title="Project Hail Mary",
        asin="B0DWVVNLC9",
        book_author="Andy Weir",
        goodreads_link="https://www.goodreads.com/book/show/54493401-project-hail-mary",
    )
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert result[0]["goodreads_link"] == "https://www.goodreads.com/book/show/54493401-project-hail-mary"


def test_find_missing_cover_bundles_goodreads_link_defaults_empty(tmp_path):
    """goodreads_link is empty string when not present in frontmatter."""
    d = tmp_path / "2021-05-13-project-hail-mary"
    d.mkdir()
    post = fm.Post(content="body", title="Project Hail Mary", asin="B0DWVVNLC9", book_author="Andy Weir")
    (d / "index.md").write_text(fm.dumps(post), encoding="utf-8")

    result = gmc.find_missing_cover_bundles(str(tmp_path))

    assert result[0]["goodreads_link"] == ""


# ---------------------------------------------------------------------------
# process_bundle — Goodreads fallback ordering
# ---------------------------------------------------------------------------


def test_process_bundle_tries_goodreads_when_openlibrary_fails(tmp_path, monkeypatch):
    """When OpenLibrary returns no cover, Goodreads fallback is attempted."""
    d = tmp_path / "2022-01-01-some-book"
    d.mkdir()
    (d / "index.md").write_text("", encoding="utf-8")  # dummy — bundle dict is passed directly

    bundle = {
        "dir": str(d),
        "slug": "2022-01-01-some-book",
        "title": "Some Book",
        "book_author": "Some Author",
        "asin": "B00FAKE001",
        "goodreads_link": "https://www.goodreads.com/book/show/12345.Some_Book",
    }

    monkeypatch.setattr(gmc, "fetch_openlibrary_cover_id", lambda *a, **kw: None)
    monkeypatch.setattr(
        gmc,
        "fetch_goodreads_cover_bytes",
        lambda *a, **kw: b"\xff\xd8\xff" + b"\x00" * 3000,
    )

    status = gmc.process_bundle(bundle, dry_run=True)
    assert status == "fetched"


def test_process_bundle_skips_goodreads_when_openlibrary_succeeds(tmp_path, monkeypatch):
    """When OpenLibrary provides a valid cover, Goodreads is never called."""
    d = tmp_path / "2022-01-01-some-book"
    d.mkdir()

    bundle = {
        "dir": str(d),
        "slug": "2022-01-01-some-book",
        "title": "Some Book",
        "book_author": "Some Author",
        "asin": "B00FAKE001",
        "goodreads_link": "https://www.goodreads.com/book/show/12345.Some_Book",
    }

    good_cover = b"\xff\xd8\xff" + b"\x00" * 3000
    monkeypatch.setattr(gmc, "fetch_openlibrary_cover_id", lambda *a, **kw: 9999)
    monkeypatch.setattr(gmc, "download_cover_bytes", lambda *a, **kw: good_cover)

    goodreads_called = []

    def fake_goodreads(*a, **kw):
        goodreads_called.append(True)
        return good_cover

    monkeypatch.setattr(gmc, "fetch_goodreads_cover_bytes", fake_goodreads)

    status = gmc.process_bundle(bundle, dry_run=True)
    assert status == "fetched"
    assert not goodreads_called, "Goodreads should not be called when OpenLibrary succeeds"


def test_process_bundle_no_cover_when_both_sources_fail(tmp_path, monkeypatch):
    """When both OpenLibrary and Goodreads fail, status is 'no_cover'."""
    d = tmp_path / "2022-01-01-some-book"
    d.mkdir()

    bundle = {
        "dir": str(d),
        "slug": "2022-01-01-some-book",
        "title": "Some Book",
        "book_author": "Some Author",
        "asin": "B00FAKE001",
        "goodreads_link": "https://www.goodreads.com/book/show/12345.Some_Book",
    }

    monkeypatch.setattr(gmc, "fetch_openlibrary_cover_id", lambda *a, **kw: None)
    monkeypatch.setattr(gmc, "fetch_goodreads_cover_bytes", lambda *a, **kw: None)

    status = gmc.process_bundle(bundle, dry_run=True)
    assert status == "no_cover"


def test_process_bundle_failed_when_goodreads_returns_invalid_image(tmp_path, monkeypatch):
    """When Goodreads returns bytes that fail validation, status is 'failed'."""
    d = tmp_path / "2022-01-01-some-book"
    d.mkdir()

    bundle = {
        "dir": str(d),
        "slug": "2022-01-01-some-book",
        "title": "Some Book",
        "book_author": "Some Author",
        "asin": "B00FAKE001",
        "goodreads_link": "https://www.goodreads.com/book/show/12345.Some_Book",
    }

    monkeypatch.setattr(gmc, "fetch_openlibrary_cover_id", lambda *a, **kw: None)
    # Return raw HTML — fails is_valid_image
    monkeypatch.setattr(gmc, "fetch_goodreads_cover_bytes", lambda *a, **kw: b"<html>" + b"x" * 3000)

    status = gmc.process_bundle(bundle, dry_run=True)
    assert status == "failed"
