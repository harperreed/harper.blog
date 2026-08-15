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

## Content

- The `content/post/*-2.md` files are mostly NOT duplicates. Of the original 21, only 3 were true same-date twins (deleted); the other 18 are real posts — titles reused years apart, or sole copies. Filename `-2` ≠ duplicate; check content before deleting.
- Permalinks are `/:year/:month/:day/:slug/` and `:slug` falls back to the title — two posts with the same title on the same date silently fight over one URL, and which file wins the render lottery flipped between hugo 0.154 and 0.164.
