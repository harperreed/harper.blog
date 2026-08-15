# ABOUTME: Static checker for Hugo i18n hygiene: key parity across languages, phantom keys
# ABOUTME: (used but defined nowhere), dead keys, duplicates, and language-scoping regressions.

"""Usage: uv run tools/check_i18n.py [--root DIR]

Exits 1 with one line per finding, 0 when clean. Run via `make check-i18n`.
"""

import re
import sys
from pathlib import Path

import yaml

# Keys referenced only by hugo-bearcub theme templates, invisible to the layouts/ scan.
THEME_USED_KEYS = set()


def parse_bundle(text):
    """Parse Hugo's list-form i18n yaml into ({id: translation}, [duplicate ids])."""
    entries = yaml.safe_load(text) or []
    keys, dupes = {}, []
    for entry in entries:
        key = str(entry["id"])
        if key in keys:
            dupes.append(key)
        keys[key] = entry.get("translation")
    return keys, dupes


I18N_CALL = re.compile(r'\b(?:i18n|T)\s+"([^"]+)"')


def find_template_keys(text):
    """Map each i18n/T key referenced in template text to the lines using it."""
    found = {}
    for lineno, line in enumerate(text.splitlines(), start=1):
        for key in I18N_CALL.findall(line):
            found.setdefault(key, []).append(lineno)
    return found


def check_parity(bundles):
    """Every language must define exactly en.yaml's key set."""
    findings = []
    en = set(bundles["en"])
    for lang in sorted(bundles):
        if lang == "en":
            continue
        missing = sorted(en - set(bundles[lang]))
        if missing:
            findings.append(f"parity: {lang}.yaml missing {len(missing)} key(s): {', '.join(missing)}")
        orphans = sorted(set(bundles[lang]) - en)
        if orphans:
            findings.append(f"parity: {lang}.yaml has key(s) not in en.yaml: {', '.join(orphans)}")
    return findings


def check_phantom(used, bundles):
    """Keys referenced in templates but defined in no language's yaml."""
    defined = set().union(*(bundles[lang] for lang in bundles))
    findings = []
    for key in sorted(used):
        if key not in defined:
            file, line = used[key][0]
            findings.append(f"phantom: '{key}' used at {file}:{line} but defined in no i18n yaml")
    return findings


def check_dead(used, bundles, allow):
    """Keys defined in en.yaml that no template references (allow covers theme-only keys)."""
    return [
        f"dead: '{key}' defined in en.yaml but used in no template"
        for key in sorted(bundles["en"])
        if key not in used and key not in allow
    ]


SCOPED_PAGES = re.compile(r"(\.Site\.RegularPages|\bsite\.RegularPages)")
SCOPING_OPTOUT = "i18n-check: allow-language-scoped"


def check_scoping(text, filename):
    """Flag language-scoped page collections in shortcodes, which render on every language."""
    if SCOPING_OPTOUT in text:
        return []
    findings = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in SCOPED_PAGES.findall(line):
            findings.append(
                f"scoping: {filename}:{lineno} uses {match} "
                "(language-scoped; shortcodes render on every language - use "
                "hugo.Sites.Default.RegularPages or mark the file "
                f"'{SCOPING_OPTOUT}')"
            )
    return findings


def run_checks(root):
    """Run every check against a repo tree; returns findings sorted by class."""
    root = Path(root)
    bundles, findings = {}, []
    for path in sorted((root / "i18n").glob("*.yaml")):
        keys, dupes = parse_bundle(path.read_text())
        bundles[path.stem] = keys
        findings += [f"duplicate: '{key}' defined twice in {path.name}" for key in dupes]

    used = {}
    for path in sorted((root / "layouts").rglob("*.html")):
        rel = str(path.relative_to(root))
        for key, lines in find_template_keys(path.read_text()).items():
            used.setdefault(key, []).extend((rel, line) for line in lines)
        if path.parent.name == "shortcodes":
            findings += check_scoping(path.read_text(), rel)

    findings += check_parity(bundles)
    findings += check_phantom(used, bundles)
    findings += check_dead(used, bundles, allow=THEME_USED_KEYS)
    return findings


def main():
    root = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path(__file__).parent.parent
    findings = run_checks(root)
    for finding in findings:
        print(finding)
    if findings:
        print(f"\n{len(findings)} i18n problem(s). See tools/check_i18n.py docstring for the rules.")
        sys.exit(1)
    print("i18n clean: parity, phantom, dead, duplicate, scoping all pass.")


if __name__ == "__main__":
    main()
