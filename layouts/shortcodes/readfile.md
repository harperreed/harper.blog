
{{$file := .Get "file"}}
{{- if eq (.Get "markdown") "true" -}}
{{- $file  | readFile | markdownify -}}
{{- else -}}
{{ $file  | readFile | safeHTML }}
{{- end -}}