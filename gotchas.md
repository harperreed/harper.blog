# Gotchas

Hard-won facts about working on harper.blog. Add yours; keep entries short.

## Build & deploy

- Netlify CSP has no `unsafe-inline`: template-emitted `<style>` blocks and `style=` attributes die in production while every local check passes. All CSS goes through the `assets/css/*` bundle.
- Production deploys run `./scripts/build_with_random_theme.sh` — every deploy gets a random theme from `themes.css`. Visual changes must survive all themes, and the first deploy after a CSS change is worth a look.
- Two hugo binaries exist: `.mise.toml` pins the real one; `/opt/homebrew/bin/hugo` drifts. If a build error names an API that greps clean, check `hugo version` first.
- Never run a one-shot `hugo` build in the checkout while `hugo serve` is running — the server serves `public/` from disk, and the build poisons it and silently kills the watcher. Use `hugo --destination /tmp/hugo-verify` or stop the server. Recovery: kill server, `rm -rf public`, relaunch.
- Build output is still slightly nondeterministic: photos RSS stamps `lastBuildDate` from `now`, and hugo silently drops GitInfo if git is locked mid-build. (Footer and out_of_date `partialCached` calls are now keyed properly.) Normalize before diffing two builds.

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

## Theme CSS

- Theme dark mode cascades as: root light block ← root dark block ← **theme light block** ← theme dark block. A variable set only in a theme's light block applies in dark mode too unless the dark block overrides it. Per-theme `--color-muted` overrides regressed dark mode exactly this way and were removed — the `color-mix` derivation in `root-colors.css` covers muted for every palette; the explicit hexes in `:root` are only the no-color-mix fallback.
- `make check-contrast` sweeps all 26 palettes × light/dark (468 pairs) for WCAG AA 4.5:1, modeling that cascade. Run it after touching `root-colors.css` or `themes.css`.

## Verification on this machine

- Headless Chrome hangs from agent shells — don't use it for layout checks. Verify via the served CSS bundle + arithmetic + Harper's eyes on the tailscale HTTPS preview (`tailscale serve` proxying to a localhost hugo).
- `~/workspace` symlinks to `~/Public/src` — same repo behind both paths, not two clones.
- `hugo --quiet` swallows `warnf` output. When debugging templates with `warnf`, build without `--quiet` or the probe looks like it never ran.
- The dev server's `partialCached` output survives incremental rebuilds AND template touches: a frontmatter change that alters a cached partial's output (e.g. setting `bsky:` on a post — comments.html is cached by `.Title`) won't show on the preview until the server restarts. Fresh one-shot builds are correct; restart the server before declaring a cached partial broken.

## Multilingual

- `site.RegularPages` is language-scoped: on an /es/ page it returns only Spanish pages. Books/music/links exist only on the en site (translations are `_index.<lang>.md` suffix files), so filtering it by those sections comes back empty there and lists/stats render blank. For cross-language data use `hugo.Sites.Default.RegularPages` — and it's `hugo.Sites`, not `site.Sites` (deprecated since hugo 0.156, WARNs in the server log).
- `i18n` placeholders: a key called as `{{ i18n "key" arg }}` must use `{{ . }}` in its value; `%s`/`%d` values only work via `printf (i18n "key") args`. Mixing the styles renders blanks or `%!(EXTRA …)` garbage. `make check-i18n` catches parity/phantom/dead keys — run it after touching `layouts/` or `i18n/`.
- Frontmatter `aliases:` on section `_index.*.md` pages with a `url:` override never emitted redirect stubs (dev server, full rebuilds included). URL moves go in `static/_redirects` (Netlify) instead — the `/id/*` and `/es/media/*/list/` entries are the pattern.

## Python tools

- `grab_starred_links.py` initializes `FirecrawlApp` and `OpenAI` at module level — importing it in tests without live credentials crashes. Test against source directly, not via import.
- Registry writes in `grab_micro_posts_fixed.py` are atomic (temp + `os.replace`). `save_url_registry` and `save_content_registry` leave temp files prefixed with the registry filename if interrupted; safe to delete.
- CI workflow caches `./tools/.script_cache` (dot-prefixed). Code must use `CACHE_DIRECTORY = ".script_cache"` — no dot was the old mismatch that meant every OpenAI call was a cache miss.
- `grab_micro_posts_fixed.main()`, `grab_starred_links.main()`, `grab_spotify_saved_tracks.main()`, and `grab_read_books.main()` all return `int` and call `sys.exit(main())`. Per-item failures log and continue; run-level failures (auth, feed unreachable, all items failed) exit non-zero so GitHub Actions goes red.
- `grab_read_books.py` skips any book whose `index.md` exists — content unchecked. python-frontmatter ≥ 1.2 writes str (not bytes), so the old `open(path, "wb")` + `frontmatter.dump` pattern truncated the file then raised, committing zero-byte bundles that blocked re-fetching forever (dormant since April, activated by the 2026-08-14 dep upgrade). Book writes now go through `book_files.write_frontmatter_file` — serialize first, then open. If a zero-byte bundle appears, delete the dir and re-run the goodreads workflow.
- `markup.toml` sets goldmark `unsafe = true` (old posts need raw HTML). Feed-ingestion tools must sanitize all feed-derived content that lands in markdown bodies — use `html.escape()` for text and `frontmatter.Post(content, **metadata)` (never `frontmatter.loads(feed_body)`) to prevent frontmatter injection.

## Content

- The `content/post/*-2.md` files are mostly NOT duplicates. Of the original 21, only 3 were true same-date twins (deleted); the other 18 are real posts — titles reused years apart, or sole copies. Filename `-2` ≠ duplicate; check content before deleting.
- Permalinks are `/:year/:month/:day/:slug/` and `:slug` falls back to the title — two posts with the same title on the same date silently fight over one URL, and which file wins the render lottery flipped between hugo 0.154 and 0.164.
