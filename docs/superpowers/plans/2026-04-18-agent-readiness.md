# Agent Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve harper.blog's isitagentready.com score by adding Content Signals, Link headers, API catalog, and Agent Skills index — all as static files with zero runtime cost.

**Architecture:** Four independent changes: a custom Hugo robots.txt template, static JSON files in `static/.well-known/`, and Netlify header config. Everything is generated at build time or served as-is.

**Tech Stack:** Hugo templates, Netlify headers (`netlify.toml`), static JSON (linkset+json, Agent Skills Discovery v0.2.0)

**Spec:** `docs/superpowers/specs/2026-04-18-agent-readiness-design.md`

---

### Task 1: Custom robots.txt with Content Signals

**Files:**
- Create: `layouts/robots.txt`

Hugo's `enableRobotsTXT = true` (in `config/_default/hugo.toml`) uses a default template. Creating `layouts/robots.txt` overrides it. Hugo robots.txt templates have access to `.Site` but use a plain-text output format.

- [ ] **Step 1: Create the custom robots.txt template**

Create `layouts/robots.txt`:

```
User-agent: *
Allow: /
Sitemap: {{ "sitemap.xml" | absURL }}
Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

- [ ] **Step 2: Build and verify output**

Run: `hugo`

Then check the output:

Run: `cat public/robots.txt`

Expected output:
```
User-agent: *
Allow: /
Sitemap: https://harper.blog/sitemap.xml
Content-Signal: ai-train=yes, search=yes, ai-input=yes
```

Verify: the `Content-Signal` line is present, and the existing `User-agent`, `Allow`, and `Sitemap` lines are preserved.

- [ ] **Step 3: Commit**

```bash
git add layouts/robots.txt
git commit -m "feat: add Content Signals to robots.txt for AI agent discovery"
```

---

### Task 2: API Catalog (RFC 9727)

**Files:**
- Create: `static/.well-known/api-catalog`

This is a static JSON file served at `/.well-known/api-catalog`. It uses `application/linkset+json` format to advertise the blog's machine-readable endpoints (RSS feed and sitemap). The content-type header is handled in Task 4.

- [ ] **Step 1: Create the .well-known directory**

Run: `mkdir -p static/.well-known`

- [ ] **Step 2: Create the api-catalog file**

Create `static/.well-known/api-catalog`:

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

- [ ] **Step 3: Build and verify**

Run: `hugo`

Then verify the file exists in the build output:

Run: `cat public/.well-known/api-catalog`

Expected: valid JSON matching the content above.

Run: `uv run python3 -c "import json; json.load(open('public/.well-known/api-catalog')); print('valid JSON')"`

Expected: `valid JSON`

- [ ] **Step 4: Commit**

```bash
git add static/.well-known/api-catalog
git commit -m "feat: add API catalog for agent discovery (RFC 9727)"
```

---

### Task 3: Agent Skills Index

**Files:**
- Create: `static/.well-known/agent-skills/browse-posts/SKILL.md`
- Create: `static/.well-known/agent-skills/read-rss/SKILL.md`
- Create: `static/.well-known/agent-skills/search-sitemap/SKILL.md`
- Create: `static/.well-known/agent-skills/index.json`

The Agent Skills Discovery spec (v0.2.0) requires an `index.json` with a `$schema` field and a `skills` array. Each skill has a `sha256` digest of its SKILL.md file. We create the skill files first, compute digests, then write the index.

- [ ] **Step 1: Create skill directories**

Run: `mkdir -p static/.well-known/agent-skills/browse-posts static/.well-known/agent-skills/read-rss static/.well-known/agent-skills/search-sitemap`

- [ ] **Step 2: Create browse-posts skill**

Create `static/.well-known/agent-skills/browse-posts/SKILL.md`:

```markdown
---
name: browse-posts
description: Browse and read blog posts on harper.blog
---

# Browse Posts

Navigate the blog's post archive at https://harper.blog/.

## Usage

- **Homepage:** `GET https://harper.blog/` — latest posts
- **Post archive:** `GET https://harper.blog/post/` — all posts
- **Individual post:** `GET https://harper.blog/post/{slug}/` — full post content

## Content Format

All pages return HTML. Posts include YAML frontmatter metadata (title, date, tags, summary) rendered into semantic HTML with proper heading hierarchy.
```

- [ ] **Step 3: Create read-rss skill**

Create `static/.well-known/agent-skills/read-rss/SKILL.md`:

```markdown
---
name: read-rss
description: Subscribe to harper.blog via RSS for recent posts
---

# Read RSS Feed

Consume the blog's RSS feed for structured access to recent content.

## Usage

- **Main feed:** `GET https://harper.blog/index.xml` — latest 20 posts (full content)
- **Content-Type:** `application/rss+xml`

## Feed Contents

Each item includes: title, link, publication date, full HTML content, and author. The feed is limited to the 20 most recent posts.
```

- [ ] **Step 4: Create search-sitemap skill**

Create `static/.well-known/agent-skills/search-sitemap/SKILL.md`:

```markdown
---
name: search-sitemap
description: Discover all URLs on harper.blog via XML sitemap
---

# Search via Sitemap

Use the XML sitemap to discover all available pages and content.

## Usage

- **Sitemap index:** `GET https://harper.blog/sitemap.xml`
- **Content-Type:** `application/xml`

## Sitemap Contents

The sitemap lists all public URLs including posts, notes, links, books, and music pages with last-modification dates. Use this to build a complete index of available content.
```

- [ ] **Step 5: Compute sha256 digests and create index.json**

Run:
```bash
echo "browse-posts: $(shasum -a 256 static/.well-known/agent-skills/browse-posts/SKILL.md | cut -d' ' -f1)"
echo "read-rss: $(shasum -a 256 static/.well-known/agent-skills/read-rss/SKILL.md | cut -d' ' -f1)"
echo "search-sitemap: $(shasum -a 256 static/.well-known/agent-skills/search-sitemap/SKILL.md | cut -d' ' -f1)"
```

Then create `static/.well-known/agent-skills/index.json` using the computed digests:

```json
{
  "$schema": "https://agentskills.io/schema/v0.2.0/index.json",
  "skills": [
    {
      "name": "browse-posts",
      "type": "skill",
      "description": "Browse and read blog posts on harper.blog",
      "url": "https://harper.blog/.well-known/agent-skills/browse-posts/SKILL.md",
      "sha256": "<COMPUTED_DIGEST>"
    },
    {
      "name": "read-rss",
      "type": "skill",
      "description": "Subscribe to harper.blog via RSS for recent posts",
      "url": "https://harper.blog/.well-known/agent-skills/read-rss/SKILL.md",
      "sha256": "<COMPUTED_DIGEST>"
    },
    {
      "name": "search-sitemap",
      "type": "skill",
      "description": "Discover all URLs on harper.blog via XML sitemap",
      "url": "https://harper.blog/.well-known/agent-skills/search-sitemap/SKILL.md",
      "sha256": "<COMPUTED_DIGEST>"
    }
  ]
}
```

Replace each `<COMPUTED_DIGEST>` with the actual sha256 from the previous command.

- [ ] **Step 6: Build and verify**

Run: `hugo`

Verify the index is valid JSON with correct structure:

Run: `uv run python3 -c "import json; d=json.load(open('public/.well-known/agent-skills/index.json')); assert '\$schema' in d; assert len(d['skills'])==3; print('valid:', [s['name'] for s in d['skills']])"`

Expected: `valid: ['browse-posts', 'read-rss', 'search-sitemap']`

Verify skill files are present:

Run: `ls public/.well-known/agent-skills/*/SKILL.md`

Expected: three files listed.

- [ ] **Step 7: Commit**

```bash
git add static/.well-known/agent-skills/
git commit -m "feat: add Agent Skills discovery index with blog capabilities"
```

---

### Task 4: Netlify Link Headers and Content-Type

**Files:**
- Modify: `netlify.toml:92-96` (existing `for = "/"` block)
- Modify: `netlify.toml` (add new `[[headers]]` block for api-catalog)

Two changes: add a `Link` header to the homepage, and set the correct `Content-Type` for the api-catalog endpoint.

- [ ] **Step 1: Add Link header to homepage**

In `netlify.toml`, find the existing block at line 92:

```toml
[[headers]]
for = "/"
[headers.values]
Cache-Control = "public, max-age=3600"
```

Replace with:

```toml
[[headers]]
for = "/"
[headers.values]
Cache-Control = "public, max-age=3600"
Link = """</.well-known/api-catalog>; rel="api-catalog", </sitemap.xml>; rel="sitemap"; type="application/xml", </index.xml>; rel="alternate"; type="application/rss+xml"; title="RSS Feed\""""
```

- [ ] **Step 2: Add Content-Type header for api-catalog**

Append to `netlify.toml`:

```toml
# Agent discovery: API Catalog content type
[[headers]]
for = "/.well-known/api-catalog"
[headers.values]
Content-Type = "application/linkset+json"
Access-Control-Allow-Origin = "*"

# Agent discovery: Agent Skills index content type
[[headers]]
for = "/.well-known/agent-skills/index.json"
[headers.values]
Access-Control-Allow-Origin = "*"
```

- [ ] **Step 3: Verify netlify.toml is valid**

Run: `uv run python3 -c "import tomllib; tomllib.load(open('netlify.toml','rb')); print('valid TOML')"`

Expected: `valid TOML`

- [ ] **Step 4: Commit**

```bash
git add netlify.toml
git commit -m "feat: add Link headers and content-type for agent discovery endpoints"
```

---

### Task 5: Full Build Verification

No new files — this is a verification-only task.

- [ ] **Step 1: Clean build**

Run: `hugo --cleanDestinationDir`

Expected: builds without errors.

- [ ] **Step 2: Verify all agent-readiness files**

Run:
```bash
echo "=== robots.txt ===" && cat public/robots.txt && echo "" && echo "=== api-catalog ===" && cat public/.well-known/api-catalog && echo "" && echo "=== agent-skills index ===" && cat public/.well-known/agent-skills/index.json && echo "" && echo "=== skill files ===" && ls public/.well-known/agent-skills/*/SKILL.md
```

Verify:
- `robots.txt` has `Content-Signal` line
- `api-catalog` is valid linkset+json
- `agent-skills/index.json` has 3 skills with sha256 digests
- All 3 SKILL.md files exist

- [ ] **Step 3: Verify netlify headers reference valid paths**

Run: `grep -A2 'for = "/.well-known' netlify.toml`

Confirm each `for` path corresponds to a file in `public/`.
