#!/bin/bash

# ABOUTME: Manual workflow script to check the micro.blog archive for missing posts
# ABOUTME: Runs grab_micro_posts_fixed.py --check-archive and optionally commits changes

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default options
VERBOSE=false
COMMIT=false
DRY_RUN=false

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
}

# Function to show usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Manually check the micro.blog archive for missing posts and optionally import them.

This script runs the grab_micro_posts_fixed.py script with --check-archive flag,
which compares the archive feed against local content and imports any missing posts.

Options:
    -v, --verbose     Enable verbose/debug logging
    -c, --commit      Auto-commit and push changes if any posts are imported
    -d, --dry-run     Show what would be done without making changes
    -h, --help        Show this help message

Examples:
    $0                      # Check archive, import missing posts
    $0 --verbose            # Check with detailed logging
    $0 --commit             # Check, import, and auto-commit changes
    $0 --dry-run --verbose  # Preview what would be imported

Archive URL checked:
    https://raw.githubusercontent.com/harperreed/harper.micro.blog/refs/heads/main/feed.json

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -c|--commit)
                COMMIT=true
                shift
                ;;
            -d|--dry-run)
                DRY_RUN=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                usage
                exit 1
                ;;
        esac
    done
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."

    # Check if uv is available
    if ! command -v uv &> /dev/null; then
        print_error "uv is not installed. Please install it first."
        echo "  Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi

    # Check if the Python script exists
    if [[ ! -f "$SCRIPT_DIR/grab_micro_posts_fixed.py" ]]; then
        print_error "grab_micro_posts_fixed.py not found in $SCRIPT_DIR"
        exit 1
    fi

    # Check if we're in a git repo (only if commit is requested)
    if [[ "$COMMIT" == "true" ]]; then
        if ! git -C "$PROJECT_ROOT" rev-parse --git-dir &> /dev/null; then
            print_error "Not in a git repository. Cannot use --commit flag."
            exit 1
        fi
    fi

    print_success "Prerequisites check passed"
}

# Run the archive check
run_archive_check() {
    print_header "Checking Micro.blog Archive for Missing Posts"

    # Build the command
    local cmd="uv run grab_micro_posts_fixed.py --check-archive"

    if [[ "$VERBOSE" == "true" ]]; then
        cmd="$cmd --verbose"
    fi

    print_status "Running: $cmd"
    echo

    if [[ "$DRY_RUN" == "true" ]]; then
        print_warning "DRY RUN: Would execute the following command:"
        echo "  cd $SCRIPT_DIR && $cmd"
        echo
        print_status "To see what posts would be imported, run without --dry-run"
        return 0
    fi

    # Change to tools directory and run
    cd "$SCRIPT_DIR"

    if eval "$cmd"; then
        print_success "Archive check completed successfully"
        return 0
    else
        print_error "Archive check encountered an error"
        return 1
    fi
}

# Commit changes if requested
commit_changes() {
    if [[ "$COMMIT" != "true" ]]; then
        return 0
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        print_warning "DRY RUN: Would check for and commit changes"
        return 0
    fi

    print_header "Checking for Changes to Commit"

    cd "$PROJECT_ROOT"

    # Check if there are any changes
    git add content/notes data/notes 2>/dev/null || true

    if git diff --quiet && git diff --staged --quiet; then
        print_status "No changes to commit"
        return 0
    fi

    # Show what changed
    print_status "Changes detected:"
    git status --short content/notes data/notes
    echo

    # Commit and push
    print_status "Committing changes..."
    git commit -m "fix(tools): improve micro posts archive handling"

    print_status "Pushing to remote..."
    if git push; then
        print_success "Changes committed and pushed successfully"
    else
        print_error "Failed to push changes"
        return 1
    fi
}

# Show summary
show_summary() {
    echo
    print_header "Summary"

    # Count notes
    local note_count
    note_count=$(find "$PROJECT_ROOT/content/notes" -type d -name "20*" 2>/dev/null | wc -l | tr -d ' ')

    print_status "Total notes in content/notes: $note_count"

    # Show recent notes if verbose
    if [[ "$VERBOSE" == "true" ]]; then
        echo
        print_status "Most recent notes:"
        find "$PROJECT_ROOT/content/notes" -type d -name "20*" 2>/dev/null | sort -r | head -5 | while read -r dir; do
            echo "  - $(basename "$dir")"
        done
    fi

    echo
    print_success "Done!"
}

# Main function
main() {
    parse_args "$@"

    print_header "Micro.blog Archive Checker"
    echo

    # Show options
    print_status "Options:"
    echo "  Verbose:  $VERBOSE"
    echo "  Commit:   $COMMIT"
    echo "  Dry-run:  $DRY_RUN"
    echo

    check_prerequisites
    echo

    run_archive_check
    echo

    commit_changes

    show_summary
}

# Run main function with all arguments
main "$@"
