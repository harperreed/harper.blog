# gotchas

Hard-won facts about this repo. Add yours; keep entries short.

- **Inline styles die in production.** Netlify CSP (`style-src` without `unsafe-inline`) blocks template-emitted `<style>` blocks and `style=` attributes. Local builds/serves pass anyway — no CSP headers locally. Put styles in the `customcss` bundle (`config/_default/params.toml` → `assets/css/`).
- **Two hugo binaries.** `.mise.toml` pins hugo (0.164.0 as of the migration PR); homebrew has its own. Without mise activation you get homebrew and version-skew breakage (removed APIs like `.Site.Author`, fixed PR #159). Check `which -a hugo` before trusting a weird template error.
- **Build output is nondeterministic.** `partialCached "footer.html" .` has no cache key, so one arbitrary page's `.GitInfo` hash lands in every footer; `out_of_date.html` is cached by year, so "N years ago" numbers come from whichever post in that year renders first. Two builds of identical source can differ on thousands of pages. Normalize these before trusting a build diff.
- **WordPress import left `content/post/*-2.md` duplicates (21 files).** Two pairs share a title+date with their sibling and collide on the same permalink (`/2004/06/29/updates/`, `/2005/02/01/ipod-mini-…`); which file publishes is a render lottery and flipped between hugo 0.154 and 0.164.
- **Deploys randomize the theme.** Netlify runs `scripts/build_with_random_theme.sh` — test CSS changes against the themes in `assets/css/themes.css`, not just the default.
- **`~/workspace` symlinks to `~/Public/src`.** Same repo behind both paths; not two clones.
- **PR #156 (Tailwind redesign) was closed unmerged.** Notes referencing Tailwind/PurgeCSS/postcss describe that dead branch, not main.
