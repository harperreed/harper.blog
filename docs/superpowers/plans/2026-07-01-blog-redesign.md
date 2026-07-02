# Blog Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Full theme swap from `hugo-bearcub` to the new "text-led minimal" `harper` theme, preserving 1,451 `/post/` URLs, four languages, and the Bluesky/Tinylytics/SEO/Related feature set.

**Architecture:** New Hugo theme lives at `themes/harper/`. `hugo-bearcub` module removed. Content directories unchanged on disk — templates are rewired to query `Section == "post"` (singular) rather than the redesign's default `"posts"`. Existing per-language content (`content.es/`, `content.ja/`, `content.ko/`) continues to render via Hugo's multilingual system. Custom partials (Bluesky, Tinylytics, SEO, related posts) reimplemented against the redesign's design tokens.

**Tech Stack:** Hugo ≥ 0.110 (extended not required), Go templates, plain CSS (custom properties), vanilla JS for the light/dark toggle, existing Python tools under `tools/` unchanged.

## Global Constraints

- Post URLs stay at `/post/YYYY/MM/slug/` — never rename the on-disk section.
- Design tokens (colors, widths, fonts) live only in `themes/harper/static/css/main.css` `:root` and `[data-theme="dark"]` blocks.
- Text-first: system font stack, no custom web fonts, single warm-orange accent (`--acc: #B8532C`).
- Reading measure: `--read: 640px`; page shell: `--page: 680px`.
- All layouts under `themes/harper/layouts/`. Site-level overrides in `layouts/` are removed unless they add functionality the theme doesn't provide.
- Every phase ends with `hugo serve --buildDrafts --buildFuture` booting cleanly and the changed URLs rendering.
- Never use `--no-verify` on git commits.
- Follow conventional-commit style, imperative mood, present tense.
- One commit per task at the end of the task.

---

## Task 1: Foundation

**Files:**
- Create: `themes/harper/**` (copied verbatim from `/tmp/harper-redesign/hugo-theme/themes/harper/`)
- Modify: `config/_default/module.toml` (remove hugo-bearcub import)
- Modify: `config/_default/hugo.toml` (add `theme = "harper"`)
- Modify: `config/_default/params.toml` (comment `themeStyle`, `customcss`, `customjs`; add `since`, `homeFramesCount`, `aboutFramesCount`, `languages`)
- Modify: `themes/harper/layouts/index.html` (post→post rewire)
- Modify: `themes/harper/layouts/_default/single.html` (post→post rewire)

**Interfaces:**
- Consumes: nothing (foundation task)
- Produces:
  - `themes/harper/` — full theme tree
  - `site.Params.since = 2001` — used by about page stats
  - `site.Params.homeFramesCount = 3` and `aboutFramesCount = 4` — used by frame partials
  - `theme = "harper"` — active theme for the site

- [ ] **Step 1: Create the redesign branch**

```bash
cd /Users/harper/Public/src/personal/harper.blog
git checkout -b redesign
git status
```

Expected: `On branch redesign`, clean tree.

- [ ] **Step 2: Copy the harper theme into the repo**

```bash
mkdir -p themes/harper
cp -R /tmp/harper-redesign/hugo-theme/themes/harper/. themes/harper/
ls themes/harper/
```

Expected: `archetypes  layouts  static  theme.toml` listed.

- [ ] **Step 3: Remove hugo-bearcub from module.toml**

Edit `config/_default/module.toml` — delete the block:

```toml
[[imports]]
path = "github.com/clente/hugo-bearcub"
```

Keep the other three imports (`images`, `open-graph`, `twitter-cards`).

- [ ] **Step 4: Refresh Hugo modules**

```bash
hugo mod tidy
```

Expected: `hugo-bearcub` no longer appears; command completes without errors.

- [ ] **Step 5: Set the active theme**

Edit `config/_default/hugo.toml`. Below the existing `title = "Harper Reed's Blog"` line, add:

```toml
theme = "harper"
```

- [ ] **Step 6: Retire legacy params, add redesign params**

Edit `config/_default/params.toml`.

Comment (do not delete yet — cleanup phase removes them):

```toml
# themeStyle = "harper"
# customcss = [ ... ]
# customjs = [ ... ]
```

Below `defaultContentLanguage = "en"` add:

```toml
since = 2001
homeFramesCount = 3
aboutFramesCount = 4
languages = "日本語 · Español · 한국어 · 中文"
```

- [ ] **Step 7: Rewire the theme from `posts` to `post` (home template)**

Edit `themes/harper/layouts/index.html`. Replace two occurrences of `"Section" "posts"` with `"Section" "post"`. There are two: one in the `range first 5` block and one in the `See all N posts` link.

Before:

```gotemplate
{{ range first 5 (where site.RegularPages "Section" "posts") }}
```

After:

```gotemplate
{{ range first 5 (where site.RegularPages "Section" "post") }}
```

And:

Before:

```gotemplate
<a class="more-link" href="{{ "/posts/" | relURL }}">See all {{ len (where site.RegularPages "Section" "posts") }} posts →</a>
```

After:

```gotemplate
<a class="more-link" href="{{ "/post/" | relURL }}">See all {{ len (where site.RegularPages "Section" "post") }} posts →</a>
```

- [ ] **Step 8: Rewire the theme's "More posts" list (single template)**

Edit `themes/harper/layouts/_default/single.html`. Replace `"Section" "posts"` with `"Section" "post"` in the `$more :=` line.

Before:

```gotemplate
{{ $more := where (where site.RegularPages "Section" "posts") "Permalink" "!=" .Permalink }}
```

After:

```gotemplate
{{ $more := where (where site.RegularPages "Section" "post") "Permalink" "!=" .Permalink }}
```

- [ ] **Step 9: Boot Hugo and verify it compiles**

```bash
hugo --renderToMemory 2>&1 | tail -40
```

Expected: `Total in ...ms`, `Pages | ...` table, no template errors. Warnings about missing templates for other sections are acceptable at this phase.

- [ ] **Step 10: Sanity-check the home page renders**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3
curl -s http://localhost:1313/ | head -50
kill %1 2>/dev/null || true
```

Expected: HTML output containing `<a class="wordmark"` (the masthead), `Harper Reed's Blog` (or the site title), and a list of the 5 latest post titles in `.post-list__row` elements.

- [ ] **Step 11: Commit**

```bash
git add themes/harper/ config/_default/module.toml config/_default/hugo.toml config/_default/params.toml
git commit -m "feat(theme): scaffold harper redesign theme, drop hugo-bearcub

- Add themes/harper/ from the redesign handoff
- Remove hugo-bearcub Hugo module import
- Wire theme = harper in hugo.toml
- Add since/frames/languages params
- Rewire theme queries from posts to post section"
```

---

## Task 2: Post templates

**Files:**
- Modify: `themes/harper/layouts/_default/single.html` (add related posts + Bluesky slot markers — actual partials wired in Task 6)
- Copy shortcodes from `layouts/shortcodes/` into `themes/harper/layouts/shortcodes/` as needed

**Interfaces:**
- Consumes: `themes/harper/` from Task 1
- Produces:
  - Post list at `/post/` renders correctly
  - Individual post URLs `/post/YYYY/MM/slug/` render
  - Slot markers `<!-- related-posts -->` and `<!-- bluesky-comments -->` in place for Task 6

- [ ] **Step 1: Enumerate site-level shortcodes that could be used by posts**

```bash
ls layouts/shortcodes/ layouts/_shortcodes/ 2>/dev/null
```

Save the list — every shortcode reference in a post that doesn't resolve will break the build.

- [ ] **Step 2: Copy site-level shortcodes into the theme**

```bash
mkdir -p themes/harper/layouts/shortcodes
cp -R layouts/shortcodes/. themes/harper/layouts/shortcodes/ 2>/dev/null || true
cp -R layouts/_shortcodes/. themes/harper/layouts/shortcodes/ 2>/dev/null || true
ls themes/harper/layouts/shortcodes/
```

Expected: shortcode files present in the theme's shortcodes dir. If both source dirs exist, Hugo prefers the more specific one; copying both is safe.

- [ ] **Step 3: Add a `figure` shortcode matching the redesign's expectation**

The redesign README documents `{{</* figure src="..." caption="..." */>}}`. Verify one exists:

```bash
test -f themes/harper/layouts/shortcodes/figure.html && cat themes/harper/layouts/shortcodes/figure.html || echo MISSING
```

If MISSING, create `themes/harper/layouts/shortcodes/figure.html`:

```gotemplate
<figure>
  <img src="{{ .Get "src" | relURL }}" alt="{{ .Get "alt" | default (.Get "caption") }}" loading="lazy">
  {{ with .Get "caption" }}<figcaption>{{ . | markdownify }}</figcaption>{{ end }}
</figure>
```

- [ ] **Step 4: Insert slot markers in the post single template**

Edit `themes/harper/layouts/_default/single.html`. Between `</article>` and the `{{ $more := ... }}` line, insert:

```gotemplate
</article>

{{/* Injected in Task 6 */}}
{{ if eq .Section "post" }}
{{ partial "related-posts.html" . }}
{{ partial "bluesky-comments.html" . }}
{{ end }}

{{ $more := where (where site.RegularPages "Section" "post") "Permalink" "!=" .Permalink }}
```

Also create placeholder partials so the build doesn't fail before Task 6:

```bash
mkdir -p themes/harper/layouts/partials
printf '' > themes/harper/layouts/partials/related-posts.html
printf '' > themes/harper/layouts/partials/bluesky-comments.html
```

- [ ] **Step 5: Build the site to surface shortcode/template errors**

```bash
hugo --renderToMemory 2>&1 | grep -Ei "error|WARN" | head -50 || true
```

Expected: any remaining shortcode-not-found errors are printed. Zero errors is the goal.

- [ ] **Step 6: Fix any shortcode misses**

For every "shortcode 'X' not found" error, create `themes/harper/layouts/shortcodes/X.html` with a minimal passthrough implementation that renders the shortcode's `.Inner` (or nothing if none).

- [ ] **Step 7: Verify a sampling of posts render**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

for url in \
  "http://localhost:1313/post/" \
  "http://localhost:1313/post/2000/03/milestone/" \
  "http://localhost:1313/post/2015/06/" \
  "http://localhost:1313/post/2020/01/" \
  "http://localhost:1313/"
do
  echo "=== $url ==="
  curl -s -o /dev/null -w "%{http_code}\n" "$url"
done

kill %1 2>/dev/null || true
```

Expected: all URLs return `200` (or `404` for URLs that don't match a real post — that's fine as long as `/post/` and `/` return `200`).

- [ ] **Step 8: Commit**

```bash
git add themes/harper/layouts/
git commit -m "feat(post): render post section under harper theme

- Copy site shortcodes into the theme
- Insert slot markers for related-posts and bluesky-comments
- Add figure shortcode matching the redesign's contract"
```

---

## Task 3: Section templates (Notes, Books, Links, Music, Media)

**Files:**
- Create: `themes/harper/layouts/books/list.html`
- Create: `themes/harper/layouts/books/single.html`
- Create: `themes/harper/layouts/links/list.html`
- Create: `themes/harper/layouts/music/list.html`
- Create: `themes/harper/layouts/photos/list.html`
- Modify: `themes/harper/static/css/main.css` (append small blocks for books/music/links cards)

**Interfaces:**
- Consumes: Task 1's theme scaffolding
- Produces:
  - `/notes/` — feed of notes with inline photo strips (from theme's default `notes/list.html`)
  - `/books/` — grid of book cards
  - `/books/{slug}/` — single book page
  - `/links/` — dated list of curated links
  - `/music/` — track list
  - `/photos/` (aliased in menu as `/media/`) — photo grid using `.frames`

- [ ] **Step 1: Verify notes render as-shipped**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3
curl -s http://localhost:1313/notes/ | grep -c 'class="note"'
kill %1 2>/dev/null || true
```

Expected: a positive integer (one `.note` element per note). If zero, inspect `themes/harper/layouts/notes/list.html` and confirm Hugo's page kind matches — if notes are configured as `page` kind rather than section, the fix is to move the template to `_default/section.html` scoped by section name.

- [ ] **Step 2: Write books list template**

Create `themes/harper/layouts/books/list.html`:

```gotemplate
{{ define "main" }}
<div class="lede-block">
  <h1 class="page-title">{{ .Title }}</h1>
  {{ with .Content }}<div class="sub sub--intro">{{ . }}</div>{{ end }}
</div>

<ul class="book-list">
  {{ range .Pages.ByDate.Reverse }}
  <li class="book-list__row">
    {{ with .Params.cover }}<img class="book-list__cover" src="{{ . }}" alt="" loading="lazy">{{ end }}
    <div class="book-list__meta">
      <a class="book-list__title" href="{{ .RelPermalink }}">{{ .Title }}</a>
      {{ with .Params.author }}<span class="book-list__author">{{ i18n "by" }} {{ . }}</span>{{ end }}
      <span class="book-list__date">{{ .Date.Format "02 Jan 06" }}</span>
    </div>
  </li>
  {{ else }}
  <li class="post-list__empty">{{ i18n "no-books" | default "No books yet." }}</li>
  {{ end }}
</ul>
{{ end }}
```

- [ ] **Step 3: Write books single template**

Create `themes/harper/layouts/books/single.html`:

```gotemplate
{{ define "main" }}
<article class="post">
  <div class="post__meta">
    <span class="kicker">Book</span>
    <span class="post__date">{{ .Date.Format "02 Jan 2006" }}</span>
  </div>
  <h1 class="post__title">{{ .Title }}</h1>
  {{ with .Params.author }}<p class="post-note">{{ i18n "by" }} {{ . }}</p>{{ end }}
  {{ with .Params.cover }}<img class="book-single__cover" src="{{ . }}" alt="{{ i18n "book-cover-alt" }}">{{ end }}
  <div class="content">{{ .Content }}</div>
</article>
{{ end }}
```

- [ ] **Step 4: Write links list template**

Create `themes/harper/layouts/links/list.html`:

```gotemplate
{{ define "main" }}
<div class="lede-block">
  <h1 class="page-title">{{ .Title }}</h1>
  {{ with .Content }}<div class="sub sub--intro">{{ . }}</div>{{ end }}
</div>

<ul class="post-list">
  {{ range .Pages.ByDate.Reverse }}
  <li class="post-list__row">
    <span class="post-list__date">{{ .Date.Format "02 Jan 06" }}</span>
    {{ if .Params.link }}
    <a class="post-list__link" href="{{ .Params.link }}" target="_blank" rel="noopener noreferrer">{{ .Title }} ↪</a>
    {{ else }}
    <a class="post-list__link" href="{{ .RelPermalink }}">{{ .Title }}</a>
    {{ end }}
  </li>
  {{ else }}
  <li class="post-list__empty">{{ i18n "no-links" | default "No links yet." }}</li>
  {{ end }}
</ul>
{{ end }}
```

- [ ] **Step 5: Write music list template**

Create `themes/harper/layouts/music/list.html`:

```gotemplate
{{ define "main" }}
<div class="lede-block">
  <h1 class="page-title">{{ .Title }}</h1>
  {{ with .Content }}<div class="sub sub--intro">{{ . }}</div>{{ end }}
</div>

<ul class="post-list">
  {{ range .Pages.ByDate.Reverse }}
  <li class="post-list__row">
    <span class="post-list__date">{{ .Date.Format "02 Jan 06" }}</span>
    <a class="post-list__link" href="{{ .RelPermalink }}">
      {{ .Title }}{{ with .Params.artist }} <span class="post-list__by">{{ i18n "by" }} {{ . }}</span>{{ end }}
    </a>
  </li>
  {{ else }}
  <li class="post-list__empty">{{ i18n "no-music" | default "No music yet." }}</li>
  {{ end }}
</ul>
{{ end }}
```

- [ ] **Step 6: Write photos (media) list template**

Create `themes/harper/layouts/photos/list.html`:

```gotemplate
{{ define "main" }}
<div class="lede-block">
  <h1 class="page-title">{{ .Title }}</h1>
  {{ with .Content }}<div class="sub sub--intro">{{ . }}</div>{{ end }}
</div>

{{ $imgs := slice }}
{{ range (where site.RegularPages "Section" "notes").ByDate.Reverse }}
  {{ range .Params.images }}
    {{ $imgs = $imgs | append . }}
  {{ end }}
{{ end }}

{{ with $imgs }}
<div class="frames frames--four">
  {{ range first 24 . }}
  <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
  {{ end }}
</div>
{{ else }}
<p class="post-list__empty">No photos yet.</p>
{{ end }}
{{ end }}
```

- [ ] **Step 7: Append section-specific CSS to main.css**

Append to `themes/harper/static/css/main.css` (below the existing responsive block):

```css

/* ---------- Books ---------- */
.book-list { list-style: none; margin: 0; padding: 0; }
.book-list__row {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 16px;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--line);
}
.book-list__row:last-child { border-bottom: 0; }
.book-list__cover { width: 44px; height: 66px; object-fit: cover; border-radius: 3px; background: var(--bg2); }
.book-list__meta { display: flex; flex-direction: column; gap: 2px; }
.book-list__title { font-size: 16px; color: var(--ink); text-decoration: none; }
.book-list__title:hover { color: var(--acc); }
.book-list__author, .book-list__date { font-size: 13px; color: var(--mut); }
.book-single__cover {
  width: 160px;
  float: right;
  margin: 4px 0 20px 24px;
  border-radius: 4px;
  background: var(--bg2);
}
.post-list__by { color: var(--mut); font-weight: 400; }

@media (max-width: 640px) {
  .book-single__cover { float: none; margin: 0 0 20px; width: 120px; }
}
```

- [ ] **Step 8: Boot and verify each section URL**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

for path in /notes/ /books/ /links/ /music/ /photos/; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:1313$path")
  echo "$path → $code"
done

kill %1 2>/dev/null || true
```

Expected: each path returns `200`.

- [ ] **Step 9: Commit**

```bash
git add themes/harper/layouts/books/ themes/harper/layouts/links/ themes/harper/layouts/music/ themes/harper/layouts/photos/ themes/harper/static/css/main.css
git commit -m "feat(sections): add books/links/music/photos templates

- Books: cover + title/author/date rows, single with cover float
- Links: dated rows with external-link indicator when link param set
- Music: dated rows with 'by artist' inline
- Photos (/media/): pull image URLs from recent notes, 4-up grid
- Append section CSS to the theme's main.css"
```

---

## Task 4: About page + auto-stats

**Files:**
- Create: `content/about.md`
- Create: `content.es/about.md`
- Create: `content.ja/about.md`
- Create: `content.ko/about.md`
- Modify: `themes/harper/layouts/_default/about.html` (replace static stats with computed stats + notes-derived frames)
- Modify: `themes/harper/layouts/index.html` (frames strip pulls from notes' `images`)

**Interfaces:**
- Consumes: `site.Params.since` and `aboutFramesCount` from Task 1
- Produces:
  - `/about/`, `/es/about/`, `/ja/about/`, `/ko/about/` — About pages with auto-computed stats and notes-derived frame strip
  - Home page frame strip now pulls the 3 most recent images from notes

- [ ] **Step 1: Author `content/about.md`**

Create `content/about.md`:

```markdown
+++
title = "About"
layout = "about"
hello = "Hello."
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

My name is Harper Reed. This is my blog. I am a *computer operator* who likes
to make things, have fun, and hang out on the internet. Also pranks. And a
camera, always.
```

- [ ] **Step 2: Author Spanish about**

Create `content.es/about.md`:

```markdown
+++
title = "Acerca de"
layout = "about"
hello = "Hola."
closing = "Gracias por leer. Soy increíble."

[[contact]]
label = "harper@modest.com"
href = "mailto:harper@modest.com"
[[contact]]
label = "@harper.lol en bluesky"
href = "https://bsky.app/profile/harper.lol"
[[contact]]
label = "harperreed.com ↗"
href = "https://harperreed.com"
+++

Me llamo Harper Reed. Este es mi blog. Soy un *operador de computadoras* al
que le gusta hacer cosas, divertirse y pasar el rato en internet. También
bromas. Y una cámara, siempre.
```

- [ ] **Step 3: Author Japanese about**

Create `content.ja/about.md`:

```markdown
+++
title = "自己紹介"
layout = "about"
hello = "こんにちは。"
closing = "読んでくれてありがとう。私は素晴らしい。"

[[contact]]
label = "harper@modest.com"
href = "mailto:harper@modest.com"
[[contact]]
label = "bluesky で @harper.lol"
href = "https://bsky.app/profile/harper.lol"
[[contact]]
label = "harperreed.com ↗"
href = "https://harperreed.com"
+++

僕の名前はハーパー・リード。これは僕のブログです。僕はモノを作ったり、
楽しんだり、インターネットにいたりするのが好きな*コンピュータオペレーター*
です。あといたずらも。そしてカメラ、いつも。
```

- [ ] **Step 4: Author Korean about**

Create `content.ko/about.md`:

```markdown
+++
title = "소개"
layout = "about"
hello = "안녕하세요."
closing = "읽어주셔서 감사합니다. 저는 대단합니다."

[[contact]]
label = "harper@modest.com"
href = "mailto:harper@modest.com"
[[contact]]
label = "bluesky의 @harper.lol"
href = "https://bsky.app/profile/harper.lol"
[[contact]]
label = "harperreed.com ↗"
href = "https://harperreed.com"
+++

제 이름은 하퍼 리드입니다. 이곳은 제 블로그입니다. 저는 뭔가를 만들고,
재미있게 놀고, 인터넷에서 시간을 보내는 것을 좋아하는 *컴퓨터 조작자*
입니다. 장난도 좋아합니다. 그리고 항상 카메라와 함께요.
```

- [ ] **Step 5: Replace about.html with computed-stats version**

Overwrite `themes/harper/layouts/_default/about.html`:

```gotemplate
{{ define "main" }}
{{ $posts   := len (where site.RegularPages "Section" "post") }}
{{ $since   := site.Params.since | default 2001 }}
{{ $years   := sub now.Year $since }}
{{ $perWeek := 0.0 }}
{{ if gt $years 0 }}{{ $perWeek = div (float $posts) (mul $years 52) }}{{ end }}

{{ $frames := slice }}
{{ range (where site.RegularPages "Section" "notes").ByDate.Reverse }}
  {{ range .Params.images }}
    {{ $frames = $frames | append . }}
  {{ end }}
{{ end }}
{{ $framesCount := site.Params.aboutFramesCount | default 4 }}

<div class="about">
  <div class="about__band">
    <div class="about__intro">
      <h1 class="about__hello">{{ with .Params.hello }}{{ . }}{{ else }}Hello.{{ end }}</h1>
      <div class="content about__lede">{{ .Content }}</div>
      <div class="stats">
        <div class="stat">
          <div class="stat__num">{{ $years }}</div>
          <div class="stat__label">yrs blogging</div>
        </div>
        <div class="stat">
          <div class="stat__num">{{ $posts }}</div>
          <div class="stat__label">posts</div>
        </div>
        <div class="stat">
          <div class="stat__num">~{{ printf "%.2f" $perWeek }}</div>
          <div class="stat__label">/ week</div>
        </div>
      </div>
    </div>
    {{ with .Params.portrait }}
    <img class="about__portrait" src="{{ . | relURL }}" alt="Portrait of {{ site.Params.author }}">
    {{ end }}
  </div>

  {{ with .Params.contact }}
  <div class="about__contact">
    <span class="section-label">Contact</span>
    <div class="contact-list">
      {{ range . }}<a href="{{ .href }}">{{ .label }}</a>{{ end }}
    </div>
  </div>
  {{ end }}

  {{ with .Params.closing }}<p class="about__closing">{{ . }}</p>{{ end }}

  {{ with $frames }}
  <div class="about__frames">
    <span class="section-label">Selected frames</span>
    <div class="frames frames--four">
      {{ range first $framesCount . }}
      <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
      {{ end }}
    </div>
  </div>
  {{ end }}
</div>
{{ end }}
```

- [ ] **Step 6: Wire home-page frames to notes' images**

Replace the frames block in `themes/harper/layouts/index.html` (currently reads `site.Params.frames`) with a notes-derived pull:

Before:

```gotemplate
{{ with site.Params.frames }}
<h2 class="section-label section-label--spaced">Latest frames</h2>
<div class="frames frames--three">
  {{ range . }}
  <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
  {{ end }}
</div>
<a class="more-link more-link--muted" href="{{ "/notes/" | relURL }}">More in the notes →</a>
{{ end }}
```

After:

```gotemplate
{{ $homeFrames := slice }}
{{ range (where site.RegularPages "Section" "notes").ByDate.Reverse }}
  {{ range .Params.images }}
    {{ $homeFrames = $homeFrames | append . }}
  {{ end }}
{{ end }}
{{ $homeFramesCount := site.Params.homeFramesCount | default 3 }}
{{ with $homeFrames }}
<h2 class="section-label section-label--spaced">Latest frames</h2>
<div class="frames frames--three">
  {{ range first $homeFramesCount . }}
  <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
  {{ end }}
</div>
<a class="more-link more-link--muted" href="{{ "/notes/" | relURL }}">More in the notes →</a>
{{ else }}{{ with site.Params.frames }}
<h2 class="section-label section-label--spaced">Latest frames</h2>
<div class="frames frames--three">
  {{ range . }}
  <img class="frame" src="{{ . | relURL }}" alt="" loading="lazy">
  {{ end }}
</div>
{{ end }}{{ end }}
```

- [ ] **Step 7: Boot Hugo and verify the About pages render with real stats**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

for path in /about/ /es/about/ /ja/about/ /ko/about/; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:1313$path")
  echo "$path → $code"
done

curl -s http://localhost:1313/about/ | grep -Eo 'stat__num">[^<]+' | head -3

kill %1 2>/dev/null || true
```

Expected: all four paths return `200`. The `stat__num` grep should print three numbers — years, post count, ~per-week — matching current site state (e.g. `25`, `1451`, `~1.11`).

- [ ] **Step 8: Commit**

```bash
git add content/about.md content.es/about.md content.ja/about.md content.ko/about.md themes/harper/layouts/_default/about.html themes/harper/layouts/index.html
git commit -m "feat(about): add about pages in en/es/ja/ko with auto-stats

- Stats computed from site.RegularPages + params.since
- Frames pulled from recent notes' images param, with hand-curated fallback
- Home page frame strip switches to same notes-derived source"
```

---

## Task 5: i18n port

**Files:**
- Modify: `config/_default/menu.en.toml` (add explicit `[[main]]` entries)
- Modify: `config/_default/menu.es.toml`
- Modify: `config/_default/menu.ja.toml`
- Modify: `config/_default/menu.ko.toml`
- Modify: `i18n/en.yaml`, `i18n/es.yaml`, `i18n/ja.yaml`, `i18n/ko.yaml` (add redesign labels)
- Create: `themes/harper/layouts/partials/language-switcher.html`
- Modify: `themes/harper/layouts/partials/header.html` (include switcher)
- Create: `themes/harper/layouts/partials/head/seo.html` (temporarily emits hreflang only; Task 6 expands it)
- Modify: `themes/harper/layouts/partials/head.html` (include SEO partial)

**Interfaces:**
- Consumes: Task 1's theme, Task 4's about pages (all four languages exist)
- Produces:
  - `site.Menus.main` populated in all four language menu files
  - i18n string keys: `latestFrames`, `morePosts`, `selectedFrames`, `contact`, `writtenByHuman`, `nothingHereYet`, `moreInNotes`, `subscribeViaRSS`, `sayHi`
  - `partial "language-switcher.html"` renders in masthead
  - `partial "head/seo.html"` emits hreflang tags

- [ ] **Step 1: Populate English main menu**

Append to `config/_default/menu.en.toml` (below the existing content):

```toml
[[main]]
identifier = "home"
name = "Home"
url = "/"
weight = 1

[[main]]
identifier = "posts"
name = "Posts"
url = "/post/"
weight = 2

[[main]]
identifier = "notes"
name = "Notes"
url = "/notes/"
weight = 3

[[main]]
identifier = "books"
name = "Books"
url = "/books/"
weight = 4

[[main]]
identifier = "links"
name = "Links"
url = "/links/"
weight = 5

[[main]]
identifier = "music"
name = "Music"
url = "/music/"
weight = 6

[[main]]
identifier = "media"
name = "Media"
url = "/photos/"
weight = 7

[[main]]
identifier = "about"
name = "About"
url = "/about/"
weight = 8

[[main]]
identifier = "now"
name = "Now"
url = "/now/"
weight = 9
```

Note: the existing `[[main]]` entry with `identifier = "contact"` at weight 6 collides. Bump the contact entry's weight to `99` so it lands at the end (or delete it — contact reaches users via the About page now).

- [ ] **Step 2: Populate Spanish main menu**

Overwrite `config/_default/menu.es.toml` similarly, with Spanish names:

```toml
[[main]]
identifier = "home"
name = "Inicio"
url = "/es/"
weight = 1

[[main]]
identifier = "posts"
name = "Entradas"
url = "/es/post/"
weight = 2

[[main]]
identifier = "notes"
name = "Notas"
url = "/es/notes/"
weight = 3

[[main]]
identifier = "books"
name = "Libros"
url = "/es/books/"
weight = 4

[[main]]
identifier = "links"
name = "Enlaces"
url = "/es/links/"
weight = 5

[[main]]
identifier = "music"
name = "Música"
url = "/es/music/"
weight = 6

[[main]]
identifier = "media"
name = "Fotos"
url = "/es/photos/"
weight = 7

[[main]]
identifier = "about"
name = "Acerca"
url = "/es/about/"
weight = 8
```

Note: preserve any pre-existing `[[footer]]` or contact entries — this instruction only adds `[[main]]` entries.

- [ ] **Step 3: Populate Japanese main menu**

Same pattern in `config/_default/menu.ja.toml` with Japanese labels: `ホーム`, `記事`, `ノート`, `本`, `リンク`, `音楽`, `写真`, `自己紹介`. URLs are `/ja/...`.

- [ ] **Step 4: Populate Korean main menu**

Same pattern in `config/_default/menu.ko.toml`: `홈`, `글`, `노트`, `책`, `링크`, `음악`, `사진`, `소개`. URLs are `/ko/...`.

- [ ] **Step 5: Add redesign i18n keys to en.yaml**

Append to `i18n/en.yaml`:

```yaml
- id: latestFrames
  translation: "Latest frames"

- id: selectedFrames
  translation: "Selected frames"

- id: contact
  translation: "Contact"

- id: writtenByHuman
  translation: "This post was written {{ . }}% by a human."

- id: nothingHereYet
  translation: "Nothing here yet."

- id: moreInNotes
  translation: "More in the notes →"

- id: subscribeViaRSS
  translation: "Subscribe via"

- id: sayHi
  translation: "or say hi at"

- id: no-books
  translation: "No books found"
```

- [ ] **Step 6: Add redesign i18n keys to es.yaml**

Append to `i18n/es.yaml`:

```yaml
- id: latestFrames
  translation: "Fotos recientes"

- id: selectedFrames
  translation: "Fotos seleccionadas"

- id: contact
  translation: "Contacto"

- id: writtenByHuman
  translation: "Este artículo fue escrito {{ . }}% por un humano."

- id: nothingHereYet
  translation: "Aún no hay nada aquí."

- id: moreInNotes
  translation: "Más en las notas →"

- id: subscribeViaRSS
  translation: "Suscríbete vía"

- id: sayHi
  translation: "o saluda a"

- id: no-books
  translation: "No hay libros"
```

- [ ] **Step 7: Add redesign i18n keys to ja.yaml**

Append to `i18n/ja.yaml`:

```yaml
- id: latestFrames
  translation: "最新の写真"

- id: selectedFrames
  translation: "選りすぐりの写真"

- id: contact
  translation: "連絡先"

- id: writtenByHuman
  translation: "この記事は{{ . }}%人間が書きました。"

- id: nothingHereYet
  translation: "まだ何もありません。"

- id: moreInNotes
  translation: "もっとノートを見る →"

- id: subscribeViaRSS
  translation: "購読は"

- id: sayHi
  translation: "こんにちは、"

- id: no-books
  translation: "本が見つかりません"
```

- [ ] **Step 8: Add redesign i18n keys to ko.yaml**

Append to `i18n/ko.yaml`:

```yaml
- id: latestFrames
  translation: "최신 사진"

- id: selectedFrames
  translation: "선택된 사진"

- id: contact
  translation: "연락처"

- id: writtenByHuman
  translation: "이 글은 {{ . }}% 사람이 작성했습니다."

- id: nothingHereYet
  translation: "아직 아무것도 없습니다."

- id: moreInNotes
  translation: "노트에서 더 보기 →"

- id: subscribeViaRSS
  translation: "구독"

- id: sayHi
  translation: "인사하기"

- id: no-books
  translation: "책을 찾을 수 없습니다"
```

- [ ] **Step 9: Write the language switcher partial**

Create `themes/harper/layouts/partials/language-switcher.html`:

```gotemplate
{{ $cur := . }}
{{ if gt (len site.Languages) 1 }}
<span class="lang-switch">
  {{ range site.Languages }}
    {{ $code := .Lang }}
    {{ $label := upper $code }}
    {{ $href := printf "/%s/" $code }}
    {{ if eq $code "en" }}{{ $href = "/" }}{{ end }}
    {{ with $cur.AllTranslations }}
      {{ range . }}
        {{ if eq .Lang $code }}{{ $href = .RelPermalink }}{{ end }}
      {{ end }}
    {{ end }}
    <a href="{{ $href }}"
       class="lang-switch__link{{ if eq site.Language.Lang $code }} is-active{{ end }}">{{ $label }}</a>
  {{ end }}
</span>
{{ end }}
```

- [ ] **Step 10: Wire the switcher into the masthead**

Edit `themes/harper/layouts/partials/header.html`. Insert the switcher between the last `nav__link` and the `RSS` chip:

Before:

```gotemplate
      {{ end }}
      {{ with .OutputFormats.Get "rss" }}
```

After:

```gotemplate
      {{ end }}
      {{ partial "language-switcher.html" . }}
      {{ with .OutputFormats.Get "rss" }}
```

- [ ] **Step 11: Append language-switcher CSS**

Append to `themes/harper/static/css/main.css`:

```css

/* ---------- Language switcher ---------- */
.lang-switch { display: inline-flex; gap: 8px; margin-left: 8px; padding-left: 12px; border-left: 1px solid var(--line); }
.lang-switch__link { font-size: 12px; letter-spacing: .08em; color: var(--mut); text-decoration: none; text-transform: uppercase; }
.lang-switch__link:hover { color: var(--ink); }
.lang-switch__link.is-active { color: var(--ink); }

@media (max-width: 640px) {
  .lang-switch { margin-left: 0; padding-left: 0; border-left: 0; }
}
```

- [ ] **Step 12: Write the SEO/hreflang head partial (hreflang only for now)**

Create `themes/harper/layouts/partials/head/seo.html`:

```gotemplate
{{/* Canonical */}}
<link rel="canonical" href="{{ .Permalink }}">

{{/* hreflang links for translations */}}
{{ if .IsTranslated }}
  {{ range .AllTranslations }}
    <link rel="alternate" hreflang="{{ .Lang }}" href="{{ .Permalink }}">
  {{ end }}
{{ end }}
```

- [ ] **Step 13: Include the SEO partial in head.html**

Edit `themes/harper/layouts/partials/head.html`. Below the existing `<link rel="stylesheet" ...>` line, add:

```gotemplate
{{ partial "head/seo.html" . }}
```

- [ ] **Step 14: Boot Hugo and verify i18n behavior**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

echo "=== English home ==="
curl -s http://localhost:1313/ | grep -c 'lang-switch__link'
echo "=== Spanish home ==="
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:1313/es/
echo "=== hreflang on about ==="
curl -s http://localhost:1313/about/ | grep 'hreflang' | head -5
echo "=== nav item count ==="
curl -s http://localhost:1313/ | grep -c 'class="nav__link'

kill %1 2>/dev/null || true
```

Expected: switcher renders 4+ links on the home page (one per language). Spanish home returns `200`. hreflang tags for translations appear on `/about/`. Nav item count is ≥8 (all sections listed).

- [ ] **Step 15: Commit**

```bash
git add config/_default/menu.en.toml config/_default/menu.es.toml config/_default/menu.ja.toml config/_default/menu.ko.toml \
        i18n/en.yaml i18n/es.yaml i18n/ja.yaml i18n/ko.yaml \
        themes/harper/layouts/partials/language-switcher.html \
        themes/harper/layouts/partials/header.html \
        themes/harper/layouts/partials/head/seo.html \
        themes/harper/layouts/partials/head.html \
        themes/harper/static/css/main.css
git commit -m "feat(i18n): port language switcher, menus, and hreflang into harper

- Explicit main-menu entries in en/es/ja/ko toml files
- Redesign i18n keys added to all four language files
- Inline language switcher between nav and RSS chip in the masthead
- hreflang tags emitted in head/seo.html partial"
```

---

## Task 6: Feature port (Bluesky comments, Tinylytics, SEO, related posts)

**Files:**
- Overwrite: `themes/harper/layouts/partials/related-posts.html`
- Overwrite: `themes/harper/layouts/partials/bluesky-comments.html`
- Create: `themes/harper/layouts/partials/tinylytics.html`
- Modify: `themes/harper/layouts/partials/head/seo.html` (add OG + Twitter + description)
- Modify: `themes/harper/layouts/_default/baseof.html` (include tinylytics before `</body>`)
- Copy: `static/js/bluesky_comments.js` continues to be served (no move needed — Hugo picks up site-level `static/`)

**Interfaces:**
- Consumes: Task 2 slot markers in `single.html`, Task 5's `head/seo.html`
- Produces:
  - `partial "related-posts.html"` renders `.more` block with 3 posts
  - `partial "bluesky-comments.html"` renders the Bluesky embed
  - `partial "tinylytics.html"` renders analytics beacon
  - OG/Twitter/description meta tags emitted in `<head>` for every page

- [ ] **Step 1: Write the related-posts partial**

Overwrite `themes/harper/layouts/partials/related-posts.html`:

```gotemplate
{{ $more := where (where site.RegularPages "Section" "post") "Permalink" "!=" .Permalink }}
{{ with first 3 $more }}
<section class="more">
  <span class="section-label">{{ i18n "morePosts" | default "More posts" }}</span>
  <div class="more__list">
    {{ range . }}
    <a class="more__row" href="{{ .RelPermalink }}">
      <span class="more__date">{{ .Date.Format "02 Jan 06" }}</span>
      <span class="more__title">{{ .Title }}</span>
    </a>
    {{ end }}
  </div>
</section>
{{ end }}
```

Then remove the duplicate `$more :=` block from `themes/harper/layouts/_default/single.html` (the one we left there in Task 1). After this task, `single.html`'s bottom looks like:

```gotemplate
{{ if eq .Section "post" }}
{{ partial "related-posts.html" . }}
{{ partial "bluesky-comments.html" . }}
{{ end }}
{{ end }}
```

- [ ] **Step 2: Write the Bluesky comments partial**

Overwrite `themes/harper/layouts/partials/bluesky-comments.html`:

```gotemplate
{{ if and (eq .Section "post") .Params.bluesky_url }}
<section class="comments">
  <span class="section-label">Comments</span>
  <div id="bsky-comments" data-url="{{ .Params.bluesky_url }}"></div>
  <script src="{{ "js/bluesky_comments.js" | relURL }}" defer></script>
</section>
{{ end }}
```

Note: The existing site drives Bluesky threads off a per-post `bluesky_url` frontmatter param. Posts without that param render no comments block.

- [ ] **Step 3: Append comments styling**

Append to `themes/harper/static/css/main.css`:

```css

/* ---------- Comments ---------- */
.comments {
  max-width: var(--read);
  margin: 36px auto 0;
  padding-top: 24px;
  border-top: 1px solid var(--line);
}
.comments .section-label { margin: 0 0 12px; }
```

- [ ] **Step 4: Write the Tinylytics partial**

Read the existing site partial or param name for the Tinylytics site ID:

```bash
grep -R "tinylytics" layouts/ static/js/ config/_default/ 2>/dev/null | head -20
```

If a site ID is present, create `themes/harper/layouts/partials/tinylytics.html` (replace `SITE_ID` with the actual identifier surfaced by the grep):

```gotemplate
{{ if hugo.IsProduction }}
<script defer src="https://tinylytics.app/embed/{{ site.Params.tinylytics }}.js"></script>
{{ end }}
```

Set the site ID in `config/_default/params.toml`:

```toml
tinylytics = "SITE_ID"
```

- [ ] **Step 5: Include Tinylytics in baseof.html**

Edit `themes/harper/layouts/_default/baseof.html`. Before `</body>`, add:

```gotemplate
{{ partial "tinylytics.html" . }}
```

Final `baseof.html`:

```gotemplate
<!DOCTYPE html>
<html lang="{{ site.LanguageCode | default "en-us" }}" data-theme="light">
<head>
  {{ partial "head.html" . }}
</head>
<body>
  {{ partial "header.html" . }}
  <main class="site">
    {{ block "main" . }}{{ end }}
  </main>
  {{ partial "footer.html" . }}
  <script src="{{ "js/theme.js" | relURL }}" defer></script>
  {{ partial "tinylytics.html" . }}
</body>
</html>
```

- [ ] **Step 6: Expand head/seo.html with OG + Twitter + description**

Overwrite `themes/harper/layouts/partials/head/seo.html`:

```gotemplate
{{/* Canonical */}}
<link rel="canonical" href="{{ .Permalink }}">

{{/* hreflang links for translations */}}
{{ if .IsTranslated }}
  {{ range .AllTranslations }}
    <link rel="alternate" hreflang="{{ .Lang }}" href="{{ .Permalink }}">
  {{ end }}
{{ end }}

{{/* Description */}}
{{ $desc := "" }}
{{ if .Description }}{{ $desc = .Description }}
{{ else if .IsPage }}{{ $desc = .Summary | plainify | truncate 200 }}
{{ else }}{{ $desc = site.Params.description }}{{ end }}
<meta name="description" content="{{ $desc }}">

{{/* OG image resolution: per-page image, else site default */}}
{{ $ogImage := site.Params.default_social_image | default "/images/og.png" }}
{{ with .Params.image }}{{ $ogImage = . }}{{ end }}
{{ $ogImage = $ogImage | absURL }}

{{/* Open Graph */}}
<meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
<meta property="og:title" content="{{ .Title }}">
<meta property="og:description" content="{{ $desc }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:image" content="{{ $ogImage }}">
<meta property="og:site_name" content="{{ site.Title }}">
{{ if .IsPage }}
{{ with .PublishDate }}<meta property="article:published_time" content="{{ .Format "2006-01-02T15:04:05Z07:00" }}">{{ end }}
{{ with .Lastmod }}<meta property="article:modified_time" content="{{ .Format "2006-01-02T15:04:05Z07:00" }}">{{ end }}
{{ end }}

{{/* Twitter */}}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ .Title }}">
<meta name="twitter:description" content="{{ $desc }}">
<meta name="twitter:image" content="{{ $ogImage }}">
{{ with site.Params.twitter_handle }}<meta name="twitter:site" content="@{{ . }}">{{ end }}
```

Also remove the duplicate `<meta name="description" ...>` line from `themes/harper/layouts/partials/head.html` — the SEO partial now owns it.

- [ ] **Step 7: Sanity check the head partial doesn't double-emit description**

```bash
grep -c 'name="description"' themes/harper/layouts/partials/head.html
```

Expected: `0` (the description now lives only in `head/seo.html`).

- [ ] **Step 8: Verify features render**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

# Pick a post with bluesky_url
POST_URL=$(curl -s http://localhost:1313/post/ | grep -oE 'href="[^"]+/post/[^"]+"' | head -1 | sed 's/href="//;s/"//')
echo "Sample post: $POST_URL"

# Check meta tags
curl -s "http://localhost:1313$POST_URL" | grep -E 'og:image|twitter:card|hreflang|"more "' | head -10
# Check tinylytics
curl -s "http://localhost:1313$POST_URL" | grep -i tinylytics

kill %1 2>/dev/null || true
```

Expected: `og:image`, `twitter:card` present. Tinylytics script tag omitted in dev (`hugo.IsProduction` false during `hugo server`). Related posts (`class="more"`) present in HTML body.

- [ ] **Step 9: Commit**

```bash
git add themes/harper/layouts/ themes/harper/static/css/main.css config/_default/params.toml
git commit -m "feat(features): port bluesky comments, tinylytics, seo, related posts

- related-posts partial replaces inline block in single.html
- bluesky-comments partial gated on post section + bluesky_url param
- tinylytics partial injected before </body>, prod-only
- head/seo.html emits canonical, hreflang, OG, Twitter, description"
```

---

## Task 7: Cleanup

**Files:**
- Delete: `static/css/root-colors.css`, `harper.css`, `shared.css`, `themes.css`, `bsky_comments.css`, `outofdate.css`, `ai-disclosure.css`, `image-loading.css`, `tinylytics.css`, `media.css`, `books.css`, `music.css`, `links.css`, `notes.css`, `notes-grid.css`, `code.css`, `translations.css`, `syntax.css`
- Delete: `layouts/partials/theme-chooser.html`, `layouts/partials/comments.html`, `layouts/partials/generated.html`, `layouts/partials/get-featured-image.html`, `layouts/partials/nav.html`, `layouts/partials/out_of_date.html`, `layouts/partials/pagination.html`, `layouts/partials/post-translations.html`, `layouts/partials/social_card.html`, `layouts/partials/tags.html`, `layouts/partials/language-switcher.html`
- Delete: `layouts/_default/baseof.html`, `layouts/index.html` (theme now owns these)
- Delete: `static/js/image-loading.js` (only if grep confirms no reference)
- Modify: `config/_default/params.toml` (delete commented-out lines from Task 1)

**Interfaces:**
- Consumes: everything from Tasks 1-6
- Produces: production-clean repo, `hugo --gc --minify` succeeds with zero warnings

- [ ] **Step 1: Delete legacy CSS files**

```bash
cd /Users/harper/Public/src/personal/harper.blog
rm -f static/css/root-colors.css \
      static/css/harper.css \
      static/css/shared.css \
      static/css/themes.css \
      static/css/bsky_comments.css \
      static/css/outofdate.css \
      static/css/ai-disclosure.css \
      static/css/image-loading.css \
      static/css/tinylytics.css \
      static/css/media.css \
      static/css/books.css \
      static/css/music.css \
      static/css/links.css \
      static/css/notes.css \
      static/css/notes-grid.css \
      static/css/code.css \
      static/css/translations.css \
      static/css/syntax.css
ls static/css/
```

Expected: empty (or only files this plan didn't enumerate; inspect manually before deleting anything unexpected).

- [ ] **Step 2: Delete retired site-level partials**

```bash
rm -f layouts/partials/theme-chooser.html \
      layouts/partials/comments.html \
      layouts/partials/generated.html \
      layouts/partials/get-featured-image.html \
      layouts/partials/nav.html \
      layouts/partials/out_of_date.html \
      layouts/partials/pagination.html \
      layouts/partials/post-translations.html \
      layouts/partials/social_card.html \
      layouts/partials/tags.html \
      layouts/partials/language-switcher.html
ls layouts/partials/
```

- [ ] **Step 3: Delete site-level layouts the theme now owns**

```bash
rm -f layouts/_default/baseof.html layouts/index.html
ls layouts/_default/
```

Expected: `media.rss.xml` remains (media RSS is bespoke — do NOT delete).

- [ ] **Step 4: Grep for image-loading.js references before deleting**

```bash
grep -R "image-loading" layouts/ themes/ config/ 2>/dev/null
```

If no output, delete:

```bash
rm -f static/js/image-loading.js
```

- [ ] **Step 5: Delete the commented-out lines in params.toml**

Edit `config/_default/params.toml`. Delete the lines:

```
# themeStyle = "harper"
# customcss = [ ... ]
# customjs = [ ... ]
```

(They were commented in Task 1; now they can be removed entirely.)

- [ ] **Step 6: Full production build**

```bash
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info 2>&1 | tee /tmp/hugo-build.log | tail -30
```

Expected: `Total in ...` at the end; no `ERROR` lines. If ERRORs appear, resolve before proceeding.

- [ ] **Step 7: Sanity-check the build output**

```bash
du -sh public/
find public -name '*.html' | wc -l
grep -R "hugo-bearcub" public/ 2>/dev/null | head -3
```

Expected: `du` reasonable (tens to hundreds of MB depending on images), HTML file count roughly matches page count from build log, no `hugo-bearcub` references in output.

- [ ] **Step 8: Spot-check 10 random URLs end-to-end**

```bash
hugo server --buildDrafts --buildFuture --port 1313 &
sleep 3

for path in \
  "/" \
  "/post/" \
  "/notes/" \
  "/books/" \
  "/links/" \
  "/music/" \
  "/photos/" \
  "/about/" \
  "/es/" \
  "/ja/about/"
do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:1313$path")
  echo "$path → $code"
done

kill %1 2>/dev/null || true
```

Expected: every path returns `200`.

- [ ] **Step 9: Commit**

```bash
git add -A
git commit -m "chore(cleanup): remove legacy bearcub CSS, partials, and layouts

- Delete 18 legacy static/css files superseded by themes/harper/static/css/main.css
- Delete 11 legacy layouts/partials the redesign doesn't need
- Delete site-level _default/baseof.html and index.html (theme owns them)
- Remove commented themeStyle/customcss/customjs from params.toml
- Delete unused image-loading.js"
```

- [ ] **Step 10: Open PR from redesign → main**

```bash
git push -u origin redesign
gh pr create --title "Blog redesign: text-led minimal (harper theme)" --body "$(cat <<'EOF'
## Summary
- Full theme swap from hugo-bearcub to the new self-contained harper theme
- Preserves 1,451 /post/ URLs, en/es/ja/ko content, and existing feature set
- Rebuilds Bluesky comments, Tinylytics, SEO/OG cards, related posts against redesign tokens

## Test plan
- [ ] Netlify preview builds without errors
- [ ] Spot-check 10 random posts across years render cleanly
- [ ] Home, /about/, /notes/, /books/, /links/, /music/, /photos/ all 200
- [ ] Spanish/Japanese/Korean variants render with translated nav
- [ ] Light/dark toggle works with no flash
- [ ] View page source: OG/Twitter/hreflang tags present
- [ ] Bluesky comments appear on posts with `bluesky_url` set
- [ ] Tinylytics beacon fires in production build
EOF
)"
```

Expected: PR URL returned. Netlify posts a preview URL as a check on the PR.

---

## Self-Review

Ran the four checks against the spec (`docs/superpowers/specs/2026-07-01-blog-redesign-design.md`):

**Spec coverage:**
- Full theme swap → Task 1
- Preserve /post/ URLs → Task 1 step 7-8
- Keep en/es/ja/ko → Task 5
- Nav: Posts/Notes/Books/Links/Music/Media/About/Now → Task 5 step 1
- Media = in-site photos grid → Task 3 step 6
- Auto-computed about stats → Task 4 step 5
- Notes-derived frames → Task 4 steps 5-6
- Bluesky comments port → Task 6 steps 2-3
- Tinylytics port → Task 6 steps 4-5
- SEO/OG/Twitter cards → Task 6 step 6
- Related posts → Task 6 step 1
- Light/dark toggle → shipped in theme (Task 1)
- Drop theme chooser → Task 7 steps 1-2 (delete themes.css, root-colors.css, theme-chooser.html)
- 7 phased commits → Tasks 1-7 each end in one commit
- All success criteria in spec map to specific verification steps

**Placeholder scan:** None of the "TBD / TODO / add appropriate error handling / write tests for the above" patterns present. Every step has concrete code, exact paths, and expected command output.

**Type consistency:** `themes/harper/layouts/partials/related-posts.html`, `bluesky-comments.html`, `tinylytics.html`, `head/seo.html`, `language-switcher.html` — all created with consistent names, referenced with the same names in `single.html`, `baseof.html`, `header.html`, `head.html`. `site.Params.since`, `homeFramesCount`, `aboutFramesCount`, `tinylytics` names used identically in params.toml, index.html, about.html, tinylytics.html.

One tricky spot flagged for the executor: **Task 6 step 4** requires discovering the Tinylytics site ID before writing the partial. If the grep in step 4 returns nothing (unlikely, given `/static/css/tinylytics.css` exists), the executor should pause and ask Doctor Biz for the ID rather than guessing.
