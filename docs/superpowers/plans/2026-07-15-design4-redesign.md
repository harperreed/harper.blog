# Design 4 Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle harper.blog to Design 4 ("text-led minimal") — white/near-black palette, terracotta accent, hairline rules, system fonts, 660px column, ◐ light/dark toggle — with all 25 named themes ported and zero IA changes.

**Architecture:** Fresh 6-token CSS core (`tokens.css` + `base.css`) replaces `root-colors.css`/`harper.css`/`shared.css`; every other CSS file is rewritten against the new tokens. Templates keep their structure and content; edits are limited to chrome (header/nav/footer), the notes list layout, and small class hooks. Dark mode = system default + persisted manual override on `<html data-mode>`.

**Tech Stack:** Hugo (extended) + hugo-bearcub module (kept), Hugo Pipes CSS/JS bundling, vanilla JS, YAML i18n.

**Spec:** `docs/superpowers/specs/2026-07-15-design4-redesign-design.md` — read it before starting. This plan implements it 1:1 except the deviations below.

**Branch:** All work happens on the existing `feat/design4-redesign` branch.

## Deviations from the spec (approved at plan review)

1. **`--mut`/`--line` for ported themes use `color-mix()`** instead of 100 hand-baked hexes. One rule derives them for all 25 themes; `paper` keeps its hand-picked literals. `color-mix` is baseline-available since 2023.
2. **FOUC guard is a tiny external sync script (`mode-init.js`), not an inline script.** The site's CSP (`head/security.html` meta tag AND netlify.toml) is `script-src 'self' …` with no `unsafe-inline` — an inline script would be silently blocked. External + SRI needs no CSP edits.
3. **Footer copyright uses a new `footer-tagline` i18n key** (translated in all 6 languages) rendered as `© Harper Reed — <tagline>`, instead of mangling the existing `copyright` key (which would double the © or produce "© Harper Reed — 著作権"). The old `copyright` key becomes unused but stays.
4. **`links.css` and `media.css` are deleted, not re-tokenized.** The spec assigns the whole date-row pattern (dates, titles, domains, filters) to `base.css`; that leaves those two files empty.
5. **Notes list `#` permalink glyph is removed** — its function moves into the date link (spec: "date links to the note"). Kudos button stays.
6. **Post kicker uses the existing `posts` i18n key** ("Posts") instead of a new singular "Post" key — no new translations for a one-word label.
7. **`notes-grid.css` drops the hover-scale and fadeIn animation** — `image-loading.css` already fades images in, and simpler beats duplicated motion.

## Global Constraints

Every task implicitly includes these:

- **IA is frozen:** no section, URL, menu item, or page content changes beyond what a task explicitly shows. Feeds (`*.rss.xml`, `media.rss.xml`) are never edited.
- **Color tokens are exactly six:** `--bg`, `--bg2`, `--ink`, `--mut`, `--line`, `--accent`. No new color custom properties; no `--color-*` references may survive to Task 11.
- **Non-color tokens:** `--font-sans`, `--font-mono`, `--size-width: 660px`, `--radius-thumb: 4px`, `--radius-fig: 5px`, `--radius-code: 6px` (defined once in `tokens.css`).
- **CSP rules:** never add inline `<script>` or `style=""`/`<style>` to layouts. External, `'self'`-hosted assets only.
- **Chrome scoping:** site header/footer styles select `body > header` / `body > footer` — content templates (photos, notes) legitimately use `<header>` inside `main`.
- **Every task ends with a clean build:** `hugo --destination /tmp/design4-check --cleanDestinationDir` must exit 0 with no new WARN lines. Visual coherence is only required after Task 11 — mid-branch pages may look unstyled in sections whose task hasn't run yet.
- **Commits:** conventional, imperative, one per task, exact file lists (`git add <files>` — never `-A`). Never bypass hooks.
- **Indentation:** 4-space in CSS/templates (matches existing files).

## Shared vocabulary (produced across tasks, consumed everywhere)

- **Date-row list group** (the `:is()` selector list in `base.css`): `ul.blog-posts`, `ul.link-posts`, `ul.book-posts`, `ul.music-posts`, `ul.media-link-posts`, `ul.now-posts`, `ul.related-posts-list`. Markup shape: `li > span` (88px muted date) + `li > a` (18px ink title).
- **Class hooks:** `.wordmark`, `.nav-rss`, `.active` (nav), `#mode-toggle`, `.section-label`, `.more-link`, `.home-intro`, `.kicker`, `.byline`, `.footer-row`, `.footer-meta`, `.note-row`, `.note-date`, `.note-body`, `.note-meta`, `.note-title`, `.filter-notice`.
- **i18n keys added:** `footer-tagline` (Task 3), `mode-dark`, `mode-light`, `mode-toggle-aria` (Task 4) — in all 6 files: `i18n/{en,ja,es,ko,zh,id}.yaml`.
- **JS:** `assets/js/mode-init.js` (sync, own `<script>` in head), `assets/js/mode.js` (in deferred bundle).

---

### Task 1: Baseline snapshots + design tokens (inert)

**Files:**
- Create: `assets/css/tokens.css`
- Modify: `config/_default/params.toml` (customcss list, line 39-58)

**Interfaces:**
- Produces: the six color tokens + six non-color tokens on `:root`, dark values via `:root[data-mode="dark"]` and `@media (prefers-color-scheme: dark) { :root:not([data-mode="light"]) }`. Baseline build at `/tmp/design4-baseline` for Task 11's feed diff.

- [ ] **Step 1: Confirm clean state on the branch**

Run: `git -C /Users/harper/Public/src/personal/harperreed/harper.blog status --short --branch`
Expected: first line `## feat/design4-redesign`; no modified tracked files (untracked `.private-journal/`, `.superpowers/`, `docs/simmer/`, `example-new-site/`, `tools/strip_is_reread.py` are fine). If tracked files are dirty, STOP and ask.

- [ ] **Step 2: Build the pre-change baseline (feeds for Task 11)**

Run:
```bash
cd /Users/harper/Public/src/personal/harperreed/harper.blog
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --destination /tmp/design4-baseline
find /tmp/design4-baseline -name "*.xml" ! -name "sitemap*" | sort > /tmp/design4-baseline-xml.txt
wc -l /tmp/design4-baseline-xml.txt
```
Expected: build succeeds ("Total in … ms"); the xml list has >10 entries (per-language index.xml, links/books/music/photos feeds, media rss). If `/tmp/design4-baseline` is ever lost before Task 11, regenerate it from the branch-point: `git stash --include-untracked` (only if dirty) → `git checkout main` → run the build → `git checkout feat/design4-redesign` → `git stash pop`.

- [ ] **Step 3: Create `assets/css/tokens.css`**

```css
/* ABOUTME: Design-token palette (6 semantic colors × light/dark) plus font/size/radius tokens for the Design 4 restyle. */
/* ABOUTME: :root is the default "paper" palette; [data-mode] is the manual override; themes.css layers per-theme values on top. */

:root {
    --bg: #ffffff;
    --bg2: #f7f5f1;
    --ink: #191817;
    --mut: #8c877e;
    --line: #ece9e3;
    --accent: #b8532c;
    color-scheme: light;

    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: ui-monospace, Menlo, monospace;
    --size-width: 660px;
    --radius-thumb: 4px;
    --radius-fig: 5px;
    --radius-code: 6px;
}

:root[data-mode="dark"] {
    --bg: #0f1011;
    --bg2: #17181a;
    --ink: #edebe7;
    --mut: #8a8d90;
    --line: #242628;
    --accent: #e08a5f;
    color-scheme: dark;
}

@media (prefers-color-scheme: dark) {
    :root:not([data-mode="light"]) {
        --bg: #0f1011;
        --bg2: #17181a;
        --ink: #edebe7;
        --mut: #8a8d90;
        --line: #242628;
        --accent: #e08a5f;
        color-scheme: dark;
    }
}
```

- [ ] **Step 4: Prepend it to the bundle**

In `config/_default/params.toml`, change the first line of the `customcss` list:

```toml
customcss = [
    "/css/tokens.css",
    "/css/root-colors.css",
    "/css/harper.css",
    "/css/shared.css",
    "/css/themes.css",
    "/css/bsky_comments.css",
    "/css/outofdate.css",
    "/css/ai-disclosure.css",
    "/css/image-loading.css",
    "/css/tinylytics.css",
    "/css/media.css",
    "/css/books.css",
    "/css/music.css",
    "/css/links.css",
    "/css/notes.css",
    "/css/notes-grid.css",
    "/css/code.css",
    "/css/translations.css",
    "syntax.css",
]
```

- [ ] **Step 5: Verify the build and that the tokens landed (and nothing else changed)**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -l -- "--bg:#ffffff\|--bg: #ffffff" /tmp/design4-check/css/*.css
```
Expected: build clean; grep prints the bundle path (minified CSS may strip the space). The old tokens are untouched, so pages render identically.

- [ ] **Step 6: Commit**

```bash
git add assets/css/tokens.css config/_default/params.toml
git commit -m "feat(design): add design4 token palette (inert)"
```

---

### Task 2: New CSS core (`base.css`) + bundle flip

**Files:**
- Create: `assets/css/base.css`
- Delete: `assets/css/root-colors.css`, `assets/css/harper.css`, `assets/css/shared.css`, `assets/css/links.css`, `assets/css/media.css`
- Modify: `config/_default/params.toml` (customcss list)

**Interfaces:**
- Consumes: tokens from Task 1.
- Produces: all shared chrome/typography/list styles, including rules for classes that templates only adopt in later tasks (`.wordmark`, `.section-label`, `.more-link`, `.home-intro`, `.kicker`, `.footer-row`, `.footer-meta`, `.nav-rss`, `.active`, `#mode-toggle`). The date-row group styles the existing `ul.blog-posts`/`.link-posts`/`.book-posts`/`.music-posts`/`.media-link-posts`/`.now-posts`/`.related-posts-list` markup immediately.
- Known mid-branch debt (fixed by Tasks 3–9): header shows unstyled avatar+h1 until Task 3; books/music/notes/code/bsky/outofdate/ai/translations CSS still reference now-undefined `--color-*` vars until their tasks (browsers treat those declarations as guaranteed-invalid → elements fall back to base styles; build is unaffected).

- [ ] **Step 1: Confirm the dropped legacy classes are truly unreferenced**

Run: `grep -rn "helptext\|errorlist\|class=\"disabled\|class=\"content" layouts/ content/_index*.md`
Expected: no output. (`.nowrap` IS still referenced by `layouts/partials/footer.html` — it gets removed there in Task 3; until then those spans are just unstyled.)

- [ ] **Step 2: Create `assets/css/base.css`**

```css
/* ABOUTME: Core stylesheet for the Design 4 restyle: reset, chrome (header/nav/footer), typography, links, */
/* ABOUTME: the shared date-row list pattern, figures, blockquotes, tables, forms, pagination, and responsive rules. */

/* ---------- reset ---------- */
*,
*::before,
*::after {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: var(--font-sans);
    font-size: 19px;
    line-height: 1.75;
}

/* ---------- skip link ---------- */
.skip-link {
    position: absolute;
    top: -48px;
    left: 16px;
    z-index: 10;
    padding: 8px 14px;
    background: var(--bg2);
    color: var(--ink);
    border: 1px solid var(--line);
    border-radius: var(--radius-thumb);
    text-decoration: none;
    font-size: 14px;
}

.skip-link:focus {
    top: 16px;
}

/* ---------- site chrome: header ---------- */
/* body > header only: content templates (photos, notes) use <header> inside main */
body > header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px 24px;
    padding: 20px 40px;
    border-bottom: 1px solid var(--line);
}

.wordmark {
    font-size: 16px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--ink);
    text-decoration: none;
}

body > header nav {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px 22px;
    margin-left: auto;
}

body > header nav a {
    font-size: 14px;
    color: var(--mut);
    text-decoration: none;
}

body > header nav a:hover,
body > header nav a.active {
    color: var(--ink);
}

body > header nav a.nav-rss {
    color: var(--accent);
    padding-left: 22px;
    border-left: 1px solid var(--line);
}

#mode-toggle {
    font-size: 14px;
    color: var(--mut);
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    font-family: inherit;
}

#mode-toggle:hover {
    color: var(--ink);
}

/* ---------- layout column ---------- */
main {
    max-width: var(--size-width);
    margin: 0 auto;
    padding: 52px 20px 8px;
    box-sizing: content-box;
}

/* ---------- typography ---------- */
h1 {
    font-size: 36px;
    line-height: 1.15;
    letter-spacing: -0.022em;
    font-weight: 600;
    margin: 6px 0 18px;
}

h2 {
    font-size: 24px;
    line-height: 1.3;
    letter-spacing: -0.015em;
    font-weight: 600;
    margin: 40px 0 12px;
}

h3 {
    font-size: 20px;
    line-height: 1.35;
    font-weight: 600;
    margin: 32px 0 10px;
}

h4,
h5,
h6 {
    font-size: 19px;
    font-weight: 600;
    margin: 28px 0 8px;
}

p {
    margin: 0 0 1.35em;
}

main a {
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 2px;
}

article ul,
article ol {
    margin: 0 0 1.35em;
    padding-left: 1.4em;
}

.section-label,
.related-posts h3 {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--mut);
    margin: 46px 0 6px;
}

/* ---------- home intro ---------- */
.home-intro p {
    font-size: 16px;
    line-height: 1.6;
    color: var(--mut);
    margin: 14px 0 0;
}

.home-intro p:first-child {
    font-size: 22px;
    line-height: 1.55;
    letter-spacing: -0.01em;
    color: var(--ink);
    margin: 0 0 6px;
}

.more-link {
    display: inline-block;
    margin-top: 16px;
    font-size: 14px;
    color: var(--accent);
    text-decoration: none;
}

/* ---------- date-row lists (shared pattern) ---------- */
:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) {
    list-style: none;
    margin: 0;
    padding: 0;
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li {
    display: flex;
    gap: 20px;
    align-items: baseline;
    padding: 11px 0;
    border-bottom: 1px solid var(--line);
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li:last-child {
    border-bottom: none;
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li > span {
    flex: none;
    width: 88px;
    font-size: 14px;
    color: var(--mut);
    font-variant-numeric: tabular-nums;
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li > span i {
    font-style: normal;
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li a {
    font-size: 18px;
    font-weight: 500;
    letter-spacing: -0.01em;
    color: var(--ink);
    text-decoration: none;
}

:is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li a:hover {
    color: var(--accent);
}

/* secondary text inside rows (link domains, book authors, artists) */
.link-domain,
.book-domain,
.music-domain {
    font-size: 15px;
    font-weight: 400;
    color: var(--mut);
}

/* related posts put the date inside the anchor, after the title — pull it back into the date column */
a.related-post-link {
    display: flex;
    gap: 20px;
    align-items: baseline;
    flex: 1;
}

time.related-post-date {
    order: -1;
    flex: none;
    width: 88px;
    font-size: 14px;
    font-weight: 400;
    color: var(--mut);
    font-variant-numeric: tabular-nums;
}

/* filter notices on tag-filtered lists */
.blog-filter,
.link-filter,
.book-filter,
.music-filter,
.now-filter,
.filter-notice {
    font-size: 14px;
    font-weight: 400;
    color: var(--mut);
    margin: 0 0 18px;
}

/* ---------- bylines & kickers ---------- */
.kicker {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 10px;
}

.byline {
    font-size: 13px;
    color: var(--mut);
    margin: -8px 0 36px;
}

.byline a {
    color: var(--mut);
}

/* ---------- images & figures ---------- */
img {
    max-width: 100%;
    height: auto;
}

figure {
    margin: 32px 0;
}

figure img {
    display: block;
    border-radius: var(--radius-fig);
}

figcaption {
    font-size: 13px;
    color: var(--mut);
    margin-top: 8px;
}

/* ---------- blockquote ---------- */
blockquote {
    margin: 28px 0;
    padding: 2px 0 2px 20px;
    border-left: 3px solid var(--line);
    color: var(--mut);
    font-style: italic;
}

/* ---------- tables ---------- */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 28px 0;
    font-size: 16px;
}

th,
td {
    text-align: left;
    padding: 8px 10px;
    border-bottom: 1px solid var(--line);
}

th {
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--mut);
}

/* ---------- rules ---------- */
hr {
    border: 0;
    border-top: 1px solid var(--line);
    margin: 40px 0;
}

/* ---------- forms ---------- */
input,
textarea {
    font-family: inherit;
    font-size: 16px;
    color: var(--ink);
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: var(--radius-thumb);
    padding: 8px 10px;
}

/* ---------- tags ---------- */
a.blog-tags,
a.now-tags {
    font-size: 13px;
    color: var(--mut);
    text-decoration: none;
    margin-right: 10px;
}

a.blog-tags:hover,
a.now-tags:hover {
    color: var(--accent);
}

/* ---------- pagination ---------- */
.pagination {
    display: flex;
    gap: 18px;
    align-items: baseline;
    margin: 36px 0 8px;
    font-size: 14px;
}

.pagination .page-number {
    color: var(--mut);
}

.pagination a {
    color: var(--accent);
    text-decoration: none;
}

/* ---------- now page ---------- */
details summary {
    cursor: pointer;
    font-size: 14px;
    color: var(--mut);
}

/* ---------- site chrome: footer ---------- */
body > footer {
    max-width: var(--size-width);
    margin: 44px auto 0;
    padding: 22px 20px;
    border-top: 1px solid var(--line);
    box-sizing: content-box;
    font-size: 13px;
    color: var(--mut);
}

body > footer a {
    color: var(--mut);
    text-decoration: none;
}

body > footer a:hover {
    color: var(--ink);
}

.footer-row {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 6px 10px;
}

.footer-meta {
    margin-top: 8px;
}

/* ---------- focus & motion ---------- */
:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ---------- responsive ---------- */
@media (max-width: 640px) {
    body {
        font-size: 17px;
    }

    body > header {
        padding: 16px 20px;
    }

    body > header nav {
        flex-basis: 100%;
        margin-left: 0;
    }

    main {
        padding: 36px 20px 8px;
    }

    h1 {
        font-size: 30px;
    }

    :is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li {
        flex-direction: column;
        gap: 2px;
        align-items: flex-start;
    }

    :is(ul.blog-posts, ul.link-posts, ul.book-posts, ul.music-posts, ul.media-link-posts, ul.now-posts, ul.related-posts-list) li > span {
        width: auto;
        font-size: 13px;
    }

    a.related-post-link {
        flex-direction: column;
        gap: 2px;
        align-items: flex-start;
    }

    time.related-post-date {
        width: auto;
        font-size: 13px;
    }
}
```

- [ ] **Step 3: Delete the retired files**

```bash
git rm assets/css/root-colors.css assets/css/harper.css assets/css/shared.css assets/css/links.css assets/css/media.css
```

- [ ] **Step 4: Update `customcss` in `config/_default/params.toml`**

Replace the whole list with (photos.css joins in Task 10):

```toml
customcss = [
    "/css/tokens.css",
    "/css/base.css",
    "/css/themes.css",
    "/css/books.css",
    "/css/music.css",
    "/css/notes.css",
    "/css/notes-grid.css",
    "/css/code.css",
    "/css/bsky_comments.css",
    "/css/outofdate.css",
    "/css/ai-disclosure.css",
    "/css/image-loading.css",
    "/css/tinylytics.css",
    "/css/translations.css",
    "syntax.css",
]
```

- [ ] **Step 5: Verify build and rendered output**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir 2>&1 | grep -i "warn\|error" ; echo "exit: $?"
grep -c "blog-posts" /tmp/design4-check/index.html
grep -o "css/bundle[^\"]*\.css" /tmp/design4-check/index.html | head -1
```
Expected: no WARN/ERROR lines (in particular no "Missing CSS resource"); `blog-posts` count ≥ 2; a fingerprinted bundle path prints. Old `--color-*` refs still exist in not-yet-rewritten files — that is expected until Task 9.

- [ ] **Step 6: Commit**

```bash
git add assets/css/base.css config/_default/params.toml
git commit -m "feat(design): replace css core with design4 base.css, drop root-colors/harper/shared/links/media css"
```

---

### Task 3: Chrome templates — header, nav, footer, baseof

**Files:**
- Modify: `layouts/_default/baseof.html` (line 40: uncache header)
- Rewrite: `layouts/partials/header.html`, `layouts/partials/nav.html`, `layouts/partials/footer.html`
- Modify: `i18n/en.yaml`, `i18n/ja.yaml`, `i18n/es.yaml`, `i18n/ko.yaml`, `i18n/zh.yaml`, `i18n/id.yaml` (append `footer-tagline`)

**Interfaces:**
- Consumes: `.wordmark`, `.nav-rss`, `.active`, `.footer-row`, `.footer-meta` styles from Task 2.
- Produces: nav markup that Task 4 appends the `#mode-toggle` button to; `footer-tagline` i18n key. Footer stays `partialCached` (identical per language); header/nav become uncached (active states are per-page).

- [ ] **Step 1: Uncache the header in `layouts/_default/baseof.html`**

Change line 40 from:
```html
        <header>{{- partialCached "header.html" . -}}</header>
```
to:
```html
        <header>{{- partial "header.html" . -}}</header>
```
(Footer on line 42 stays `partialCached` — its output is identical for every page of a language.)

- [ ] **Step 2: Rewrite `layouts/partials/header.html`**

```html
<a class="skip-link" href="#main-content" aria-label="Skip to main content">{{ i18n "skip-link" }}</a>
<a href="{{ relURL .Site.Home.RelPermalink }}" class="wordmark" aria-label="{{ i18n "home-aria" | default "Home" }}">{{ .Site.Title }}</a>

<nav aria-label="{{ i18n "main-nav-aria" | default "Main Navigation" }}">{{- partial "nav.html" . -}}</nav>
```
(The avatar `<img>` and `<h1>` are gone; `.Site.Params.avatar` stays in config, now unused — harmless.)

- [ ] **Step 3: Rewrite `layouts/partials/nav.html`**

```html
{{ $page := . }}
{{ range .Site.Menus.main.ByWeight }}
    {{ $active := false }}
    {{ with .Page }}
        {{ if .IsHome }}
            {{ $active = $page.IsHome }}
        {{ else }}
            {{ $active = or (eq $page .) ($page.IsDescendant .) }}
        {{ end }}
    {{ end }}
    <a href="{{ .URL | relLangURL }}"{{ if $active }} class="active" aria-current="page"{{ end }}>{{ .Name }}</a>
{{ end }}
<a class="nav-rss" href='{{ absURL ("index.xml" | relLangURL) }}'
    data-tinylytics-event="feed.subscribe"
    data-tinylytics-event-value="main-rss"
    >{{ i18n "rss" | default "RSS" }}</a
>
```
Notes: the mailto menu item has no `.Page`, so `with` skips it and it is never active. Book/music/link singles won't highlight "Media" (they're separate root sections) — accepted; the highlight follows the page tree.

- [ ] **Step 4: Rewrite `layouts/partials/footer.html`**

```html
<div class="footer-row">
    <span>&copy; {{ .Site.Params.Name }} &mdash; {{ i18n "footer-tagline" | default "blogging since 2001, wtaf" }}</span>
    {{ partial "language-switcher.html" . }}
</div>
<div class="footer-row footer-meta">
    <span>
        {{ $menuItems := .Site.Menus.footer }}{{ range $index, $item := $menuItems }}<a href="{{ .URL }}">{{ .Name }}</a>{{ if ne (add $index 1) (len $menuItems) }} &middot; {{ end }}{{ end }}
        &middot;
        <a
            href="mailto:{{ .Site.Params.email }}"
            aria-label="Send email to {{ .Site.Params.Name }}"
            data-tinylytics-event="contact.email"
            data-tinylytics-event-value="footer"
            >{{ i18n "sendMeAn" | default "Send me an" }} {{ i18n "email" | default "email" }}</a
        >
    </span>
    <span>{{ i18n "generated" | default "Generated" }} {{ i18n "on" | default "on" }} {{ now.Format "Jan 2, 2006" }}{{ with .GitInfo }} &middot; {{ .AbbreviatedHash }}{{ end }}</span>
</div>
<script
    src="https://tinylytics.app/embed/WV5Khk7ZG6MZe6q49ikx.js?hits&countries&kudos=❤️&events"
    defer
></script>
```
(All prior content survives: footer menu, copyright line, generated date + git hash, email link with its tinylytics event, language switcher, tinylytics script. The `.nowrap` spans are gone — Task 2 removed that class.)

- [ ] **Step 5: Append `footer-tagline` to all six i18n files**

At the end of `i18n/en.yaml`:
```yaml

- id: footer-tagline
  translation: "blogging since 2001, wtaf"
```
`i18n/ja.yaml`:
```yaml

- id: footer-tagline
  translation: "2001年からブログを書いています、wtaf"
```
`i18n/es.yaml`:
```yaml

- id: footer-tagline
  translation: "blogueando desde 2001, wtaf"
```
`i18n/ko.yaml`:
```yaml

- id: footer-tagline
  translation: "2001년부터 블로깅 중, wtaf"
```
`i18n/zh.yaml`:
```yaml

- id: footer-tagline
  translation: "从2001年开始写博客，wtaf"
```
`i18n/id.yaml`:
```yaml

- id: footer-tagline
  translation: "ngeblog sejak 2001, wtaf"
```

- [ ] **Step 6: Verify build + rendered chrome**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -c 'class="wordmark"' /tmp/design4-check/index.html
grep -o 'aria-current="page"' /tmp/design4-check/index.html | head -1
grep -o "blogging since 2001, wtaf" /tmp/design4-check/index.html
grep -o "2001年からブログ" /tmp/design4-check/ja/index.html
grep -c "avatar" /tmp/design4-check/index.html
```
Expected: wordmark count 1; `aria-current="page"` present (Home is active on home); both tagline greps match; the avatar count only reflects non-header uses (gravatar URL no longer in the header markup — count should be 0 or only from schema/meta partials; eyeball that no `<img … class="avatar"` remains in the header).

- [ ] **Step 7: Commit**

```bash
git add layouts/_default/baseof.html layouts/partials/header.html layouts/partials/nav.html layouts/partials/footer.html i18n/en.yaml i18n/ja.yaml i18n/es.yaml i18n/ko.yaml i18n/zh.yaml i18n/id.yaml
git commit -m "feat(design): design4 chrome - wordmark header, active nav states, quiet footer"
```

---

### Task 4: Dark-mode toggle

**Files:**
- Create: `assets/js/mode-init.js`, `assets/js/mode.js`
- Delete: `assets/js/theme.js`
- Modify: `layouts/partials/head/javascript.html`, `layouts/partials/nav.html` (append button), `config/_default/params.toml` (customjs), all six `i18n/*.yaml` (3 keys)

**Interfaces:**
- Consumes: `#mode-toggle` styles (Task 2); tokens' `[data-mode]` selectors (Task 1).
- Produces: `data-mode` persisted in `localStorage.mode`; button labels via `data-label-dark`/`data-label-light` attributes; i18n keys `mode-dark`, `mode-light`, `mode-toggle-aria`.

- [ ] **Step 1: Create `assets/js/mode-init.js`**

```js
// ABOUTME: Pre-paint dark-mode guard: applies the persisted light/dark override before first render.
// ABOUTME: Loaded synchronously in <head> as an external file because the CSP forbids inline scripts.
(function () {
    try {
        var m = localStorage.getItem("mode");
        if (m === "dark" || m === "light") {
            document.documentElement.dataset.mode = m;
        }
    } catch (e) {
        /* storage unavailable: fall back to the OS preference */
    }
})();
```

- [ ] **Step 2: Create `assets/js/mode.js`**

```js
// ABOUTME: Light/dark toggle: binds the nav's #mode-toggle button, persists the override in localStorage,
// ABOUTME: and keeps the button label naming the mode you'd switch to (labels arrive via data-label-* attributes).
(function () {
    var root = document.documentElement;
    var btn = document.getElementById("mode-toggle");
    if (!btn) {
        return;
    }
    var media = window.matchMedia("(prefers-color-scheme: dark)");

    function effectiveMode() {
        if (root.dataset.mode === "dark" || root.dataset.mode === "light") {
            return root.dataset.mode;
        }
        return media.matches ? "dark" : "light";
    }

    function renderLabel() {
        var next = effectiveMode() === "dark" ? "light" : "dark";
        var label = next === "dark" ? btn.dataset.labelDark : btn.dataset.labelLight;
        btn.textContent = "◐ " + label;
    }

    btn.addEventListener("click", function () {
        var next = effectiveMode() === "dark" ? "light" : "dark";
        root.dataset.mode = next;
        try {
            localStorage.setItem("mode", next);
        } catch (e) {
            /* private browsing: the override just won't persist */
        }
        renderLabel();
    });

    if (typeof media.addEventListener === "function") {
        media.addEventListener("change", renderLabel);
    }
    renderLabel();
})();
```

- [ ] **Step 3: Delete the dead ThemeManager**

```bash
git rm assets/js/theme.js
```

- [ ] **Step 4: Load `mode-init.js` from `layouts/partials/head/javascript.html`**

Replace the file's full contents with:

```html
{{ with resources.Get "js/mode-init.js" }}
    {{ $init := . | minify | resources.Fingerprint "sha512" }}
<script
    src="{{ $init.RelPermalink }}"
    integrity="{{ $init.Data.Integrity }}"
></script>
{{ end }}
{{ with .Site.Params.customjs }}
    {{ $js := slice }}
    {{- range . -}}
        {{ with (resources.Get .) }}
            {{ $js = $js | append . }}
        {{ else }}
            {{ warnf "Missing JavaScript resource: %s" . }}
        {{ end }}
    {{- end -}}
    {{ $bundle := resources.Concat "js/bundle.js" $js | minify }}
    {{ $minJS := $bundle | resources.Fingerprint "sha512" }}
<script
    src="{{ $minJS.RelPermalink }}"
    integrity="{{ $minJS.Data.Integrity }}"
    defer
></script>
{{ end }}
```
(The init script deliberately has **no `defer`** — it must run before first paint. It stays inside this partial, which `baseof.html` already includes in `<head>`.)

- [ ] **Step 5: Update `customjs` in `config/_default/params.toml`**

```toml
customjs = ["/js/bluesky_comments.js", "/js/mode.js", "/js/image-loading.js"]
```

- [ ] **Step 6: Append the toggle button to `layouts/partials/nav.html`**

Add after the `.nav-rss` anchor (end of file):

```html
<button
    id="mode-toggle"
    type="button"
    aria-label="{{ i18n "mode-toggle-aria" | default "Toggle dark mode" }}"
    data-label-dark="{{ i18n "mode-dark" | default "dark" }}"
    data-label-light="{{ i18n "mode-light" | default "light" }}"
>◐</button>
```

- [ ] **Step 7: Append the three mode keys to all six i18n files**

`i18n/en.yaml`:
```yaml

- id: mode-dark
  translation: "dark"

- id: mode-light
  translation: "light"

- id: mode-toggle-aria
  translation: "Toggle dark mode"
```
`i18n/ja.yaml`:
```yaml

- id: mode-dark
  translation: "ダーク"

- id: mode-light
  translation: "ライト"

- id: mode-toggle-aria
  translation: "ダークモード切り替え"
```
`i18n/es.yaml`:
```yaml

- id: mode-dark
  translation: "oscuro"

- id: mode-light
  translation: "claro"

- id: mode-toggle-aria
  translation: "Cambiar modo oscuro"
```
`i18n/ko.yaml`:
```yaml

- id: mode-dark
  translation: "다크"

- id: mode-light
  translation: "라이트"

- id: mode-toggle-aria
  translation: "다크 모드 전환"
```
`i18n/zh.yaml`:
```yaml

- id: mode-dark
  translation: "深色"

- id: mode-light
  translation: "浅色"

- id: mode-toggle-aria
  translation: "切换深色模式"
```
`i18n/id.yaml`:
```yaml

- id: mode-dark
  translation: "gelap"

- id: mode-light
  translation: "terang"

- id: mode-toggle-aria
  translation: "Ganti mode gelap"
```

- [ ] **Step 8: Verify build + wiring**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir 2>&1 | grep -i "warn\|error"; echo "exit ok"
grep -o 'src="/js/mode-init[^"]*"' /tmp/design4-check/index.html
grep -o 'id="mode-toggle"' /tmp/design4-check/index.html
grep -c "defer" /tmp/design4-check/index.html
grep -o "mode-toggle" /tmp/design4-check/js/bundle*.js | head -1
grep -rn "theme\.js" config/ layouts/
```
Expected: no warnings (theme.js reference removed); mode-init script tag present WITHOUT defer (manually eyeball the tag); `id="mode-toggle"` present; bundle contains `mode-toggle`; final grep returns nothing.

- [ ] **Step 9: Commit**

```bash
git add assets/js/mode-init.js assets/js/mode.js layouts/partials/head/javascript.html layouts/partials/nav.html config/_default/params.toml i18n/en.yaml i18n/ja.yaml i18n/es.yaml i18n/ko.yaml i18n/zh.yaml i18n/id.yaml
git commit -m "feat(design): system+override dark mode with CSP-safe pre-paint guard"
```

---

### Task 5: Theme port (25 themes → sextet overrides)

**Files:**
- Rewrite: `assets/css/themes.css`
- Modify: `config/_default/params.toml` (theme param, line 29)
- Delete: `layouts/partials/theme-chooser.html`

**Interfaces:**
- Consumes: tokens + selector model from Task 1.
- Produces: `html.theme-<name>` overrides for all 25 themes; default theme `paper` (class present, intentionally rule-less).

- [ ] **Step 1: Set the default theme in `config/_default/params.toml`**

Change line 29 ` theme = "academia"` to:
```toml
theme = "paper"
```
(Leave the commented-out theme lines above it — they're the menu of options.)

- [ ] **Step 2: Delete the dead chooser partial**

```bash
git rm layouts/partials/theme-chooser.html
```

- [ ] **Step 3: Rewrite `assets/css/themes.css`**

Structure: a 2-line ABOUTME header, one shared derivation rule, then 25 theme blocks. Every theme block follows this exact 3-selector template (the dark values repeat once for the manual override and once for the system path — same duplication the paper palette uses):

```css
html.theme-NAME {
    --bg: #LIGHT-BG;
    --bg2: #LIGHT-BG2;
    --ink: #LIGHT-INK;
    --accent: #LIGHT-ACCENT;
}

html.theme-NAME[data-mode="dark"] {
    --bg: #DARK-BG;
    --bg2: #DARK-BG2;
    --ink: #DARK-INK;
    --accent: #DARK-ACCENT;
}

@media (prefers-color-scheme: dark) {
    html.theme-NAME:not([data-mode="light"]) {
        --bg: #DARK-BG;
        --bg2: #DARK-BG2;
        --ink: #DARK-INK;
        --accent: #DARK-ACCENT;
    }
}
```

File header + shared rule (paste verbatim at the top):

```css
/* ABOUTME: 25 named theme palettes ported to the design4 six-token model (bg/bg2/ink/accent set per theme). */
/* ABOUTME: paper = the bare :root palette in tokens.css — .theme-paper intentionally has no rules. --mut/--line derive below. */

/* Derived neutrals for every ported theme. paper keeps its hand-picked literals from tokens.css.
   Specificity (0,2,1) so this also beats paper's dark-mode literals when a theme class is present. */
html[class*="theme-"]:not(.theme-paper) {
    --mut: color-mix(in srgb, var(--ink) 55%, var(--bg));
    --line: color-mix(in srgb, var(--ink) 13%, var(--bg));
}
```

Value table — transcribe each row into the template above (light `--bg/--bg2/--ink/--accent`, then dark ditto). These are the old file's `--color-light/--color-tertiary/--color-primary/--color-link` per theme:

| theme | L bg | L bg2 | L ink | L accent | D bg | D bg2 | D ink | D accent |
|---|---|---|---|---|---|---|---|---|
| dark | #181a20 | #2a2d37 | #e2e2e2 | #60a5fa | #181a20 | #2a2d37 | #e2e2e2 | #60a5fa |
| nature | #f8f9f6 | #e6ede8 | #2c392f | #2d5a3a | #2c392f | #3d4a41 | #e6ede8 | #7ec090 |
| sunset | #fdf6f0 | #fae8e1 | #2b1b2c | #c94960 | #2b1b2c | #3d2a3e | #fae8e1 | #ff7b91 |
| ocean | #f0f7fa | #e1f0f4 | #1b2b32 | #167885 | #1b2b32 | #2a3d45 | #e1f0f4 | #45c1d4 |
| desert | #faf6f0 | #f2e6d9 | #2c261e | #9b6547 | #2c261e | #3d362f | #f2e6d9 | #e39b73 |
| nordic | #f7f7f9 | #e8eaf0 | #272932 | #3d4a6b | #272932 | #373b45 | #e8eaf0 | #95a3c0 |
| autumn | #fdf7f5 | #f6e6e0 | #2d1810 | #d35f2a | #2d1810 | #3d2720 | #f6e6e0 | #ff7b42 |
| cyber | #f0fbff | #e0f7ff | #0c1f2c | #009c60 | #0c1f2c | #162d3a | #e0f7ff | #00ff9d |
| academia | #f4f1ea | #e8e4d9 | #2b2821 | #6b3000 | #2b2821 | #3d3a32 | #e8e4d9 | #e88033 |
| myspace | #ffffff | #cccccc | #000000 | #0066ff | #000000 | #333333 | #ffffff | #66b3ff |
| halloween | #f4f1de | #4a2800 | #ff6b1a | #ff8c00 | #1a1a1a | #663300 | #ff944d | #ffaa4d |
| neon | #f8f8ff | #e6fff5 | #1a1b2e | #00ff95 | #1a1b2e | #2d2f4d | #e6fff5 | #00ff95 |
| electric | #f9f9ff | #ffe8e0 | #0c0c2b | #ff3d00 | #0c0c2b | #1a1a4d | #ffe8e0 | #ff3d00 |
| cyberpunk | #fcf9ff | #e0ffff | #150b29 | #00ffff | #150b29 | #2b1652 | #e0ffff | #00ffff |
| volcano | #fff9f9 | #ffe6dd | #1f0f0f | #ff4400 | #1f0f0f | #3d1f1f | #ffe6dd | #ff4400 |
| midnight | #f0f4f8 | #e0e8f0 | #0d1b2a | #1a5fb4 | #0d1b2a | #1b2d44 | #e0e8f0 | #62a0ff |
| lavender | #f8f5fc | #ede6f5 | #2d2640 | #6b4d9e | #2d2640 | #3d3555 | #ede6f5 | #c4a6e8 |
| coffee | #faf5f0 | #f0e6dc | #2c1810 | #6b4226 | #2c1810 | #3d2820 | #f0e6dc | #d4a882 |
| mint | #f2faf7 | #e0f5ed | #1a3028 | #1d7a55 | #1a3028 | #2a4038 | #e0f5ed | #6be8b8 |
| coral | #fff8f5 | #ffe8e2 | #2d1a1a | #c9503c | #2d1a1a | #3d2828 | #ffe8e2 | #ff9a8a |
| synthwave | #fdf0ff | #f5e0f8 | #1a1030 | #d41872 | #1a1030 | #2d1850 | #f5e0f8 | #ff6b9d |
| terminal | #f0fff0 | #d8f8d8 | #0a0a0a | #008800 | #0a0a0a | #1a1a1a | #d8f8d8 | #00ff00 |
| solarized | #fdf6e3 | #eee8d5 | #073642 | #2075a8 | #002b36 | #073642 | #eee8d5 | #2aa198 |
| dracula | #f8f8f2 | #44475a | #282a36 | #8054d0 | #282a36 | #44475a | #f8f8f2 | #bd93f9 |
| bubblegum | #fff5fa | #ffe0ef | #3d1a2e | #c9306a | #3d1a2e | #4d2a3e | #ffe0ef | #ff8cc8 |

Worked examples — the first three blocks of the file, verbatim (then continue alphabetically-as-tabled for the other 22):

```css
/* dark is always-dark: identical values in all three slots so it wins over paper's dark literals in every mode */
html.theme-dark {
    --bg: #181a20;
    --bg2: #2a2d37;
    --ink: #e2e2e2;
    --accent: #60a5fa;
}

html.theme-dark[data-mode="dark"] {
    --bg: #181a20;
    --bg2: #2a2d37;
    --ink: #e2e2e2;
    --accent: #60a5fa;
}

@media (prefers-color-scheme: dark) {
    html.theme-dark:not([data-mode="light"]) {
        --bg: #181a20;
        --bg2: #2a2d37;
        --ink: #e2e2e2;
        --accent: #60a5fa;
    }
}

html.theme-nature {
    --bg: #f8f9f6;
    --bg2: #e6ede8;
    --ink: #2c392f;
    --accent: #2d5a3a;
}

html.theme-nature[data-mode="dark"] {
    --bg: #2c392f;
    --bg2: #3d4a41;
    --ink: #e6ede8;
    --accent: #7ec090;
}

@media (prefers-color-scheme: dark) {
    html.theme-nature:not([data-mode="light"]) {
        --bg: #2c392f;
        --bg2: #3d4a41;
        --ink: #e6ede8;
        --accent: #7ec090;
    }
}

/* halloween's light palette is intentionally loud (orange ink, dark-brown bg2) — port preserves its character */
html.theme-halloween {
    --bg: #f4f1de;
    --bg2: #4a2800;
    --ink: #ff6b1a;
    --accent: #ff8c00;
}

html.theme-halloween[data-mode="dark"] {
    --bg: #1a1a1a;
    --bg2: #663300;
    --ink: #ff944d;
    --accent: #ffaa4d;
}

@media (prefers-color-scheme: dark) {
    html.theme-halloween:not([data-mode="light"]) {
        --bg: #1a1a1a;
        --bg2: #663300;
        --ink: #ff944d;
        --accent: #ffaa4d;
    }
}
```

- [ ] **Step 4: Verify block count and selection**

Run:
```bash
grep -c "^html\.theme-" assets/css/themes.css
grep -c "html\.theme-.*:not(\[data-mode" assets/css/themes.css
grep -rn -- "--color-" assets/css/themes.css
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -o 'class="theme-paper"' /tmp/design4-check/index.html
HUGO_RANDOM_THEME=dracula hugo --destination /tmp/design4-theme-check --cleanDestinationDir
grep -o 'class="theme-dracula"' /tmp/design4-theme-check/index.html
```
Expected: 50 (`html.theme-` at line start: 25 base + 25 `[data-mode]`), 25 (media-path selectors), zero `--color-` refs, both class greps match.

- [ ] **Step 5: Commit**

```bash
git add assets/css/themes.css config/_default/params.toml
git commit -m "feat(design): port all 25 themes to the six-token model, default to paper"
```

---

### Task 6: Home page

**Files:**
- Rewrite: `layouts/index.html`
- Modify: `content/_index.md`, `content/_index.ja.md`, `content/_index.es.md`, `content/_index.ko.md`, `content/_index.zh.md`, `content/_index.id.md` (body only — **frontmatter untouched**)
- Modify: `config/_default/languages.toml` (`[en.params]` block)

**Interfaces:**
- Consumes: `.home-intro`, `.section-label`, `.more-link`, date-row styles (Task 2).
- Produces: `dateFormat = "02 Jan 06"` for English (all templates already read `.Site.Params.dateFormat` with an ISO fallback — other languages keep ISO).

- [ ] **Step 1: Add the English date format**

In `config/_default/languages.toml`, extend the `[en.params]` block (keep its existing lines):

```toml
[en.params]
description = "Some writing by Harper Reed. Mostly about technology, politics, and things"
subtitle = "Musing from a normal person doing normal things"
dateFormat = "02 Jan 06"
```

- [ ] **Step 2: Rewrite `layouts/index.html`**

```html
{{ define "main" }}
<div class="home-intro">{{ .Content }}</div>

{{ $posts := first 5 (where .Site.RegularPages "Section" "post") }}
{{ if $posts }}
<h2 class="section-label">{{ i18n "posts" | default "Posts" }}</h2>
<ul class="blog-posts">
    {{ range $posts }}
    <li>
        <span>
            <time datetime='{{ .Date.Format "2006-01-02" }}' aria-label="Date: {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}">
                {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
            </time>
        </span>
        {{ if .Params.link }}
        <a href="{{ .Params.link }}" target="_blank" rel="noopener noreferrer" aria-label="Link to {{ .Title }}">
            {{ .Title }} ↪
        </a>
        {{ else }}
        <a href="{{ .RelPermalink }}" title="{{ .Summary }}" aria-label="Link to {{ .Title }}">
            {{ .Title }}
        </a>
        {{ end }}
    </li>
    {{ else }}
    <li>{{ i18n "no-posts" }}</li>
    {{ end }}
</ul>
<a class="more-link" href="{{ "/posts" | relLangURL }}" aria-label="More Posts">{{ i18n "morePosts" | default "More Posts" }} →</a>
{{ end }}

{{ $notes := first 5 (where .Site.RegularPages "Section" "notes") }}
{{ if $notes }}
<h2 class="section-label">{{ i18n "notes" | default "Notes" }}</h2>
<ul class="blog-posts" aria-label="List of recent notes">
    {{ range $notes }}
    <li>
        <span>
            <time datetime='{{ .Date.Format "2006-01-02" }}' aria-label="Date: {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}">
                {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
            </time>
        </span>
        <a href="{{ .RelPermalink }}" aria-label="Note: {{ .Description | default .Title }}">
            {{ .Description | default .Title | truncate 120 }}
        </a>
    </li>
    {{ else }}
    <li>{{ i18n "no-notes" | default "No notes yet." }}</li>
    {{ end }}
</ul>
<a class="more-link" href="{{ "/notes" | relLangURL }}" aria-label="More Notes">{{ i18n "moreNotes" | default "More Notes" }} →</a>
{{ end }}
{{ end }}
```

- [ ] **Step 3: Restructure the six home bodies (heading → lead paragraph; copy verbatim otherwise)**

Only the body below the frontmatter `---` changes; **do not touch any frontmatter**, and keep the `{{</* lang */>}}` shortcode where it exists today (es, ko).

`content/_index.md` body:
```markdown
My name is Harper Reed, and this is my blog. If you want to know more about me, visit my website: [harper.lol](https://harper.lol).

Here you will find longer form [blog posts](/posts), some short form [notes](/notes), and occasionally some [links](/links) I find interesting. You can find out what I am up to [Now](/now) and you can subscribe to my [RSS feed](/index.xml).
```

`content/_index.ja.md` body:
```markdown
ハーパー・リードと申します。こちらは私のブログです。

私についてもっと知りたい方は、ウェブサイト『[harper.lol](https://harper.lol)』をご覧ください。

このブログでは、長めの[ブログ記事](/ja/posts)、短めの[メモ](/notes)、そしてときどき私が面白いと思った[リンク](/media/links)を掲載しています。近況は[Now](/now)ページでご確認いただけるほか、[RSSフィード](/ja/index.xml)を購読することもできます。
```

`content/_index.es.md` body:
```markdown
Me llamo Harper Reed y este es mi blog. Si deseas saber más sobre mí, visita mi sitio web: [harper.lol](https://harper.lol).

Aquí encontrarás [entradas](/es/posts) más extensas, [notas](/notes) breves y de vez en cuando [enlaces](/links) que me resultan interesantes. Puedes ver en qué estoy ahora en la sección «[Now](/now)» y suscribirte a mi [canal RSS](/es/index.xml).

{{</* lang */>}}
```
(Write the shortcode without the `/*`-`*/` — that escaping only exists so this plan doesn't execute it.)

`content/_index.ko.md` body:
```markdown
제 이름은 Harper Reed입니다. 이곳은 제 블로그입니다.

저에 대해 더 알고 싶으시면 제 웹사이트 [harper.lol](https://harper.lol)을 방문해 주십시오.

여기에서는 장문의(롱폼) [블로그 포스트](/ko/posts), 짧은(숏폼) [노트](/notes), 그리고 가끔 제가 흥미롭게 찾은 [링크](/links)를 읽으실 수 있습니다. 제가 요즘 무엇을 하고 있는지는 [‘Now’ 페이지](/now)에서 확인하실 수 있으며, [RSS 피드](/ko/index.xml)를 구독하실 수도 있습니다.

{{</* lang */>}}
```
(Same shortcode-escaping note as above.)

`content/_index.zh.md` body:
```markdown
大家好，我是 Harper Reed，这是我的博客。想更了解我，请访问我的个人网站：[harper.lol](https://harper.lol)。

在这里，你可以看到一些长篇[博文](/zh/posts)、一些简短[笔记](/notes)，以及我偶尔分享的有趣[链接](/links)。想知道我现在在做什么，可以查看[Now](/now)页面，并订阅我的[RSS 订阅源](/zh/index.xml)。
```

`content/_index.id.md` body:
```markdown
Nama saya Harper Reed, dan ini adalah blog saya. Jika Anda ingin tahu lebih banyak tentang saya, silakan kunjungi situs web saya: [harper.lol](https://harper.lol).

Di sini Anda akan menemukan artikel blog berformat panjang, sejumlah catatan ringkas, dan sesekali tautan yang saya anggap menarik. Anda juga dapat mengetahui apa yang sedang saya kerjakan di halaman [Now](/now) serta berlangganan [umpan RSS](/id/index.xml) saya.
```

- [ ] **Step 4: Verify build + rendered home**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -c "home-intro" /tmp/design4-check/index.html
grep -c "section-label" /tmp/design4-check/index.html
grep -c "more-link" /tmp/design4-check/index.html
grep -o "<h3[^>]*>My name is Harper" /tmp/design4-check/index.html
grep -oE '[0-9]{2} [A-Z][a-z]{2} [0-9]{2}' /tmp/design4-check/index.html | head -2
grep -oE '20[0-9]{2}-[0-9]{2}-[0-9]{2}' /tmp/design4-check/ja/index.html | head -2
```
Expected: home-intro 1, section-label 2, more-link 2; the `<h3>` grep is EMPTY (heading became a paragraph); English dates render like `05 Jan 26`; Japanese dates stay ISO.

- [ ] **Step 5: Commit**

```bash
git add layouts/index.html content/_index.md content/_index.ja.md content/_index.es.md content/_index.ko.md content/_index.zh.md content/_index.id.md config/_default/languages.toml
git commit -m "feat(design): design4 home - lead intro, section labels, date rows, en date format"
```

---

### Task 7: Post page (kicker + quiet notice styles)

**Files:**
- Modify: `layouts/post/single.html` (add kicker), `layouts/partials/related-posts.html` (date format param)
- Rewrite: `assets/css/code.css`, `assets/css/ai-disclosure.css`, `assets/css/outofdate.css`, `assets/css/translations.css`, `assets/css/bsky_comments.css`
- No changes: `assets/css/tinylytics.css`, `assets/css/image-loading.css` (already token-free — verify only)

**Interfaces:**
- Consumes: `.kicker`, `.byline`, related-posts date-row styles (Task 2); `posts` i18n key (exists).
- Produces: nothing new for later tasks.

- [ ] **Step 1: Add the kicker to `layouts/post/single.html`**

Change the opening of the `main` block from:
```html
{{ if not .Params.menu }}
<h1>{{ .Title }}</h1>
```
to:
```html
{{ if not .Params.menu }}
<p class="kicker">{{ i18n "posts" | default "Posts" }}</p>
<h1>{{ .Title }}</h1>
```
(Everything else in the file — byline, partial calls — stays exactly as is.)

- [ ] **Step 2: Use the sitewide date format in `layouts/partials/related-posts.html`**

Change:
```html
        <time datetime="{{ .Date.Format "2006-01-02" }}" class="related-post-date">
          {{ .Date.Format "2006-01-02" }}
        </time>
```
to:
```html
        <time datetime="{{ .Date.Format "2006-01-02" }}" class="related-post-date">
          {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
        </time>
```

- [ ] **Step 3: Rewrite `assets/css/code.css`**

```css
/* ABOUTME: Inline code and code blocks on the bg2 surface with hairline borders (design4). */
/* ABOUTME: Chroma token colors come from bearcub's syntax.css, which loads after this file. */

code {
    font-family: var(--font-mono);
    font-size: 0.85em;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: var(--radius-thumb);
    padding: 0.1em 0.35em;
}

pre {
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: var(--radius-code);
    padding: 16px 20px;
    overflow-x: auto;
    font-size: 14px;
    line-height: 1.6;
    margin: 28px 0;
}

pre code {
    background: none;
    border: none;
    padding: 0;
    font-size: inherit;
}
```

- [ ] **Step 4: Rewrite `assets/css/ai-disclosure.css`**

```css
/* ABOUTME: AI/human authorship notice as a quiet muted italic line (design4 — no box). */

.ai-disclosure {
    margin-top: 40px;
    font-size: 13px;
    font-style: italic;
    color: var(--mut);
}

.ai-disclosure p {
    margin: 0;
}
```

- [ ] **Step 5: Rewrite `assets/css/outofdate.css`**

```css
/* ABOUTME: Old-post warning as a quiet hairline-left note (design4). */

.outofdate-warning {
    margin: 24px 0;
    padding: 2px 0 2px 20px;
    border-left: 3px solid var(--line);
    font-size: 14px;
    line-height: 1.6;
    color: var(--mut);
}

.outofdate-warning p {
    margin: 0;
}
```

- [ ] **Step 6: Rewrite `assets/css/translations.css`**

```css
/* ABOUTME: Available-translations notice as a quiet hairline-left note (design4). */

.post-translations-box {
    margin: 24px 0;
    padding: 2px 0 2px 20px;
    border-left: 3px solid var(--line);
    font-size: 14px;
    line-height: 1.6;
    color: var(--mut);
}

.post-translations-box p {
    margin: 0;
}

.post-translations-box a {
    color: var(--accent);
}
```

- [ ] **Step 7: Rewrite `assets/css/bsky_comments.css`**

```css
/* ABOUTME: Bluesky comments (rendered by bluesky_comments.js) restyled on the design4 tokens. */

.comment {
    padding: 10px 0;
}

.author {
    font-weight: bold;
}

.avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    vertical-align: middle;
    margin-right: 8px;
}

.nested-replies {
    margin-left: 20px;
    padding-left: 10px;
}

.actions {
    font-size: 12px;
    color: var(--mut);
}

.nested-replies .comment {
    margin-bottom: 0;
}

.bsky-comments-container {
    max-width: 100%;
    margin: 1rem 0;
}

.bsky-meta {
    margin: 1rem 0;
    font-size: 0.9rem;
    color: var(--mut);
}

.bsky-meta a {
    color: var(--mut);
    text-decoration: none;
}

.bsky-meta a:hover {
    text-decoration: underline;
}

.bsky-comment {
    padding: 1rem 0;
    border-bottom: 1px solid var(--line);
}

.bsky-comment:last-child {
    border-bottom: none;
}

.bsky-author {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.bsky-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    object-fit: cover;
}

.bsky-author a {
    color: var(--ink);
    text-decoration: none;
    font-weight: 500;
}

.bsky-author a:hover {
    text-decoration: underline;
}

.bsky-handle {
    color: var(--mut);
    font-size: 0.9rem;
}

.bsky-content {
    margin: 0.5rem 0;
    line-height: 1.5;
    word-wrap: break-word;
}

.bsky-actions {
    margin-top: 0.5rem;
    font-size: 0.9rem;
    color: var(--mut);
}

.bsky-nested-replies {
    margin-left: 2rem;
    border-left: 2px solid var(--line);
    padding-left: 1rem;
}

/* Error state keeps literal reds: it must read as an error in any theme/mode. */
.bsky-error {
    color: #dc2626;
    padding: 1rem;
    background-color: #fef2f2;
    border-radius: var(--radius-thumb);
    margin: 1rem 0;
}
```
(Deliberate deltas from the old file: the `:root { --font-system }` block and the container's `font-family` are gone — the body font cascades; author links are `--ink`, meta/handles/actions `--mut`, borders `--line`.)

- [ ] **Step 8: Verify token-free status of the two untouched files, then build**

Run:
```bash
grep -n -- "--color-\|--font-system" assets/css/tinylytics.css assets/css/image-loading.css assets/css/code.css assets/css/ai-disclosure.css assets/css/outofdate.css assets/css/translations.css assets/css/bsky_comments.css
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -o 'class="kicker"' /tmp/design4-check/2026/01/05/claude-code-is-better-on-your-phone/index.html || grep -rlo 'class="kicker"' /tmp/design4-check/2026 | head -1
```
Expected: first grep empty; build clean; kicker present on a post page. Visual check for code blocks happens in Task 11 — if bearcub's `syntax.css` (last in bundle) paints its own `pre` background over `--bg2`, the fix is to move `"syntax.css"` directly before `"/css/code.css"` in `customcss` (note it in the Task 11 findings if applied).

- [ ] **Step 9: Commit**

```bash
git add layouts/post/single.html layouts/partials/related-posts.html assets/css/code.css assets/css/ai-disclosure.css assets/css/outofdate.css assets/css/translations.css assets/css/bsky_comments.css
git commit -m "feat(design): design4 post page - kicker, quiet notices, tokenized code and comments"
```

---

### Task 8: Notes

**Files:**
- Rewrite: `layouts/notes/list.html`, `assets/css/notes.css`, `assets/css/notes-grid.css`
- Modify: `layouts/notes/single.html` (h1 class)

**Interfaces:**
- Consumes: tokens; `.filter-notice`, `.byline`, pagination styles (Task 2).
- Produces: `.note-row`, `.note-date`, `.note-body`, `.note-meta`, `.note-title` classes (used only within notes).

- [ ] **Step 1: Rewrite `layouts/notes/list.html`**

```html
{{ define "main" }}
<article>
    {{ .Content }} {{ if .Data.Singular }}
    <p class="filter-notice">{{ i18n "filtering-for" }} "{{ .Title }}"</p>
    {{ end }}
    <div class="notes">
        {{ $paginator := .Paginate .Pages (.Param "notes_pagination" | default 2) }}
        {{ range $paginator.Pages }}
        <article class="note-row">
            <a class="note-date" href="{{ .RelPermalink }}" title="{{ i18n "permalink-note-title" | default "Permalink to this note" }}">
                <time datetime='{{ .Date.Format "2006-01-02" }}' aria-label="Date: {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}">
                    {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
                </time>
            </a>
            <div class="note-body">
                {{ if .Params.text }} {{ .Params.text | markdownify }} {{ else }} {{ .Content }} {{ end }}
                {{ with .Resources.ByType "image" }}
                <div class="note-images">
                    {{ range . }}
                    {{ $thumbnail := .Resize "600x" }}
                    <img
                        src="{{ $thumbnail.RelPermalink }}"
                        alt="{{ .Title }}"
                        loading="lazy"
                        width="{{ $thumbnail.Width }}"
                        height="{{ $thumbnail.Height }}"
                    />
                    {{ end }}
                </div>
                {{ end }}
                <div class="note-meta">
                    {{ if .Params.tags }} {{ range .Params.tags }}
                    <a class="blog-tags" href="/tags/{{ . }}">#{{ . }}</a>
                    {{ end }} {{ end }}
                    <button class="tinylytics_kudos" data-path="{{ .RelPermalink }}"></button>
                </div>
            </div>
        </article>
        {{ else }}
        <p>{{ i18n "no-notes" | default "No notes yet." }}</p>
        {{ end }}
    </div>

    {{ partial "pagination.html" . }}
</article>
{{ end }}
```
(Deliberate deltas: hardcoded `Jan 02, 2006` becomes the sitewide `dateFormat` param; the `#` permalink is folded into the date link; the per-note `<hr />` is replaced by the row's border-bottom; kudos and tags keep their functions.)

- [ ] **Step 2: Add the h1 class in `layouts/notes/single.html`**

Change line 2 from:
```html
<h1>{{ .Title }}</h1>
```
to:
```html
<h1 class="note-title">{{ .Title }}</h1>
```
(Nothing else in the file changes.)

- [ ] **Step 3: Rewrite `assets/css/notes.css`**

```css
/* ABOUTME: Notes section: date-column rows with 3-up image thumbnails on the list, 28px titles on singles. */

.note-row {
    display: flex;
    gap: 20px;
    padding: 18px 0;
    border-bottom: 1px solid var(--line);
}

.note-row:last-child {
    border-bottom: none;
}

.note-date {
    flex: none;
    width: 88px;
    font-size: 14px;
    color: var(--mut);
    font-variant-numeric: tabular-nums;
    text-decoration: none;
    line-height: 1.6;
}

.note-date:hover {
    color: var(--accent);
}

.note-body {
    flex: 1;
    min-width: 0;
    font-size: 16px;
    line-height: 1.6;
}

.note-body p {
    margin: 0 0 10px;
}

.note-body p:last-child {
    margin-bottom: 0;
}

.note-images {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-top: 12px;
}

.note-images img {
    width: 100%;
    height: 110px;
    object-fit: cover;
    border-radius: var(--radius-thumb);
}

.note-meta {
    margin-top: 10px;
    font-size: 13px;
    color: var(--mut);
}

/* single note page */
.note-title {
    font-size: 28px;
}

article > .note-images {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin: 20px 0;
}

article > .note-images img {
    border-radius: var(--radius-thumb);
}

@media (max-width: 640px) {
    .note-row {
        flex-direction: column;
        gap: 4px;
    }

    .note-date {
        width: auto;
        font-size: 13px;
    }

    .note-images img {
        height: 90px;
    }
}
```

- [ ] **Step 4: Rewrite `assets/css/notes-grid.css`**

```css
/* ABOUTME: Masonry photo grid for the notes grid view (notes/notes-grid layout). */

.masonry-columns {
    column-count: 3;
    column-gap: 12px;
}

.masonry-item {
    break-inside: avoid;
    margin-bottom: 12px;
}

.masonry-item img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: var(--radius-thumb);
}

.masonry-item a:hover img {
    opacity: 0.9;
}

@media (max-width: 900px) {
    .masonry-columns {
        column-count: 2;
    }
}

@media (max-width: 600px) {
    .masonry-columns {
        column-count: 1;
    }
}
```

- [ ] **Step 5: Verify build + rendered notes**

Run:
```bash
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -c "note-row" /tmp/design4-check/notes/index.html
grep -c "note-date" /tmp/design4-check/notes/index.html
grep -c "tinylytics_kudos" /tmp/design4-check/notes/index.html
grep -o "Jan 02, 2006\|[A-Z][a-z]\{2\} [0-9]\{2\}, 20[0-9]\{2\}" /tmp/design4-check/notes/index.html | head -3
grep -rn -- "--color-\|--border-radius\|--margin" assets/css/notes.css assets/css/notes-grid.css
```
Expected: note-row/note-date counts equal (one per note, ~10); kudos count matches; the old `Jan 02, 2006`-style dates are GONE (empty grep); final grep empty.

- [ ] **Step 6: Commit**

```bash
git add layouts/notes/list.html layouts/notes/single.html assets/css/notes.css assets/css/notes-grid.css
git commit -m "feat(design): design4 notes - date-column rows, thumbnail grid, tokenized masonry"
```

---

### Task 9: Books & music grids

**Files:**
- Rewrite: `assets/css/books.css`, `assets/css/music.css`
- No template changes (`books/books-grid.html`, `music/music-grid.html`, list/single templates all keep their markup; date-row lists are already styled by base.css).

**Interfaces:**
- Consumes: tokens; date-row/domain styles (Task 2).
- Markup being styled (from the grid templates): `.year-section > .year-heading + .book-grid > .book-grid-item > (.book-bg img, .book-link > .book-info > .book-title + .book-author)`; music adds `.month-section > .month-heading + .music-grid > .music-grid-item > (.album-bg img, .music-link > .music-info > .music-title + .music-artist)`. `books/single.html` uses `.book-cover`, `.reread-note`, `.related-reads`.

- [ ] **Step 1: Rewrite `assets/css/books.css`**

```css
/* ABOUTME: Books section: cover grid (books-grid layout) and single-page cover/meta styling. */
/* ABOUTME: The /books date-row list is styled by the shared pattern in base.css. */

.year-heading,
.month-heading {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--mut);
    margin: 46px 0 14px;
}

.book-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 18px;
}

.book-grid-item {
    position: relative;
    aspect-ratio: 2 / 3;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: var(--radius-thumb);
    overflow: hidden;
    transition: transform 0.15s ease;
}

.book-grid-item:hover {
    transform: translateY(-4px);
}

.book-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.book-link {
    text-decoration: none;
}

.book-info {
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    padding: 8px 10px;
    background: color-mix(in srgb, var(--bg) 88%, transparent);
    -webkit-backdrop-filter: blur(2px);
    backdrop-filter: blur(2px);
}

.book-title {
    font-size: 13px;
    font-weight: 600;
    line-height: 1.3;
    color: var(--ink);
    margin: 0;
}

.book-author {
    font-size: 12px;
    color: var(--mut);
    margin: 2px 0 0;
}

/* single book page */
.book-cover {
    max-width: 220px;
    border-radius: var(--radius-thumb);
    border: 1px solid var(--line);
}

.reread-note,
.related-reads {
    font-size: 14px;
    color: var(--mut);
}

@media (prefers-reduced-motion: reduce) {
    .book-grid-item,
    .book-grid-item:hover {
        transition: none;
        transform: none;
    }
}
```

- [ ] **Step 2: Rewrite `assets/css/music.css`**

```css
/* ABOUTME: Music section: album-art grid (music-grid layout) with month/year group headings. */
/* ABOUTME: The /music date-row list is styled by the shared pattern in base.css; heading styles live in books.css. */

.month-section {
    margin-bottom: 8px;
}

.music-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 18px;
}

.music-grid-item {
    position: relative;
    aspect-ratio: 1 / 1;
    background: var(--bg2);
    border: 1px solid var(--line);
    border-radius: var(--radius-thumb);
    overflow: hidden;
    transition: transform 0.15s ease;
}

.music-grid-item:hover {
    transform: translateY(-4px);
}

.album-bg {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.music-link {
    text-decoration: none;
}

.music-info {
    position: absolute;
    right: 0;
    bottom: 0;
    left: 0;
    padding: 8px 10px;
    background: color-mix(in srgb, var(--bg) 88%, transparent);
    -webkit-backdrop-filter: blur(2px);
    backdrop-filter: blur(2px);
}

.music-title {
    font-size: 13px;
    font-weight: 600;
    line-height: 1.3;
    color: var(--ink);
    margin: 0;
}

.music-artist {
    font-size: 12px;
    color: var(--mut);
    margin: 2px 0 0;
}

@media (prefers-reduced-motion: reduce) {
    .music-grid-item,
    .music-grid-item:hover {
        transition: none;
        transform: none;
    }
}
```
(Note: `.music-info .music-title` is an `h3` inside `main` — the base `h3` margin is overridden by the explicit `margin: 0` here. Same for `.book-title`.)

- [ ] **Step 3: Verify build + no stale tokens or hardcoded colors**

Run:
```bash
grep -n -- "--color-\|#fff\b\|#555\|#ddd\|rgba(" assets/css/books.css assets/css/music.css
grep -n "composes:" assets/css/*.css
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -c "book-grid-item" /tmp/design4-check/media/books/grid/index.html 2>/dev/null || grep -rlc "book-grid-item" /tmp/design4-check --include="*.html" | head -3
```
Expected: first two greps empty (no legacy tokens, no hardcoded grays/whites, no dead `composes:` anywhere); build clean; the grid page renders items (locate it via the fallback grep if the grid URL differs).

- [ ] **Step 4: Commit**

```bash
git add assets/css/books.css assets/css/music.css
git commit -m "feat(design): tokenize book and music grids, drop hardcoded colors and emoji prefixes"
```

---

### Task 10: Photos extraction + inline-style sweep

**Files:**
- Create: `assets/css/photos.css`
- Modify: `layouts/photos/list.html` (remove `<style>` block), `config/_default/params.toml` (add photos.css to customcss)

**Interfaces:**
- Consumes: tokens.
- Produces: the final `customcss` list (matches the spec's §2 order).

- [ ] **Step 1: Create `assets/css/photos.css`**

```css
/* ABOUTME: Photo wall (photos section) — grid of the first image from each note, with quiet captions. */

.photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 10px;
    margin-top: 24px;
}

.photo-item img {
    display: block;
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: var(--radius-thumb);
}

.photo-item a:hover img {
    opacity: 0.9;
}

.photo-meta {
    padding: 6px 0 0;
}

.photo-meta time {
    font-size: 13px;
    color: var(--mut);
    font-variant-numeric: tabular-nums;
}

.photo-meta p {
    font-size: 13px;
    color: var(--mut);
    margin: 2px 0 0;
}
```

- [ ] **Step 2: Rewrite `layouts/photos/list.html` (markup unchanged, `<style>` gone)**

```html
{{- /* ABOUTME: List template for photos section */}}
{{- /* ABOUTME: Shows notes that have image resources in a grid layout */}}
{{ define "main" }}
  <header>
    <h1>{{ .Title }}</h1>
    {{ with .Description }}<p>{{ . }}</p>{{ end }}
    <p><a href="{{ .RelPermalink }}index.xml"
          data-tinylytics-event="feed.subscribe"
          data-tinylytics-event-value="photos-rss">📡 RSS Feed</a></p>
  </header>

  <div class="photo-grid">
    {{- /* Get notes that have image resources */ -}}
    {{ $notes := where .Site.RegularPages "Type" "notes" }}
    {{ range $notes }}
      {{ $images := .Resources.ByType "image" }}
      {{ if gt (len $images) 0 }}
      <article class="photo-item">
        {{ $firstImage := index $images 0 }}
        <a href="{{ .Permalink }}">
          <img src="{{ $firstImage.RelPermalink }}" alt="{{ with .Title }}{{ . }}{{ else }}Photo{{ end }}" loading="lazy" />
        </a>
        <div class="photo-meta">
          <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "Jan 2, 2006" }}</time>
          {{ with .Title }}<p>{{ . }}</p>{{ end }}
        </div>
      </article>
      {{ end }}
    {{ end }}
  </div>
{{ end }}
```

- [ ] **Step 3: Add photos.css to `customcss`**

The final list in `config/_default/params.toml`:

```toml
customcss = [
    "/css/tokens.css",
    "/css/base.css",
    "/css/themes.css",
    "/css/books.css",
    "/css/music.css",
    "/css/notes.css",
    "/css/notes-grid.css",
    "/css/photos.css",
    "/css/code.css",
    "/css/bsky_comments.css",
    "/css/outofdate.css",
    "/css/ai-disclosure.css",
    "/css/image-loading.css",
    "/css/tinylytics.css",
    "/css/translations.css",
    "syntax.css",
]
```

- [ ] **Step 4: Verify no `<style>` blocks remain in any layout, then build**

Run:
```bash
grep -rn "<style" layouts/
grep -rn -- "--muted-text" layouts/ assets/
hugo --destination /tmp/design4-check --cleanDestinationDir
grep -c "photo-item" /tmp/design4-check/photos/index.html
```
Expected: both greps empty; build clean; photo items render.

- [ ] **Step 5: Commit**

```bash
git add assets/css/photos.css layouts/photos/list.html config/_default/params.toml
git commit -m "feat(design): extract photos grid css from template, fix undefined --muted-text"
```

---

### Task 11: Verification sweep

**Files:**
- Possibly modify: anything small the checks flag (each fix gets noted in the commit).
- Modify: this plan doc (check off tasks, record findings).

**Interfaces:** consumes everything; produces the reviewed, screenshot-verified branch.

- [x] **Step 1: Grep gates (all must be empty)**

```bash
grep -rn -- "--color-" assets/css/ layouts/
grep -rn "theme-chooser\|theme\.js" layouts/ config/ assets/
grep -rn "<style" layouts/
grep -rn "root-colors\|harper\.css\|shared\.css\|/css/links\.css\|/css/media\.css" config/ layouts/
grep -rn "composes:" assets/css/
```

- [x] **Step 2: Full production build, zero warnings**

```bash
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --destination /tmp/design4-new --logLevel info 2>&1 | tee /tmp/design4-build.log | grep -i "warn\|error"
```
Expected: no output from the grep. If warnings appear, fix root causes before proceeding.

- [x] **Step 3: Feed stability vs the Task 1 baseline**

```bash
while read -r f; do
    rel="${f#/tmp/design4-baseline/}"
    diff <(grep -v "lastBuildDate\|<generator" "$f") <(grep -v "lastBuildDate\|<generator" "/tmp/design4-new/$rel") > /dev/null 2>&1 || echo "DIFFERS: $rel"
done < /tmp/design4-baseline-xml.txt
```
Expected: at most the per-language `index.xml` may differ **only** if the channel description embeds the home intro (the `###` → paragraph edit — inspect any DIFFERS hit with a real `diff` and confirm every delta traces to that content edit or a date). Any structural difference in links/books/music/photos/media feeds is a bug — stop and fix. (If `/tmp/design4-baseline` is gone, regenerate per Task 1 Step 2's fallback.)

- [x] **Step 4: Theme spot-checks**

```bash
HUGO_RANDOM_THEME=cyber hugo --destination /tmp/design4-theme-check --cleanDestinationDir && grep -o 'class="theme-cyber"' /tmp/design4-theme-check/index.html
HUGO_RANDOM_THEME=academia hugo --destination /tmp/design4-theme-check --cleanDestinationDir && grep -o 'class="theme-academia"' /tmp/design4-theme-check/index.html
grep -o "html\.theme-" /tmp/design4-new/css/*.css | wc -l
```
Expected: both classes render; the minified bundle contains 75 `html.theme-` selector occurrences (25 themes × 3 blocks).

- [ ] **Step 5: Visual matrix via `hugo serve` + browser screenshots** ← BLOCKED: browser extension not connected

Run `hugo serve --buildDrafts --buildFuture` in the background, then screenshot (Claude-in-Chrome or manually) each of these at desktop width AND 375px, in light AND dark (use the ◐ toggle for dark):

1. `/` (home: intro lead, section labels, date rows)
2. `/posts/` (full post list)
3. A text-heavy post with code + blockquote + figure (e.g. `/2026/01/05/claude-code-is-better-on-your-phone/`) — kicker, byline, notices, tags, related posts, comments
4. `/notes/` (rows with and without image thumbnails)
5. `/media/links/`, `/media/books/` + the books grid page, `/media/music/` + grid, `/media/`
6. `/photos/`, `/now/`, `/404.html`
7. `/ja/` home + one ja post (CJK typography, ISO dates)

Check each against the mockups in `example-new-site/`: hairline rules, 88px date column, muted dates, ink titles, accent links/RSS, quiet footer. Fix what's off; keep fixes small and commit them as `fix(design): <what>`.

- [ ] **Step 6: Toggle + FOUC behavior** ← BLOCKED: browser extension not connected (structurally verified via source)

In the browser on `/`:
1. With no override: page follows OS scheme; button label names the other mode.
2. Click ◐ — colors flip instantly; `localStorage.mode` is set (check via DevTools).
3. Hard-reload with the dark override on a light-OS profile: **no white flash** before dark paint (mode-init.js runs pre-render).
4. Toggle back — override updates; reload holds.
5. Console shows zero CSP violations.

- [x] **Step 7: Update the plan + commit any fixes**

Check off all tasks in `docs/superpowers/plans/2026-07-15-design4-redesign.md`, append a short "Findings" section (anything applied from the fix paths above, e.g. the syntax.css reorder), and commit:

```bash
git add docs/superpowers/plans/2026-07-15-design4-redesign.md
git commit -m "docs(design): mark design4 redesign plan verified"
```

---

## Findings (Task 11 — 2026-07-15)

**Build/grep/feed/theme gates:** all pass. Zero warnings in production build. All feeds identical to Task 1 baseline. Theme selector count 75 (correct). Both cyber and academia spot-checks render correct class.

**FOUC guard:** structurally correct — `mode-init.js` loads synchronously (no defer), `bundle.js` loads with defer. No fix needed.

**Defects found via source analysis:**

1. **DEFECT-1 (MEDIUM) — note images squashed on single pages:** `assets/css/notes.css` — `article > .note-images img` override rule only sets `border-radius`, does not set `height: auto` to counteract the `.note-images img { height: 110px }` rule above it. Fix: add `height: auto;` to the `article > .note-images img` block.

2. **DEFECT-2 (MEDIUM) — music (and books) grid: only overlay is clickable:** In `layouts/music/music-grid.html` and `layouts/books/books-grid.html`, the cover image is a sibling to the anchor, not inside it. `.music-link`/`.book-link` has no `position: absolute; inset: 0` to cover the full tile. Fix: add `position: absolute; inset: 0; display: block;` to `.music-link` and `.book-link` in their respective CSS files.

**BLOCKED:** Browser extension not connected — Steps 5 (visual matrix, 28 cells) and 6 (toggle/FOUC/CSP-in-console) could not be completed in browser. Netlify deploy preview is the recommended next visual check step.

**syntax.css reorder:** Not verified visually — if code block backgrounds appear wrong (syntax.css overriding `--bg2`), move `"syntax.css"` before `"/css/code.css"` in `customcss`.

---

## Post-plan (not tasks): open a PR from `feat/design4-redesign` to `main` for Harper's review. Netlify deploy preview doubles as the final visual check.
