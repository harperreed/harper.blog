# Blog redesign — text-led minimal (harper theme)

Date: 2026-07-01
Owner: Harper Reed (Doctor Biz)
Source: `~/Downloads/Harper blog redesign.zip` (extracted to `/tmp/harper-redesign/`)

## Goal

Replace the current `hugo-bearcub`-based theme on harper.blog with the "text-led
minimal" redesign delivered as a self-contained Hugo theme (`harper`). Preserve
1,451 existing `/post/` URLs, four languages of content, six content
sub-sections, and the site's existing feature set (Bluesky comments,
Tinylytics, SEO/OG/Twitter cards, related posts, RSS).

## Non-goals

- Migrate URLs from `/post/` to `/posts/` (rejected — SEO risk)
- Preserve the 20+ theme chooser (autumn, cyber, cyberpunk, halloween, xmas,
  etc.) — replaced by a light/dark toggle
- Keep the id/zh language variants live (dormant on disk, out of nav)
- Move automation tools (`tools/*.py`) — they continue to write to
  `content/*/*.md` unchanged

## Decisions (locked in)

| Question              | Decision                                                  |
| --------------------- | --------------------------------------------------------- |
| Approach              | Full theme swap (drop `hugo-bearcub`)                     |
| Languages             | Keep en / es / ja / ko in nav                             |
| Sections in nav       | Posts, Notes, Books, Links, Music, Media, About, Now      |
| Media slot            | In-site photos grid at `/media/` (from `content/photos/`) |
| Features to port      | Bluesky comments, Tinylytics, SEO cards, related posts, RSS |
| Theme chooser         | Dropped — light/dark only                                 |
| Post URL structure    | Keep `/post/YYYY/MM/slug/` (rewire theme to `post` section) |
| Frame images (home)   | Auto-pull 3 latest photos (from `content/notes/` `images`) |
| Frame images (about)  | Auto-pull 4 latest photos (from `content/notes/` `images`) |
| About page stats      | Auto-compute (post count, years, per-week rate)           |
| Rollout               | Phased branch migration (7 commits on `redesign` branch)  |

## Architecture

### Repo structure changes

```
harper.blog/
├── config/_default/
│   ├── hugo.toml           # + theme = "harper"
│   ├── module.toml         # - hugo-bearcub import (keep SEO modules)
│   └── params.toml         # - themeStyle/customcss/customjs
│                           # + since, languages, framesFromPhotos
├── content/                # unchanged on disk
├── layouts/                # site-level overrides (kept minimal, most goes into theme)
├── themes/harper/          # NEW — from the redesign zip
│   ├── layouts/
│   ├── static/css/main.css
│   └── static/js/theme.js
└── static/css/*.css        # legacy chooser files deleted in phase 7
```

### Content section handling

The redesign templates assume a `posts` (plural) section. This site uses `post`
(singular). Resolution: **rewire the theme's queries**, not the URLs.

- `themes/harper/layouts/index.html` line ~15 → `where site.RegularPages "Section" "post"`
- `themes/harper/layouts/_default/list.html` — no change (uses `.Pages`)
- `themes/harper/layouts/_default/single.html` line ~18 → `where site.RegularPages "Section" "post"`

All 1,451 permalinks stay at `/post/YYYY/MM/slug/`.

### Template inventory

**Ported verbatim from zip (with `post`/`posts` fix):**
`_default/baseof.html`, `_default/single.html`, `_default/list.html`,
`_default/about.html`, `index.html`, `notes/list.html`, `notes/single.html`,
`partials/head.html`, `partials/header.html`, `partials/footer.html`

**New/adapted for this site's content types:**

| Path                                       | Purpose                                    |
| ------------------------------------------ | ------------------------------------------ |
| `layouts/books/list.html`                  | Book cards (cover, title, author)          |
| `layouts/books/single.html`                | Single book page                           |
| `layouts/links/list.html`                  | Dated link list (row pattern)              |
| `layouts/music/list.html`                  | Track list (compact rows)                  |
| `layouts/photos/list.html` (alias `/media/`) | Photo grid using `.frames`               |
| `layouts/now/single.html`                  | One-off Now page                           |
| `layouts/partials/language-switcher.html`  | 4-lang selector (masthead)                 |
| `layouts/partials/related-posts.html`      | 3 more posts under an article              |
| `layouts/partials/bluesky-comments.html`   | Comment embed                              |
| `layouts/partials/tinylytics.html`         | Analytics snippet                          |
| `layouts/partials/head/seo.html`           | OG/Twitter/canonical/hreflang              |

**Retired (deleted in phase 7):**
`layouts/partials/comments.html`, `generated.html`, `get-featured-image.html`,
`nav.html`, `out_of_date.html`, `pagination.html`, `post-translations.html`,
`social_card.html`, `tags.html`, `theme-chooser.html`

### Design tokens

Single source in `themes/harper/static/css/main.css:6-27`:

```css
:root {
  --bg:   #FFFFFF;
  --bg2:  #F7F5F1;
  --ink:  #191817;
  --mut:  #8C877E;
  --line: #ECE9E3;
  --acc:  #B8532C;   /* warm orange — the one accent */
  --page: 680px;     /* masthead + shell width */
  --read: 640px;     /* article measure */
  --font: -apple-system, ...;
  --mono: ui-monospace, ...;
}
[data-theme="dark"] { ... }
```

Retheming = edit `:root` + `[data-theme="dark"]`. No other files.

### i18n

- Language config in `config/_default/languages.toml` unchanged
- Menu files `config/_default/menu.{en,es,ja,ko}.toml` are currently sparse
  (only `contact`/`footer` entries). Phase 5 adds explicit `[[main]]` entries
  for Home, Posts (→ `/post/`), Notes, Books, Links, Music, Media (→ `/photos/`),
  About, Now in each of the four language menu files. `menu.{id,zh}.toml`
  remain untouched (dormant).
- Translation keys in `i18n/{en,es,ja,ko}.yaml` extended with new redesign
  labels needed by the theme: `latestFrames`, `morePosts`, `selectedFrames`,
  `contact`, `writtenByHuman`, `nothingHereYet`, `moreInNotes`,
  `subscribeViaRSS`, `sayHi`
- Language switcher rendered inline in masthead as `EN · ES · JA · KO`
  (small, muted, active in ink color). Points at the current page's
  translated equivalent via `.Translations`, falls back to language home.
- `hreflang` link tags emitted per language in `partials/head/seo.html`

### Feature port

| Feature            | Where                                                        |
| ------------------ | ------------------------------------------------------------ |
| Bluesky comments   | `single.html` for `post` section, below content, above More posts. Uses existing `static/js/bluesky_comments.js`. |
| Tinylytics         | `baseof.html`, one line before `</body>`                     |
| SEO/OG/Twitter     | `partials/head/seo.html`, uses `/images/og.png` default, per-post `.Params.image` override |
| Related posts      | `partials/related-posts.html`, 3 posts, styled as `.more`    |
| RSS/JSON feeds     | Hugo default per section; nav `RSS` chip → `/index.xml`      |

### About page

`content/about.md` — new file (English), with per-language variants:
`content.es/about.md`, `content.ja/about.md`, `content.ko/about.md`.

```toml
+++
title = "About"
layout = "about"
hello = "Hello."
portrait = "img/portrait.jpg"
closing = "Thanks for reading. I am incredible."

[[contact]]
label = "harper@modest.com"
href = "mailto:harper@modest.com"
[[contact]]
label = "@harper.lol on bluesky"
href = "https://bsky.app/profile/harper.lol"
[[contact]]
label = "harperreed.com ↗"
href = "https://harperreed.com"
+++

My name is Harper Reed. ...
```

Stats block in `_default/about.html` computed inline:

```gotemplate
{{ $posts := len (where site.RegularPages "Section" "post") }}
{{ $years := sub now.Year (site.Params.since | default 2001) }}
{{ $perWeek := div (float $posts) (mul $years 52) }}
```

Rendered as three stat cards: `{{ $years }} yrs blogging`, `{{ $posts }} posts`,
`~{{ printf "%.2f" $perWeek }} / week`.

### Frames (home + about)

`content/photos/` is not populated on this site — photos live inline in notes
via `images = [...]` frontmatter. Frame strips pull from there:

```gotemplate
{{/* Collect the most-recent image references from notes */}}
{{ $frames := slice }}
{{ range (where site.RegularPages "Section" "notes").ByDate.Reverse }}
  {{ range .Params.images }}
    {{ $frames = $frames | append . }}
  {{ end }}
  {{ if ge (len $frames) 3 }}{{ break }}{{ end }}
{{ end }}
{{ range first 3 $frames }}
  <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
{{ end }}
```

If notes have no `images`, the frame strip is hidden entirely (the theme
wraps it in `{{ with site.Params.frames }}`). Fallback: a hand-curated
`frames = ["/img/..."]` list can be set in `params.toml`.

Params:

```toml
homeFramesCount  = 3
aboutFramesCount = 4
```

## Phased rollout

Branch: `redesign`. Each phase = one commit. `hugo serve --buildDrafts --buildFuture`
must render without errors at the end of every phase.

### Phase 1 — Foundation

- `git checkout -b redesign`
- Remove `hugo-bearcub` import from `config/_default/module.toml`
- `hugo mod tidy`
- Copy `/tmp/harper-redesign/hugo-theme/themes/harper/` → `themes/harper/`
- Set `theme = "harper"` in `config/_default/hugo.toml`
- Comment out `themeStyle`, `customcss`, `customjs` in `params.toml`
- Rewire `post`/`posts` (three lines across `index.html` and `_default/single.html`)
- **Verification**: `hugo serve` boots, home page renders (posts list may be broken),
  no template errors

### Phase 2 — Post templates

- Confirm `_default/single.html` renders a random post cleanly
- Confirm `_default/list.html` at `/post/` renders a paginated list
- Home page shows 5 latest posts with `See all N posts →`
- **Verification**: pick 10 random posts across years, confirm they render;
  visit `/post/`, confirm listing

### Phase 3 — Section templates

- `books/list.html`, `books/single.html`
- `links/list.html`
- `music/list.html`
- `photos/list.html` (aliased to `/media/`)
- `notes/{list,single}.html` — already in the zip, verify against real notes
- **Verification**: visit each section URL, confirm layouts match the redesign
  spirit and content renders

### Phase 4 — About page + auto-stats

- Write `content/about.md`, `content.es/about.md`, `content.ja/about.md`,
  `content.ko/about.md`
- Update `_default/about.html` to auto-compute stats
- Wire frames from `content/photos/`
- **Verification**: `/about/` renders with correct stats; language variants
  render at `/es/about/`, `/ja/about/`, `/ko/about/`

### Phase 5 — i18n port

- Add explicit `[[main]]` menu entries (Home, Posts→/post/, Notes, Books,
  Links, Music, Media→/photos/, About, Now) to `config/_default/menu.en.toml`
  and translate labels in `menu.{es,ja,ko}.toml`
- Add new redesign translation keys to `i18n/{en,es,ja,ko}.yaml`
  (`latestFrames`, `morePosts`, `selectedFrames`, `contact`,
  `writtenByHuman`, `nothingHereYet`, `moreInNotes`, `subscribeViaRSS`, `sayHi`)
- Write `partials/language-switcher.html`, include in `partials/header.html`
- Add `hreflang` tags to `partials/head/seo.html`
- **Verification**: switcher toggles between languages on same slug; hreflang
  present in `<head>` of every page; each language home renders full nav

### Phase 6 — Feature port

- `partials/bluesky-comments.html` + include in `_default/single.html` (post section only)
- `partials/tinylytics.html` + include in `_default/baseof.html`
- `partials/head/seo.html` (OG/Twitter/canonical/hreflang/description)
- `partials/related-posts.html` + include below content on `_default/single.html`
- Verify RSS: `/index.xml`, `/post/index.xml`, `/notes/index.xml`, etc.
- **Verification**: view page source on a post, confirm OG tags + Bluesky
  embed present; hit RSS URLs, confirm valid XML; Tinylytics beacon fires

### Phase 7 — Cleanup

- Delete `static/css/root-colors.css`, `harper.css`, `shared.css`, `themes.css`,
  `bsky_comments.css`, `outofdate.css`, `ai-disclosure.css`, `image-loading.css`,
  `tinylytics.css`, `media.css`, `books.css`, `music.css`, `links.css`, `notes.css`,
  `notes-grid.css`, `code.css`, `translations.css`, `syntax.css`
  (fold anything still needed into `themes/harper/static/css/main.css`)
- Delete `layouts/partials/theme-chooser.html`, `comments.html`, `generated.html`,
  `get-featured-image.html`, `nav.html`, `out_of_date.html`, `pagination.html`,
  `post-translations.html`, `social_card.html`, `tags.html`
- Delete `static/js/image-loading.js` if unused
- `hugo --cleanDestinationDir --minify --gc` — full production build, zero errors
- **Verification**: production build succeeds; `du -sh public/` sanity check;
  spot-check 10 random posts across sections and languages

### Merge

- PR from `redesign` → `main`
- Netlify preview URL for final review
- Merge on approval

## Success criteria

1. `hugo --gc --minify` builds without errors after every phase.
2. All 1,451 posts render at their existing `/post/YYYY/MM/slug/` URLs.
3. `/es/`, `/ja/`, `/ko/` variants render with translated nav and switcher.
4. Home page matches the redesign: lede + 5 posts + 3 frames from real photos.
5. About page auto-computes stats and renders the 4-frame strip.
6. Bluesky comments embed appears on `/post/*` pages.
7. Tinylytics beacon fires on every page.
8. OG/Twitter cards present in `<head>` of every content page.
9. Related posts appear below content on `/post/*` pages.
10. Light/dark toggle works with no flash and persists across reloads.
11. No console errors on any page.
12. Automation tools (`tools/*.py`) continue to produce content that renders correctly.

## Risks + mitigations

| Risk                                                       | Mitigation                                                     |
| ---------------------------------------------------------- | -------------------------------------------------------------- |
| Old posts use bearcub-specific shortcodes that break       | Phase 2 spot-check across years surfaces this early; port any needed shortcodes into `themes/harper/layouts/shortcodes/` |
| Removing bearcub breaks something we don't know it depends on | `hugo mod tidy` after removal + full `hugo serve` boot at end of phase 1 |
| Translation content references removed CSS classes         | i18n content is text-only in frontmatter/body; low risk        |
| Frame auto-pull returns empty (recent notes have no `images`) | Theme conditionally hides the frame strip when list is empty; hand-curated `frames = [...]` in `params.toml` as fallback |
| Netlify redirects break                                    | `/post/` URL scheme unchanged; no redirect rules touched       |

## Out of scope for this design

- Adding new content types
- Redesigning the automation tools
- Migrating to a different site generator
- Custom fonts (staying on system stack per the redesign)
- New shortcodes beyond what's needed to render existing posts
