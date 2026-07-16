# Design 4 Redesign — "Text-led minimal"

**Date:** 2026-07-15
**Source of truth:** `example-new-site/design4.html` (master), `design4-home.html`, `design4-post.html`, `design4-notes.html`
**Status:** Approved design, pending implementation plan

## Overview

Restyle harper.blog to match Design 4 ("Text-led minimal — photos as quiet punctuation"): white/near-black palette, warm-gray muted text, terracotta accent, hairline rules, system font stack, ~660px reading column, manual ◐ light/dark toggle. Whole-site visual redesign built on a fresh CSS core with a 6-token palette model. The 25 existing named themes are ported as palette variations of the new structure.

## Hard constraint: the IA does not change

- All sections, URLs, menus, and page content stay exactly as they are.
- Nav keeps every current main-menu item: Home · Posts · Notes · Now · Media · harper@modest.com, plus the hardcoded RSS link. Nothing added (no About page), nothing removed.
- Home keeps its current content: intro + 5 recent posts + 5 recent notes (text rows) + "More" links. The mockup's "Latest frames" image strip is **not** built (it replaced the notes list in the mockup; that's an IA change — deferred, see Out of scope).
- Every existing post-page feature stays: byline (date · author · word count · reading time · kudos), translations notice, out-of-date warning, AI disclosure, tags, related posts, Bluesky comments.
- RSS / MediaRSS / JSON output templates are untouched.

## 1. Design tokens

New `assets/css/tokens.css` defines the palette on `html` (`:root`):

| Token | Light | Dark |
|---|---|---|
| `--bg` | `#FFFFFF` | `#0F1011` |
| `--bg2` | `#F7F5F1` | `#17181A` |
| `--ink` | `#191817` | `#EDEBE7` |
| `--mut` | `#8C877E` | `#8A8D90` |
| `--line` | `#ECE9E3` | `#242628` |
| `--accent` | `#B8532C` | `#E08A5F` |

Contrast note: muted-on-bg is ~3.5:1, below AA for small text. Accepted deliberately to match the mockup (per Harper).

Non-color tokens (also in `tokens.css`):

- `--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` (replaces Verdana)
- `--font-mono: ui-monospace, Menlo, monospace`
- `--size-width: 660px` (was 720px)
- Type scale from the mockup: wordmark 16px/600; nav 14px; intro lead 22px/1.55; body 19px/1.75; list titles 18px/500; list dates 13–14px tabular-nums; section labels 12px/600 uppercase +0.14em tracking; post h1 36px/1.15/−0.022em; notes h1 28px; captions/footer 13px.
- Radii: 4px (thumbnails), 5px (figures), 6px (code blocks).
- Code blocks: `--bg2` background + 1px `--line` border (replaces the old inverted dark-on-light code scheme; `--color-code-fg/bg` are retired).

Dark mode is applied through two selector paths (system default + manual override):

```css
:root { /* light tokens */ }
:root[data-mode="dark"] { /* dark tokens */ }
@media (prefers-color-scheme: dark) {
  :root:not([data-mode="light"]) { /* dark tokens */ }
}
```

Yes, each dark set appears twice; accepted duplication, grouped per theme so it stays mechanical.

## 2. CSS architecture

All CSS remains in `assets/css/`, bundled by the existing Hugo Pipes pipeline (`partials/head/css.html`, order from `params.toml:customcss`).

**New files**

- `tokens.css` — palette/type/sizing tokens, light + dark (§1).
- `base.css` — reset bits, body/typography, header + wordmark + nav, footer, links/underline style (accent, `text-underline-offset: 2px`), the shared **date-row list pattern** (date column `88px` + title, hairline dividers — used by home, post list, links, books, music, media, notes), section labels, figures + captions, blockquote (3px `--line` left border, italic, muted), `pre`/`code`, pagination, tags, skip-link, focus styles.
- `photos.css` — the `.photo-grid` / `.photo-item` styles currently inlined in `layouts/photos/list.html`, moved into the bundle and re-tokenized.

**Rewritten**

- `themes.css` — 25 ported theme blocks, each just the 6-token sextet × light/dark (§4). `paper` (the default) is the bare `:root` palette from `tokens.css`; its class intentionally has no rules (noted in a comment).

**Re-tokenized in place** (structure kept, colors/fonts swapped to tokens, old-token references removed): `notes.css`, `notes-grid.css`, `books.css` (also fix hardcoded `#555`, `#fff`, `rgba(255,255,255,.9)` and delete the dead `composes:` line), `links.css`, `music.css`, `media.css`, `code.css`, `bsky_comments.css`, `outofdate.css`, `ai-disclosure.css` (restyled: quiet muted italic line, no box — the mockup's "This post was written 98% by a human."), `image-loading.css`, `tinylytics.css`, `translations.css`.

**Deleted**

- `root-colors.css` (→ `tokens.css`), `harper.css` + `shared.css` (→ `base.css`), `assets/js/theme.js` (broken ThemeManager, unwired), `layouts/partials/theme-chooser.html` (dead stub).

**New `customcss` order:** tokens, base, themes, media, books, music, links, notes, notes-grid, photos, code, bsky_comments, outofdate, ai-disclosure, image-loading, tinylytics, translations, `syntax.css` (still from bearcub).

**New `customjs`:** `bluesky_comments.js`, `mode.js`, `image-loading.js`.

The hugo-bearcub module stays (syntax highlighting CSS, Font Awesome). No eject.

## 3. Dark-mode toggle

- **FOUC guard:** tiny inline script in `baseof.html` `<head>`, before the CSS link: reads `localStorage.mode` and, if set, applies `document.documentElement.dataset.mode`. Wrapped in try/catch.
- **`assets/js/mode.js`:** binds the nav's `#mode-toggle` button. Effective mode = `html[data-mode]` if set, else `matchMedia('(prefers-color-scheme: dark)')`. Click toggles, writes `data-mode` on `<html>` and `localStorage.mode`, updates the button label.
- **Button:** `◐ dark` / `◐ light` — label names the mode you'd switch *to* (as in the mockup). Labels come from new i18n keys (`mode-dark`, `mode-light`) rendered into `data-label-*` attributes so `mode.js` stays language-agnostic. `aria-label` via i18n too.
- First visit follows the OS; the override persists per-browser.

## 4. Theme port

- Base `:root` palette (§1) is the new default theme, named **`paper`**. `params.toml:theme = "paper"`; the `theme-paper` class applies no overrides.
- All 25 existing themes (academia, autumn, bubblegum, coffee, coral, cyber, cyberpunk, dark, desert, dracula, electric, halloween, lavender, midnight, mint, myspace, nature, neon, nordic, ocean, solarized, sunset, synthwave, terminal, volcano) are re-expressed as sextet overrides scoped to `html.theme-<name>`, with dark variants via the same two selector paths as §1.
- Derivation from each theme's current 9-token block in old `themes.css`:
  - `--bg` ← `--color-light` · `--bg2` ← `--color-tertiary` · `--ink` ← `--color-primary` · `--accent` ← `--color-link`
  - `--mut` ← ink mixed toward bg ≈ 55% strength, baked to hex
  - `--line` ← ink mixed toward bg ≈ 12–15% strength, baked to hex
  - Dark variants map the same way from each theme's existing `prefers-color-scheme: dark` block.
  - Hand-tune where mechanical mapping fails (accent-on-bg should stay ≥ 3:1; loud themes keep their character — cyber stays neon-on-black).
- Build-time selection is unchanged: `baseof.html` keeps `class="theme-{{ params.theme }}"` on `<html>`, `HUGO_RANDOM_THEME` keeps working. No runtime theme chooser (the broken one is deleted); ◐ only toggles light/dark within the active theme.

## 5. Template changes

- **`_default/baseof.html`** — add the inline mode script; default theme class `paper`. Structure otherwise unchanged.
- **`partials/header.html`** — drop the avatar `<img>` and the `<h1>` wrapper; wordmark becomes a plain `<a class="wordmark">{{ .Site.Title }}</a>`. Skip-link stays first. Header row: wordmark left, nav right (`margin-left: auto`), 1px `--line` bottom border.
- **`partials/nav.html`** — same menu iteration + RSS link (tinylytics event kept). Add: current-page state (`ClassCurrent`-style check → ink color; others muted), RSS styled accent with a hairline left divider, and the `#mode-toggle` button at the end. Because of the active state, drop `partialCached` for nav (or key the cache by `.RelPermalink`) — it's a cheap partial.
- **`partials/footer.html`** — same contents, quiet layout: row 1 left = copyright (© Harper Reed — en i18n string updated to "blogging since 2001, wtaf"; other languages keep their existing strings) + footer menu (Harper.lol) + email link; row 1 right = language switcher. Row 2, small muted: generated date · git hash. Tinylytics script tag stays.
- **`index.html`** — same two lists, restyled: section labels ("Posts", "Notes" via existing i18n), date-row pattern, "More Posts →" / "More Notes →" links (existing i18n strings, arrow added in template). `.Content` intro wrapped in `.home-intro` (first paragraph renders 22px lead, rest muted 16px).
- **`post/single.html`** — byline restyled per mockup: accent uppercase section kicker ("Post" — i18n) + `date · author · words · reading time · kudos` in muted 13px. `h1` 36px. All partials stay in place, restyled via CSS only: `post-translations` (quiet hairline note replacing the dashed box), `out_of_date`, `generated` (muted italic line), `tags` (muted row), `related-posts` (mockup's "More posts" date-row block), `comments`.
- **`post/list.html`, `links/list.html`, `books/list.html`, `music/list.html`, `media/list.html`** — adopt the shared date-row pattern (mostly CSS; template edits only where markup blocks it). Grid alternates (`books-grid`, `music-grid`, `notes-grid`) keep structure — covers stay 2:3 with hover — re-tokenized.
- **`notes/list.html`** — mockup layout: 88px date column (date links to the note) + 18px text; when a note has image resources they render as a 3-column thumbnail grid (110px tall, cover-cropped, radius 4). Same images as today, different layout. Pagination restyled.
- **`notes/single.html`, `links/single.html`, `books/single.html`, `music/single.html`, `now/single.html`, `now/list.html`, `404.html`** — inherit base typography; small per-template byline/kicker alignment where needed.
- **`photos/list.html`** — remove the inline `<style>` block (→ `photos.css`); grid structure unchanged.

Rename safety: deleting `harper.css`/`shared.css` classes requires checking every class they define against templates and JS (`blog-posts`, `link-posts`, `book-posts`, `music-posts`, `media-posts`, `avatar`, `title`, `byline`, `skip-link`, pagination classes, …) — carried classes get styles in `base.css`/section files; nothing referenced by a template may lose its ruleset.

## 6. Config, content, i18n edits

- **`config/_default/params.toml`** — `theme = "paper"`; new `customcss`/`customjs` lists (§2). `avatar` param stays (unused by header afterward; harmless).
- **`config/_default/languages.toml`** — `[en.params] dateFormat = "02 Jan 06"` (mockup format; tabular). English only — Go's `Format` can't localize month names, so es/ja/ko/zh/id keep today's ISO default. One deliberate deviation from the mockup: post bylines show `02 Jan 06` too (mockup shows a 4-digit year there); one sitewide param beats a second format mechanism.
- **`content/_index.md` (+ `.es`, `.ja`, `.ko`, `.zh`, `.id`)** — structural edit only: the `###` intro heading becomes a plain paragraph (copy otherwise untouched) so the lead-paragraph styling applies. Frontmatter (menu registration) untouched.
- **`i18n/*.yaml` (6 files)** — add `mode-dark`, `mode-light`, `mode-toggle-aria`; update en `copyright` string to the "blogging since 2001, wtaf" line. New keys get real translations for ja/es/ko/zh/id (single words: dark/light).

## 7. Responsive

Mockups are 820px desktop cards; behavior below that is ours:

- Content column: `max-width: var(--size-width)` with 20px side padding.
- ≤ 640px: date-row lists stack (date above title, smaller), header wraps to two rows (wordmark, then nav with horizontal wrap), notes thumbnails stay 3-up but shrink, post body drops to ~17px.
- Nothing hides at any width — same content everywhere.

## 8. Verification

No test infra exists in this repo; verification is build + rendered-output checks:

1. `hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info` — clean build, no new warnings.
2. Feed stability: build before/after on the same content commit; `diff` `index.xml`, links/books/music/photos RSS, and the MediaRSS output — must be byte-identical (modulo build date).
3. Visual pass via local `hugo serve` + browser screenshots: home, posts list, a text-heavy post (code + blockquote + figure), notes (with and without images), links, books + grid, music, media, photos, now, 404 — each in light and dark, en plus one CJK language, desktop and 375px.
4. Toggle behavior: first visit follows OS; ◐ overrides; persists across reload; no FOUC on hard reload with dark override.
5. Theme spot-check: `HUGO_RANDOM_THEME` build or `theme` param flips to cyber/academia/dracula — pages render with ported palettes in both modes.
6. Grep gate: no remaining references to retired tokens (`--color-`), deleted files, or `theme-chooser`; no `<style>` blocks left in layouts.

## Out of scope (explicitly deferred)

- "Latest frames" image strip on home (IA change — revisit later if wanted).
- About page (doesn't exist; mockup fiction).
- Ejecting the bearcub module; Font Awesome/syntax.css ownership.
- Runtime theme *chooser* UI (only light/dark toggles at runtime).
- Copy rewrites beyond the en copyright line and the intro heading→paragraph restructure.
