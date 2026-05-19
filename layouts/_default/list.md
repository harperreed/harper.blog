{{- /* ABOUTME: Markdown mirror of a section/list page for AI/LLM agents (a14y). */ -}}
{{- /* ABOUTME: Lists all pages in the section with titles, dates, and URLs. */ -}}
{{- $description := "" -}}
{{- with .Description -}}{{ $description = . }}{{- end -}}
{{- if not $description -}}{{ $description = printf "Index of pages under %q on %s." .Title .Site.Title }}{{- end -}}
{{- $lastmod := .Lastmod -}}
{{- if $lastmod.IsZero -}}{{ $lastmod = now }}{{- end -}}
---
title: {{ .Title | jsonify }}
description: {{ $description | jsonify }}
last_updated: {{ $lastmod.Format "2006-01-02T15:04:05Z07:00" }}
doc_version: {{ $lastmod.Format "2006-01-02" | jsonify }}
url: {{ with .OutputFormats.Get "html" }}{{ .Permalink }}{{ else }}{{ $.Permalink }}{{ end }}
language: {{ .Language.Lang }}
---

# {{ .Title }}

{{ with .Content }}{{ . | plainify }}{{ end }}

{{ if .Pages }}
## Pages

{{ range .Pages.ByDate.Reverse }}
- [{{ .Title }}]({{ .Permalink }}) — {{ .Date.Format "2006-01-02" }}{{ with .Description }} — {{ . | plainify }}{{ end }}
{{- end }}
{{ end }}

## Sitemap

- Site index: [{{ .Site.BaseURL }}]({{ .Site.BaseURL }})
- All pages: [sitemap.xml]({{ .Site.BaseURL }}sitemap.xml) · [sitemap.md]({{ .Site.BaseURL }}sitemap.md)
- Agent guide: [AGENTS.md]({{ .Site.BaseURL }}AGENTS.md) · [llms.txt]({{ .Site.BaseURL }}llms.txt)
