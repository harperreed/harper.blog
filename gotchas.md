# Gotchas

Hard-won facts about working on harper.blog. Add yours; keep entries short.

## Build & deploy

- Netlify CSP has no `unsafe-inline`: template-emitted `<style>` blocks and `style=` attributes die in production while every local check passes. All CSS goes through the `assets/css/*` bundle.
- Production deploys run `./scripts/build_with_random_theme.sh` — every deploy gets a random theme from `themes.css`. Visual changes must survive all themes, and the first deploy after a CSS change is worth a look.
- Two hugo binaries exist: `.mise.toml` pins the real one; `/opt/homebrew/bin/hugo` drifts. The pin resolves per-directory — `hugo --source <repo>` run from OUTSIDE the repo gets the global/homebrew binary. If a build error names an API that greps clean (e.g. `.Site.Language.Locale` "can't evaluate field"), check `hugo version` first.
- Never run a one-shot `hugo` build in the checkout while `hugo serve` is running — the server serves `public/` from disk, and the build poisons it and silently kills the watcher. Use `hugo --destination /tmp/hugo-verify` or stop the server. Recovery: kill server, `rm -rf public`, relaunch.
- Build output can still differ across runs: hugo silently drops GitInfo if git is locked mid-build. (Photos RSS `lastBuildDate` now comes from the newest image note, and footer/out_of_date `partialCached` calls are keyed properly.) Normalize before diffing two builds.
- Netlify's build cache (`/opt/build/cache`, holds `HUGO_CACHEDIR` with the processed-image cache) is shared across deploy contexts: a deploy-preview build warms production and vice versa. Measured on PR #187: 32min cold, ~1.5min warm. Flip side: poisoned cache from any context reaches them all — fix via "Clear cache and retry deploy".

## CI workflows

- `make check` is the canonical local gate: tools ruff+pytest, i18n parity, contrast sweep. CI mirrors it — tools-tests lints and tests `tools/`, check-i18n covers translations, and build-check does a pinned-hugo production build to /tmp plus feed/redirect/inline-style checkers on anything touching layouts/config/assets/static/i18n.
- Cron content workflows push with a rebase-retry loop under a `concurrency` queue-of-one: a waiting run replaces the queued one, and a manual `workflow_dispatch` can be silently eaten by the next cron tick. If your dispatch vanished, that's why.
- Job timeouts conclude `cancelled`, not `failure` — `if: failure()` alert steps stay silent on them, so a persistently hanging cron eats ticks without alerting (known gap; `failure() || cancelled()` is the candidate fix).
- Runner network weather is real: checkout fetches sometimes hang dead mid-stream (three times on 2026-08-20 alone). Rerun on a fresh runner before redesigning anything; job timeouts exist to bound exactly this.

## Design decisions (settled — don't re-litigate)

- Body type is **sans** (system-ui at 1.125rem/1.6). A serif stack was tried in PR #161 and reverted on sight.
- Post byline keeps **everything**: date · author · word count · reading time · kudos. A slimmed byline was tried and reverted.
- Photos get the **white-mat frame** (padding + border, white like a physical print across all themes). Bare images were tried and reverted.
- Feed contexts show photos small (3-across thumbs in /notes/, one-line strips on home), the individual note page shows them big (breakout to 1000px). Thumbs link to their note.
- Any visual change is provisional until Harper has seen it rendered on the preview — approval of a written list is not visual sign-off.
- Markdown `![]()` images in posts stay bare. The figure/image shortcodes are the deliberate opt-in for the framed breakout treatment — an auto-wrapping render hook was tried and reverted. Don't blanket-normalize how content renders.
- PR #156 (Tailwind redesign) was closed unmerged. Notes referencing Tailwind/PurgeCSS/postcss describe that dead branch, not main.
- Headings wrap `pretty`, not `balance` — balance's even-line break read as a phantom width limit on long titles (looked capped well short of the 720px column). Harper confirmed pretty on preview, 2026-08-16.
- Paragraphs get NO `text-wrap` rule (default greedy wrap). `p { text-wrap: pretty }` shipped in #161 and read fine then, but Safari's pretty now rag-balances whole paragraphs — lines stop short of the column edge, same phantom-width look. Harper confirmed the removal on preview, 2026-08-16.

## Templates

- `RegularPages` sorts by weight before date: `/about/` (menu weight 3, dateless, `nofeed: true`) is `RegularPages[0]` on every language site. Anything taking "the newest page" must filter nofeed/dateless pages first — this zeroed the root feed's `lastBuildDate` and silently wasted a feed slot.
- `.Paginate` may only get one collection+size per page, but repeat calls return the first paginator — so head partials (which render before the main block) and list templates share `partials/paginator.html` as the single place that defines collections and sizes. Never call `.Paginator`/`.Paginate` anywhere else.
- `canonifyURLs = true` only absolutizes URLs in rendered HTML output — `.Content` embedded in RSS templates keeps root-relative img srcs. Feed templates that need absolute srcs must prefix `site.BaseURL` themselves (`index.rss.xml` does); prefixing `.Permalink` onto an already-root-relative src mangles the path.
- Never add `width=`/`height=` attrs to `.book-cover` imgs: the CSS sizes them with `width:100%` + `aspect-ratio:2/3` and no `height:auto`, so the height attr becomes the used height (CSS `aspect-ratio` only applies when a dimension is auto) and `object-fit:cover` crops ~half the cover away. Layout-shift attrs need `height:auto` in the CSS first.

## Theme CSS

- Theme dark mode cascades as: root light block ← root dark block ← **theme light block** ← theme dark block. A variable set only in a theme's light block applies in dark mode too unless the dark block overrides it. Per-theme `--color-muted` overrides regressed dark mode exactly this way and were removed — the `color-mix` derivation in `root-colors.css` covers muted for every palette; the explicit hexes in `:root` are only the no-color-mix fallback.
- `make check-contrast` sweeps all 26 palettes × light/dark (468 pairs) for WCAG AA 4.5:1, modeling that cascade. Run it after touching `root-colors.css` or `themes.css`.

## Verification on this machine

- Headless Chrome hangs from agent shells — don't use it for layout checks. Verify via the served CSS bundle + arithmetic + Harper's eyes on the tailscale HTTPS preview (`tailscale serve` proxying to a localhost hugo).
- `~/workspace` symlinks to `~/Public/src` — same repo behind both paths, not two clones.
- `hugo --quiet` swallows `warnf` output. When debugging templates with `warnf`, build without `--quiet` or the probe looks like it never ran.
- The dev server's `partialCached` output survives incremental rebuilds AND template touches: a frontmatter change that alters a cached partial's output (e.g. setting `bsky:` on a post — comments.html is cached by `.Title`) won't show on the preview until the server restarts. Fresh one-shot builds are correct; restart the server before declaring a cached partial broken.
- After mise upgrades Go, hugo servers launched from stale shells segfault on the next config reload (inherited GOROOT points at the deleted toolchain). Relaunch via a fresh `mise x -- hugo serve`.

## Multilingual

- `site.RegularPages` is language-scoped: on an /es/ page it returns only Spanish pages. Books/music/links exist only on the en site (translations are `_index.<lang>.md` suffix files), so filtering it by those sections comes back empty there and lists/stats render blank. For cross-language data use `hugo.Sites.Default.RegularPages` — and it's `hugo.Sites`, not `site.Sites` (deprecated since hugo 0.156, WARNs in the server log).
- `i18n` placeholders: a key called as `{{ i18n "key" arg }}` must use `{{ . }}` in its value; `%s`/`%d` values only work via `printf (i18n "key") args`. Mixing the styles renders blanks or `%!(EXTRA …)` garbage. `make check-i18n` catches parity/phantom/dead keys — run it after touching `layouts/` or `i18n/`.
- Frontmatter `aliases:` on section `_index.*.md` pages with a `url:` override never emitted redirect stubs (dev server, full rebuilds included). URL moves go in `static/_redirects` (Netlify) instead — the `/id/*` and `/es/media/*/list/` entries are the pattern.
- A section URL move breaks a whole family, not one page: list, grid, feed (`index.xml`), and pagination each need a redirect, and individual pages may stay at the old path (so no broad splats). The media consolidation shipped with only the es redirects; the en 404s — including feed subscribers — went unnoticed for a day. Review a URL move by curling the old URLs.

## Python tools

- `grab_starred_links.py` initializes `FirecrawlApp` and `OpenAI` at module level — importing it in tests without live credentials crashes. Test against source directly, not via import.
- Registry writes in `grab_micro_posts_fixed.py` are atomic (temp + `os.replace`). `save_url_registry` and `save_content_registry` leave temp files prefixed with the registry filename if interrupted; safe to delete.
- CI workflow caches `./tools/.script_cache` (dot-prefixed). Code must use `CACHE_DIRECTORY = ".script_cache"` — no dot was the old mismatch that meant every OpenAI call was a cache miss.
- Note registries live only in `data/notes/` (`processed_urls.json`, `processed_content_hashes.json`; the split copies were merged in PR #180). A registry that fails to parse ABORTS the run (`RegistryCorruptError`) by design — restore the file from git, never regenerate: a fresh registry forgets every published URL and re-posts the whole feed.
- ruff ≥0.16 ships far more default rules than the old E4/E7/E9/F — `tools/pyproject.toml` pins `[tool.ruff.lint] select` to keep lint scope fixed. Don't "clean up" the pin; removing it detonates ~300 new violations.
- `git check-ignore` never matches dir-only patterns (`foo/`) for paths absent from disk — "not ignored" for a directory that doesn't exist yet proves nothing. `tools/.gitignore` keeps both `script_cache` (stale pre-rename dir still on disk) and `.script_cache/` (the live cache) deliberately.
- `grab_micro_posts_fixed.main()`, `grab_starred_links.main()`, `grab_spotify_saved_tracks.main()`, and `grab_read_books.main()` all return `int` and call `sys.exit(main())`. Per-item failures log and continue; run-level failures (auth, feed unreachable, all items failed) exit non-zero so GitHub Actions goes red.
- `grab_read_books.py` skips any book whose `index.md` exists — content unchecked. python-frontmatter ≥ 1.2 writes str (not bytes), so the old `open(path, "wb")` + `frontmatter.dump` pattern truncated the file then raised, committing zero-byte bundles that blocked re-fetching forever (dormant since April, activated by the 2026-08-14 dep upgrade). Book writes now go through `book_files.write_frontmatter_file` — serialize first, then open. If a zero-byte bundle appears, delete the dir and re-run the goodreads workflow.
- Spotify revokes refresh tokens now and then (Jul 21 2026: expired, then revoked); the poller then dies nightly with `invalid_grant`, and CI can't re-auth itself (`open_browser=False`). Recover with `cd tools && uv run spotify_reauth.py`, then `gh secret set SPOTIFY_TOKEN_CACHE < tools/.spotify_cache` and re-dispatch — backfill is automatic (full-library pagination, existing tracks skipped). The token is bound to the client id that minted it, so all SPOTIFY_* secrets must come from the same dashboard app.
- `markup.toml` sets goldmark `unsafe = true` (old posts need raw HTML). Feed-ingestion tools must sanitize all feed-derived content that lands in markdown bodies — use `html.escape()` for text and `frontmatter.Post(content, **metadata)` (never `frontmatter.loads(feed_body)`) to prevent frontmatter injection.

## Content

- The `content/post/*-2.md` files are mostly NOT duplicates. Of the original 21, only 3 were true same-date twins (deleted); the other 18 are real posts — titles reused years apart, or sole copies. Filename `-2` ≠ duplicate; check content before deleting.
- Permalinks are `/:year/:month/:day/:slug/` and `:slug` falls back to the title — two posts with the same title on the same date silently fight over one URL, and which file wins the render lottery flipped between hugo 0.154 and 0.164.
