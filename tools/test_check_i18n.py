# ABOUTME: Tests for check_i18n.py, the static checker for Hugo i18n hygiene.
# ABOUTME: Covers yaml bundle parsing, key parity, phantom/dead keys, and scoping regressions.

import textwrap

import check_i18n


def test_parse_bundle_reads_hugo_list_form():
    text = textwrap.dedent("""
        # i18n/en.yaml
        - id: readmore
          translation: "Read more"

        - id: "on"
          translation: "on"
    """)
    keys, dupes = check_i18n.parse_bundle(text)
    assert keys == {"readmore": "Read more", "on": "on"}
    assert dupes == []


def test_parse_bundle_keeps_plural_dict_as_one_key():
    text = textwrap.dedent("""
        - id: reading-stats-books
          translation:
            one: "{{ . }} book"
            other: "{{ . }} books"
    """)
    keys, dupes = check_i18n.parse_bundle(text)
    assert list(keys) == ["reading-stats-books"]
    assert keys["reading-stats-books"] == {"one": "{{ . }} book", "other": "{{ . }} books"}
    assert dupes == []


def test_parse_bundle_reports_duplicate_ids():
    text = textwrap.dedent("""
        - id: readmore
          translation: "Read more"
        - id: readmore
          translation: "Read even more"
    """)
    keys, dupes = check_i18n.parse_bundle(text)
    assert dupes == ["readmore"]
    assert keys["readmore"] == "Read even more"


def test_parse_bundle_empty_file():
    keys, dupes = check_i18n.parse_bundle("")
    assert keys == {}
    assert dupes == []


def test_find_template_keys_extracts_i18n_and_T_calls():
    text = textwrap.dedent("""
        <a>{{ i18n "readmore" }}</a>
        {{ $label := (T "posts") }}
        {{ i18n "related-posts" | default "Related Posts" }}
        {{ printf (i18n "date-aria") .Date }}
    """)
    assert check_i18n.find_template_keys(text) == {
        "readmore": [2],
        "posts": [3],
        "related-posts": [4],
        "date-aria": [5],
    }


def test_check_parity_flags_missing_and_orphan_keys():
    bundles = {
        "en": {"a": "A", "b": "B"},
        "es": {"a": "A"},
        "ja": {"a": "A", "b": "B", "extra": "X"},
    }
    findings = check_i18n.check_parity(bundles)
    assert findings == [
        "parity: es.yaml missing 1 key(s): b",
        "parity: ja.yaml has key(s) not in en.yaml: extra",
    ]


def test_check_parity_clean_when_bundles_match():
    bundles = {"en": {"a": "A"}, "es": {"a": "A"}}
    assert check_i18n.check_parity(bundles) == []


def test_check_phantom_flags_keys_defined_in_no_bundle():
    used = {"ghost": [("layouts/partials/x.html", 7)], "a": [("layouts/y.html", 2)]}
    bundles = {"en": {"a": "A"}, "es": {"a": "A"}}
    findings = check_i18n.check_phantom(used, bundles)
    assert findings == [
        "phantom: 'ghost' used at layouts/partials/x.html:7 but defined in no i18n yaml"
    ]


def test_check_dead_flags_unused_en_keys_respecting_allowlist():
    used = {"a": [("layouts/y.html", 2)]}
    bundles = {"en": {"a": "A", "unused": "U", "theme-key": "T"}}
    findings = check_i18n.check_dead(used, bundles, allow={"theme-key"})
    assert findings == ["dead: 'unused' defined in en.yaml but used in no template"]


def test_check_scoping_flags_language_scoped_regularpages():
    text = textwrap.dedent("""
        {{ range where .Site.RegularPages "Section" "post" }}
        {{ range where site.RegularPages "Section" "books" }}
    """)
    findings = check_i18n.check_scoping(text, "layouts/shortcodes/postcount.html")
    assert findings == [
        "scoping: layouts/shortcodes/postcount.html:2 uses .Site.RegularPages "
        "(language-scoped; shortcodes render on every language - use "
        "hugo.Sites.Default.RegularPages or mark the file 'i18n-check: allow-language-scoped')",
        "scoping: layouts/shortcodes/postcount.html:3 uses site.RegularPages "
        "(language-scoped; shortcodes render on every language - use "
        "hugo.Sites.Default.RegularPages or mark the file 'i18n-check: allow-language-scoped')",
    ]


def test_check_scoping_accepts_cross_language_pattern():
    text = '{{ range where hugo.Sites.Default.RegularPages "Section" "books" }}'
    assert check_i18n.check_scoping(text, "layouts/shortcodes/x.html") == []


def test_check_scoping_honors_optout_marker():
    text = textwrap.dedent("""
        {{- /* i18n-check: allow-language-scoped - this list SHOULD differ per language */ -}}
        {{ range .Site.RegularPages }}
    """)
    assert check_i18n.check_scoping(text, "layouts/shortcodes/x.html") == []


def test_run_checks_walks_repo_and_reports_all_classes(tmp_path):
    (tmp_path / "i18n").mkdir()
    (tmp_path / "i18n" / "en.yaml").write_text(
        '- id: readmore\n  translation: "Read more"\n- id: only-en\n  translation: "X"\n'
    )
    (tmp_path / "i18n" / "es.yaml").write_text('- id: readmore\n  translation: "Leer más"\n')
    partials = tmp_path / "layouts" / "partials"
    partials.mkdir(parents=True)
    (partials / "a.html").write_text('{{ i18n "readmore" }}\n{{ i18n "ghost" }}\n')
    shortcodes = tmp_path / "layouts" / "shortcodes"
    shortcodes.mkdir()
    (shortcodes / "bad.html").write_text('{{ range where .Site.RegularPages "Section" "post" }}\n')

    findings = check_i18n.run_checks(tmp_path)

    assert "parity: es.yaml missing 1 key(s): only-en" in findings
    assert any(f.startswith("phantom: 'ghost' used at layouts/partials/a.html:2") for f in findings)
    assert "dead: 'only-en' defined in en.yaml but used in no template" in findings
    assert any(f.startswith("scoping: layouts/shortcodes/bad.html:1") for f in findings)
    assert len(findings) == 4


def test_run_checks_clean_tree_returns_nothing(tmp_path):
    (tmp_path / "i18n").mkdir()
    (tmp_path / "i18n" / "en.yaml").write_text('- id: readmore\n  translation: "Read more"\n')
    (tmp_path / "layouts").mkdir()
    (tmp_path / "layouts" / "a.html").write_text('{{ i18n "readmore" }}\n')
    assert check_i18n.run_checks(tmp_path) == []
