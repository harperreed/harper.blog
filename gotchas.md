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

## Verification on this machine

- Headless Chrome hangs from agent shells — don't use it for layout checks. Verify via the served CSS bundle + arithmetic + Harper's eyes on the tailscale HTTPS preview (`tailscale serve` proxying to a localhost hugo).
- `~/workspace` symlinks to `~/Public/src` — same repo behind both paths, not two clones.

## Multilingual

- `site.RegularPages` is language-scoped: on an /es/ page it returns only Spanish pages. Books/music/links exist only on the en site (translations are `_index.<lang>.md` suffix files), so filtering it by those sections comes back empty there and lists/stats render blank. For cross-language data use `hugo.Sites.Default.RegularPages` — and it's `hugo.Sites`, not `site.Sites` (deprecated since hugo 0.156, WARNs in the server log).
- `i18n` placeholders: a key called as `{{ i18n "key" arg }}` must use `{{ . }}` in its value; `%s`/`%d` values only work via `printf (i18n "key") args`. Mixing the styles renders blanks or `%!(EXTRA …)` garbage. `make check-i18n` catches parity/phantom/dead keys — run it after touching `layouts/` or `i18n/`.
- Frontmatter `aliases:` on section `_index.*.md` pages with a `url:` override never emitted redirect stubs (dev server, full rebuilds included). URL moves go in `static/_redirects` (Netlify) instead — the `/id/*` and `/es/media/*/list/` entries are the pattern.

## Python tools

- `grab_starred_links.py` initializes `FirecrawlApp` and `OpenAI` at module level — importing it in tests without live credentials crashes. Test against source directly, not via import.
- Registry writes in `grab_micro_posts_fixed.py` are atomic (temp + `os.replace`). `save_url_registry` and `save_content_registry` leave temp files prefixed with the registry filename if interrupted; safe to delete.
- CI workflow caches `./tools/.script_cache` (dot-prefixed). Code must use `CACHE_DIRECTORY = ".script_cache"` — no dot was the old mismatch that meant every OpenAI call was a cache miss.
- `grab_micro_posts_fixed.main()`, `grab_starred_links.main()`, `grab_spotify_saved_tracks.main()`, and `grab_read_books.main()` all return `int` and call `sys.exit(main())`. Per-item failures log and continue; run-level failures (auth, feed unreachable, all items failed) exit non-zero so GitHub Actions goes red.
- `markup.toml` sets goldmark `unsafe = true` (old posts need raw HTML). Feed-ingestion tools must sanitize all feed-derived content that lands in markdown bodies — use `html.escape()` for text and `frontmatter.Post(content, **metadata)` (never `frontmatter.loads(feed_body)`) to prevent frontmatter injection.

## Content

- The `content/post/*-2.md` files are mostly NOT duplicates. Of the original 21, only 3 were true same-date twins (deleted); the other 18 are real posts — titles reused years apart, or sole copies. Filename `-2` ≠ duplicate; check content before deleting.
- Permalinks are `/:year/:month/:day/:slug/` and `:slug` falls back to the title — two posts with the same title on the same date silently fight over one URL, and which file wins the render lottery flipped between hugo 0.154 and 0.164.
