{{- /* ABOUTME: Markdown mirror of a single page for AI/LLM agents (a14y). */ -}}
{{- /* ABOUTME: Renders YAML frontmatter plus the page's markdown content as text/markdown. */ -}}
{{- $description := "" -}}
{{- with .Description -}}{{ $description = . }}{{- end -}}
{{- if not $description -}}{{ with .Summary }}{{ $description = . | plainify | truncate 200 }}{{ end }}{{- end -}}
{{- if not $description -}}{{ $description = .Site.Params.description | default (printf "Page on %s." .Site.Title) }}{{- end -}}
{{- $lastmod := .Lastmod -}}
{{- if $lastmod.IsZero -}}{{ $lastmod = .Date }}{{- end -}}
{{- if $lastmod.IsZero -}}{{ $lastmod = now }}{{- end -}}
---
title: {{ .Title | jsonify }}
description: {{ $description | jsonify }}
date: {{ .Date.Format "2006-01-02T15:04:05Z07:00" }}
last_updated: {{ $lastmod.Format "2006-01-02T15:04:05Z07:00" }}
doc_version: {{ $lastmod.Format "2006-01-02" | jsonify }}
{{- with .Params.tags }}
tags:
{{- range . }}
  - {{ . | jsonify }}
{{- end }}
{{- end }}
{{- with .Params.categories }}
categories:
{{- range . }}
  - {{ . | jsonify }}
{{- end }}
{{- end }}
url: {{ with .OutputFormats.Get "html" }}{{ .Permalink }}{{ else }}{{ $.Permalink }}{{ end }}
language: {{ .Language.Lang }}
---

# {{ .Title }}

{{ .RawContent }}

## Sitemap

- Site index: [{{ .Site.BaseURL }}]({{ .Site.BaseURL }})
- All pages: [sitemap.xml]({{ .Site.BaseURL }}sitemap.xml) · [sitemap.md]({{ .Site.BaseURL }}sitemap.md)
- Agent guide: [AGENTS.md]({{ .Site.BaseURL }}AGENTS.md) · [llms.txt]({{ .Site.BaseURL }}llms.txt)
{{- with .Parent }}
- Section: [{{ .Title }}]({{ .Permalink }})
{{- end }}
