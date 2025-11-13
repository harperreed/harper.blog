#!/bin/bash
# Script to create all GitHub issues
# Run this after reviewing GITHUB_ISSUES.md

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Creating GitHub issues for blog improvements...${NC}\n"

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}ERROR: GitHub CLI (gh) is not installed.${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}ERROR: Not authenticated with GitHub CLI.${NC}"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI is ready${NC}\n"

# Function to create an issue
create_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"

    echo -e "Creating issue: ${YELLOW}$title${NC}"

    gh issue create \
        --title "$title" \
        --body "$body" \
        --label "$labels"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Created successfully${NC}\n"
    else
        echo -e "${RED}✗ Failed to create${NC}\n"
    fi
}

# 🔴 Critical Priority Issues

echo -e "${RED}=== CRITICAL PRIORITY ISSUES ===${NC}\n"

create_issue \
    "🔴 [Critical] Standardize Hugo versions across all environments" \
    "## Problem
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
2. Update \`.github/workflows/*.yaml\` to use Hugo 0.145.0
3. Update \`go.mod\` to require Go 1.23
4. Document version requirements in README.md

## Files to Update
- \`.github/workflows/new-hugo-deploy.yaml\`
- \`.github/workflows/notes.yaml\`
- \`.github/workflows/links.yaml\`
- \`.github/workflows/grab_goodreads.yaml\`
- \`.github/workflows/grab_spotify_saved_tracks.yaml\`
- \`go.mod\`
- \`netlify.toml\` (verify version)

## Priority
🔴 **Critical** - Should be fixed immediately to prevent deployment issues" \
    "critical,infrastructure,build"

create_issue \
    "🔴 [Critical] Add timeout configurations to all GitHub Actions workflows" \
    "## Problem
Several GitHub Actions workflows are missing timeout configurations:
- \`notes.yaml\` - runs every 10 minutes
- \`links.yaml\` - runs every 30 minutes
- \`grab_goodreads.yaml\` - runs every 12 hours
- \`grab_spotify_saved_tracks.yaml\` - runs every 24 hours

## Impact
- Workflows could run indefinitely if they hang
- Consumes GitHub Actions minutes unnecessarily
- Blocks concurrent runs due to concurrency groups
- Difficult to detect stuck workflows

## Proposed Solution
Add \`timeout-minutes\` to all workflow jobs:
\`\`\`yaml
jobs:
  job-name:
    timeout-minutes: 15  # or appropriate value
\`\`\`

## Recommended Timeouts
- \`notes.yaml\`: 10 minutes
- \`links.yaml\`: 20 minutes (uses OpenAI API)
- \`grab_goodreads.yaml\`: 15 minutes
- \`grab_spotify_saved_tracks.yaml\`: 10 minutes
- \`new-hugo-deploy.yaml\`: Already has timeouts ✅

## Priority
🔴 **Critical** - Prevents runaway workflows" \
    "critical,ci-cd,workflows"

create_issue \
    "🔴 [Critical] Fix workflow concurrency group naming errors" \
    "## Problem
Copy-paste errors in workflow concurrency groups causing conflicts:

1. **grab_goodreads.yaml**:
   - Uses concurrency group: \`spotify-tracks-\${{ github.ref }}\` ❌
   - Commit message says \"Auto update spotify tracks\" ❌
   - Should be \"goodreads\" related

2. **Duplicate concurrency group**: Both Goodreads and Spotify workflows could share the same group name

## Impact
- Workflows may cancel each other incorrectly
- Concurrent git commits could conflict
- Confusing commit messages in git history
- Difficult to debug workflow behavior

## Proposed Solution

**grab_goodreads.yaml:**
\`\`\`yaml
concurrency:
  group: goodreads-books-\${{ github.ref }}
  cancel-in-progress: true
\`\`\`

Commit message should be:
\`\`\`
Auto update Goodreads books
\`\`\`

## Files to Fix
- \`.github/workflows/grab_goodreads.yaml\`

## Priority
🔴 **Critical** - Currently causing incorrect workflow behavior" \
    "critical,ci-cd,bug"

create_issue \
    "🔴 [Critical] Implement atomic registry updates with file locking" \
    "## Problem
Registry files are updated non-atomically, creating race conditions:
- \`/data/notes/processed_urls.json\`
- \`/data/notes/processed_content_hashes.json\`

**Current flow:**
1. Read registry
2. Process content
3. Write to disk
4. Update registry ❌ (Could fail here)

**Issues:**
- Multiple workflows could write simultaneously
- Partial state on failures (content created but not tracked)
- \`shutil.rmtree\` happens AFTER registry update (could lose tracking)
- No corruption detection/recovery

## Impact
- Duplicate content could be created
- Registry corruption over time
- Lost tracking of processed items
- Manual cleanup required

## Proposed Solution
See GITHUB_ISSUES.md for detailed implementation including:
1. File locking with fcntl
2. Transactional updates
3. Corruption detection

## Files to Update
- \`tools/grab_micro_posts_fixed.py\`
- \`tools/grab_starred_links.py\`

## Priority
🔴 **Critical** - Data integrity issue" \
    "critical,automation,data-integrity"

create_issue \
    "🔴 [Critical] Review and fix goldmark unsafe HTML rendering" \
    "## Problem
Configuration allows unsafe HTML rendering:

**config/_default/markup.toml:**
\`\`\`toml
[goldmark.renderer]
unsafe = true
\`\`\`

## Impact
- Potential XSS vulnerabilities if untrusted content is processed
- Arbitrary HTML/JavaScript can be injected
- Violates Content Security Policy principles

## Proposed Solution

### Option 1: Disable Unsafe (Recommended)
\`\`\`toml
[goldmark.renderer]
unsafe = false
\`\`\`
- Review all content that uses raw HTML
- Convert to Hugo shortcodes where needed
- Add shortcodes for specific use cases (embeds, etc.)

### Option 2: Keep Unsafe but Document
If raw HTML is required:
1. Document WHY it's needed
2. Add content validation pipeline
3. Ensure all automated content is sanitized
4. Never allow user-submitted content

## Files to Review
- \`config/_default/markup.toml\`
- Content files using raw HTML
- Python scripts generating content

## Priority
🔴 **Critical** - Security concern" \
    "critical,security,config"

create_issue \
    "🔴 [Critical] Update deprecated GitHub Actions to latest versions" \
    "## Problem
Workflows using deprecated action versions:
- \`actions/checkout@v2\` → Should use \`v4\`
- \`actions/cache@v2\` → Should use \`v4\`
- \`actions/setup-python@v2\` → Should use \`v5\`

## Impact
- Security vulnerabilities in old versions
- Deprecated features may stop working
- Missing performance improvements
- GitHub warnings in workflow logs

## Proposed Solution
Update all workflows to latest stable versions.

## Files to Update
- \`.github/workflows/notes.yaml\`
- \`.github/workflows/links.yaml\`
- \`.github/workflows/grab_goodreads.yaml\`
- \`.github/workflows/grab_spotify_saved_tracks.yaml\`
- \`.github/workflows/new-hugo-deploy.yaml\`

## Priority
🔴 **Critical** - Security and maintenance" \
    "critical,ci-cd,dependencies"

create_issue \
    "🔴 [Critical] Add comprehensive unit tests for Python automation scripts" \
    "## Problem
Zero test coverage for Python automation scripts:
- \`tools/grab_micro_posts_fixed.py\` (838 lines)
- \`tools/grab_starred_links.py\` (238 lines)
- \`tools/grab_read_books.py\` (540 lines)
- \`tools/grab_spotify_saved_tracks.py\` (205 lines)
- \`tools/deduplicate_notes.py\` (273 lines)

## Impact
- No confidence when refactoring
- Bugs discovered in production only
- Difficult to validate behavior changes
- Regression risks when updating dependencies

## Proposed Solution
See GITHUB_ISSUES.md for detailed testing strategy including:
1. Testing infrastructure setup (pytest)
2. Priority test areas
3. Mock strategies
4. Target coverage goals

## Priority
🔴 **Critical** - Foundation for reliability" \
    "critical,testing,automation"

# 🟡 High Priority Issues

echo -e "${YELLOW}=== HIGH PRIORITY ISSUES ===${NC}\n"

create_issue \
    "🟡 [High] Implement retry mechanisms with exponential backoff for API calls" \
    "## Problem
Python scripts lack retry logic for API calls:
- OpenAI API calls (no retries)
- Firecrawl API calls (no retries)
- Spotify API calls (no retries)
- Goodreads API calls (no retries)

## Impact
- Transient network failures cause complete script failure
- Manual re-runs required for temporary issues

## Proposed Solution
Use \`tenacity\` library for retry logic with exponential backoff.

See GITHUB_ISSUES.md for detailed implementation.

## Priority
🟡 **High** - Significantly improves reliability" \
    "high,automation,resilience"

create_issue \
    "🟡 [High] Add API key validation before script execution" \
    "## Problem
Scripts don't validate required environment variables/API keys before execution.

## Impact
- Scripts fail partway through execution
- Partial state changes without completion
- Confusing error messages

## Proposed Solution
Add validation function that checks all required env vars at startup.

See GITHUB_ISSUES.md for implementation details.

## Priority
🟡 **High** - Prevents wasted execution" \
    "high,automation,validation"

create_issue \
    "🟡 [High] Implement cache corruption detection and recovery" \
    "## Problem
Disk cache and registries lack corruption detection:
- No validation on load
- No automatic repair
- No backup restoration

## Impact
- Silent failures with cached corrupted data
- Scripts crash on corrupted registries
- Manual intervention required

## Proposed Solution
See GITHUB_ISSUES.md for implementation of:
1. Registry validation with auto-repair
2. Cache entry validation
3. Health check commands

## Priority
🟡 **High** - Prevents data loss" \
    "high,automation,data-integrity"

create_issue \
    "🟡 [High] Create backup mechanism for registry files" \
    "## Problem
Registry files have no backup strategy.

## Impact
- Corruption means complete loss
- No way to recover from mistakes
- Re-processing everything required

## Proposed Solution
Implement:
1. Automatic timestamped backups
2. Git-tracked registries (optional)
3. Recovery command

See GITHUB_ISSUES.md for details.

## Priority
🟡 **High** - Data safety" \
    "high,automation,data-integrity"

create_issue \
    "🟡 [High] Add workflow failure notifications" \
    "## Problem
GitHub Actions workflows fail silently - no notifications.

## Impact
- Automation failures go unnoticed
- Content stops updating
- Manual monitoring required

## Proposed Solution
Add Slack/Discord/email notifications on failure.

See GITHUB_ISSUES.md for implementation.

## Priority
🟡 **High** - Essential for operations" \
    "high,ci-cd,monitoring"

create_issue \
    "🟡 [High] Implement integration tests for workflow orchestration" \
    "## Problem
No testing of how workflows interact.

## Impact
- Workflows could conflict
- Race conditions possible
- Behavior untested

## Proposed Solution
Create integration test workflow with dry-run modes.

See GITHUB_ISSUES.md for details.

## Priority
🟡 **High** - Prevents production issues" \
    "high,testing,ci-cd"

# 🟢 Medium Priority Issues

echo -e "${GREEN}=== MEDIUM PRIORITY ISSUES ===${NC}\n"

create_issue \
    "🟢 [Medium] Replace deprecated Goodreads API" \
    "## Problem
Goodreads API is deprecated and could stop working.

## Proposed Solutions
1. OpenLibrary API
2. Manual JSON file
3. Literal.club integration
4. Goodreads RSS (may last longer)

See GITHUB_ISSUES.md for detailed options.

## Priority
🟢 **Medium** - Not urgent but needs addressing" \
    "medium,automation,dependencies,breaking-change"

create_issue \
    "🟢 [Medium] Tighten Python dependency version constraints" \
    "## Problem
Loose version constraints could pull in breaking changes.

## Proposed Solution
Use restrictive constraints and regular update workflow.

See GITHUB_ISSUES.md for details.

## Priority
🟢 **Medium** - Maintenance and security" \
    "medium,dependencies,maintenance"

create_issue \
    "🟢 [Medium] Add Dependabot or Renovate configuration" \
    "## Problem
No automated dependency updates.

## Proposed Solution
Add Dependabot configuration for Python, GitHub Actions, and Go modules.

See GITHUB_ISSUES.md for configuration.

## Priority
🟢 **Medium** - Ongoing maintenance" \
    "medium,dependencies,automation"

create_issue \
    "🟢 [Medium] Implement CDN purge mechanism for updated content" \
    "## Problem
No CDN cache invalidation when content updates.

## Proposed Solution
Add Netlify cache purging to workflows.

See GITHUB_ISSUES.md for implementation.

## Priority
🟢 **Medium** - UX improvement" \
    "medium,performance,deployment"

create_issue \
    "🟢 [Medium] Add content validation pipeline" \
    "## Problem
No validation of generated content frontmatter.

## Proposed Solution
Create content validator script and add to CI.

See GITHUB_ISSUES.md for implementation.

## Priority
🟢 **Medium** - Quality assurance" \
    "medium,quality,ci-cd"

create_issue \
    "🟢 [Medium] Add pre-commit hooks for code quality" \
    "## Problem
No automated code quality checks before commit.

## Proposed Solution
Set up pre-commit with ruff, bandit, and general hooks.

See GITHUB_ISSUES.md for configuration.

## Priority
🟢 **Medium** - Developer experience" \
    "medium,quality,developer-experience"

create_issue \
    "🟢 [Medium] Add metrics collection for builds and automations" \
    "## Problem
No visibility into automation performance.

## Proposed Solution
Implement metrics collection and dashboard.

See GITHUB_ISSUES.md for implementation.

## Priority
🟢 **Medium** - Operations visibility" \
    "medium,monitoring,observability"

create_issue \
    "🟢 [Medium] Implement secret rotation strategy" \
    "## Problem
17 different secrets with no rotation strategy.

## Proposed Solution
Document all secrets and create rotation reminders.

See GITHUB_ISSUES.md for process.

## Priority
🟢 **Medium** - Security hygiene" \
    "medium,security,operations"

echo -e "\n${BLUE}=== SUMMARY ===${NC}"
echo -e "Created issues across all priority levels."
echo -e "\n${GREEN}✓ All issues created successfully!${NC}"
echo -e "\nView issues at: https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner)/issues"
echo -e "\nNext steps:"
echo -e "1. Review and prioritize issues"
echo -e "2. Assign issues to milestones"
echo -e "3. Create project board for tracking"
echo -e "4. Start with Phase 1 (Critical fixes)"
