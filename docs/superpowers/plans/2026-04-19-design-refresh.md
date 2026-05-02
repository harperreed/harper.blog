# Design Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the blog's visual design with a unified design language — new compact header with section tabs, posts-first homepage with photo strip and widgets, consistent section page patterns, updated typography, and themes trimmed from 25 to 5.

**Architecture:** CSS-first refresh. Update CSS custom properties and layout styles, rewrite Hugo layout templates for header/homepage/section pages, trim theme definitions. No content structure changes, no build pipeline changes. The 9-token color system stays. Theme class applied on `<html>` element stays.

**Tech Stack:** Hugo templates (Go), CSS custom properties, vanilla JS (theme.js)

**Spec:** `docs/superpowers/specs/2026-04-19-design-refresh-design.md`

---

### Task 1: Typography & Spacing Foundation

Update CSS custom properties to establish the new typographic hierarchy and spacing. This is the foundation everything else builds on.

**Files:**
- Modify: `assets/css/root-colors.css`
- Modify: `assets/css/harper.css`

- [ ] **Step 1: Update root-colors.css with new typography tokens**

Replace the typography and sizing section in `assets/css/root-colors.css`. The font family changes from Verdana to system-ui, width increases from 720px to 760px, and line-height increases slightly.

Find the current `:root` block (lines 15–31) and replace the sizing/typography/border section:

```css
    /* Sizing */
    --size: 1rem;
    --margin: calc(var(--size) * 0.8);
    --margin-big: calc(var(--size) * 1.5);
    --padding-body: calc(var(--size) * 1.25);
    --spacing: calc(var(--size) * 2.4);
    --size-width: 760px;
    --title-font-size: 24px;

    /* Typography */
    --font-family-base: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --font-size-base: 1rem;
    --line-height-base: 1.58;

    /* Borders */
    --border-radius-sm: 3px;
    --border-radius-base: 5px;
```

Changes from current: `--font-family-base` from `Verdana, sans-serif` to system-ui stack, `--size-width` from `720px` to `760px`, `--line-height-base` from `1.5` to `1.58`.

- [ ] **Step 2: Update heading styles in harper.css**

Add typographic hierarchy styles after the existing `h1–h6` color rule (line 28 of `harper.css`). Insert after the closing `}` of the heading color block:

```css
h1 {
    font-size: 28px;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.2;
}

h2 {
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.3;
}

h3 {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.01em;
    line-height: 1.35;
}
```

- [ ] **Step 3: Run Hugo build to verify no breakage**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Build succeeds with no errors. Site renders with new font stack and slightly wider layout.

- [ ] **Step 4: Visually verify with dev server**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo serve --buildDrafts --buildFuture --port 1313 &`

Open `http://localhost:1313` in a browser. Verify:
- Font is system-ui (San Francisco on Mac), not Verdana
- Content area is slightly wider
- Headings have clear size hierarchy

Kill the server when done.

- [ ] **Step 5: Commit**

```bash
git add assets/css/root-colors.css assets/css/harper.css
git commit -m "style: update typography to system-ui stack and refine heading hierarchy"
```

---

### Task 2: New Header with Section Tabs

Replace the current header (avatar + h1 + email/RSS nav) with a compact header that has an avatar + name row and section navigation tabs below.

**Files:**
- Modify: `layouts/partials/header.html`
- Modify: `layouts/partials/nav.html`
- Modify: `config/_default/menu.toml`
- Modify: `assets/css/harper.css`

- [ ] **Step 1: Add section links to menu.toml**

Replace the entire content of `config/_default/menu.toml`:

```toml
######### menu #########

[[main]]
identifier = "posts"
name = "Posts"
url = "/posts/"
weight = 1

[[main]]
identifier = "notes"
name = "Notes"
url = "/notes/"
weight = 2

[[main]]
identifier = "books"
name = "Books"
url = "/books/"
weight = 3

[[main]]
identifier = "links"
name = "Links"
url = "/links/"
weight = 4

[[main]]
identifier = "music"
name = "Music"
url = "/music/"
weight = 5

[[footer]]
identifier = "contact"
name = "harper@modest.com"
url = "mailto:harper@modest.com"
weight = 1

[[footer]]
identifier = "home"
name = "Harper.lol"
url = "https://harper.lol"
weight = 5
```

This moves the email contact link to the footer and adds all section links to the main menu. RSS will be hardcoded in the nav partial.

- [ ] **Step 2: Rewrite header.html**

Replace the entire content of `layouts/partials/header.html`:

```html
{{- /* ABOUTME: Compact header with avatar, name, and section nav tabs */ -}}
{{- /* ABOUTME: Avatar + name row on top, section tabs below with active state */ -}}
<a class="skip-link" href="#main-content" aria-label="Skip to main content">{{ i18n "skip-link" }}</a>
<div class="site-header">
    <a href="{{ relURL .Site.Home.RelPermalink }}" class="site-identity" aria-label="Home">
        <img
            src="{{ .Site.Params.avatar }}"
            alt="Avatar"
            class="avatar"
        />
        <span class="site-name">{{ .Site.Params.name | default .Site.Title }}</span>
    </a>
    <nav class="site-nav" aria-label="Main Navigation">
        {{- partialCached "nav.html" . -}}
    </nav>
</div>
```

- [ ] **Step 3: Rewrite nav.html with active tab support**

Replace the entire content of `layouts/partials/nav.html`:

```html
{{- /* ABOUTME: Section tab navigation with active state detection */ -}}
{{- /* ABOUTME: Renders main menu items as tabs, highlights current section */ -}}
{{- $currentSection := "" -}}
{{- with .Page -}}
    {{- $currentSection = .Section -}}
    {{- /* Homepage gets "post" as active since posts feed is the homepage content */ -}}
    {{- if .IsHome -}}
        {{- $currentSection = "post" -}}
    {{- end -}}
{{- end -}}
{{ range .Site.Menus.main.ByWeight }}
{{- $isActive := false -}}
{{- $menuSection := .Identifier -}}
{{- /* Handle "posts" menu item matching "post" section */ -}}
{{- if eq $menuSection "posts" -}}
    {{- $isActive = eq $currentSection "post" -}}
{{- else -}}
    {{- $isActive = eq $currentSection $menuSection -}}
{{- end -}}
<a href="{{ .URL | relLangURL }}" {{ if $isActive }}class="active" aria-current="page"{{ end }}>{{ .Name }}</a>
{{ end }}
<a href='{{ absURL ("index.xml" | relLangURL) }}'
    data-tinylytics-event="feed.subscribe"
    data-tinylytics-event-value="main-rss"
    >{{ i18n "rss" | default "RSS" }}</a>
```

- [ ] **Step 4: Update header and nav CSS in harper.css**

Find the existing `.title`, `.title h1`, `.title span`, `.avatar`, `nav`, `nav a`, and `nav a:visited/hover` rules in `harper.css` (approximately lines 42–82). Replace them all with:

```css
/* Site header */
.site-header {
    padding: 20px 0 0;
}

.site-identity {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    margin-bottom: 14px;
}

.site-identity .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    flex-shrink: 0;
}

.site-name {
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--color-primary);
}

.site-identity:visited .site-name {
    color: var(--color-primary);
}

.site-nav {
    display: flex;
    gap: 24px;
    font-size: 14px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--color-tertiary);
    margin-bottom: var(--margin);
    overflow-x: auto;
}

.site-nav a {
    text-decoration: none;
    color: var(--color-dark);
    opacity: 0.5;
    white-space: nowrap;
    padding-bottom: 4px;
}

.site-nav a:visited {
    color: var(--color-dark);
    opacity: 0.5;
}

.site-nav a:hover {
    opacity: 1;
    color: var(--color-link-hover);
}

.site-nav a.active {
    opacity: 1;
    font-weight: 600;
    border-bottom: 2px solid var(--color-primary);
    color: var(--color-primary);
}

.site-nav a.active:visited {
    color: var(--color-primary);
}
```

Also remove the old `.title`, `.title h1`, `.title span`, `.avatar`, `nav`, `nav a`, `nav a:visited`, `nav a:hover` rules that were replaced.

- [ ] **Step 5: Run Hugo build to verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. The new header shows avatar + name on top, section tabs below.

- [ ] **Step 6: Verify visually with dev server**

Run dev server and check:
- Avatar is 36px circle next to name
- Section tabs show Posts, Notes, Books, Links, Music, RSS
- Active tab is bold with bottom border
- Tab bar scrolls horizontally on narrow viewports

- [ ] **Step 7: Commit**

```bash
git add layouts/partials/header.html layouts/partials/nav.html config/_default/menu.toml assets/css/harper.css
git commit -m "feat: replace header with compact avatar + section nav tabs"
```

---

### Task 3: Posts Section — Feed Mode with Pagination

Convert the posts list page from a title-only flat list to a feed-style layout with article blocks and pagination.

**Files:**
- Modify: `layouts/post/list.html`
- Modify: `assets/css/harper.css`

- [ ] **Step 1: Rewrite post/list.html**

Replace the entire content of `layouts/post/list.html`:

```html
{{- /* ABOUTME: Posts section list page with feed-style article blocks */ -}}
{{- /* ABOUTME: Shows title, date, and summary excerpt per post, with pagination */ -}}
{{ define "main" }}
<article>
    {{ .Content }}

    {{ if .Data.Singular }}
    <h3 class="section-filter">{{ i18n "filtering-for" }} "{{ .Title }}"</h3>
    {{ end }}

    {{ $paginator := .Paginate .Pages 20 }}
    <div class="feed">
        {{ range $paginator.Pages }}
        <article class="feed-item">
            <h2 class="feed-title">
                {{ if .Params.link }}
                <a href="{{ .Params.link }}" target="_blank" rel="noopener noreferrer">{{ .Title }} ↪</a>
                {{ else }}
                <a href="{{ .RelPermalink }}">{{ .Title }}</a>
                {{ end }}
            </h2>
            <time class="feed-date" datetime='{{ .Date.Format "2006-01-02" }}'>
                {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
            </time>
            {{ with .Summary }}
            <p class="feed-summary">{{ . | plainify | truncate 200 }}</p>
            {{ end }}
        </article>
        {{ else }}
        <p>{{ i18n "no-posts" }}</p>
        {{ end }}
    </div>

    {{ partial "pagination.html" . }}
</article>
{{ end }}
```

- [ ] **Step 2: Add feed CSS to harper.css**

Append to the end of `harper.css` (before the `@media (prefers-reduced-motion)` block):

```css
/* Feed mode (posts, notes list pages) */
.feed-item {
    margin-bottom: 28px;
    padding-bottom: 28px;
    border-bottom: 1px solid var(--color-tertiary);
}

.feed-item:last-child {
    border-bottom: none;
}

.feed-title {
    font-size: 20px;
    font-weight: 600;
    letter-spacing: -0.02em;
    margin: 0 0 4px;
    line-height: 1.3;
}

.feed-title a {
    text-decoration: none;
    color: var(--color-primary);
}

.feed-title a:visited {
    color: var(--color-primary);
}

.feed-title a:hover {
    color: var(--color-link-hover);
}

.feed-date {
    display: block;
    font-size: 13px;
    color: var(--color-dark);
    opacity: 0.5;
    margin-bottom: 8px;
    font-style: normal;
}

.feed-summary {
    font-size: 15px;
    color: var(--color-dark);
    opacity: 0.7;
    line-height: 1.55;
    margin: 0;
}

.section-filter {
    color: var(--color-secondary);
    font-size: 1.1em;
    margin-bottom: 2em;
}
```

- [ ] **Step 3: Run Hugo build and verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. Posts page now shows feed-style articles with pagination.

- [ ] **Step 4: Commit**

```bash
git add layouts/post/list.html assets/css/harper.css
git commit -m "feat: convert posts list to feed-style layout with pagination"
```

---

### Task 4: Notes Section — Refined Feed Mode

Standardize the notes list page to use the same feed CSS classes as posts while keeping its unique features (inline content, images, kudos, tags). Fix the hardcoded date format.

**Files:**
- Modify: `layouts/notes/list.html`

- [ ] **Step 1: Rewrite notes/list.html**

Replace the entire content of `layouts/notes/list.html`:

```html
{{- /* ABOUTME: Notes section list page with feed-style layout */ -}}
{{- /* ABOUTME: Shows full note content inline with images, tags, and kudos */ -}}
{{ define "main" }}
<article>
    {{ .Content }}

    {{ if .Data.Singular }}
    <h3 class="section-filter">{{ i18n "filtering-for" }} "{{ .Title }}"</h3>
    {{ end }}

    {{ $paginator := .Paginate .Pages (.Param "notes_pagination" | default 10) }}
    <div class="feed">
        {{ range $paginator.Pages }}
        <article class="feed-item">
            <header class="feed-item-header">
                <time class="feed-date" datetime='{{ .Date.Format "2006-01-02" }}'>
                    {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
                </time>
                <a href="{{ .RelPermalink }}" title="Permalink to this note">#</a>
                <button class="tinylytics_kudos" data-path="{{ .RelPermalink }}"></button>
            </header>
            {{ if .Params.text }}
                {{ .Params.text | markdownify }}
            {{ else }}
                {{ .Content }}
            {{ end }}
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
            {{ if .Params.tags }}
            <div class="feed-tags">
                {{ range .Params.tags }}
                <a href="/tags/{{ . }}">#{{ . }}</a>
                {{ end }}
            </div>
            {{ end }}
        </article>
        {{ else }}
        <p>{{ i18n "no-notes" | default "No notes yet." }}</p>
        {{ end }}
    </div>

    {{ partial "pagination.html" . }}
</article>
{{ end }}
```

Key changes from current: uses `.section-filter` instead of `.filter-notice`, wraps items in `.feed` div, uses `.feed-item` and `.feed-date` classes, uses site date format instead of hardcoded `"Jan 02, 2006"`, removes the `<hr />` separator (handled by CSS border on `.feed-item`).

- [ ] **Step 2: Add note-specific feed CSS**

Append to `assets/css/harper.css` after the feed CSS from Task 3:

```css
/* Note feed extras */
.feed-item-header {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
}

.feed-item-header a {
    font-size: 13px;
    text-decoration: none;
    opacity: 0.4;
}

.feed-item-header a:hover {
    opacity: 1;
}

.feed-tags {
    margin-top: 8px;
}

.feed-tags a {
    font-size: 13px;
    margin-right: var(--margin);
    line-height: calc(var(--line-height-base) * 1.2);
}
```

- [ ] **Step 3: Run Hugo build and verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. Notes page uses feed layout with consistent styling.

- [ ] **Step 4: Commit**

```bash
git add layouts/notes/list.html assets/css/harper.css
git commit -m "feat: standardize notes list to feed layout with consistent date format"
```

---

### Task 5: Dense Row Mode — Books, Links, Music

Standardize all three media sections to use a consistent dense row layout with shared CSS classes.

**Files:**
- Modify: `layouts/books/list.html`
- Modify: `layouts/links/list.html`
- Modify: `layouts/music/list.html`
- Modify: `assets/css/shared.css`

- [ ] **Step 1: Rewrite shared.css**

Replace the entire content of `assets/css/shared.css`:

```css
/* ABOUTME: Shared dense row styles for books, links, and music sections */
/* ABOUTME: Consistent list layout with date column, title, and metadata */

.dense-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.dense-list li {
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding: 10px 0;
    border-bottom: 1px solid var(--color-tertiary);
}

.dense-list li:last-child {
    border-bottom: none;
}

.dense-date {
    flex: 0 0 80px;
    font-size: 13px;
    color: var(--color-dark);
    opacity: 0.5;
    font-style: italic;
}

.dense-title {
    font-size: 15px;
    font-weight: 500;
    color: var(--color-primary);
    text-decoration: underline;
}

.dense-meta {
    font-size: 13px;
    color: var(--color-dark);
    opacity: 0.5;
    text-decoration: none;
}

.dense-list a {
    text-decoration: none;
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.dense-list a:visited .dense-title {
    color: var(--color-link-visited);
}

.dense-list a:hover .dense-title {
    color: var(--color-link-hover);
}

.section-filter {
    color: var(--color-secondary);
    font-size: 1.1em;
    margin-bottom: 2em;
}

/* Grid toggle */
.view-toggle {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    font-size: 13px;
}

.view-toggle a {
    text-decoration: none;
    color: var(--color-dark);
    opacity: 0.5;
    padding: 4px 8px;
    border-radius: var(--border-radius-sm);
}

.view-toggle a.active,
.view-toggle a:hover {
    opacity: 1;
    background: var(--color-tertiary);
}

@media (max-width: 600px) {
    .dense-list li {
        flex-direction: column;
        gap: 4px;
        padding: 12px 0;
    }

    .dense-date {
        flex: 0 0 auto;
    }
}
```

- [ ] **Step 2: Rewrite books/list.html**

Replace the entire content of `layouts/books/list.html`:

```html
{{- /* ABOUTME: Books section list page with dense row layout */ -}}
{{- /* ABOUTME: Shows date, title, and author per book in consistent rows */ -}}
{{ define "main" }}
<article>
    {{ .Content }}

    {{ if .Data.Singular }}
    <h3 class="section-filter">{{ i18n "filtering-for" }} "{{ .Title }}"</h3>
    {{ end }}

    <div class="view-toggle">
        <a class="active">List</a>
        <a href="{{ "/media/books/grid" | relLangURL }}">Grid</a>
    </div>

    {{ $pages := .Pages }}
    {{ if not $pages }}
    <p>{{ i18n "no-posts" }}</p>
    {{ else }}
    {{ $paginator := .Paginate $pages 20 }}
    <ul class="dense-list">
        {{ range $paginator.Pages }}
        <li>
            <span class="dense-date">
                <time datetime='{{ .Date.Format "2006-01-02" }}'>
                    {{ .Date.Format (default "2006-01-02" $.Site.Params.dateFormat) }}
                </time>
            </span>
            {{ if .Params.asin }}
            <a href="{{ .RelPermalink }}">
                <span class="dense-title">{{ .Title }}</span>
                {{ with .Params.book_author }}
                <span class="dense-meta">({{ . }})</span>
                {{ end }}
            </a>
            {{ else }}
            <span class="dense-title">{{ .Title }}</span>
            {{ end }}
        </li>
        {{ end }}
    </ul>

    {{ partial "pagination.html" . }}
    {{ end }}
</article>
{{ end }}
```

- [ ] **Step 3: Rewrite links/list.html**

Replace the entire content of `layouts/links/list.html`:

```html
{{- /* ABOUTME: Links section list page with dense row layout */ -}}
{{- /* ABOUTME: Shows date, title, and source domain per link in consistent rows */ -}}
{{ define "main" }}
<article>
    {{ .Content }}

    {{ if .Data.Singular }}
    <h3 class="section-filter">{{ i18n "filtering-for" }} "{{ .Title }}"</h3>
    {{ end }}

    {{ $pages := .Pages }}
    {{ if not $pages }}
    <p>{{ i18n "no-posts" }}</p>
    {{ else }}
    {{ $paginator := .Paginate $pages 20 }}
    <ul class="dense-list">
        {{ range $paginator.Pages }}
        {{ $url := urls.Parse .Params.original_url }}
        <li>
            <span class="dense-date">
                <time datetime='{{ .Date.Format "2006-01-02" }}'>
                    {{ .Date.Format (default "2006-01-02" $.Site.Params.dateFormat) }}
                </time>
            </span>
            {{ if .Params.original_url }}
            <a
                href="{{ .Params.original_url }}"
                target="_blank"
                rel="noopener noreferrer"
                data-tinylytics-event="outbound.link"
                data-tinylytics-event-value="{{ .Title }}"
            >
                <span class="dense-title">{{ .Title }}</span>
                <span class="dense-meta">({{ $url.Hostname }})</span>
            </a>
            {{ else }}
            <span class="dense-title">{{ .Title }}</span>
            {{ end }}
        </li>
        {{ end }}
    </ul>

    {{ partial "pagination.html" . }}
    {{ end }}
</article>
{{ end }}
```

- [ ] **Step 4: Rewrite music/list.html**

Replace the entire content of `layouts/music/list.html`:

```html
{{- /* ABOUTME: Music section list page with dense row layout */ -}}
{{- /* ABOUTME: Shows date, title, and artist per track in consistent rows */ -}}
{{ define "main" }}
<article>
    {{ .Content }}

    {{ if .Data.Singular }}
    <h3 class="section-filter">{{ i18n "filtering-for" }} "{{ .Title }}"</h3>
    {{ end }}

    <div class="view-toggle">
        <a class="active">List</a>
        <a href="{{ "/media/music/grid" | relLangURL }}">Grid</a>
    </div>

    {{ $pages := .Pages }}
    {{ if not $pages }}
    <p>{{ i18n "no-posts" }}</p>
    {{ else }}
    {{ $paginator := .Paginate $pages 20 }}
    <ul class="dense-list">
        {{ range $paginator.Pages }}
        <li>
            <span class="dense-date">
                <time datetime='{{ .Date.Format "2006-01-02" }}'>
                    {{ .Date.Format (default "2006-01-02" $.Site.Params.dateFormat) }}
                </time>
            </span>
            {{ if .Params.spotify_url }}
            <a
                href="{{ .RelPermalink }}"
                data-tinylytics-event="outbound.spotify"
                data-tinylytics-event-value="{{ .Title }}"
            >
                <span class="dense-title">{{ .Title }}</span>
                {{ with .Params.artist }}
                <span class="dense-meta">({{ . }})</span>
                {{ end }}
            </a>
            {{ else }}
            <span class="dense-title">{{ .Title }}</span>
            {{ end }}
        </li>
        {{ end }}
    </ul>

    {{ partial "pagination.html" . }}
    {{ end }}
</article>
{{ end }}
```

- [ ] **Step 5: Run Hugo build and verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. Books, links, and music pages all show consistent dense row layout.

- [ ] **Step 6: Commit**

```bash
git add layouts/books/list.html layouts/links/list.html layouts/music/list.html assets/css/shared.css
git commit -m "feat: unify books/links/music to consistent dense row layout"
```

---

### Task 6: Homepage — Posts Feed + Photo Strip + Widgets

Rewrite the homepage to show a posts feed, photo strip from notes, and compact widgets for recent content across sections.

**Files:**
- Modify: `layouts/index.html`
- Modify: `content/_index.md`
- Create: `assets/css/homepage.css`
- Modify: `config/_default/params.toml` (add homepage.css to bundle)

- [ ] **Step 1: Create homepage.css**

Create `assets/css/homepage.css`:

```css
/* ABOUTME: Homepage-specific styles for photo strip and compact widgets */
/* ABOUTME: Handles the posts feed, snapshot photo strip, and three-column widget grid */

/* Photo strip */
.photo-strip {
    margin: 32px 0;
}

.photo-strip-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 12px;
}

.section-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--color-dark);
    opacity: 0.5;
    font-weight: 600;
    margin: 0;
}

.section-more {
    font-size: 13px;
    color: var(--color-dark);
    opacity: 0.5;
    text-decoration: none;
}

.section-more:hover {
    opacity: 1;
}

.photo-strip-row {
    display: flex;
    gap: 8px;
    overflow: hidden;
}

.photo-strip-row a {
    flex-shrink: 0;
}

.photo-strip-row img {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 6px;
    display: block;
}

/* Compact widgets */
.widgets {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 20px;
    margin: 32px 0;
}

.widget {
    padding: 16px;
    background: var(--color-tertiary);
    border-radius: var(--border-radius-base);
}

.widget-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
}

.widget-item {
    margin-bottom: 8px;
}

.widget-item:last-child {
    margin-bottom: 0;
}

.widget-item-title {
    font-size: 14px;
    font-weight: 500;
    color: var(--color-primary);
}

.widget-item-meta {
    font-size: 12px;
    color: var(--color-dark);
    opacity: 0.5;
}

.widget-item-excerpt {
    font-size: 14px;
    color: var(--color-dark);
    opacity: 0.7;
    line-height: 1.45;
}

/* Homepage feed top margin */
.home-feed {
    margin-bottom: 8px;
}

.home-more {
    font-size: 14px;
    color: var(--color-dark);
    opacity: 0.5;
    text-decoration: none;
}

.home-more:hover {
    opacity: 1;
}

@media (max-width: 600px) {
    .widgets {
        grid-template-columns: 1fr;
    }

    .photo-strip-row img {
        width: 100px;
        height: 100px;
    }
}
```

- [ ] **Step 2: Add homepage.css to the CSS bundle**

In `config/_default/params.toml`, add `"/css/homepage.css"` to the `customcss` array. Insert it after `"/css/shared.css"` (line 42):

```toml
customcss = [
    "/css/root-colors.css",
    "/css/harper.css",
    "/css/shared.css",
    "/css/homepage.css",
    "/css/themes.css",
```

- [ ] **Step 3: Rewrite layouts/index.html**

Replace the entire content of `layouts/index.html`:

```html
{{- /* ABOUTME: Homepage with posts feed, photo strip, and compact widgets */ -}}
{{- /* ABOUTME: Posts-first layout with snapshots and reading/notes/links widgets */ -}}
{{ define "main" }}

{{- /* Posts feed */ -}}
{{ $posts := first 5 (where .Site.RegularPages "Section" "post") }}
{{ if $posts }}
<div class="home-feed">
    <div class="feed">
        {{ range $posts }}
        <article class="feed-item">
            <h2 class="feed-title">
                {{ if .Params.link }}
                <a href="{{ .Params.link }}" target="_blank" rel="noopener noreferrer">{{ .Title }} ↪</a>
                {{ else }}
                <a href="{{ .RelPermalink }}">{{ .Title }}</a>
                {{ end }}
            </h2>
            <time class="feed-date" datetime='{{ .Date.Format "2006-01-02" }}'>
                {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}
            </time>
            {{ with .Summary }}
            <p class="feed-summary">{{ . | plainify | truncate 200 }}</p>
            {{ end }}
        </article>
        {{ end }}
    </div>
    <a href="{{ "/posts" | relLangURL }}" class="home-more" aria-label="More Posts">{{ i18n "morePosts" | default "More Posts" }} →</a>
</div>
{{ end }}

{{- /* Photo strip — recent notes with images */ -}}
{{ $photoNotes := slice }}
{{ $allNotes := where .Site.RegularPages "Section" "notes" }}
{{ range first 20 $allNotes }}
    {{ if gt (len (.Resources.ByType "image")) 0 }}
        {{ $photoNotes = $photoNotes | append . }}
    {{ end }}
{{ end }}
{{ $photoNotes = first 6 $photoNotes }}
{{ if $photoNotes }}
<div class="photo-strip">
    <div class="photo-strip-header">
        <h3 class="section-label">Recent Photos</h3>
        <a href="{{ "/photos" | relLangURL }}" class="section-more">More →</a>
    </div>
    <div class="photo-strip-row">
        {{ range $photoNotes }}
        {{ $firstImage := index (.Resources.ByType "image") 0 }}
        {{ $thumb := $firstImage.Fill "240x240" }}
        <a href="{{ .Permalink }}">
            <img src="{{ $thumb.RelPermalink }}" alt="{{ with .Title }}{{ . }}{{ else }}Photo{{ end }}" loading="lazy" width="120" height="120" />
        </a>
        {{ end }}
    </div>
</div>
{{ end }}

{{- /* Compact widgets */ -}}
<div class="widgets">
    {{- /* Reading widget */ -}}
    {{ $books := first 3 (where .Site.RegularPages "Section" "books") }}
    {{ if $books }}
    <div class="widget">
        <div class="widget-header">
            <h3 class="section-label">Reading</h3>
            <a href="{{ "/books" | relLangURL }}" class="section-more">More →</a>
        </div>
        {{ range $books }}
        <div class="widget-item">
            <div class="widget-item-title">
                <a href="{{ .RelPermalink }}" style="text-decoration: none; color: inherit;">{{ .Title }}</a>
            </div>
            {{ with .Params.book_author }}
            <div class="widget-item-meta">{{ . }}</div>
            {{ end }}
        </div>
        {{ end }}
    </div>
    {{ end }}

    {{- /* Notes widget */ -}}
    {{ $notes := first 2 (where .Site.RegularPages "Section" "notes") }}
    {{ if $notes }}
    <div class="widget">
        <div class="widget-header">
            <h3 class="section-label">Notes</h3>
            <a href="{{ "/notes" | relLangURL }}" class="section-more">More →</a>
        </div>
        {{ range $notes }}
        <div class="widget-item">
            <div class="widget-item-excerpt">{{ .Description | default .Title | truncate 80 }}</div>
        </div>
        {{ end }}
    </div>
    {{ end }}

    {{- /* Links widget */ -}}
    {{ $links := first 2 (where .Site.RegularPages "Section" "links") }}
    {{ if $links }}
    <div class="widget">
        <div class="widget-header">
            <h3 class="section-label">Links</h3>
            <a href="{{ "/links" | relLangURL }}" class="section-more">More →</a>
        </div>
        {{ range $links }}
        {{ $url := urls.Parse .Params.original_url }}
        <div class="widget-item">
            <div class="widget-item-title">
                {{ if .Params.original_url }}
                <a href="{{ .Params.original_url }}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit;"
                    data-tinylytics-event="outbound.link"
                    data-tinylytics-event-value="{{ .Title }}"
                >{{ .Title }} ↪</a>
                {{ else }}
                {{ .Title }}
                {{ end }}
            </div>
            {{ if .Params.original_url }}
            <div class="widget-item-meta">{{ $url.Hostname }}</div>
            {{ end }}
        </div>
        {{ end }}
    </div>
    {{ end }}
</div>

{{ end }}
```

- [ ] **Step 4: Simplify content/_index.md**

Remove the intro paragraph from `content/_index.md`. Replace the content below the frontmatter with nothing (the header now identifies the site):

Keep the frontmatter as-is, but clear the body content after `---`:

```markdown
---
date: 2024-05-02 20:54:26-05:00
draft: false
nodate: true
nofeed: true
title: Home
translationKey: "index"
menu:
    main:
        weight: 1
        identifier: home
        name: Home
---
```

Note: Remove the `menu.main` entry from the frontmatter too — the homepage doesn't need to appear in the nav tabs (section tabs handle navigation now). Actually, keep the frontmatter but remove the menu block and the body text:

```markdown
---
date: 2024-05-02 20:54:26-05:00
draft: false
nodate: true
nofeed: true
title: Home
translationKey: "index"
---
```

- [ ] **Step 5: Run Hugo build and verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. Homepage shows posts feed, photo strip (if notes have images), and three widget boxes.

- [ ] **Step 6: Visually verify with dev server**

Run dev server and check:
- Posts appear as article blocks with title, date, summary
- Photo strip shows square thumbnails in a horizontal row
- Three widgets appear below (Reading, Notes, Links)
- On mobile width, widgets stack to single column

- [ ] **Step 7: Commit**

```bash
git add layouts/index.html content/_index.md assets/css/homepage.css config/_default/params.toml
git commit -m "feat: redesign homepage with posts feed, photo strip, and widgets"
```

---

### Task 7: Trim Themes to 5

Remove 21 themes from CSS, update theme.js, and update the build script.

**Files:**
- Modify: `assets/css/themes.css`
- Modify: `assets/js/theme.js`
- Modify: `scripts/build_with_random_theme.sh`
- Modify: `config/_default/params.toml`

- [ ] **Step 1: Rewrite themes.css with only 5 themes**

Read the current `assets/css/themes.css` and extract only the blocks for: `nature`, `sunset`, `nordic`, `terminal`. Remove all others (`dark`, `ocean`, `desert`, `autumn`, `cyber`, `academia`, `myspace`, `halloween`, `neon`, `electric`, `cyberpunk`, `volcano`, `midnight`, `lavender`, `coffee`, `mint`, `coral`, `synthwave`, `solarized`, `dracula`, `bubblegum`).

The file should contain only these theme blocks (copy exact CSS values from the current file for each):

```
.theme-nature { ... }
@media (prefers-color-scheme: dark) { .theme-nature { ... } }

.theme-sunset { ... }
@media (prefers-color-scheme: dark) { .theme-sunset { ... } }

.theme-nordic { ... }
@media (prefers-color-scheme: dark) { .theme-nordic { ... } }

.theme-terminal { ... }
@media (prefers-color-scheme: dark) { .theme-terminal { ... } }
```

Remove `theme-dark` too — the default `:root` dark mode in `root-colors.css` handles dark mode. The old `.theme-dark` was a separate named theme.

- [ ] **Step 2: Update theme.js**

In `assets/js/theme.js`, replace the themes array (lines 4–16):

```javascript
        this.themes = [
            "default",
            "nature",
            "sunset",
            "nordic",
            "terminal",
        ];
```

- [ ] **Step 3: Update build script**

Replace the THEMES array in `scripts/build_with_random_theme.sh` (lines 9–35):

```bash
THEMES=(
    "nature"
    "sunset"
    "nordic"
    "terminal"
)
```

- [ ] **Step 4: Update params.toml default theme**

In `config/_default/params.toml`, change the active theme from `academia` (which is being removed) to no theme (default). Replace line 29:

```toml
# theme = "academia"
```

Comment it out so the site uses the default `:root` colors. Remove the other commented-out theme lines too (lines 22–36 area). Clean up to just:

```toml
# Themes: nature, sunset, nordic, terminal (or leave unset for default)
# theme = "nordic"
```

- [ ] **Step 5: Run Hugo build and verify**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. Site uses default theme (no `theme-*` class on `<html>`, or the `:root` colors).

- [ ] **Step 6: Verify theme switching still works**

Run dev server. Open browser console and run:

```javascript
const tm = new ThemeManager();
tm.applyTheme('nature');    // should work
tm.applyTheme('sunset');    // should work
tm.applyTheme('nordic');    // should work
tm.applyTheme('terminal');  // should work
tm.applyTheme('academia');  // should log error, return false
tm.applyTheme('default');   // should work, reset to default
```

- [ ] **Step 7: Commit**

```bash
git add assets/css/themes.css assets/js/theme.js scripts/build_with_random_theme.sh config/_default/params.toml
git commit -m "style: trim themes from 25 to 5 (default, nature, sunset, nordic, terminal)"
```

---

### Task 8: Cleanup Old CSS

Remove CSS classes that are no longer referenced after the template rewrites. The old section-specific list classes are replaced by `.dense-list` and `.feed`.

**Files:**
- Modify: `assets/css/harper.css`
- Modify: `assets/css/links.css`

- [ ] **Step 1: Remove old blog-posts list styles from harper.css**

Remove these rules from `harper.css` (they were used by the old `ul.blog-posts` in post/list.html and index.html):

```css
/* blog posts */
ul.blog-posts {
    list-style-type: none;
    padding: unset;
}

ul.blog-posts li {
    display: flex;
    margin-bottom: var(--margin);
}

ul.blog-posts li span {
    flex: 0 0 130px;
}

ul.blog-posts li a:visited {
    color: var(--color-link-visited);
}

a.blog-tags {
    line-height: calc(var(--line-height-base) * 1.2);
    margin-right: var(--margin);
}

h3.blog-filter {
    margin-bottom: 0;
}
```

Also remove the old `.title`, `.title h1`, `.title span` rules if they weren't already removed in Task 2.

- [ ] **Step 2: Clean up links.css**

Read `assets/css/links.css`. If it references old class names (`.link-posts`) that are no longer used, simplify or remove. The `🔗` emoji prefix behavior should be kept if desired — check with the current template. Since the new template uses `.dense-list` and `.dense-title`, the old `.link-posts` rules are unused.

If `links.css` only contains `.link-posts` rules, it can be emptied to just a comment:

```css
/* ABOUTME: Link-specific styles (now uses shared dense-list classes) */
/* ABOUTME: Kept for any future link-specific overrides */
```

- [ ] **Step 3: Run Hugo build and verify nothing broke**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --quiet`

Expected: Builds cleanly. No visual regressions.

- [ ] **Step 4: Commit**

```bash
git add assets/css/harper.css assets/css/links.css
git commit -m "refactor: remove old CSS classes replaced by feed and dense-list patterns"
```

---

### Task 9: Final Verification

Full end-to-end verification that everything works together.

**Files:** (no changes — verification only)

- [ ] **Step 1: Clean Hugo build**

Run: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info`

Expected: Builds cleanly with no errors or warnings about missing templates/partials.

- [ ] **Step 2: Visual verification checklist**

Run dev server: `cd /Users/harper/Public/src/personal/harperreed/harper.blog && hugo serve --buildDrafts --buildFuture`

Check each page:
1. **Homepage** (`/`): Posts feed → photo strip → widgets. No intro text. Header has avatar + tabs.
2. **Posts** (`/posts/`): Feed-style articles with pagination. "Posts" tab active in header.
3. **Notes** (`/notes/`): Feed-style with inline content, images, tags. "Notes" tab active.
4. **Books** (`/books/`): Dense rows with date, title, author. "Books" tab active.
5. **Links** (`/links/`): Dense rows with date, title, domain. "Links" tab active.
6. **Music** (`/music/`): Dense rows with date, title, artist. "Music" tab active.
7. **Mobile width** (resize to ~375px): Widgets stack, photo strip scrolls, tabs wrap/scroll.
8. **Dark mode** (toggle system preference): Colors invert correctly, all elements readable.
9. **Theme switching**: Try `nature`, `sunset`, `nordic`, `terminal` from console.

- [ ] **Step 3: Check for console errors**

Open browser dev tools console. Navigate through all section pages. There should be no JavaScript errors or 404s for CSS/JS resources.

- [ ] **Step 4: Verify grid views still work**

Navigate to books grid view and music grid view (if accessible via URL or toggle). The existing grid templates (`books-grid.html`, `music-grid.html`) should still render correctly — they were not modified.

- [ ] **Step 5: Report results**

Report any issues found. If all checks pass, the design refresh is complete on the `design-refresh` branch.
