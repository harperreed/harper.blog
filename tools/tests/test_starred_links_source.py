# ABOUTME: Source-level guards for grab_starred_links (not importable without
# ABOUTME: live API creds): timeouts, model-scoped cache keys, sha256, data-role prompts.
from pathlib import Path

SRC = (Path(__file__).parent.parent / "grab_starred_links.py").read_text()


def test_socket_default_timeout_is_set():
    assert "socket.setdefaulttimeout(" in SRC


def test_openai_cache_key_includes_model():
    assert 'f"{OPENAI_MODEL}:' in SRC


def test_cache_keys_use_sha256_not_md5():
    # Cache key assignments must not use md5 (slug's md5 is a separate, stable use)
    assert "hashlib.md5(prompt" not in SRC
    assert "cache_key = hashlib.md5(" not in SRC
    assert SRC.count("hashlib.sha256(") >= 2
    assert 'cache_key = hashlib.sha256(f"{OPENAI_MODEL}:{prompt}".encode())' in SRC
    assert 'cache_key = hashlib.sha256(url.encode())' in SRC


def test_feed_content_sent_as_separate_user_data_message():
    assert '"role": "system", "content": system_message' in SRC  # instructions in system_message
    assert '"role": "user", "content": user_message' in SRC  # data in user_message


def test_slug_hash_still_md5():
    # generate_unique_slug's md5 is a stable public URL component — must NOT change
    assert "hashlib.md5(url.encode()).hexdigest()[:6]" in SRC
