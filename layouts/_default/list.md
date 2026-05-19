{{- /* ABOUTME: Markdown mirror of a section/list page for AI/LLM agents (a14y). */ -}}
{{- /* ABOUTME: Lists all pages in the section with titles, dates, and URLs. */ -}}
---
title: {{ .Title | jsonify }}
{{- with .Lastmod }}
lastmod: {{ .Format "2006-01-02T15:04:05Z07:00" }}
{{- end }}
{{- with .Description }}
description: {{ . | jsonify }}
{{- end }}
url: {{ .Permalink }}
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
