# harper.blog redesign: match harperreed.com

**Date:** 2026-07-27
**Status:** Approved
**Branch:** `match-harperreed-com`

## Goal

Reskin harper.blog to the harperreed.com design language by adopting its stack
(Tailwind + SCSS + PostCSS) and porting its visual system. The blog's UI/UX is
an invariant: same pages, same navigation, same content organization, same
features. Only the visual layer changes.

Source of truth for the target design: `../harperreed-static` (the
harperreed.com repo).

## UI/UX invariants (do not change)

- All content types and URLs: posts, notes, links, books, music, now, photos,
  media, pages.
- Homepage structure: intro content, 5 recent posts, 5 recent notes, "More"
  links.
- Nav items (menu-driven): Home, harper@modest.com, RSS.
- Footer contents: footer menu, copyright, "generated on" gitinfo line, email
  link, language switcher.
- Multilingual system (en/es/ja/ko + id/zh index pages), i18n strings,
  hreflang.
- Features: Bluesky comments, tinylytics (+events), image lazy-loading,
  AI-disclosure, out-of-date warnings, translation notices, chroma code
  highlighting, RSS/SEO/schema partials, skip-link.
- Python content automation and GitHub Actions content updaters.

Approved deltas (explicitly decided, visible to users):

- Header identity: lowercase bold **harper.blog** wordmark; avatar retired.
- The 25 theme variations, the random-theme-per-deploy behavior, and the
  localStorage theme picker are retired. One design, light + dark via
  `prefers-color-scheme` only.
- Column width 720px → 800px.

## Target design system (ported from harperreed-static)

### Tokens

Six CSS custom properties, defined in `assets/scss/base.scss`:

| Variable              | Light     | Dark      |
| --------------------- | --------- | --------- |
| `--color-text-primary`| `#111111` | `#F0F0F0` |
| `--color-text-body`   | `#555555` | `#D8D8D8` |
| `--color-text-muted`  | `#767676` | `#9A9A9A` |
| `--color-text-faint`  | `#949494` | `#717171` |
| `--color-bg-page`     | `#FFFFFF` | `#111111` |
| `--color-border-rule` | `#EEEEEE` | `#3A3A3C` |

Dark values apply under `@media (prefers-color-scheme: dark)`. No manual
toggle, no `:root.dark` override (that exists in the static site for its own
reasons; the blog has no toggle UI — YAGNI).

### Fonts

- **DM Sans** (variable, `100 900`) — body (`font-sans`).
- **Sora** (variable, `100 900`) — headings/display (`font-display`).
- Self-hosted woff2 copied from `harperreed-static/assets/fonts/`
  (`DMSans-Variable.woff2`, `Sora-Variable.woff2`), preloaded, inline
  `@font-face` with `font-display: swap` — same pattern as the static site's
  `head/style.html`.
- Font stacks end in `sans-serif`: ja/ko/zh glyphs are not in these fonts and
  must fall back to system sans. Colors, layout, and chrome still match on
  CJK pages.
- Verdana is fully retired.

### Chrome

- **Layout:** `max-w-[800px] mx-auto px-6` everywhere.
- **Header:** wordmark `harper.blog` left — `text-lg font-bold
  text-text-primary no-underline`; right side: existing nav items (Home,
  email, RSS) as `text-base text-text-muted no-underline
  hover:text-text-primary transition-colors`; container
  `flex justify-between items-baseline pt-8 pb-4 sm:pt-12 sm:pb-7` with
  `border-bottom: 1px solid var(--color-border-rule)`.
- **Footer:** `mt-16` with top border-rule; inside `py-10`, all text
  `text-xs text-text-muted`; links muted → primary on hover; keeps footer
  menu, ©, gitinfo line, email, language switcher.
- **Skip-link:** static site's sr-only/focus pattern.

### Content treatment

- `page_content` class = Tailwind typography `prose sm:prose-lg lg:prose-xl`
  with all `--tw-prose-*` mapped to the six tokens (port of
  `content.scss`): body `#555`, headings `#111` in Sora, links
  `text-text-primary font-semibold underline hover:no-underline`.
- List pages (homepage posts/notes, section lists): keep the existing
  date | title two-column structure, restyled — date column
  `text-text-faint tabular-nums`, title links `text-text-primary`. Grid
  treatment mirrors the static site's timeline
  (`grid grid-cols-[8.125rem_1fr] gap-x-4 gap-y-3` — 8.125rem preserves the
  current 130px date column).
- Code: chroma highlighting preserved; block wrapper restyled to the
  monochrome idiom (border-rule border, small radius). Note: params lists a
  `syntax.css` resource that does not exist in `assets/` (latent build warn) —
  resolve while converting `code.css`.
- Blockquotes, tables, figures: prose defaults with token mapping; figure
  captions muted italic. The current heavy padded/white-bg figure style is
  replaced by the prose figure treatment.

## Stack changes

New files (ported and adapted from harperreed-static):

- `package.json` — devDeps: `tailwindcss@^3.4`, `@tailwindcss/typography`,
  `@tailwindcss/forms`, `postcss`, `postcss-cli`, `autoprefixer`,
  `@fullhuman/postcss-purgecss`. Scripts: `dev`, `build` (hugo with the
  blog's existing production flags).
- `tailwind.config.js` — `content: ["./hugo_stats.json"]`, `darkMode:
  "media"`, fontFamily `{primary/display: Sora, sans: "DM Sans"}`, colors
  mapped to the six CSS vars. No `theme.json` indirection (static site's
  legacy) — plain config.
- `postcss.config.js` — tailwind + purgecss/autoprefixer in production,
  hugo_stats extractor; safelist trimmed to what the blog actually needs
  (lightbox/gallery classes only if present).
- `assets/scss/main.scss` + partials: `base.scss` (tokens),
  `content.scss` (prose mapping), `components.scss` (converted functional
  styles), plus per-feature partials as needed.
- `layouts/partials/head/style.html` — SCSS→libsass→PostCSS pipeline +
  font preload + inline @font-face; replaces the `customcss` concat logic in
  `head/css.html`.
- `assets/fonts/DMSans-Variable.woff2`, `assets/fonts/Sora-Variable.woff2`.

Config changes:

- `config/_default/hugo.toml`: enable `[build] writeStats` (hugo_stats.json
  for Tailwind purge).
- `config/_default/params.toml`: remove `customcss` list and theme selection
  block; drop `/js/theme.js` from `customjs`.
- `netlify.toml`: build commands become `npm install && hugo <existing
  flags>` (all contexts); random-theme script removed. `NODE_VERSION` env
  added.
- `.gitignore`: add `node_modules/`. `hugo_stats.json` is committed (same as
  the static site) so Tailwind's content scan never sees an empty file on a
  fresh build.

## Conversion inventory

Every layout template converts to Tailwind utilities. Per-section order, each
step leaving a building site and deleting its legacy CSS file:

1. Chrome: `baseof.html` (drop `HUGO_RANDOM_THEME`/theme-class logic),
   `header.html`, `nav.html`, `footer.html`, `language-switcher.html` →
   retires `harper.css`, `root-colors.css`, `shared.css` (absorbed into
   scss).
2. Homepage `index.html` + post/notes lists.
3. Posts: `post/list.html`, `post/single.html` (+ related posts, byline,
   tags, pagination partials).
4. Notes: `notes/list.html`, `notes/single.html`, `notes-grid.html` →
   retires `notes.css`, `notes-grid.css`.
5. Links: `links/list.html`, `links/single.html` → retires `links.css`.
6. Books: `books/list.html`, `books/single.html`, `books-grid.html` →
   retires `books.css`.
7. Music: `music/list.html`, `music/single.html`, `music-grid.html` →
   retires `music.css`.
8. Now, photos, media, 404, remaining shortcodes → retires `media.css`.
9. Functional styles → scss components: `bsky_comments.css`,
   `tinylytics.css`, `image-loading.css`, `ai-disclosure.css`,
   `outofdate.css`, `translations.css`, `code.css` (+ syntax highlighting
   resolution).

Grids (books/music/notes) keep their existing responsive grid UX; colors,
borders, and fonts move to tokens.

## Deletions

- `assets/css/themes.css` (25 variations, 696 lines)
- `assets/js/theme.js` (localStorage ThemeManager)
- `scripts/build_with_random_theme.sh`
- `assets/css/*.css` — every file, as its section converts
- Theme-selection comments/config in `params.toml`

## Easter eggs

- The ASCII-art head comment from the static site's `head.html` ports into
  the blog's head (with the same email note).
- The `heads-row` fade animation stays exclusive to harperreed.com.

## Out of scope

- The stale `redesign` branch (a different, hand-rolled-theme effort from
  2026-07-02) — left untouched.
- Content edits, tool changes, new features, homepage restructuring.
- Manual dark-mode toggle.

## Verification

- `hugo` clean build with zero new warnings (the pre-existing `syntax.css`
  warn gets fixed, not silenced).
- `hugo serve` visual matrix: {en, es, ja, ko} × {home, post single, posts
  list, notes, notes single, books, music, links, now} × {light, dark}.
- Fonts: confirm DM Sans/Sora load self-hosted (no external requests),
  CJK pages readable via system fallback.
- Netlify deploy preview green before merge to main.
- No Tailwind purge misses: spot-check dynamically-composed classes
  (safelist as needed, logged in the plan).
