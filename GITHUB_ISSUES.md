# GitHub Issues for Blog Improvements

This document contains all the issues identified during the comprehensive codebase review. Copy each issue into GitHub's issue tracker.

---

## 🔴 Critical Priority Issues

### Issue 1: Standardize Hugo versions across all environments

**Labels:** `critical`, `infrastructure`, `build`

**Description:**

## Problem
Version mismatch detected across deployment environments:
- **Netlify**: Hugo 0.145.0
- **GitHub Actions**: Hugo 0.136.4
- **Go version**: go.mod requires 1.19, Netlify uses 1.23

## Impact
- Potential build inconsistencies between local/CI/production
- Template behavior differences
- Unexpected deployment failures
- Difficult to reproduce issues

## Proposed Solution
1. Standardize on Hugo 0.145.0 (latest) across all environments
2. Update `.github/workflows/*.yaml` to use Hugo 0.145.0
3. Update `go.mod` to require Go 1.23
4. Document version requirements in README.md

## Files to Update
- `.github/workflows/new-hugo-deploy.yaml`
- `.github/workflows/notes.yaml`
- `.github/workflows/links.yaml`
- `.github/workflows/grab_goodreads.yaml`
- `.github/workflows/grab_spotify_saved_tracks.yaml`
- `go.mod`
- `netlify.toml` (verify version)

## Priority
🔴 **Critical** - Should be fixed immediately to prevent deployment issues

---

### Issue 2: Add timeout configurations to all GitHub Actions workflows

**Labels:** `critical`, `ci-cd`, `workflows`

**Description:**

## Problem
Several GitHub Actions workflows are missing timeout configurations:
- `notes.yaml` - runs every 10 minutes
- `links.yaml` - runs every 30 minutes
- `grab_goodreads.yaml` - runs every 12 hours
- `grab_spotify_saved_tracks.yaml` - runs every 24 hours

## Impact
- Workflows could run indefinitely if they hang
- Consumes GitHub Actions minutes unnecessarily
- Blocks concurrent runs due to concurrency groups
- Difficult to detect stuck workflows

## Proposed Solution
Add `timeout-minutes` to all workflow jobs:
```yaml
jobs:
  job-name:
    timeout-minutes: 15  # or appropriate value
```

## Recommended Timeouts
- `notes.yaml`: 10 minutes
- `links.yaml`: 20 minutes (uses OpenAI API)
- `grab_goodreads.yaml`: 15 minutes
- `grab_spotify_saved_tracks.yaml`: 10 minutes
- `new-hugo-deploy.yaml`: Already has timeouts ✅

## Priority
🔴 **Critical** - Prevents runaway workflows

---

### Issue 3: Fix workflow concurrency group naming errors

**Labels:** `critical`, `ci-cd`, `bug`

**Description:**

## Problem
Copy-paste errors in workflow concurrency groups causing conflicts:

1. **grab_goodreads.yaml**:
   - Uses concurrency group: `spotify-tracks-${{ github.ref }}` ❌
   - Commit message says "Auto update spotify tracks" ❌
   - Should be "goodreads" related

2. **Duplicate concurrency group**: Both Goodreads and Spotify workflows could share the same group name

## Impact
- Workflows may cancel each other incorrectly
- Concurrent git commits could conflict
- Confusing commit messages in git history
- Difficult to debug workflow behavior

## Proposed Solution

**grab_goodreads.yaml:**
```yaml
concurrency:
  group: goodreads-books-${{ github.ref }}
  cancel-in-progress: true
```

Commit message should be:
```
Auto update Goodreads books
```

## Files to Fix
- `.github/workflows/grab_goodreads.yaml`

## Priority
🔴 **Critical** - Currently causing incorrect workflow behavior

---

### Issue 4: Implement atomic registry updates with file locking

**Labels:** `critical`, `automation`, `data-integrity`

**Description:**

## Problem
Registry files are updated non-atomically, creating race conditions:
- `/data/notes/processed_urls.json`
- `/data/notes/processed_content_hashes.json`

**Current flow:**
1. Read registry
2. Process content
3. Write to disk
4. Update registry ❌ (Could fail here)

**Issues:**
- Multiple workflows could write simultaneously
- Partial state on failures (content created but not tracked)
- `shutil.rmtree` happens AFTER registry update (could lose tracking)
- No corruption detection/recovery

## Impact
- Duplicate content could be created
- Registry corruption over time
- Lost tracking of processed items
- Manual cleanup required

## Proposed Solution

### 1. Implement File Locking
```python
import fcntl
from contextlib import contextmanager

@contextmanager
def locked_registry(registry_path):
    with open(registry_path, 'r+') as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            data = json.load(f)
            yield data
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

### 2. Transactional Updates
- Write to temp file first
- Atomic rename only on success
- Rollback on failure

### 3. Add Corruption Detection
- Validate JSON before loading
- Checksum verification
- Auto-repair from backup

## Files to Update
- `tools/grab_micro_posts_fixed.py`
- `tools/grab_starred_links.py`

## Priority
🔴 **Critical** - Data integrity issue

---

### Issue 5: Review and fix goldmark unsafe HTML rendering

**Labels:** `critical`, `security`, `config`

**Description:**

## Problem
Configuration allows unsafe HTML rendering:

**config/_default/markup.toml:**
```toml
[goldmark.renderer]
unsafe = true
```

## Impact
- Potential XSS vulnerabilities if untrusted content is processed
- Arbitrary HTML/JavaScript can be injected
- Violates Content Security Policy principles

## Proposed Solution

### Option 1: Disable Unsafe (Recommended)
```toml
[goldmark.renderer]
unsafe = false
```
- Review all content that uses raw HTML
- Convert to Hugo shortcodes where needed
- Add shortcodes for specific use cases (embeds, etc.)

### Option 2: Keep Unsafe but Document
If raw HTML is required:
1. Document WHY it's needed
2. Add content validation pipeline
3. Ensure all automated content is sanitized
4. Never allow user-submitted content

## Required Actions
1. Audit content for raw HTML usage
2. Identify legitimate use cases
3. Create shortcodes as alternatives
4. Update documentation

## Files to Review
- `config/_default/markup.toml`
- Content files using raw HTML
- Python scripts generating content

## Priority
🔴 **Critical** - Security concern

---

### Issue 6: Update deprecated GitHub Actions to latest versions

**Labels:** `critical`, `ci-cd`, `dependencies`

**Description:**

## Problem
Workflows using deprecated action versions:
- `actions/checkout@v2` → Should use `v4`
- `actions/cache@v2` → Should use `v4`
- `actions/setup-python@v2` → Should use `v5`

## Impact
- Security vulnerabilities in old versions
- Deprecated features may stop working
- Missing performance improvements
- GitHub warnings in workflow logs

## Proposed Solution
Update all workflows to latest stable versions:

```yaml
# Old
- uses: actions/checkout@v2

# New
- uses: actions/checkout@v4
  with:
    fetch-depth: 1  # Specify depth explicitly
```

## Files to Update
- `.github/workflows/notes.yaml`
- `.github/workflows/links.yaml`
- `.github/workflows/grab_goodreads.yaml`
- `.github/workflows/grab_spotify_saved_tracks.yaml`
- `.github/workflows/new-hugo-deploy.yaml`

## Migration Notes
- `actions/checkout@v4` uses Node 20 (v2 used Node 12)
- `actions/cache@v4` has improved performance
- Review breaking changes in each action's CHANGELOG

## Priority
🔴 **Critical** - Security and maintenance

---

### Issue 7: Add comprehensive unit tests for Python automation scripts

**Labels:** `critical`, `testing`, `automation`

**Description:**

## Problem
Zero test coverage for Python automation scripts:
- `tools/grab_micro_posts_fixed.py` (838 lines)
- `tools/grab_starred_links.py` (238 lines)
- `tools/grab_read_books.py` (540 lines)
- `tools/grab_spotify_saved_tracks.py` (205 lines)
- `tools/deduplicate_notes.py` (273 lines)

## Impact
- No confidence when refactoring
- Bugs discovered in production only
- Difficult to validate behavior changes
- Regression risks when updating dependencies

## Proposed Solution

### 1. Set up Testing Infrastructure
```bash
# Add to pyproject.toml
[project.optional-dependencies]
test = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.11.1",
    "responses>=0.23.1",  # HTTP mocking
]
```

### 2. Priority Test Areas
**High Priority:**
- Registry operations (load, save, update)
- Content deduplication logic
- Frontmatter generation
- Error handling paths

**Medium Priority:**
- API response parsing
- Date/time handling
- File I/O operations

**Low Priority:**
- Logging
- CLI argument parsing

### 3. Testing Strategy
- Unit tests: Test individual functions in isolation
- Integration tests: Test full script flow with mocked APIs
- Fixture data: Create sample API responses
- Mock external services: OpenAI, Spotify, Goodreads, Firecrawl

### 4. Target Coverage
- Start with 50% coverage for critical paths
- Work towards 80% coverage overall
- 100% coverage for registry operations

## Files to Create
- `tests/test_grab_micro_posts.py`
- `tests/test_grab_starred_links.py`
- `tests/test_grab_read_books.py`
- `tests/test_grab_spotify_saved_tracks.py`
- `tests/test_deduplicate_notes.py`
- `tests/conftest.py` (shared fixtures)
- `tests/fixtures/` (sample API responses)
- `.github/workflows/test.yaml` (CI integration)

## Priority
🔴 **Critical** - Foundation for reliability

---

## 🟡 High Priority Issues

### Issue 8: Implement retry mechanisms with exponential backoff for API calls

**Labels:** `high`, `automation`, `resilience`

**Description:**

## Problem
Python scripts lack retry logic for API calls:
- OpenAI API calls (no retries)
- Firecrawl API calls (no retries)
- Spotify API calls (no retries)
- Goodreads API calls (no retries)
- RSS feed fetching (no retries)

## Impact
- Transient network failures cause complete script failure
- Manual re-runs required for temporary issues
- Wasted CI/CD minutes
- Incomplete content updates

## Proposed Solution

### 1. Use `tenacity` library
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=2, max=30),
    retry=retry_if_exception_type((requests.RequestException, TimeoutError))
)
def call_api_with_retry(url, **kwargs):
    response = requests.get(url, timeout=30, **kwargs)
    response.raise_for_status()
    return response
```

### 2. API-Specific Strategies
**OpenAI:**
- Max 4 retries
- Handle rate limits (429) with longer backoff
- Don't retry on 4xx errors (except 429)

**Spotify:**
- Max 3 retries
- Handle token expiration separately
- Shorter timeout (10s)

**Firecrawl:**
- Max 3 retries
- Handle scraping failures gracefully
- Fall back to simpler scraping on repeated failures

## Files to Update
- `tools/grab_micro_posts_fixed.py`
- `tools/grab_starred_links.py`
- `tools/grab_read_books.py`
- `tools/grab_spotify_saved_tracks.py`

Add to `pyproject.toml`:
```toml
dependencies = [
    # ... existing ...
    "tenacity>=8.2.3",
]
```

## Priority
🟡 **High** - Significantly improves reliability

---

### Issue 9: Add API key validation before script execution

**Labels:** `high`, `automation`, `validation`

**Description:**

## Problem
Scripts don't validate required environment variables/API keys before execution:
- Missing `OPENAI_API_KEY` discovered mid-execution
- Missing `FIRECRAWL_API_KEY` causes silent failures
- Missing `SPOTIFY_CLIENT_ID`/`SPOTIFY_CLIENT_SECRET` not checked upfront
- Missing `GOODREADS_USER_ID` causes late failures

## Impact
- Scripts fail partway through execution
- Partial state changes without completion
- Confusing error messages
- Wasted CI/CD time

## Proposed Solution

### 1. Create Validation Function
```python
def validate_environment():
    """Validate all required environment variables are present."""
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for content processing',
        'FIRECRAWL_API_KEY': 'Firecrawl API key for web scraping',
        # ... add per script
    }

    missing = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing.append(f"{var}: {description}")

    if missing:
        print("❌ Missing required environment variables:")
        for item in missing:
            print(f"  - {item}")
        sys.exit(1)

    print("✅ All required environment variables present")
```

### 2. Add to Each Script
Call `validate_environment()` at the start of `main()` before any processing.

### 3. Test API Keys
```python
def test_api_keys():
    """Test that API keys are valid, not just present."""
    try:
        # Quick test call
        client = OpenAI()
        client.models.list()
    except Exception as e:
        print(f"❌ OpenAI API key validation failed: {e}")
        sys.exit(1)
```

## Files to Update
- All scripts in `tools/` directory
- Create `tools/common/validation.py` for shared logic

## Priority
🟡 **High** - Prevents wasted execution

---

### Issue 10: Implement cache corruption detection and recovery

**Labels:** `high`, `automation`, `data-integrity`

**Description:**

## Problem
Disk cache and registries lack corruption detection:
- `diskcache` could store corrupted data
- Registry JSON files could be malformed
- No validation on load
- No automatic repair

## Impact
- Silent failures with cached corrupted data
- Scripts crash on corrupted registries
- Manual intervention required
- Lost processing history

## Proposed Solution

### 1. Registry Validation
```python
import json
from pathlib import Path
from typing import Dict, Set

def load_registry_safe(registry_path: Path) -> Set[str]:
    """Load registry with validation and auto-repair."""
    backup_path = registry_path.with_suffix('.json.backup')

    # Try main registry
    try:
        if registry_path.exists():
            with open(registry_path) as f:
                data = json.load(f)
                if not isinstance(data, dict) or 'entries' not in data:
                    raise ValueError("Invalid registry structure")

                # Validate entries
                entries = set(data['entries'])
                if len(entries) != len(data['entries']):
                    print("⚠️  Duplicate entries found, cleaning...")

                # Create backup of good registry
                shutil.copy2(registry_path, backup_path)
                return entries
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️  Registry corrupted: {e}")

        # Try backup
        if backup_path.exists():
            print("📦 Restoring from backup...")
            try:
                with open(backup_path) as f:
                    data = json.load(f)
                    shutil.copy2(backup_path, registry_path)
                    return set(data['entries'])
            except Exception as e:
                print(f"❌ Backup also corrupted: {e}")

    # Start fresh
    print("🆕 Creating new registry...")
    return set()
```

### 2. Cache Validation
```python
def validate_cache_entry(key, value):
    """Validate cached data structure."""
    if value is None:
        return False

    # Add type-specific validation
    if isinstance(value, dict):
        required_keys = {'content', 'timestamp'}
        if not required_keys.issubset(value.keys()):
            return False

    return True
```

### 3. Health Check Command
Add `--check-health` flag to each script:
```bash
uv run tools/grab_micro_posts_fixed.py --check-health
```

Should validate:
- Registry files are valid JSON
- Cache directory is accessible
- No obvious corruption

## Files to Update
- All scripts using registries or caches
- Create `tools/common/registry.py` for shared logic

## Priority
🟡 **High** - Prevents data loss

---

### Issue 11: Create backup mechanism for registry files

**Labels:** `high`, `automation`, `data-integrity`

**Description:**

## Problem
Registry files have no backup strategy:
- `/data/notes/processed_urls.json`
- `/data/notes/processed_content_hashes.json`
- Single point of failure
- No version history
- No disaster recovery

## Impact
- Corruption means complete loss
- No way to recover from mistakes
- Re-processing everything required
- Historical data lost

## Proposed Solution

### 1. Automatic Backups Before Updates
```python
def backup_registry(registry_path: Path):
    """Create timestamped backup of registry."""
    if not registry_path.exists():
        return

    backup_dir = registry_path.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"{registry_path.stem}_{timestamp}.json"

    shutil.copy2(registry_path, backup_path)

    # Keep only last 30 backups
    backups = sorted(backup_dir.glob(f"{registry_path.stem}_*.json"))
    for old_backup in backups[:-30]:
        old_backup.unlink()

    return backup_path
```

### 2. Git-Track Registries (Optional)
Add registries to git with daily commits:
```yaml
# .github/workflows/backup-registries.yaml
name: Backup Registries
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Commit registry changes
        run: |
          git add data/notes/*.json
          git commit -m "Backup registries $(date +%Y-%m-%d)" || true
          git push
```

### 3. Recovery Command
```bash
uv run tools/recover_registry.py --from-backup data/notes/backups/processed_urls_20250113_120000.json
```

## Files to Create
- `tools/common/backup.py`
- `tools/recover_registry.py`
- `.github/workflows/backup-registries.yaml`

## Files to Update
- All scripts that modify registries

## Priority
🟡 **High** - Data safety

---

### Issue 12: Add workflow failure notifications

**Labels:** `high`, `ci-cd`, `monitoring`

**Description:**

## Problem
GitHub Actions workflows fail silently:
- No notifications on failure
- Must manually check Actions tab
- Long delays before issues are noticed
- Stale content when automations break

## Impact
- Automation failures go unnoticed
- Content stops updating
- Issues compound over time
- Manual monitoring required

## Proposed Solution

### 1. Add Slack/Discord/Email Notifications
```yaml
# Add to each workflow
jobs:
  job-name:
    steps:
      # ... existing steps ...

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "❌ Workflow '${{ github.workflow }}' failed",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Workflow*: ${{ github.workflow }}\n*Run*: <${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View Details>"
                  }
                }
              ]
            }
```

### 2. GitHub Issues on Repeated Failures
Create issue automatically after 3 consecutive failures:
```yaml
- name: Create issue on repeated failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      const runs = await github.rest.actions.listWorkflowRuns({
        owner: context.repo.owner,
        repo: context.repo.repo,
        workflow_id: context.workflow,
        per_page: 3
      });

      const allFailed = runs.data.workflow_runs
        .slice(0, 3)
        .every(run => run.conclusion === 'failure');

      if (allFailed) {
        await github.rest.issues.create({
          owner: context.repo.owner,
          repo: context.repo.repo,
          title: `🚨 Workflow ${context.workflow} failing repeatedly`,
          body: 'This workflow has failed 3 times in a row. Investigation needed.',
          labels: ['automation', 'bug', 'critical']
        });
      }
```

### 3. Status Badge in README
Add badges showing workflow status:
```markdown
![Notes Automation](https://github.com/harper/harper.blog/actions/workflows/notes.yaml/badge.svg)
![Links Automation](https://github.com/harper/harper.blog/actions/workflows/links.yaml/badge.svg)
```

## Files to Update
- All workflow YAML files
- `README.md` (add status badges)

## Secrets to Add
- `SLACK_WEBHOOK_URL` or similar

## Priority
🟡 **High** - Essential for operations

---

### Issue 13: Implement integration tests for workflow orchestration

**Labels:** `high`, `testing`, `ci-cd`

**Description:**

## Problem
No testing of how workflows interact:
- Multiple workflows commit to same branch
- Race conditions possible
- Concurrent execution not tested
- No validation of end-to-end flow

## Impact
- Workflows could conflict
- Git merge issues
- Data corruption possible
- Behavior untested

## Proposed Solution

### 1. Test Workflow File
```yaml
# .github/workflows/integration-test.yaml
name: Integration Tests
on:
  pull_request:
  workflow_dispatch:

jobs:
  test-content-automation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Test micro posts (dry run)
        run: |
          export OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          # Add --dry-run flag to scripts
          uv run tools/grab_micro_posts_fixed.py --dry-run --limit 5

      - name: Test links (dry run)
        run: |
          export OPENAI_API_KEY=${{ secrets.OPENAI_API_KEY }}
          export FIRECRAWL_API_KEY=${{ secrets.FIRECRAWL_API_KEY }}
          uv run tools/grab_starred_links.py --dry-run --limit 5

      - name: Validate Hugo build
        run: |
          hugo --minify

      - name: Check for broken links
        uses: lycheeverse/lychee-action@v1
        with:
          args: --base public --no-progress 'public/**/*.html'

  test-concurrent-execution:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Simulate concurrent commits
        run: |
          # Test that scripts handle concurrent execution
          echo "Test concurrent git operations"
```

### 2. Add Dry-Run Modes
Update all scripts to support `--dry-run`:
```python
parser.add_argument('--dry-run', action='store_true',
                   help='Run without making changes')

if args.dry_run:
    print("DRY RUN: Would create content/notes/test.md")
else:
    with open(filepath, 'w') as f:
        f.write(content)
```

### 3. Smoke Tests
Add post-deployment smoke tests:
```yaml
- name: Smoke test deployment
  run: |
    curl -f https://harperreed.com || exit 1
    curl -f https://harperreed.com/notes/ || exit 1
    curl -f https://harperreed.com/links/ || exit 1
```

## Files to Create
- `.github/workflows/integration-test.yaml`
- `tests/integration/` directory

## Files to Update
- All Python scripts (add `--dry-run` flag)

## Priority
🟡 **High** - Prevents production issues

---

## 🟢 Medium Priority Issues

### Issue 14: Replace deprecated Goodreads API

**Labels:** `medium`, `automation`, `dependencies`, `breaking-change`

**Description:**

## Problem
Goodreads API is deprecated:
- No longer officially supported
- Could stop working at any time
- Using XML API (outdated)
- Hard-coded limit of 15 books

## Impact
- Book automation will eventually break
- No alternative currently in place
- Lost functionality for reading list

## Proposed Solution

### Option 1: OpenLibrary API
Free, open-source alternative:
```python
def fetch_reading_list_openlibrary(user_id):
    # Use OpenLibrary's APIs
    # https://openlibrary.org/developers/api
    pass
```

### Option 2: Manual JSON File
User maintains `data/reading_list.json`:
```json
{
  "books": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "isbn": "1234567890",
      "date_read": "2025-01-01",
      "rating": 5
    }
  ]
}
```

### Option 3: Literal.club Integration
Modern reading tracking platform with API.

### Option 4: Goodreads RSS
Continue using RSS feed (may last longer than API):
```python
def fetch_goodreads_rss(user_id):
    rss_url = f"https://www.goodreads.com/review/list_rss/{user_id}"
    # Parse RSS feed
```

## Recommendation
Implement Option 2 (manual JSON) as interim solution, then add Option 1 (OpenLibrary) for additional metadata.

## Files to Update
- `tools/grab_read_books.py`
- `.github/workflows/grab_goodreads.yaml`
- `pyproject.toml` (update dependencies)

## Priority
🟢 **Medium** - Not urgent but needs addressing

---

### Issue 15: Tighten Python dependency version constraints

**Labels:** `medium`, `dependencies`, `maintenance`

**Description:**

## Problem
Loose version constraints in `pyproject.toml`:
```toml
dependencies = [
    "openai>=1.54.3",  # Too loose
    "feedparser",      # No version at all
    # ...
]
```

## Impact
- Breaking changes could be pulled in automatically
- Inconsistent behavior across environments
- Difficult to reproduce bugs
- Supply chain security concerns

## Proposed Solution

### 1. Use Restrictive Constraints
```toml
dependencies = [
    "openai>=1.54.3,<2.0.0",  # Allow patches and minors, block majors
    "feedparser~=6.0.10",     # Allow patches only
    "beautifulsoup4==4.12.3", # Pin exactly for critical deps
]
```

### 2. Keep uv.lock in Sync
```bash
uv lock --upgrade
```

### 3. Regular Dependency Updates
Create scheduled workflow:
```yaml
name: Update Dependencies
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Update dependencies
        run: |
          uv lock --upgrade
          uv sync
      - name: Run tests
        run: uv run pytest
      - name: Create PR
        uses: peter-evans/create-pull-request@v6
        with:
          title: "chore: Update Python dependencies"
          body: "Automated dependency updates"
          branch: deps/python-updates
```

## Files to Update
- `pyproject.toml`
- `uv.lock` (regenerate)

## Priority
🟢 **Medium** - Maintenance and security

---

### Issue 16: Add Dependabot or Renovate configuration

**Labels:** `medium`, `dependencies`, `automation`

**Description:**

## Problem
No automated dependency updates:
- Must manually check for updates
- Security vulnerabilities may go unnoticed
- Dependencies drift out of date
- No GitHub Actions version updates

## Impact
- Security risks
- Missing bug fixes
- Missing performance improvements
- Technical debt accumulation

## Proposed Solution

### Option 1: GitHub Dependabot
```yaml
# .github/dependabot.yml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "ci-cd"

  # Hugo modules
  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "monthly"
    labels:
      - "dependencies"
      - "hugo"
```

### Option 2: Renovate (More Features)
```json
// renovate.json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchManagers": ["pip_requirements"],
      "groupName": "Python dependencies"
    },
    {
      "matchManagers": ["github-actions"],
      "groupName": "GitHub Actions"
    }
  ],
  "schedule": ["before 5am on Monday"],
  "labels": ["dependencies"]
}
```

## Recommendation
Start with Dependabot (simpler, built-in).

## Files to Create
- `.github/dependabot.yml`

## Priority
🟢 **Medium** - Ongoing maintenance

---

### Issue 17: Implement CDN purge mechanism for updated content

**Labels:** `medium`, `performance`, `deployment`

**Description:**

## Problem
No CDN cache invalidation when content updates:
- Assets cached for 1 year (immutable)
- Images cached for 3600s
- Updates may not be visible immediately
- No way to force cache refresh

## Impact
- Stale content served to users
- Changes take time to propagate
- No control over cache invalidation
- User confusion

## Proposed Solution

### 1. Netlify Cache Purging
Add to deployment workflow:
```yaml
- name: Purge Netlify cache
  run: |
    curl -X POST \
      -H "Authorization: Bearer ${{ secrets.NETLIFY_TOKEN }}" \
      "https://api.netlify.com/api/v1/sites/${{ secrets.NETLIFY_SITE_ID }}/deploys/latest/publish_deploys"
```

### 2. Selective Purging for Content Updates
When content workflows run:
```yaml
# In notes.yaml, links.yaml, etc.
- name: Trigger Netlify rebuild
  run: |
    curl -X POST -d '{}' \
      "https://api.netlify.com/build_hooks/${{ secrets.NETLIFY_BUILD_HOOK }}"
```

### 3. Asset Versioning
Use Hugo's fingerprinting:
```go-html-template
{{ $css := resources.Get "css/main.css" }}
{{ $css := $css | fingerprint }}
<link rel="stylesheet" href="{{ $css.RelPermalink }}">
```

## Files to Update
- `.github/workflows/new-hugo-deploy.yaml`
- `.github/workflows/notes.yaml`
- `.github/workflows/links.yaml`
- Hugo templates (add fingerprinting)

## Secrets to Add
- `NETLIFY_TOKEN`
- `NETLIFY_SITE_ID`
- `NETLIFY_BUILD_HOOK`

## Priority
🟢 **Medium** - UX improvement

---

### Issue 18: Add content validation pipeline

**Labels:** `medium`, `quality`, `ci-cd`

**Description:**

## Problem
No validation of generated content:
- Frontmatter might be malformed
- Required fields could be missing
- Dates might be invalid
- Content could be empty

## Impact
- Malformed content breaks Hugo builds
- Issues discovered late in pipeline
- Manual fixes required
- Build failures

## Proposed Solution

### 1. Content Validator Script
```python
# tools/validate_content.py
import frontmatter
from pathlib import Path
from datetime import datetime

def validate_frontmatter(filepath):
    """Validate frontmatter has required fields and correct types."""
    post = frontmatter.load(filepath)

    required_fields = {
        'title': str,
        'date': datetime,
        'draft': bool,
    }

    errors = []
    for field, expected_type in required_fields.items():
        if field not in post.metadata:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(post.metadata[field], expected_type):
            errors.append(f"Field {field} has wrong type")

    return errors

def validate_all_content(content_dir):
    """Validate all markdown files in directory."""
    errors = {}
    for md_file in Path(content_dir).rglob('*.md'):
        if errs := validate_frontmatter(md_file):
            errors[str(md_file)] = errs

    return errors
```

### 2. Add to Workflows
```yaml
- name: Validate generated content
  run: |
    uv run tools/validate_content.py content/notes/
    uv run tools/validate_content.py content/links/
```

### 3. Pre-commit Hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: validate-content
        name: Validate frontmatter
        entry: uv run tools/validate_content.py
        language: system
        files: \.md$
```

### 4. Hugo Validation
```bash
# Check for broken shortcodes, invalid templates
hugo --printPathWarnings --printI18nWarnings
```

## Files to Create
- `tools/validate_content.py`
- `.pre-commit-config.yaml`

## Files to Update
- All workflow YAML files

## Priority
🟢 **Medium** - Quality assurance

---

### Issue 19: Add pre-commit hooks for code quality

**Labels:** `medium`, `quality`, `developer-experience`

**Description:**

## Problem
No automated code quality checks:
- No linting before commit
- No formatting enforcement
- Inconsistent code style
- Quality issues found late

## Impact
- Code quality varies
- Style debates in reviews
- Bugs slip through
- CI failures on preventable issues

## Proposed Solution

### 1. Install pre-commit
```bash
pip install pre-commit
# or add to pyproject.toml
```

### 2. Configuration File
```yaml
# .pre-commit-config.yaml
repos:
  # Python code quality
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # General quality
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: check-added-large-files
        args: [--maxkb=1000]
      - id: detect-private-key

  # Python-specific
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]

  # Markdown
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args: [--fix]
```

### 3. Ruff Configuration
```toml
# pyproject.toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = []

[tool.bandit]
exclude_dirs = ["tests", "venv"]
```

### 4. Setup Instructions
```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### 5. CI Integration
```yaml
# Add to workflows
- name: Run pre-commit
  uses: pre-commit/action@v3.0.0
```

## Files to Create
- `.pre-commit-config.yaml`

## Files to Update
- `pyproject.toml` (add ruff config)
- `README.md` (document setup)
- `.github/workflows/test.yaml` (add pre-commit check)

## Priority
🟢 **Medium** - Developer experience

---

### Issue 20: Add metrics collection for builds and automations

**Labels:** `medium`, `monitoring`, `observability`

**Description:**

## Problem
No visibility into automation performance:
- Build times not tracked
- Script execution duration unknown
- Success/failure rates not measured
- No trending data

## Impact
- Performance regressions go unnoticed
- Can't optimize slow operations
- No historical data for debugging
- Reactive vs proactive monitoring

## Proposed Solution

### 1. Simple Metrics Collection
```python
# tools/common/metrics.py
import time
import json
from pathlib import Path
from datetime import datetime

class MetricsCollector:
    def __init__(self, script_name):
        self.script_name = script_name
        self.start_time = time.time()
        self.metrics = {
            'script': script_name,
            'timestamp': datetime.now().isoformat(),
        }

    def record(self, key, value):
        self.metrics[key] = value

    def finish(self, success=True):
        self.metrics['duration'] = time.time() - self.start_time
        self.metrics['success'] = success

        # Append to metrics file
        metrics_file = Path('data/metrics.jsonl')
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(self.metrics) + '\n')

# Usage
metrics = MetricsCollector('grab_micro_posts')
metrics.record('posts_processed', 10)
metrics.record('new_posts', 3)
metrics.finish(success=True)
```

### 2. Workflow Metrics
```yaml
- name: Record workflow metrics
  if: always()
  run: |
    echo "workflow: ${{ github.workflow }}" >> metrics.log
    echo "duration: ${{ steps.run.duration }}" >> metrics.log
    echo "outcome: ${{ steps.run.outcome }}" >> metrics.log
```

### 3. Visualization Dashboard
Create simple dashboard:
```python
# tools/metrics_dashboard.py
import pandas as pd
import plotly.express as px

def generate_dashboard():
    df = pd.read_json('data/metrics.jsonl', lines=True)

    # Success rate over time
    fig1 = px.line(df.groupby('timestamp')['success'].mean())

    # Duration trends
    fig2 = px.box(df, x='script', y='duration')

    # Save as HTML
    with open('metrics_dashboard.html', 'w') as f:
        f.write(fig1.to_html() + fig2.to_html())
```

### 4. GitHub Actions Insights
Use built-in metrics:
- Workflow run duration
- Success/failure rates
- Trends over time

## Files to Create
- `tools/common/metrics.py`
- `tools/metrics_dashboard.py`
- `data/metrics.jsonl`

## Files to Update
- All Python scripts (add metrics collection)

## Priority
🟢 **Medium** - Operations visibility

---

### Issue 21: Implement secret rotation strategy

**Labels:** `medium`, `security`, `operations`

**Description:**

## Problem
17 different secrets with no rotation strategy:
- API keys never rotated
- No expiration dates tracked
- No rotation process documented
- Secrets could be compromised for extended periods

## Impact
- Security risk if keys leaked
- No proactive security posture
- Compliance issues
- Manual, error-prone rotation

## Proposed Solution

### 1. Document All Secrets
```markdown
# SECRETS.md

## Required Secrets

| Secret Name | Purpose | Rotation Schedule | Last Rotated |
|------------|---------|-------------------|--------------|
| OPENAI_API_KEY | Content processing | Quarterly | 2025-01-01 |
| FIRECRAWL_API_KEY | Web scraping | Quarterly | 2025-01-01 |
| SPOTIFY_CLIENT_ID | Music automation | Annually | 2025-01-01 |
| SPOTIFY_CLIENT_SECRET | Music automation | Annually | 2025-01-01 |
| GOODREADS_API_KEY | Book automation | Annually | Never (deprecated) |
| NETLIFY_TOKEN | Deployment | Annually | 2025-01-01 |
| ... | ... | ... | ... |

## Rotation Process
1. Generate new key from provider
2. Update GitHub Secrets
3. Test workflows with new key
4. Revoke old key
5. Update rotation date in this document
```

### 2. Rotation Reminders
```yaml
# .github/workflows/secret-rotation-reminder.yaml
name: Secret Rotation Reminder
on:
  schedule:
    - cron: '0 0 1 * *'  # First of every month

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check rotation dates
        run: |
          # Parse SECRETS.md and check dates
          # Create issue if any secret needs rotation

          echo "Checking secret rotation dates..."
          # (Implementation would parse SECRETS.md)
```

### 3. Automated Rotation (Where Possible)
Some APIs support programmatic key rotation:
```python
def rotate_api_key(service):
    """Rotate API key automatically."""
    # Generate new key
    new_key = service.create_api_key()

    # Update GitHub Secret via API
    update_github_secret('OPENAI_API_KEY', new_key)

    # Revoke old key after validation period
    time.sleep(3600)  # 1 hour grace period
    service.revoke_api_key(old_key)
```

### 4. Least Privilege Review
Audit what permissions each secret actually needs:
- Read-only where possible
- Scope limitations
- IP restrictions where supported

## Files to Create
- `SECRETS.md`
- `.github/workflows/secret-rotation-reminder.yaml`
- `tools/rotate_secrets.py`

## Priority
🟢 **Medium** - Security hygiene

---

## 🔵 Low Priority / Nice to Have Issues

### Issue 22: Add Hugo resources cache invalidation strategy

**Labels:** `low`, `performance`, `maintenance`

**Description:**

## Problem
Hugo resources cache uses same key forever:
- No invalidation strategy
- Could serve stale processed assets
- Cache grows indefinitely

## Proposed Solution
Add version number or date to cache key:
```yaml
cache-key: hugo-resources-v2-${{ hashFiles('assets/**') }}
```

---

### Issue 23: Increase RSS feed limit from 20 to 50 items

**Labels:** `low`, `feature`, `content`

**Description:**

## Problem
RSS feed limited to 20 items - could be higher for better subscriber experience.

## Proposed Solution
Update Hugo config to increase limit.

---

### Issue 24: Add HTML validation to deployment pipeline

**Labels:** `low`, `quality`, `ci-cd`

**Description:**

## Problem
No HTML validation ensures pages are valid markup.

## Proposed Solution
Add validator step:
```yaml
- name: Validate HTML
  uses: Cyb3r-Jak3/html5validator-action@v7
  with:
    root: public/
```

---

### Issue 25: Add accessibility testing

**Labels:** `low`, `accessibility`, `quality`

**Description:**

## Problem
No automated accessibility testing (WCAG compliance).

## Proposed Solution
Add axe-core or Pa11y to test suite.

---

### Issue 26: Create architecture documentation

**Labels:** `low`, `documentation`

**Description:**

## Problem
No comprehensive architecture documentation.

## Proposed Solution
Create `ARCHITECTURE.md` documenting:
- System overview
- Data flow
- Component interactions
- Deployment process

---

### Issue 27: Create runbook for common issues

**Labels:** `low`, `documentation`, `operations`

**Description:**

## Problem
No documented troubleshooting procedures.

## Proposed Solution
Create `RUNBOOK.md` with:
- Common error scenarios
- Resolution steps
- Emergency procedures

---

## Summary

**Total Issues: 27**
- 🔴 Critical: 7 issues
- 🟡 High: 6 issues
- 🟢 Medium: 8 issues
- 🔵 Low: 6 issues

### Recommended Implementation Order

**Phase 1 - Critical Fixes (Week 1):**
1. Standardize Hugo versions (#1)
2. Add workflow timeouts (#2)
3. Fix concurrency group errors (#3)
4. Update deprecated actions (#6)

**Phase 2 - Data Integrity (Week 2):**
5. Implement atomic registry updates (#4)
6. Add cache corruption detection (#10)
7. Create backup mechanism (#11)

**Phase 3 - Testing Foundation (Week 3):**
8. Add unit tests for Python scripts (#7)
9. Add API key validation (#9)
10. Add pre-commit hooks (#19)

**Phase 4 - Resilience (Week 4):**
11. Implement retry mechanisms (#8)
12. Add workflow failure notifications (#12)
13. Review goldmark unsafe setting (#5)

**Phase 5 - Monitoring & Quality (Ongoing):**
14. Add integration tests (#13)
15. Add content validation (#18)
16. Add metrics collection (#20)
17. Add Dependabot (#16)

This provides a clear roadmap for systematically improving the blog's robustness and reliability.
