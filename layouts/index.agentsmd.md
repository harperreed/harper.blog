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

## How agents should use this site

- Prefer the **Markdown mirror** (`{url}index.md`) over the HTML when consuming content programmatically — it strips template chrome.
- Use **sitemap.xml** for full enumeration; **sitemap.md** for a curated, human-readable overview.
- Respect **robots.txt** at {{ .Site.BaseURL }}robots.txt. AI training is currently allowed via `Content-Signal: ai-train=yes, search=yes, ai-generate=yes`.
- Each post has JSON-LD `BlogPosting` with author, `datePublished`, `dateModified`, language, and tags.

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
  - 2026-05-19 — 67 (scorecard 0.2.0)
