{{- /* ABOUTME: Generates /AGENTS.md — agent skill manifest at site root for a14y. */ -}}
{{- /* ABOUTME: Describes the site so AI/LLM agents can navigate and use its content. */ -}}
# AGENTS.md — {{ .Site.Title }}

> Agent-readable guide to {{ .Site.BaseURL }} for AI/LLM agents, crawlers, and coding assistants.

## About

{{ .Site.Title }} is the personal blog of {{ .Site.Params.author.name | default "Harper Reed" }}.
The site covers long-form essays on engineering, AI/LLMs, and product work, alongside short-form
notes, curated links, books I've read, and music I've listened to.

- **Author:** {{ .Site.Params.author.name | default "Harper Reed" }} (<{{ .Site.Params.email }}>)
- **Base URL:** {{ .Site.BaseURL }}
- **Generator:** Hugo (static site)
- **Languages:** {{ range $i, $lang := .Site.Languages }}{{ if $i }}, {{ end }}{{ $lang.LanguageName }} (`/{{ $lang.Lang }}/`){{ end }}

## Content sections

- **Posts** — long-form essays. Index: {{ .Site.BaseURL }}posts/
- **Notes** — short micro-posts (automated from JSON feeds). Index: {{ .Site.BaseURL }}notes/
- **Links** — curated links (automated from RSS). Index: {{ .Site.BaseURL }}links/
- **Books** — reading list (Goodreads integration). Index: {{ .Site.BaseURL }}books/
- **Music** — Spotify tracks. Index: {{ .Site.BaseURL }}music/
- **About** — {{ .Site.BaseURL }}about/
- **Colophon / Glossary** — terminology, tooling, and credits: {{ .Site.BaseURL }}colophon/

## Machine-readable endpoints

- **Sitemap (XML):** {{ .Site.BaseURL }}sitemap.xml
- **Sitemap (Markdown):** {{ .Site.BaseURL }}sitemap.md
- **llms.txt:** {{ .Site.BaseURL }}llms.txt
- **RSS (all posts):** {{ .Site.BaseURL }}index.xml
- **Markdown mirror:** every page is also served as Markdown at `{permalink}index.md` (linked via `<link rel="alternate" type="text/markdown">`).

## Installation

This is a public website, not a package. No installation required to read it. Agents and crawlers can fetch any URL directly with HTTP GET. If you want a local copy of the source:

```bash
git clone https://github.com/harperreed/harper.blog.git
cd harper.blog
hugo serve --buildDrafts --buildFuture   # local preview at http://localhost:1313/
```

The site is built with Hugo (see Generator above) and deployed to Netlify.

## Usage

How agents should consume this site:

- **Read Markdown over HTML.** Prefer the `.md` mirror at `{permalink}index.md` — it strips template chrome and gives you the article body plus YAML frontmatter (title, description, date, tags, language).
- **Use the sitemap for enumeration.** `sitemap.xml` is the canonical list of every URL. `sitemap.md` is a human-readable overview.
- **Use `llms.txt` for a curated quick-start.** Lists primary sections and the most recent posts. Useful for one-shot context.
- **Respect `robots.txt`.** AI training is currently allowed via `Content-Signal: ai-train=yes, search=yes, ai-generate=yes`. This is a personal blog — please rate-limit yourself.
- **Discover structure via JSON-LD.** Every post emits a `BlogPosting` block with author, `datePublished`, `dateModified`, language, and tags. Every page emits a `BreadcrumbList`.
- **Languages:** content is mirrored across English, 日本語, Español, 한국어, 中文, and Indonesia. Use the `language` field in the Markdown frontmatter or the `<html lang>` attribute to pick the right one.

## Configuration

This site is statically generated. There is no per-agent configuration to set — fetch and parse normally. See the **a14y configuration** section below for the agent-readability audit settings.

## Recent long-form posts

{{ $posts := where .Site.RegularPages "Section" "post" }}
{{ range first 15 $posts.ByDate.Reverse }}
- [{{ .Title }}]({{ .Permalink }}) — {{ .Date.Format "2006-01-02" }}
{{- end }}

## Contact

- Email: <{{ .Site.Params.email }}>
- Profile / links: <https://harper.lol>

## a14y configuration

- Target URL: {{ .Site.BaseURL }}
- Scorecard: 0.2.0
- Mode: site
- Last runs:
  - 2026-05-19 — 72 (scorecard 0.2.0, deploy-preview-151)
  - 2026-05-19 — 67 (scorecard 0.2.0)
