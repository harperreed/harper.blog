# Robustness Audit — harper.blog

Date: 2026-08-20. Method: seven parallel expert reviews (build reliability, content pipeline, CI/CD, Netlify/edge, security, data integrity, verification coverage), each read the actual source and — where possible — verified against live data (`gh run list`, `curl` against harper.blog, dry-run tooling). Findings deduplicated and re-verified where experts disagreed.

## Verified solid (checked, not assumed)

- **Zero URL collisions** across 4,788 content files. 301 dates have multiple posts; all slugs distinct after Hugo normalization.
- **Zero** duplicate notes (dedup dry-run), zero-byte files, orphan translations, non-UTF-8 files, NFD filename hazards, case collisions.
- **CSS fingerprinting works**: bundle is sha512-fingerprinted, so `immutable, max-age=31536000` on `/css/*` is safe despite the random theme per deploy. Live-verified.
- **Injection hardening held** under adversarial review: YAML injection blocked (ruamel quoting), `javascript:` hrefs neutered by Go templates (`#ZgotmplZ`), image path traversal blocked, Bluesky comments render via `textContent`, no secrets in git history, `.spotify_cache` properly ignored, Goodreads XML parse safe (expat defaults).
- **Hugo module pinned** (pseudo-version + go.sum). **Netlify header blocks merge additively** — no security-header shadowing on `/images/*` (live-verified).
- **Cron health**: 0 failures in last 30 runs for notes/links/goodreads; 1/30 for spotify (the 2026-08-17 token revocation).
- Past-incident regression tests exist and are correct (zero-byte bundles, spotify auth exit code) — but see Critical #1.

## CRITICAL

### C1. The security test suite never runs in CI
`tools/pyproject.toml:35` sets `testpaths = ["tests"]`; `test_security_fixes.py` lives in `tools/` root, so `uv run pytest` (what tools-tests.yaml runs) never discovers it. All ~20 tests covering frontmatter injection, HTML escaping, atomic registry writes, and exit-code signaling are dead weight. Found independently by two reviewers.
**Fix (1 line):** add `"."` to `testpaths`, or move the file into `tools/tests/`.

### C2. Notes dedup registry is split; 520 of 654 notes unprotected
Active registry `data/notes/processed_urls.json` has 114 entries (CI sets `NOTES_HUGO_DATA_DIR=../data/notes`). The pre-migration registry `content/data/notes/processed_urls.json` has 665 and was never merged. 520 notes exist only in the abandoned one; 1 note (`2024-09-23_7ffb4f38b368_nice-hangs-with-clint-jacqui`) is in neither. A `--check-archive` or any fetch beyond the recent window recreates them as duplicates. Content-hash registries have the same split (665 vs 701).
**Fix:** merge old into new (dict union, old values win on conflict), delete the old files, commit.

### C3. Corrupt registry JSON silently resets to empty
`grab_micro_posts_fixed.py:206-208` and `:249-251` catch `JSONDecodeError`, log, and return `{}` — the run proceeds treating every URL as new. Directory-existence guards limit the blast, but the registry gets rewritten wrong. Amplifies C2.
**Fix:** abort the run (non-zero exit) on corrupt registry instead of continuing.

### C4. No network timeouts anywhere in the pipeline; no job timeouts in CI
- `grab_micro_posts_fixed.py:88,129,359` — bare `requests.get`, no timeout.
- `grab_starred_links.py:48` — `feedparser.parse(url)` no timeout; `:203` Firecrawl scrape no timeout.
- `grab_read_books.py:54` — OpenAI call no timeout.
- `download_image()` (`grab_micro_posts_fixed.py:128-133`) additionally has no size cap and no content-type check — a hostile feed image URL can push a 1 GB blob into memory and the repo.
- No workflow declares `timeout-minutes`; GitHub default is 6 hours.
**Fix:** `timeout=30` on every HTTP call; stream + ~10 MB cap + `Content-Type: image/*` check on image downloads; `timeout-minutes: 10-15` on all four cron jobs.

### C5. Cron commit race: bare `git push`, no rebase
`notes.yaml:51`, `links.yaml:49`, `grab_goodreads.yaml:43`, `grab_spotify_saved_tracks.yaml:42` all commit and push without `git pull --rebase`. Notes (every 10 min) and links (every 30) collide at :00/:30 whenever GitHub's cron scheduler bunches them; the loser fails non-fast-forward with no retry. Currently green by scheduling luck. Related: `cancel-in-progress: true` on notes/links can kill a run after disk writes but before push, silently dropping state.
**Fix:** `git pull --rebase origin main && git push` in all four; reconsider `cancel-in-progress` (queue instead of kill) given writes are not all atomic.

## IMPORTANT

### Build & deploy
- **`make getmodules` runs `hugo mod get -u` inside the deploy-preview build** (`netlify.toml:14`) and local `prod_build` (`Makefile:29,35`) — unpinned upgrade of all Hugo modules at build time, defeating go.sum. Remove it from the preview command (use `hugo mod download` if anything); reserve upgrades for deliberate commits.
- **`new-hugo-deploy.yaml` is dead code with production credentials**: push triggers commented out, zero runs ever, still `workflow_dispatch`-able with `NETLIFY_SITE_ID`/`NETLIFY_API_TOKEN`. Delete it (Netlify's git integration is the real deploy path). Deleting also moots the `fetch-depth: 1` GitInfo/Lastmod problem and the self-referential `HUGO_RESOURCECACHE` env var found inside it.
- **No Hugo build gate in GitHub Actions** — a template typo is caught only by Netlify. Add a small build-check workflow (`hugo --destination /tmp/hugo-check`) on PRs and pushes to main.
- **`make check-contrast` never runs in CI** while every deploy randomizes across 24 themes. Add a workflow on `assets/css/**` changes.
- **Homepage served stale by the CDN**: live probe showed `age: 12046` against `max-age=3600` (Cloudflare revalidates lazily). With 10-minute automation, cold PoPs show an hours-old homepage. Set `/` to `max-age=600` (or split browser/CDN with `s-maxage`).
- **photos RSS `lastBuildDate` uses `now`** (`layouts/photos/rss.xml:17`) — the known build nondeterminism, still unfixed; copy the newest-item pattern from `layouts/_default/rss.xml:58-62`. Also `enclosure length="0"` (invalid RSS) in `music/rss.xml:50`, `books/rss.xml:46`, `photos/rss.xml:45`.
- **Every auto-commit triggers a full Netlify build** — no `[build.ignore]`/skip logic. Fine today; a guard is cheap insurance.

### Failure visibility
- **Spotify token revocation fails silently** (throttled GitHub email only; already bit twice — Jul 21 and Aug 17 2026). Add an `if: failure()` step to the cron workflows that opens a GitHub issue (durable, visible). Applies to all four crons.

### Security hardening (no criticals found)
- **Workflow `permissions:` blocks missing** on all four content workflows — they run with write-all `GITHUB_TOKEN` (confirmed in run logs: Packages/PRs/Issues/SecurityEvents write). Lock to `contents: write`.
- **`tools-tests.yaml` uses floating action tags** (`checkout@v4`, `setup-uv@v5`) while every other workflow SHA-pins. Pin to the SHAs check-i18n.yaml already uses.
- **Tinylytics script has no SRI** (`layouts/partials/footer.html:33`) — a Tinylytics compromise is arbitrary first-party JS. Add `integrity=` + `crossorigin` (accepting hash-rotation upkeep) or accept and document the risk.
- **CSP cleanup** (`netlify.toml:31-44`), verified against live headers:
  - `unpkg.com` IS used — `static/pretty-feed-v3.xsl:17` loads `@tailwindcss/browser@4` (floating major). Self-host or pin with SRI, then drop unpkg from script-src.
  - `cdnjs.cloudflare.com` serves only CSS (two SVG `<?xml-stylesheet?>`s) — remove from `script-src`; also drop the dns-prefetch in `resource-hints.html:10` if the SVGs move.
  - `img-src` contains both `*` and `http:` — drop both (mixed-content permissive, rest redundant).
  - `connect-src https:` → narrow to `'self' https://public.api.bsky.app https://bsky.social https://tinylytics.app`.
  - Add `manifest-src 'self'`; delete deprecated `X-XSS-Protection`.
- **Deploy previews build drafts/future with no noindex** — add `{{ if not hugo.IsProduction }}<meta name="robots" content="noindex, nofollow">{{ end }}` to baseof.

### Pipeline correctness
- **Mixed naive/aware datetime crash path** in notes sort (`grab_micro_posts_fixed.py:852-856`; also `:842` catches only ValueError) — a single malformed `date_published` kills the whole run. Normalize to UTC-aware at parse.
- **Books partial-state orphan**: directory + data YAML created before the OpenAI summary call; if the summary fails after data is written, the dir has no `index.md` and the data-file-exists guard blocks all retries forever (`grab_read_books.py:549,591,612`). Clean up on failure or key retries off `index.md`.
- **Prompt injection**: feed title/content interpolated raw into the OpenAI prompt (`grab_starred_links.py:140-154`); structured output limits blast radius to published tags/summary. Move data into a bracketed user message.
- **OpenAI cache key omits model name** (`grab_starred_links.py:158`) — stale-model responses served after a model change. Include `OPENAI_MODEL` in the key.
- **links.yaml cache key embeds `github.sha`** (`links.yaml:37`) — primary key never hits; one-shot cache entries forever. Key on something stable.

### Data
- **Internal files published to the live site**: `content/notes/data/deduplication_log.json` (internal paths + hashes) and two translation artifacts (`content/post/2025-12-03-getting-claude-code-to-do-your-emails/index.ja.md.log.json`, `index.ja.log`). Move/delete; add cleanup to the translation tooling.
- **46 book covers (`B0DW*` ASINs) exist only on Amazon's CDN** — the local fallback image is missing; if Amazon stops serving the legacy URL pattern those covers silently 404. Re-fetch or add `image_url` fallback in the template.
- **514 link files use RFC 2822 dates** — Hugo parses them; Python tooling doesn't. Normalize new output to ISO 8601 in `grab_starred_links.py`.

## MINOR (backlog)

- Delete legacy `tools/grab_micro_posts.py` (still has the `frontmatter.loads` injection hole; superseded by `_fixed`).
- Fuzzy 50-char prefix duplicate check (`grab_micro_posts_fixed.py:332-338`) can suppress legitimate notes and permanently registry-block them — rely on exact hash + 80% overlap.
- O(n²) note-ID assignment: `get_highest_note_id` rescans the notes dir per new item (`:628`); reuse the pre-scan from `:716`.
- `book_files.write_frontmatter_file` not atomic — temp + `os.replace` like the registries.
- MD5 → sha256 for cache keys (`grab_starred_links.py:56,158`).
- `bluesky_comments.js:326,452` — two `innerHTML` assignments (currently static strings); convert to DOM construction so future edits can't create XSS.
- Referrer-Policy downgraded to `no-referrer-when-downgrade` on `/images/social_card*` — remove the override.
- Taxonomy fragmentation: `ai`(14)/`AI`(2), `llm`/`LLM`, and 95 singular/plural pairs (worst: `personal-experience` 74 vs `personal-experiences` 1). Canonicalize; steer the tag-generation prompts.
- Makefile: no `.PHONY`; no aggregate `make check` (prereq for pre-commit). Add `check: check-i18n check-contrast + pytest (both roots)`.
- Workflow hygiene: four crons pin checkout@v2-era SHAs (Node-deprecation shim) — bump to v4 SHAs; spotify cron `0 */24 * * *` → `0 0 * * *`; `authors.yml` → `.yaml`; standardize `fetch-depth`.
- gitignore gaps: `tools/__pycache__/`, `.script_cache` (dot version) not ignored; untracked `docs/simmer/`, `tools/strip_is_reread.py` in limbo.
- `out_of_date.html` partialCached keyed by post date only but computes years-ago from `now` — add `now.Year` to the key (stale math at year boundaries).
- Local `hugo` in PATH is 0.154.1 vs pinned 0.164.0 — mise not activated in the shell (`eval (mise activate fish)`).
- `GO_VERSION = "1.23"` floats on patch — pin exact.
- HTML pages other than `/` get `max-age=0, must-revalidate` — old posts could cache for hours (CDN efficiency, optional).
- Frontmatter `---` inside field values breaks naive Python parsers on 3 files (Hugo fine) — use real YAML parsing in tools.
- Verification backlog: no feed XML validation (`xmllint` post-build, ~30 lines), no redirect smoke test (~30-60 lines; a real incident class), no internal link checker (htmltest `--skip-external`, ~20 lines), no ruff/type-checking on tools, no frontmatter schema pytest (~50 lines), no post-build `grep 'style='` guard for the CSP-kills-inline-styles class.

## Suggested attack order

1. **Same-day one-liners:** C1 testpaths, C2 registry merge, photos RSS `now`, delete legacy tool, gitignore entries.
2. **One PR across the four cron workflows:** rebase-before-push, `timeout-minutes`, `permissions: contents: write`, failure-alert step, cron/action-SHA hygiene.
3. **One PR across tools/:** HTTP timeouts everywhere, image size/type caps, registry-corruption abort, datetime normalization, books orphan cleanup, cache-key fixes.
4. **Deploy config PR:** delete new-hugo-deploy.yaml, drop getmodules from preview, homepage cache-control, CSP cleanup + SRI + preview noindex.
5. **Verification infrastructure:** `make check`, Hugo build gate, contrast-in-CI, feed/redirect/inline-style smoke checks, ruff.
