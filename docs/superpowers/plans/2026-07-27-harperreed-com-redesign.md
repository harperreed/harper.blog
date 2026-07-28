# harper.blog → harperreed.com Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reskin harper.blog to the harperreed.com design language (Tailwind + Sora/DM Sans + monochrome tokens) with zero UI/UX changes.

**Architecture:** Adopt the harperreed-static build pipeline (SCSS → libsass → PostCSS → Tailwind, purged via hugo_stats.json). Task 1 defines the new six-token palette AND a compat shim that aliases every legacy CSS variable to a new token — the whole site recolors instantly. Each later task converts one section's templates to Tailwind utilities and deletes its legacy CSS, with no visual change. The final task deletes the shim and proves nothing references legacy names.

**Tech Stack:** Hugo 0.154 (extended), Tailwind CSS 3.4, @tailwindcss/typography, @tailwindcss/forms, PostCSS, libsass, self-hosted DM Sans + Sora variable fonts.

**Spec:** `docs/superpowers/specs/2026-07-27-harperreed-com-redesign-design.md`

## Global Constraints

- **UI/UX is invariant.** Same pages, URLs, nav items, footer contents, list structures, grids, features. Visual layer only.
- **Reference repo:** `/Users/harper/Public/src/personal/harperreed/harperreed-static` (read-only source of truth; never modify it).
- **Tokens (exact):** light `#111111 / #555555 / #767676 / #949494 / #FFFFFF / #EEEEEE`, dark `#F0F0F0 / #D8D8D8 / #9A9A9A / #717171 / #111111 / #3A3A3C` for `--color-text-primary / -body / -muted / -faint / --color-bg-page / --color-border-rule`. Dark via `prefers-color-scheme` only.
- **Legacy→new variable mapping** (apply verbatim wherever legacy CSS is converted; "drop" means delete the declaration):

  | Legacy | New |
  |---|---|
  | `--color-dark` | `var(--color-text-body)` for body text; `var(--color-text-primary)` for headings/emphasis/borders |
  | `--color-light` | `var(--color-bg-page)` |
  | `--color-primary` | `var(--color-text-primary)` |
  | `--color-secondary` | `var(--color-text-muted)` |
  | `--color-tertiary` | `var(--color-border-rule)` |
  | `--color-link`, `--color-link-visited` | `var(--color-text-primary)` |
  | `--color-link-hover` | `var(--color-text-muted)` |
  | `--color-error` | `var(--color-text-primary)` (warnings become bordered notes, not amber) |
  | `--color-code-bg` | `var(--color-text-primary)` |
  | `--color-code-fg` | `var(--color-bg-page)` |
  | `--font-family-base` | `'DM Sans', sans-serif` |
  | `--size-width` | `800px` (prefer `max-w-[800px]` utility) |
  | any `font-family: Verdana...` | drop (inherit) |

- **Link idiom:** prose links `text-text-primary font-semibold underline hover:no-underline`; chrome/nav/meta links `text-text-muted no-underline hover:text-text-primary transition-colors duration-200`.
- **Fonts:** headings/display get `font-display` (Sora); everything else inherits DM Sans from `body`. All stacks end in `sans-serif` (CJK fallback).
- **Preserve verbatim in every converted template:** i18n calls, `aria-*`, `datetime` attrs, `data-tinylytics-*` attrs, `partial`/`partialCached` calls and their cache keys.
- **Chroma:** keep `style = 'monokai'` inline highlighting. The `syntax.css` params entry is dead (file doesn't exist) — it dies with the customcss list.
- **Every task ends:** `hugo --logLevel info` builds with zero NEW warnings (baseline: the pre-existing "Missing CSS resource: syntax.css" warn until Task 1 removes it), then commit.
- **Verification greps run against `public/`** after a fresh `hugo` build.
- Do not touch: `content/`, `i18n/`, Python `tools/`, `.github/workflows/`, RSS/SEO/schema partials (except where a task names them).

---

### Task 1: Build pipeline, tokens, fonts, compat shim

**Files:**
- Create: `package.json`, `postcss.config.js`, `tailwind.config.js`
- Create: `config/_default/build.toml`
- Create: `assets/scss/main.scss`, `assets/scss/base.scss`, `assets/scss/content.scss`, `assets/scss/components.scss`, `assets/scss/legacy-shim.scss`
- Create: `assets/fonts/DMSans-Variable.woff2`, `assets/fonts/Sora-Variable.woff2` (copied from reference repo)
- Create: `layouts/partials/head/style.html`
- Modify: `layouts/partials/head/css.html` (append new pipeline include), `.gitignore`
- Modify: `config/_default/params.toml` (remove dead `"syntax.css"` entry only)

**Interfaces:**
- Produces: `page_content` class (prose treatment), Tailwind utilities incl. `text-text-primary|body|muted|faint`, `bg-bg-page`, `border-rule` color, `font-display`; legacy vars still resolve (shim).

- [ ] **Step 1: Verify the failing state** — `hugo && grep -c "DM Sans" public/index.html` → expected `0` (also note the `syntax.css` warn in build output; it must be gone by Step 8).

- [ ] **Step 2: Create the Node pipeline files**

`package.json`:
```json
{
  "name": "harper-blog",
  "private": true,
  "author": "harperreed",
  "license": "MIT",
  "scripts": {
    "dev": "hugo serve --buildDrafts --buildFuture",
    "build": "hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info"
  },
  "devDependencies": {
    "@fullhuman/postcss-purgecss": "^5.0.0",
    "@tailwindcss/forms": "^0.5.7",
    "@tailwindcss/typography": "^0.5.10",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.33",
    "postcss-cli": "^11.0.0",
    "tailwindcss": "^3.4.1"
  }
}
```

`postcss.config.js`:
```js
// ABOUTME: PostCSS pipeline — Tailwind always; purgecss+autoprefixer in production.
// ABOUTME: Purge content comes from Hugo's hugo_stats.json element/class inventory.
const purgecss = {
  content: ["./hugo_stats.json"],
  defaultExtractor: (content) => {
    const elements = JSON.parse(content).htmlElements;
    return [
      ...(elements.tags || []),
      ...(elements.classes || []),
      ...(elements.ids || []),
    ];
  },
  safelist: [/^masonry-/, /^highlight/, /^chroma/, /loaded/, /visible/, /^bsky/, /^tinylytics/],
};

module.exports = {
  plugins: {
    tailwindcss: {},
    "@fullhuman/postcss-purgecss":
      process.env.HUGO_ENVIRONMENT === "production" ? purgecss : false,
    autoprefixer: process.env.HUGO_ENVIRONMENT === "production" ? {} : false,
  },
};
```

`tailwind.config.js`:
```js
// ABOUTME: Tailwind config for harper.blog — tokens live in scss/base.scss as CSS vars.
// ABOUTME: Content scan reads hugo_stats.json (enabled in config/_default/build.toml).
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./hugo_stats.json"],
  darkMode: "media",
  theme: {
    extend: {
      fontFamily: {
        primary: ["Sora", "sans-serif"],
        sans: ["DM Sans", "sans-serif"],
        display: ["Sora", "sans-serif"],
      },
      colors: {
        "text-primary": "var(--color-text-primary)",
        "text-body": "var(--color-text-body)",
        "text-muted": "var(--color-text-muted)",
        "text-faint": "var(--color-text-faint)",
        "bg-page": "var(--color-bg-page)",
        "border-rule": "var(--color-border-rule)",
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
```

- [ ] **Step 3: Hugo build stats + cachebusters** — `config/_default/build.toml`:
```toml
############################# Build ##############################
useResourceCacheWhen = 'fallback'
[buildStats]
enable = true
[[cachebusters]]
source = 'assets/watching/hugo_stats\.json'
target = 'style\.css'
[[cachebusters]]
source = '(postcss|tailwind)\.config\.js'
target = 'css'
[[cachebusters]]
source = 'assets/.*\.(css|scss|sass)'
target = 'css'
```

- [ ] **Step 4: SCSS tree**

`assets/scss/main.scss`:
```scss
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  @import "base";
}

@layer components {
  @import "content";
  @import "components";
}

@import "legacy-shim";
```

`assets/scss/base.scss`:
```scss
/* ABOUTME: Design tokens for the harperreed.com-matched skin, light + dark. */
/* ABOUTME: Six variables, system dark mode only — see the redesign spec. */
:root {
  --color-text-primary: #111111;
  --color-text-body: #555555;
  --color-text-muted: #767676;
  --color-text-faint: #949494;
  --color-bg-page: #FFFFFF;
  --color-border-rule: #EEEEEE;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-text-primary: #F0F0F0;
    --color-text-body: #D8D8D8;
    --color-text-muted: #9A9A9A;
    --color-text-faint: #717171;
    --color-bg-page: #111111;
    --color-border-rule: #3A3A3C;
  }
}
```

`assets/scss/content.scss` (port of the reference `content.scss`):
```scss
/* ABOUTME: Prose treatment for page/post content via Tailwind typography. */
/* ABOUTME: Maps all prose colors onto the six design tokens. */
.page_content {
  @apply prose sm:prose-lg lg:prose-xl;
  @apply prose-headings:font-display;
  @apply prose-a:text-text-primary prose-a:font-semibold prose-a:underline;
  @apply hover:prose-a:no-underline;
  @apply min-w-full;

  --tw-prose-body: var(--color-text-body);
  --tw-prose-headings: var(--color-text-primary);
  --tw-prose-links: var(--color-text-primary);
  --tw-prose-bold: var(--color-text-primary);
  --tw-prose-counters: var(--color-text-muted);
  --tw-prose-bullets: var(--color-text-faint);
  --tw-prose-hr: var(--color-border-rule);
  --tw-prose-quotes: var(--color-text-primary);
  --tw-prose-quote-borders: var(--color-border-rule);
  --tw-prose-captions: var(--color-text-muted);
  --tw-prose-code: var(--color-text-primary);
  --tw-prose-th-borders: var(--color-border-rule);
  --tw-prose-td-borders: var(--color-border-rule);

  hr { margin-top: 2em; margin-bottom: 2em; }
}
```

`assets/scss/components.scss`: create with only the two ABOUTME lines (`/* ABOUTME: Converted section/feature components... */`) — content arrives in Tasks 4–9.

`assets/scss/legacy-shim.scss`:
```scss
/* ABOUTME: TEMPORARY aliases mapping legacy bearcub vars onto the new tokens */
/* ABOUTME: so unconverted CSS renders the new palette. Deleted in the final task. */
:root {
  --color-dark: var(--color-text-body);
  --color-light: var(--color-bg-page);
  --color-primary: var(--color-text-primary);
  --color-secondary: var(--color-text-muted);
  --color-tertiary: var(--color-border-rule);
  --color-error: var(--color-text-primary);
  --color-link: var(--color-text-primary);
  --color-link-visited: var(--color-text-primary);
  --color-link-hover: var(--color-text-muted);
  --color-code-fg: var(--color-bg-page);
  --color-code-bg: var(--color-text-primary);
  --font-family-base: 'DM Sans', sans-serif;
  --font-size-base: 1rem;
  --line-height-base: 1.5;
  --size: 1rem;
  --margin: calc(var(--size) * 0.8);
  --margin-big: calc(var(--size) * 1.5);
  --padding-body: calc(var(--size) * 1.25);
  --spacing: calc(var(--size) * 2.4);
  --size-width: 800px;
  --title-font-size: 24px;
  --border-radius-sm: 3px;
  --border-radius-base: 5px;
}
a { text-decoration-thickness: 1px; }
```
Then edit `config/_default/params.toml` customcss list: remove `"/css/root-colors.css"` (superseded by shim+tokens) and the dead `"syntax.css"` entry. Keep everything else for now.

- [ ] **Step 5: Copy fonts** — `cp /Users/harper/Public/src/personal/harperreed/harperreed-static/assets/fonts/DMSans-Variable.woff2 /Users/harper/Public/src/personal/harperreed/harperreed-static/assets/fonts/Sora-Variable.woff2 assets/fonts/`

- [ ] **Step 6: Pipeline partial** — `layouts/partials/head/style.html`:
```html
{{/* ABOUTME: Compiles scss/main.scss through libsass + PostCSS (Tailwind) and
     inlines self-hosted font faces. Replaces the legacy customcss bundle. */}}
{{ $scss := resources.Get "scss/main.scss" }}
{{ if not $scss }}{{ errorf "Required SCSS file not found" }}{{ end }}
{{ $CSSOpts := dict "transpiler" "libsass" "targetPath" "css/style.css" }}
{{ $styles := $scss | toCSS $CSSOpts | css.PostCSS }}
{{ if hugo.IsProduction }}
  {{ $styles = $styles | minify | fingerprint "sha512" }}
{{ else }}
  {{ $styles = $styles | fingerprint "sha512" }}
{{ end }}
<link href="{{ $styles.RelPermalink }}" integrity="{{ $styles.Data.Integrity }}" rel="stylesheet" />

{{ $dmSans := resources.Get "fonts/DMSans-Variable.woff2" }}
{{ $sora := resources.Get "fonts/Sora-Variable.woff2" }}
{{ if and $dmSans $sora }}
<link rel="preload" href="{{ $dmSans.RelPermalink }}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{{ $sora.RelPermalink }}" as="font" type="font/woff2" crossorigin>
<style>
@font-face {
  font-family: 'DM Sans';
  src: url('{{ $dmSans.RelPermalink }}') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Sora';
  src: url('{{ $sora.RelPermalink }}') format('woff2');
  font-weight: 100 900;
  font-style: normal;
  font-display: swap;
}
</style>
{{ end }}
```
In `layouts/partials/head/css.html`, add as the LAST line (after the existing customcss block, so the new tokens/utilities win the cascade): `{{ partialCached "head/style.html" . }}`

- [ ] **Step 7: Install and build** — `npm install` then `hugo --logLevel info`. Expected: build succeeds; no `syntax.css` warning; `hugo_stats.json` created.

- [ ] **Step 8: Verify** —
  - `grep -o "DM Sans" public/index.html | head -1` → `DM Sans`
  - `grep -c "color-text-primary" public/css/style.*.css` (find via `ls public/css/`) → `> 0`
  - `grep -c "root-colors" public/index.html` → `0`
  - Serve and eyeball: whole site is monochrome (no blue links), DM Sans body. Layout otherwise unchanged.

- [ ] **Step 9: Commit** — `git add -A . && git status` (confirm: only intended files + hugo_stats.json + package-lock.json) then `git commit -m "feat(redesign): tailwind pipeline, tokens, fonts, legacy shim"`. Add `node_modules/` to `.gitignore` first; `hugo_stats.json` and `package-lock.json` are committed.

---

### Task 2: Chrome — baseof, header, footer, language switcher

**Files:**
- Modify: `layouts/_default/baseof.html`, `layouts/partials/header.html`, `layouts/partials/nav.html`, `layouts/partials/footer.html`, `layouts/partials/language-switcher.html`

**Interfaces:**
- Consumes: Tailwind utilities + tokens from Task 1.
- Produces: body classes `bg-bg-page font-sans text-text-body`; header/footer landmarks styled; `<main>` wrapped in `mx-auto max-w-[800px] px-6`.

- [ ] **Step 1: Failing check** — `hugo && grep -c "max-w-\[800px\]" public/index.html` → `0`.

- [ ] **Step 2: Rewrite `baseof.html`** — replace the `<html>`/`<body>` scaffolding: drop the `$randomTheme`/`$theme` logic and the `class="theme-*"` attr entirely; body gets classes and main gets the column:
```html
<!doctype html>
<html lang="{{ with .Site.LanguageCode }}{{ . }}{{ else }}en-US{{ end }}">
    <head>
        ... (keep every existing head partial line unchanged) ...
    </head>
    <body class="bg-bg-page font-sans text-text-body">
        <header class="font-sans">{{- partialCached "header.html" . -}}</header>
        <main id="main-content" class="mx-auto max-w-[800px] px-6">{{- block "main" . }}{{- end }}</main>
        <footer class="mx-auto max-w-[800px] px-6 mt-16 font-sans" style="border-top: 1px solid var(--color-border-rule);">{{- partialCached "footer.html" . -}}</footer>
        {{- partialCached "custom_body.html" . -}}
    </body>
</html>
```

- [ ] **Step 3: Rewrite `header.html`** (skip-link kept, avatar retired, wordmark + nav on one baseline row):
```html
<a class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:bg-bg-page focus:text-text-primary focus:px-4 focus:py-2 focus:rounded" href="#main-content" aria-label="Skip to main content">{{ i18n "skip-link" }}</a>
<nav aria-label="Main Navigation"
     class="mx-auto flex justify-between items-baseline max-w-[800px] px-6 pt-8 pb-4 sm:pt-12 sm:pb-7"
     style="border-bottom: 1px solid var(--color-border-rule);">
    <a href="{{ relURL .Site.Home.RelPermalink }}" aria-label="Home"
       class="text-lg font-bold text-text-primary no-underline hover:no-underline">harper.blog</a>
    <div class="flex gap-5">{{- partialCached "nav.html" . -}}</div>
</nav>
```

- [ ] **Step 4: Rewrite `nav.html`** (same items, muted idiom; note the Home item comes from page frontmatter menus — leave menu config untouched):
```html
{{ range .Site.Menus.main.ByWeight }}
<a href="{{ .URL | relLangURL }}" class="text-base text-text-muted no-underline hover:text-text-primary transition-colors duration-200">{{ .Name }}</a>
{{ end }}
<a href='{{ absURL ("index.xml" | relLangURL) }}'
    class="text-base text-text-muted no-underline hover:text-text-primary transition-colors duration-200"
    data-tinylytics-event="feed.subscribe"
    data-tinylytics-event-value="main-rss"
    >{{ i18n "rss" | default "RSS" }}</a>
```

- [ ] **Step 5: Rewrite `footer.html`** — same contents (footer menu, ©, generated line, email, language switcher, tinylytics script tag unchanged), new shell:
```html
<div class="py-10 flex flex-col gap-4 text-xs text-text-muted text-center sm:text-left">
    <nav class="flex flex-wrap gap-x-5 gap-y-2 justify-center sm:justify-start">
        {{ range .Site.Menus.footer }}
        <a href="{{ .URL }}" class="no-underline hover:text-text-primary transition-colors duration-200">{{ .Name }}</a>
        {{ end }}
    </nav>
    <span>{{ i18n "copyright" | default "Copyright" }} &copy; {{ .Site.Params.Name }}</span>
    <span>{{ i18n "generated" | default "Generated" }} {{ i18n "on" | default "on" }} {{ now.Format "Jan 2, 2006" }}{{ with .GitInfo }} &middot; {{ .AbbreviatedHash }}{{ end }}</span>
    <span>{{ i18n "sendMeAn" | default "Send me an" }}
        <a href="mailto:{{ .Site.Params.email }}" aria-label="Send email to {{ .Site.Params.Name }}"
           class="underline hover:no-underline text-text-muted hover:text-text-primary"
           data-tinylytics-event="contact.email" data-tinylytics-event-value="footer">{{ i18n "email" | default "email" }}</a>
    </span>
    {{ partial "language-switcher.html" . }}
</div>
<script src="https://tinylytics.app/embed/WV5Khk7ZG6MZe6q49ikx.js?hits&countries&kudos=❤️&events" defer></script>
```
(Keep the exact existing tinylytics `src` URL — copy it from the current file, do not retype the ID.)

- [ ] **Step 6: `language-switcher.html`** — keep all logic/i18n/aria/tinylytics attrs; change only classes: wrapper `<div class="available-languages text-xs text-text-muted">`, each `language-link` gets `class="language-link underline hover:no-underline hover:text-text-primary"`.

- [ ] **Step 7: Purge stale styles from `assets/css/harper.css`** — delete these now-unused rule blocks: `body` margin/padding/max-width/colors block (keep nothing — body is utility-styled), `.title`, `.title h1`, `.title span`, `.avatar`, `nav`, `nav a`, `nav a:visited`, `nav a:hover`, `footer`, `.skip-link`, `.skip-link:focus`. Keep the rest (lists, tables, figures, pagination…) — they die in Tasks 3–9.

- [ ] **Step 8: Build + verify** — `hugo --logLevel info` clean, then:
  - `grep -c "max-w-\[800px\]" public/index.html` → `≥ 3` (header, main, footer)
  - `grep -c "theme-" public/index.html` → `0`
  - `grep -c "avatar" public/index.html` → `0`
  - Eyeball: header is wordmark+muted links with hairline rule; footer tiny/muted; ja + es homepages same chrome.

- [ ] **Step 9: Commit** — `git commit -am "feat(redesign): chrome — header, footer, baseof on new tokens"`

---

### Task 3: Homepage lists, post list/single, now page

**Files:**
- Modify: `layouts/index.html`, `layouts/post/list.html`, `layouts/post/single.html`, `layouts/now/list.html`, `layouts/now/single.html`, `layouts/404.html`
- Modify: `assets/scss/components.scss`, `assets/css/harper.css` (delete converted rules)

**Interfaces:**
- Consumes: `page_content` from Task 1, chrome from Task 2.
- Produces: `.post-list` grid component used by ALL date|title lists site-wide (later tasks reuse it verbatim).

- [ ] **Step 1: Failing check** — `hugo && grep -c "post-list" public/index.html` → `0`.

- [ ] **Step 2: Add the list component** to `assets/scss/components.scss`:
```scss
/* Date | title list — the site-wide list idiom (posts, notes, links, now…). */
.post-list {
  @apply grid grid-cols-[8.125rem_1fr] gap-x-4 gap-y-3 list-none p-0 m-0;
}
.post-list .post-date {
  @apply text-text-faint text-right tabular-nums whitespace-nowrap not-italic;
}
.post-list a {
  @apply text-text-primary no-underline hover:text-text-muted;
}
@media (max-width: 640px) {
  .post-list { @apply grid-cols-1 gap-y-1; }
  .post-list .post-date { @apply text-left text-sm; }
  .post-list li, .post-list .post-row { @apply mb-3; }
}
```

- [ ] **Step 3: Convert `layouts/index.html`** — wrap `{{ .Content }}` in `<div class="page_content">…</div>`; each section heading becomes `<h2 class="font-display text-text-primary text-xl font-bold mt-10 mb-4">…</h2>`; each `<ul class="blog-posts">` becomes a `.post-list` grid. List item pattern (repeat for the posts and notes loops, keeping each loop's existing i18n/aria/link logic verbatim):
```html
<ul class="post-list">
    {{ range $notes }}
    <li class="contents">
        <span class="post-date">
            <time datetime='{{ .Date.Format "2006-01-02" }}' aria-label="Date: {{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}">{{ .Date.Format (default "2006-01-02" .Site.Params.dateFormat) }}</time>
        </span>
        <a href="{{ .RelPermalink }}" title="{{ .Summary }}" aria-label="Link to {{ .Title }}">{{ .Title }}</a>
    </li>
    {{ else }}
    <li>{{ i18n "no-posts" }}</li>
    {{ end }}
</ul>
```
(`li.contents` + `display: contents` lets `<li>` semantics survive inside the grid: add `.post-list li.contents { display: contents; }` to components.scss.) "More Posts"/"More Notes" links get `class="text-text-muted underline hover:no-underline hover:text-text-primary text-sm"`.

- [ ] **Step 4: Convert `post/list.html` and `now/list.html`** with the same `.post-list` pattern (external `↪` links keep `target`/`rel`); `h3.blog-filter` becomes `<p class="text-text-muted italic mb-6">`. Delete from `harper.css`: `ul.blog-posts*`, `ul.now-posts*`, `h3.blog-filter`, `a.blog-tags` (re-add tags styling in Step 5 if `tags.html` renders them — check first).

- [ ] **Step 5: Convert `post/single.html`** — title + byline + content:
```html
<h1 class="font-display text-3xl font-bold text-text-primary leading-tight tracking-tight mt-10 mb-2">{{ .Title }}</h1>
<p class="text-sm text-text-faint mb-8">
  ... (existing time/author/wordcount/kudos line verbatim, minus class="byline") ...
</p>
```
Wrap `{{ .Content }}`'s `<article>` as `<article class="page_content">`. Inspect `tags.html`, `related-posts.html`, `generated.html`, `comments.html` partials: apply muted-link idiom to any `<a>`/text classes they own (`text-sm text-text-muted`, links underlined muted); keep their markup structure. Delete from `harper.css`: `p.byline`, `content`, `.pagination*` after converting the pagination partial (if `layouts/partials/pagination.html` exists — check; the styles in harper.css are `.pagination`): pagination links get `text-text-muted hover:text-text-primary no-underline`, page-number `text-text-faint`.

- [ ] **Step 6: Convert `404.html`** — wrap its content in `page_content`, links to muted idiom.

- [ ] **Step 7: Build + verify** —
  - `grep -c "post-list" public/index.html` → `≥ 2`
  - `grep -c "blog-posts" public/index.html` → `0`
  - `ls public/posts/index.html && grep -c "post-list" public/posts/index.html` → `≥ 1`
  - Open a long post: Sora H1, DM Sans body `#555`, black semibold underlined links, monokai code intact.

- [ ] **Step 8: Commit** — `git commit -am "feat(redesign): homepage, posts, now lists on post-list idiom + prose singles"`

---

### Task 4: Notes — list, single, masonry grid

**Files:**
- Modify: `layouts/notes/list.html`, `layouts/notes/single.html`, `layouts/notes/notes-grid.html`
- Modify: `assets/scss/components.scss`
- Delete: `assets/css/notes.css`, `assets/css/notes-grid.css`; remove both from `params.toml` customcss

**Interfaces:**
- Consumes: `page_content`, muted-link idiom.
- Produces: `.masonry-columns`/`.masonry-item` (Tailwind-composed, same class names — they're purge-safelisted).

- [ ] **Step 1: Read first** — read `assets/css/notes.css` (28 lines) and `layouts/notes/single.html` fully before editing.

- [ ] **Step 2: Masonry component** in components.scss (replaces notes-grid.css; same UX):
```scss
/* Notes photo masonry — CSS columns, FOUC fade preserved. */
.masonry-columns {
  @apply w-full mx-auto p-0 opacity-0;
  column-count: 3;
  column-gap: 16px;
  column-fill: balance;
  animation: masonry-fade-in 0.3s ease forwards;
}
@media (max-width: 1200px) { .masonry-columns { column-count: 2; } }
@media (max-width: 768px) { .masonry-columns { column-count: 1; } }
.masonry-item {
  @apply relative block mb-4;
  break-inside: avoid;
}
.masonry-item img {
  @apply w-full h-auto block rounded-sm object-cover transition-transform duration-300;
}
.masonry-item:hover img { transform: scale(1.02); }
@keyframes masonry-fade-in { to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) {
  .masonry-columns { animation: none; opacity: 1; }
  .masonry-item img { transition: none; }
  .masonry-item:hover img { transform: none; }
}
```

- [ ] **Step 3: Convert notes list/single** — each note card in `list.html`: `<article class="post">` → `<article class="mb-10 pb-8" style="border-bottom: 1px solid var(--color-border-rule);">`; header time → `text-text-faint text-sm`, permalink `#` and kudos → muted idiom; note body wrapped `<div class="page_content">`; `.note-images img` → `rounded-sm w-full h-auto`; `p.filter-notice` → `text-text-muted italic`. Apply the same treatment to `single.html`. Port any still-needed rules from `notes.css` per the Global mapping; everything else in that file dies.

- [ ] **Step 4: Delete** `notes.css` + `notes-grid.css`, remove `"/css/notes.css"`, `"/css/notes-grid.css"` from params customcss.

- [ ] **Step 5: Build + verify** — clean build; `grep -c "masonry-columns" public/notes/photos/index.html` (find actual grid page path with `ls public/notes/` first) → `≥ 1`; `grep -rc "notes-grid.css" public/ | grep -v ":0" | wc -l` → `0`. Eyeball notes list + masonry in light/dark.

- [ ] **Step 6: Commit** — `git commit -am "feat(redesign): notes list/single/masonry converted, legacy notes css removed"`

---

### Task 5: Shared media lists — links, books, music, media list pages

**Files:**
- Modify: `assets/scss/components.scss`; `layouts/links/list.html`, `layouts/links/single.html`
- Delete: `assets/css/shared.css`, `assets/css/links.css`; remove both from customcss

**Interfaces:**
- Consumes: tokens + list idiom.
- Produces: `.media-list` component consumed by Tasks 5–7 templates (class names `link-posts`, `book-posts`, `music-posts`, `media-posts` all become `media-list` usages — grep each template).

- [ ] **Step 1: Read first** — `assets/css/links.css`, `layouts/links/*.html`, and grep which templates use `link-posts|book-posts|music-posts|media-posts|media-title|link-domain|link-filter` (books/music/media templates too — they convert in their own tasks but the component lands now).

- [ ] **Step 2: Component** in components.scss (replaces shared.css; same flex UX incl. mobile stack):
```scss
/* Dated media lists (links, books, music, media) — flex rows, 130px date col. */
.media-list {
  @apply list-none p-0 m-0;
}
.media-list li {
  @apply flex items-baseline mb-3;
}
.media-list li > span:first-child {
  @apply flex-none w-[8.125rem] mr-4 text-text-faint tabular-nums text-sm;
}
.media-list a {
  @apply no-underline text-text-primary;
}
.media-list a .media-title { @apply underline; }
.media-list a:hover .media-title { @apply no-underline; }
.media-domain { @apply text-text-muted no-underline text-sm; }
.media-filter { @apply text-text-muted italic mb-8; }
@media (max-width: 640px) {
  .media-list li { @apply flex-col mb-4; }
  .media-list li > span:first-child { @apply w-auto mr-0 mb-1; }
}
```

- [ ] **Step 3: Convert links templates** — swap `link-posts`→`media-list`, `link-filter`→`media-filter`, `link-domain`→`media-domain` (keep `media-title` spans); content areas → `page_content`; keep all aria/tinylytics.

- [ ] **Step 4: Delete** `shared.css` + `links.css` and their customcss entries. NOTE: books/music/media templates still reference `book-posts`/`music-posts`/`media-posts` — add temporary aliases at the bottom of components.scss so nothing breaks until Tasks 6–8 (delete the alias lines as each task converts):
```scss
/* TEMP aliases until Tasks 6-8 convert these templates: */
.book-posts { @extend .media-list; }
.music-posts { @extend .media-list; }
.media-posts { @extend .media-list; }
```
(libsass supports @extend; if the build errors, duplicate the `.media-list` rules for the three selectors instead.)

- [ ] **Step 5: Build + verify** — clean build; `grep -c "media-list" public/links/index.html` → `≥1`; links page eyeball: dates faint, titles black underlined, domains muted.

- [ ] **Step 6: Commit** — `git commit -am "feat(redesign): media-list component; links converted; shared.css retired"`

---

### Task 6: Books — grid + single

**Files:**
- Modify: `layouts/books/list.html`, `layouts/books/single.html`, `layouts/books/books-grid.html`, `assets/scss/components.scss`
- Delete: `assets/css/books.css`; remove from customcss; remove `.book-posts` temp alias

- [ ] **Step 1: Read first** — `assets/css/books.css` (99 lines) + all three templates. Inventory every class books.css defines (cover grid, cards, meta).
- [ ] **Step 2: Convert** — book cover grid keeps its column/card geometry; translate each rule to `@apply` utilities in a `/* Books */` block in components.scss using the Global mapping (colors→tokens, fonts inherit, radii→`rounded`/`rounded-sm`). Cover images: `rounded-sm`, no heavy borders; titles `text-text-primary`, authors/meta `text-text-muted text-sm`. Templates: swap `book-posts`→`media-list`, content wrappers → `page_content`.
- [ ] **Step 3: Delete** books.css + customcss entry + `.book-posts` alias line.
- [ ] **Step 4: Build + verify** — clean build; books grid page renders card grid (eyeball light/dark); `grep -rc "books.css" public/ | grep -v ":0" | wc -l` → `0`.
- [ ] **Step 5: Commit** — `git commit -am "feat(redesign): books grid/single converted"`

---

### Task 7: Music — grid + single

**Files:**
- Modify: `layouts/music/list.html`, `layouts/music/single.html`, `layouts/music/music-grid.html`, `assets/scss/components.scss`
- Delete: `assets/css/music.css`; remove from customcss; remove `.music-posts` temp alias

- [ ] **Step 1: Read first** — `assets/css/music.css` (131 lines) + templates (album art grid, track cards, any Spotify embed styling).
- [ ] **Step 2: Convert** — same procedure as Task 6: geometry preserved, colors/fonts to tokens via mapping, `music-posts`→`media-list`, embeds untouched functionally.
- [ ] **Step 3: Delete** music.css + entry + alias.
- [ ] **Step 4: Build + verify** — clean build; music grid eyeball; grep music.css refs in public → none.
- [ ] **Step 5: Commit** — `git commit -am "feat(redesign): music grid/single converted"`

---

### Task 8: Media, photos, remaining layouts

**Files:**
- Modify: `layouts/photos/list.html`, any `layouts/media/*` templates (grep for `media-posts` consumers), `assets/scss/components.scss`
- Delete: `assets/css/media.css`; remove from customcss; remove `.media-posts` temp alias

- [ ] **Step 1: Read first** — `assets/css/media.css` (74 lines); find every template using its classes: `grep -rl "media-posts\|media-title\|media-" layouts/`.
- [ ] **Step 2: Convert** — `media-posts`→`media-list`; photo grids reuse `.masonry-columns` if identical UX, else translate media.css rules per mapping into a `/* Media */` block.
- [ ] **Step 3: Delete** media.css + entry + alias.
- [ ] **Step 4: Build + verify** — clean build; photos page eyeball; `grep -rn "media-posts\|book-posts\|music-posts\|link-posts" layouts/` → no hits.
- [ ] **Step 5: Commit** — `git commit -am "feat(redesign): media/photos converted; shared aliases gone"`

---

### Task 9: Functional components — code, bsky, tinylytics, image-loading, notices

**Files:**
- Modify: `assets/scss/components.scss`, `assets/css/harper.css` (delete last rules → then delete file)
- Delete: `assets/css/code.css`, `assets/css/bsky_comments.css`, `assets/css/tinylytics.css`, `assets/css/image-loading.css`, `assets/css/ai-disclosure.css`, `assets/css/outofdate.css`, `assets/css/translations.css`, `assets/css/harper.css`; remove all from customcss

- [ ] **Step 1: Read first** — every file being deleted, plus the partials that render their markup (`comments.html`, `out_of_date.html`, `ai-disclosure` partial, `post-translations.html`).
- [ ] **Step 2: Convert each** into a labeled block in components.scss, applying the Global mapping. Specific idiom decisions:
  - `code.css`: pre/code blocks — `pre { @apply rounded p-4 overflow-x-auto text-sm; }` with monokai inline colors untouched; inline `code` inherits prose token color.
  - Warning notices (`outofdate`, `ai-disclosure`): bordered notes — `@apply border rounded p-4 my-6 text-sm text-text-muted; border-color: var(--color-border-rule);` — no amber.
  - `translations.css` + `.available-languages`: `text-xs text-text-muted`.
  - `image-loading.css`: keep its loading-state opacity/transition rules verbatim (functional), colors per mapping.
  - `bsky_comments.css`: keep layout rules, colors per mapping (avatars/cards get `border-rule` borders).
  - Remaining `harper.css` rules (tables, blockquote, figure, hr, textarea/input, `.helptext`, `.errorlist`, `.disabled`, `.nowrap`, focus-visible, reduced-motion): tables/blockquote/figure/hr are covered by `page_content` prose — delete; port ONLY `:focus-visible { outline: 2px solid var(--color-text-primary); outline-offset: 2px; }`, `.nowrap`, `.disabled`, form field styling (`@apply bg-bg-page border rounded px-2 py-1;` + border-rule), and the reduced-motion block into components.scss. Then delete harper.css.
- [ ] **Step 3: Empty the customcss list** — after deletions the list should contain nothing; remove the `customcss` param entirely AND the now-empty legacy block in `head/css.html` (leave only the `head/style.html` include). Remove `"/js/theme.js"` from `customjs` (file dies next task).
- [ ] **Step 4: Build + verify** — clean build; `ls assets/css/` → only `themes.css` remains; a post with code, a bsky-comments post, an old post (out-of-date notice), and a translated post all render correctly (eyeball).
- [ ] **Step 5: Commit** — `git commit -am "feat(redesign): functional styles converted; legacy css bundle retired"`

---

### Task 10: Retire the theme system + deploy switch + easter egg

**Files:**
- Delete: `assets/css/themes.css`, `assets/js/theme.js`, `scripts/build_with_random_theme.sh`, `assets/scss/legacy-shim.scss`
- Modify: `netlify.toml`, `config/_default/params.toml` (theme comment block), `assets/scss/main.scss` (drop shim import), `layouts/partials/head/custom_head.html` or `head/css.html` (ASCII art)

- [ ] **Step 1: Prove the shim is dead** — `grep -rn "color-dark\|color-light\|color-primary\|color-secondary\|color-tertiary\|color-link\|color-error\|color-code\|font-family-base\|size-width\|title-font-size\|padding-body" assets/scss assets/css layouts/ --include="*.scss" --include="*.css" --include="*.html" | grep -v legacy-shim` → ONLY hits are the new `--color-text-*`/`--color-bg-page`/`--color-border-rule` names. Any legacy hit = unfinished conversion; fix before proceeding.
- [ ] **Step 2: Delete** the four files; remove `@import "legacy-shim";` from main.scss; remove the theme-selection comment block and `themeStyle` from params.toml.
- [ ] **Step 3: Netlify** — in `netlify.toml`, replace every `./scripts/build_with_random_theme.sh <flags>` with `npm install && hugo <same flags>`; add `NODE_VERSION = "20"` beside each HUGO_VERSION env.
- [ ] **Step 4: ASCII art** — port the ASCII head comment block (with the email note) from the reference repo's `layouts/partials/head.html` into the top of the blog's `layouts/partials/head/custom_head.html`, wrapped the same way (`{{ "<!--" | safeHTML }} … {{ "-->" | safeHTML }}`).
- [ ] **Step 5: Build + verify** — clean build; `grep -rn "theme" layouts/ config/ | grep -iv "themeStyle\|scheme\|hugo mod"` → no theme-variation logic; `view-source` head shows ASCII art; `HUGO_ENVIRONMENT=production npm run build` also green (exercises purgecss path).
- [ ] **Step 6: Commit** — `git commit -am "feat(redesign): retire theme variations + random-theme deploys; ascii easter egg"`

---

### Task 11: Full verification matrix

**Files:** none (verification only; fixes get their own commits)

- [ ] **Step 1: Production build** — `HUGO_ENVIRONMENT=production npm run build` → zero warnings; note `public/css/style.*.css` size (sanity: purged file well under 100KB).
- [ ] **Step 2: Serve** `hugo serve --buildDrafts --buildFuture` and walk the matrix — {en, es, ja, ko} × {home, posts list, one long post (code+images+quotes), notes list, notes masonry, links, books grid, music grid, now} × {light, dark (OS toggle or DevTools emulation)}. Confirm: monochrome palette, DM Sans/Sora (CJK falls back to system sans but keeps colors/layout), no blue links anywhere, grids intact, kudos buttons/bsky comments/language switcher functional.
- [ ] **Step 3: Font network check** — DevTools network: fonts served same-origin (`/fonts/...woff2` via Hugo resources), zero third-party font requests.
- [ ] **Step 4: Fix anything found** (each fix its own commit), re-run the failing check.
- [ ] **Step 5: Push branch + Netlify deploy preview** — `git push -u origin match-harperreed-com`, open a PR, confirm the deploy preview builds green and spot-check it. Report results; merge is Doctor Biz's call.

---

## Self-review notes

- Spec coverage: tokens (T1), fonts (T1), chrome (T2), prose/lists (T3), sections (T4–8), functional styles (T9), deletions + netlify + easter egg (T10), verification matrix (T11). `syntax.css` latent warn resolved in T1. hugo_stats committed (T1 Step 9). CJK fallback verified (T11).
- The `.post-list`/`.media-list` names and the temp `@extend` aliases are the only cross-task interfaces; Tasks 6–8 each remove their own alias line.
- "Read first" steps exist wherever the plan doesn't inline current file contents (books/music/media/functional css) — conversions there are governed by the Global mapping table, which is total over the legacy variable vocabulary.
