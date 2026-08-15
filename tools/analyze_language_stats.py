# ABOUTME: Analyzes a tinylytics stats CSV export to break down traffic by site language prefix.
# ABOUTME: Feeds the keep-or-prune decision for harper.blog's translated language sites.

"""Usage: uv run tools/analyze_language_stats.py <stats.csv>

Buckets hits by language path prefix (/es/, /ja/, ...), reports hits, unique
visitors, top pages, countries, monthly trend, and language-switcher events.
"""

import csv
import sys
from collections import Counter, defaultdict

# Active languages plus the commented-out ones (residual traffic on dead prefixes matters too)
KNOWN_LANGS = {"es", "ja", "ko", "zh", "id", "it", "fr", "de"}


def lang_of(path):
    parts = path.split("/")
    if len(parts) > 2 and parts[1] in KNOWN_LANGS:
        return parts[1]
    return "en"


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)

    hits = Counter()
    uniques = defaultdict(set)
    paths = defaultdict(Counter)
    countries = defaultdict(Counter)
    monthly = defaultdict(Counter)  # month -> lang -> hits
    referrers = defaultdict(Counter)  # lang -> referrer domain -> hits
    events = Counter()  # (event, source) pairs
    first, last = "9999", "0000"

    with open(sys.argv[1], newline="", encoding="utf-8", errors="replace") as f:
        for row in csv.DictReader(f):
            path = row["path"] or "/"
            lang = lang_of(path)
            hits[lang] += 1
            uniques[lang].add(row["unique_id"])
            paths[lang][path] += 1
            countries[lang][row["country"] or "??"] += 1
            month = (row["created_at"] or "")[:7]
            monthly[month][lang] += 1
            ref = row["referrer"] or ""
            domain = ref.split("/")[2] if ref.startswith("http") and ref.count("/") >= 2 else (ref or "(direct)")
            referrers[lang][domain] += 1
            first, last = min(first, row["created_at"] or first), max(last, row["created_at"] or last)
            if row["event"]:
                events[(row["event"], row["source"] or "")] += 1

    total = sum(hits.values())
    total_uniques = len(set().union(*uniques.values()))
    print(f"Range: {first} .. {last}")
    print(f"Total hits: {total:,}   unique visitors: {total_uniques:,}\n")

    print(f"{'lang':6} {'hits':>9} {'hit%':>7} {'uniques':>9} {'uniq%':>7}")
    for lang, n in hits.most_common():
        u = len(uniques[lang])
        print(f"{lang:6} {n:>9,} {100 * n / total:>6.2f}% {u:>9,} {100 * u / total_uniques:>6.2f}%")

    for lang in sorted(hits):
        if lang == "en":
            continue
        print(f"\n--- {lang}: top pages ---")
        for p, n in paths[lang].most_common(8):
            print(f"  {n:>6,}  {p}")
        top_c = ", ".join(f"{c}:{n:,}" for c, n in countries[lang].most_common(6))
        print(f"  countries: {top_c}")
        top_r = ", ".join(f"{d}:{n:,}" for d, n in referrers[lang].most_common(6))
        print(f"  referrers: {top_r}")

    print("\n--- monthly hits (last 14 months) ---")
    langs = [lang for lang, _ in hits.most_common()]
    print(f"{'month':8}" + "".join(f"{lang:>8}" for lang in langs))
    for month in sorted(monthly)[-14:]:
        print(f"{month:8}" + "".join(f"{monthly[month][lang]:>8,}" for lang in langs))

    print("\n--- events (top 25) ---")
    for (ev, src), n in events.most_common(25):
        print(f"  {n:>7,}  {ev!r}  source={src!r}")


if __name__ == "__main__":
    main()
