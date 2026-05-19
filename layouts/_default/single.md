{{- /* ABOUTME: Markdown mirror of a single page for AI/LLM agents (a14y). */ -}}
{{- /* ABOUTME: Renders YAML frontmatter plus the page's markdown content as text/markdown. */ -}}
---
title: {{ .Title | jsonify }}
date: {{ .Date.Format "2006-01-02T15:04:05Z07:00" }}
{{- with .Lastmod }}
lastmod: {{ .Format "2006-01-02T15:04:05Z07:00" }}
{{- end }}
{{- with .Description }}
description: {{ . | jsonify }}
{{- end }}
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
url: {{ .Permalink }}
language: {{ .Language.Lang }}
---

# {{ .Title }}

{{ .RawContent }}
