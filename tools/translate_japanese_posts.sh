#!/bin/bash

# ABOUTME: This script finds posts that have Japanese translations and translates the English versions to other languages
# ABOUTME: It preserves existing translations and only translates posts that have Japanese versions

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONTENT_DIR="$PROJECT_ROOT/content"
POST_DIR="$CONTENT_DIR/post"

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

# Function to show usage
usage() {
    cat << EOF
Usage: $0 <language>

Translates English posts to a new target language, but only for posts that already have Japanese translations.

Arguments:
    language    Target language (e.g., Spanish, French, German, Korean)

Examples:
    $0 Spanish     # Translates English posts to Spanish (for posts with Japanese translations)
    $0 French      # Translates English posts to French (for posts with Japanese translations)  
    $0 Korean      # Translates English posts to Korean (for posts with Japanese translations)

The script will:
1. Find all post directories that contain Japanese translations (index.ja.md)
2. Translate the English version (index.md) to the target language
3. Create index.<lang_code>.md files for each translated post
4. Skip any posts that already have translations in the target language
5. Preserve all existing content and translations

Note: This script requires the 'translator' tool to be installed.
Install with: pip install aicoder-translator

EOF
}

# Function to get language code from language name
get_language_code() {
    local language="$1"
    local lower_language=$(echo "$language" | tr '[:upper:]' '[:lower:]')
    case "$lower_language" in
        spanish|español) echo "es" ;;
        french|français) echo "fr" ;;
        german|deutsch) echo "de" ;;
        italian|italiano) echo "it" ;;
        portuguese|português) echo "pt" ;;
        russian|русский) echo "ru" ;;
        chinese|中文) echo "zh" ;;
        japanese|日本語) echo "ja" ;;
        korean|한국어) echo "ko" ;;
        dutch|nederlands) echo "nl" ;;
        swedish|svenska) echo "sv" ;;
        norwegian|norsk) echo "no" ;;
        danish|dansk) echo "da" ;;
        finnish|suomi) echo "fi" ;;
        polish|polski) echo "pl" ;;
        czech|čeština) echo "cs" ;;
        hungarian|magyar) echo "hu" ;;
        greek|ελληνικά) echo "el" ;;
        turkish|türkçe) echo "tr" ;;
        arabic|العربية) echo "ar" ;;
        hebrew|עברית) echo "he" ;;
        hindi|हिन्दी) echo "hi" ;;
        thai|ไทย) echo "th" ;;
        vietnamese|tiếng\ việt) echo "vi" ;;
        indonesian|bahasa\ indonesia) echo "id" ;;
        malay|bahasa\ melayu) echo "ms" ;;
        *)
            print_warning "Unknown language '$language', using first two letters as language code"
            echo "${language:0:2}" | tr '[:upper:]' '[:lower:]'
            ;;
    esac
}

# Function to check if translator is available
check_translator() {
    if ! command -v translator &> /dev/null; then
        print_error "Translator tool not found. Please install it first."
        echo "Install with: pip install aicoder-translator"
        exit 1
    fi
    print_status "Found translator: $(which translator)"
}

# Function to find posts with Japanese translations
find_japanese_posts() {
    print_status "Scanning for posts with Japanese translations..."
    
    local japanese_posts=()
    
    # Find all directories in the post directory
    while IFS= read -r -d '' post_dir; do
        local japanese_file="$post_dir/index.ja.md"
        if [[ -f "$japanese_file" ]]; then
            local post_name=$(basename "$post_dir")
            japanese_posts+=("$post_name")
            print_status "Found Japanese translation: $post_name"
        fi
    done < <(find "$POST_DIR" -mindepth 1 -maxdepth 1 -type d -print0 2>/dev/null)
    
    if [[ ${#japanese_posts[@]} -eq 0 ]]; then
        print_warning "No posts with Japanese translations found"
        return 1
    fi
    
    print_success "Found ${#japanese_posts[@]} posts with Japanese translations"
    printf '%s\n' "${japanese_posts[@]}"
}

# Function to translate Japanese posts to target language
translate_posts() {
    local language="$1"
    local lang_code="$2"
    
    print_status "Starting translation of Japanese posts to $language ($lang_code)..."
    
    # Get list of posts with Japanese translations
    local japanese_posts=()
    while IFS= read -r post; do
        japanese_posts+=("$post")
    done < <(find_japanese_posts)
    
    if [[ ${#japanese_posts[@]} -eq 0 ]]; then
        print_error "No Japanese posts found to translate"
        return 1
    fi
    
    local success_count=0
    local skip_count=0
    local error_count=0
    
    for post_name in "${japanese_posts[@]}"; do
        local post_dir="$POST_DIR/$post_name"
        local english_file="$post_dir/index.md"
        local japanese_file="$post_dir/index.ja.md"
        local target_file="$post_dir/index.${lang_code}.md"
        
        # Skip if target translation already exists
        if [[ -f "$target_file" ]]; then
            print_warning "Translation already exists: $post_name (skipping)"
            ((skip_count++))
            continue
        fi
        
        # Verify English file exists
        if [[ ! -f "$english_file" ]]; then
            print_error "English file missing: $english_file"
            ((error_count++))
            continue
        fi
        
        # Verify Japanese file still exists (requirement for inclusion)
        if [[ ! -f "$japanese_file" ]]; then
            print_error "Japanese file missing: $japanese_file"
            ((error_count++))
            continue
        fi
        
        print_status "Translating $post_name: English → $language"
        
        # Translate the English file (headless mode)
        if translator "$english_file" "$language" -o "$target_file" --headless; then
            print_success "✓ Translated $post_name"
            ((success_count++))
        else
            print_error "✗ Failed to translate $post_name"
            ((error_count++))
        fi
    done
    
    # Print summary
    echo
    print_status "Translation Summary:"
    echo "  ✓ Successfully translated: $success_count posts"
    echo "  ⚠ Skipped (already exists): $skip_count posts"
    echo "  ✗ Failed: $error_count posts"
    echo "  📝 Total Japanese posts found: ${#japanese_posts[@]}"
    
    if [[ $success_count -gt 0 ]]; then
        print_success "Translation completed! Created $success_count new $language translations."
    fi
}

# Function to create summary report
create_summary_report() {
    local language="$1"
    local lang_code="$2"
    
    local report_file="$PROJECT_ROOT/japanese_translation_report_${lang_code}.md"
    
    cat > "$report_file" << EOF
# Japanese Post Translation Report

Generated on: $(date)
Target language: $language ($lang_code)
Source: English posts (index.md files) from posts that have Japanese translations

## Process Summary

This script found all post page bundles containing Japanese translations and translated their English versions to $language.

### Translation Strategy
- **Criteria**: Posts that have Japanese translations (\`index.ja.md\`)
- **Source**: English posts (\`index.md\`)
- **Target**: $language translations (\`index.${lang_code}.md\`)
- **Method**: Page bundle style (same directory, language suffix)
- **Safety**: Existing translations are never overwritten

### File Structure Created
Each translated post follows this structure:
\`\`\`
content/post/[post-name]/
├── index.md           # English (source for this translation)
├── index.ja.md        # Japanese (indicates post is multilingual)
├── index.${lang_code}.md      # New $language translation
└── [shared assets]
\`\`\`

### Next Steps
1. Review translated posts for accuracy
2. Test the site: \`hugo server --buildDrafts --buildFuture\`
3. Add any missing language configuration if needed
4. Consider translating additional posts manually if desired

### Posts Translated
$(find_japanese_posts | while read -r post; do echo "- $post"; done)

## Notes
- All translations maintain the same \`translationKey\` for Hugo's multilingual linking
- Shared assets (images) are reused across all language variants
- Translation log files may be created by the translator tool

---
Generated by: translate_japanese_posts.sh
EOF

    print_success "Created translation report: $report_file"
}

# Main function
main() {
    if [[ $# -ne 1 ]]; then
        usage
        exit 1
    fi
    
    local language="$1"
    local lang_code
    lang_code=$(get_language_code "$language")
    
    print_status "Translating Japanese posts to $language (language code: $lang_code)"
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Check prerequisites
    check_translator
    
    # Check if post directory exists
    if [[ ! -d "$POST_DIR" ]]; then
        print_error "Post directory not found: $POST_DIR"
        exit 1
    fi
    
    # Translate posts
    translate_posts "$language" "$lang_code"
    
    # Create summary report
    create_summary_report "$language" "$lang_code"
    
    print_success "Japanese post translation process complete!"
    echo
    print_status "Next steps:"
    echo "  1. Review translated posts for accuracy"
    echo "  2. Test with: hugo server --buildDrafts --buildFuture"
    echo "  3. See japanese_translation_report_${lang_code}.md for details"
}

# Run main function with all arguments
main "$@"