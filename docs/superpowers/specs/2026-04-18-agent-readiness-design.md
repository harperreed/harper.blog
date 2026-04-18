# Agent Readiness Improvements for harper.blog

**Date:** 2026-04-18
**Status:** Approved
**Scope:** Improve AI agent discoverability score from 25/100 (3/12 checks passing) to ~58/100 (7/12)

## Context

[isitagentready.com](https://isitagentready.com/harper.blog) scans websites for emerging agent-discovery standards. harper.blog currently passes 3 of 12 checks (robots.txt, sitemap.xml, AI bot rules). This spec covers 4 fixes — all static files and Netlify config, zero runtime cost.

**Deliberately skipped:**
- **Markdown for Agents** — requires Cloudflare or edge functions, adds hosting cost and complexity
- **MCP Server Card** — the blog has no MCP server; a fake card would mislead agents
- **OAuth/OIDC** — no APIs to protect
- **WebMCP** — no interactive tools to expose
- **Commerce protocols** — not applicable

## Changes

### 1. Custom robots.txt with Content Signals

**File:** `layouts/robots.txt` (new — overrides Hugo's default `enableRobotsTXT` template)

Hugo's `enableRobotsTXT = true` generates a minimal robots.txt. A custom layout template lets us add the Content Signals directive while preserving the existing content.

```
User-agent: *
Allow: /
Sitemap: {{ "sitemap.xml" | absURL }}
Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

Content Signals spec: https://contentsignals.org/

**Content policy rationale:** Harper wants full AI access — training, search indexing, and AI-assisted retrieval are all permitted.

### 2. Link Headers on Homepage (RFC 8288)

**File:** `netlify.toml` (modify existing `[[headers]]` for `"/"`)

Add a `Link` response header to the homepage pointing agents to discoverable resources:

```
Link: </.well-known/api-catalog>; rel="api-catalog", </sitemap.xml>; rel="sitemap"; type="application/xml", </index.xml>; rel="alternate"; type="application/rss+xml"; title="RSS Feed"
```

This goes in the existing `for = "/"` headers block in `netlify.toml`.

RFC 8288: https://www.rfc-editor.org/rfc/rfc8288

### 3. API Catalog (RFC 9727)

**File:** `static/.well-known/api-catalog` (new)

A `linkset+json` file advertising the blog's machine-readable endpoints. These are real, functional APIs:

- **RSS Feed** (`/index.xml`) — full-content feed of blog posts
- **Sitemap** (`/sitemap.xml`) — complete URL index

```json
{
  "linkset": [
    {
      "anchor": "https://harper.blog/",
      "service-desc": [
        {
          "href": "https://harper.blog/index.xml",
          "type": "application/rss+xml",
          "title": "RSS Feed"
        }
      ],
      "describedby": [
        {
          "href": "https://harper.blog/sitemap.xml",
          "type": "application/xml",
          "title": "Sitemap"
        }
      ]
    }
  ]
}
```

RFC 9727: https://www.rfc-editor.org/rfc/rfc9727

**Netlify header needed:** The api-catalog endpoint must return `Content-Type: application/linkset+json`. Add a `[[headers]]` block for `/.well-known/api-catalog`.

### 4. Agent Skills Index

**File:** `static/.well-known/agent-skills/index.json` (new)

An index of content discovery capabilities per the Agent Skills Discovery RFC v0.2.0. These describe how agents can consume the blog's content:

- **browse-posts** — navigate the blog's post archive
- **read-rss** — consume the RSS feed for recent content
- **search-sitemap** — discover all available URLs via sitemap

Each skill entry includes: name, type, description, url, and sha256 digest.

The skill files themselves are simple markdown documents describing each capability, placed alongside the index at `static/.well-known/agent-skills/`.

Spec: https://github.com/cloudflare/agent-skills-discovery-rfc

## File Summary

| Action | Path |
|--------|------|
| Create | `layouts/robots.txt` |
| Modify | `netlify.toml` (add Link header + api-catalog content-type) |
| Create | `static/.well-known/api-catalog` |
| Create | `static/.well-known/agent-skills/index.json` |
| Create | `static/.well-known/agent-skills/browse-posts/SKILL.md` |
| Create | `static/.well-known/agent-skills/read-rss/SKILL.md` |
| Create | `static/.well-known/agent-skills/search-sitemap/SKILL.md` |

## Verification

After implementation:
1. `hugo` build succeeds
2. `public/robots.txt` contains Content-Signal directive
3. `public/.well-known/api-catalog` is valid JSON
4. `public/.well-known/agent-skills/index.json` is valid JSON with correct sha256 digests
5. Re-scan on isitagentready.com shows improved score
