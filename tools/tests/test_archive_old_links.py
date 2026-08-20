# ABOUTME: Tests for archive_old_links.py host classification (archive services vs external links).
# ABOUTME: Exercises host_matches/is_external_link against exact domains, subdomains, and look-alike hosts.

import archive_old_links


def test_archive_domains_match_exact_and_subdomain():
    assert archive_old_links.host_matches('archive.org', archive_old_links.ARCHIVE_DOMAINS)
    assert archive_old_links.host_matches('web.archive.org', archive_old_links.ARCHIVE_DOMAINS)
    assert archive_old_links.host_matches('archive.ph', archive_old_links.ARCHIVE_DOMAINS)


def test_lookalike_hosts_rejected():
    assert not archive_old_links.host_matches('evil-archive.org.attacker.com', archive_old_links.ARCHIVE_DOMAINS)
    assert not archive_old_links.host_matches('notarchive.org', archive_old_links.ARCHIVE_DOMAINS)
    assert not archive_old_links.host_matches('archive.org.evil.com', archive_old_links.ARCHIVE_DOMAINS)


def test_empty_and_case_handled():
    assert not archive_old_links.host_matches(None, archive_old_links.ARCHIVE_DOMAINS)
    assert not archive_old_links.host_matches('', archive_old_links.ARCHIVE_DOMAINS)
    assert archive_old_links.host_matches('WEB.ARCHIVE.ORG', archive_old_links.ARCHIVE_DOMAINS)


def test_is_external_link_classification():
    assert archive_old_links.is_external_link('https://example.com/page')
    assert not archive_old_links.is_external_link('https://web.archive.org/web/2016/http://example.com')
    assert not archive_old_links.is_external_link('https://harper.blog/2016/01/01/post/')
    assert not archive_old_links.is_external_link('/relative/path')
    # Look-alike external hosts must still be archived
    assert archive_old_links.is_external_link('https://evil-archive.org.attacker.com/x')
