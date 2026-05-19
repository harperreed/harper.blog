{{- /* ABOUTME: Generates /sitemap.md — markdown sitemap at site root for a14y. */ -}}
{{- /* ABOUTME: Curated, human/LLM-readable map of all site sections and recent pages. */ -}}
# Sitemap — {{ .Site.Title }}

Last generated: {{ now.Format "2006-01-02" }}

Site: {{ .Site.BaseURL }}
Author: {{ .Site.Params.author.name | default "Harper Reed" }}

## Top-level pages

- [Home]({{ .Site.BaseURL }})
- [About]({{ .Site.BaseURL }}about/)
- [Colophon]({{ .Site.BaseURL }}colophon/)
- [Translations]({{ .Site.BaseURL }}translations/)

## Sections

{{ $sections := slice "post" "notes" "links" "books" "music" }}
{{ range $sections }}
{{ $sectionName := . }}
{{ with $.Site.GetPage (printf "/%s" $sectionName) }}
### [{{ .Title }}]({{ .Permalink }})

{{ $pages := .RegularPages.ByDate.Reverse }}
{{ if $pages }}
Recent in this section ({{ len $pages }} total):
{{ range first 15 $pages }}
- [{{ .Title }}]({{ .Permalink }}) — {{ .Date.Format "2006-01-02" }}
{{- end }}
{{ end }}
{{ end }}
{{ end }}

## Other languages

{{ range .Site.Languages }}{{ if ne .Lang $.Site.Language.Lang }}
- [{{ .LanguageName }}]({{ $.Site.BaseURL }}{{ .Lang }}/)
{{- end }}{{ end }}

## Machine-readable formats

- [sitemap.xml]({{ .Site.BaseURL }}sitemap.xml) — XML sitemap with all URLs and lastmod
- [llms.txt]({{ .Site.BaseURL }}llms.txt) — LLM-friendly index
- [AGENTS.md]({{ .Site.BaseURL }}AGENTS.md) — agent skill manifest
- [RSS]({{ .Site.BaseURL }}index.xml) — RSS feed
