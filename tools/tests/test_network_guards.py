# ABOUTME: Guards for network robustness in grab_micro_posts_fixed: every HTTP
# ABOUTME: call carries a timeout; image downloads are size- and type-capped.
import inspect

import grab_micro_posts_fixed as gm


def test_module_declares_timeout_and_size_constants():
    assert gm.HTTP_TIMEOUT == 30
    assert gm.MAX_IMAGE_BYTES == 10 * 1024 * 1024


def test_every_requests_call_passes_timeout():
    src = inspect.getsource(gm)
    calls = [line for line in src.splitlines() if "requests.get(" in line]
    assert calls, "expected requests.get call sites"
    assert all("timeout" in line for line in calls), f"missing timeout in: {calls}"


def test_download_image_rejects_non_image_content_type(tmp_path, monkeypatch):
    class FakeResp:
        headers = {"Content-Type": "text/html"}
        def raise_for_status(self): pass
        def iter_content(self, chunk_size): return iter([b"<html>"])
        def close(self): pass
    monkeypatch.setattr(gm.requests, "get", lambda *a, **k: FakeResp())
    out = tmp_path / "img.jpg"
    assert gm.download_image("https://example.com/x.jpg", str(out)) is False
    assert not out.exists()


def test_download_image_caps_size(tmp_path, monkeypatch):
    class FakeResp:
        headers = {"Content-Type": "image/jpeg"}
        def raise_for_status(self): pass
        def iter_content(self, chunk_size): return iter([b"x" * (1024 * 1024)] * 11)
        def close(self): pass
    monkeypatch.setattr(gm.requests, "get", lambda *a, **k: FakeResp())
    out = tmp_path / "img.jpg"
    assert gm.download_image("https://example.com/x.jpg", str(out)) is False
    assert not out.exists()
