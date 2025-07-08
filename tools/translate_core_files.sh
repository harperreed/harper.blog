#!/bin/bash

# ABOUTME: This script translates all core files needed for a new language in Hugo blog
# ABOUTME: It handles i18n files, index pages, and sets up the proper directory structure

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
I18N_DIR="$PROJECT_ROOT/i18n"

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

Translates all core files needed for a new language.

Arguments:
    language    Target language (e.g., Spanish, French, German, Korean)

Examples:
    $0 Spanish     # Creates Spanish translations
    $0 French      # Creates French translations  
    $0 Korean      # Creates Korean translations

The script will:
1. Translate the i18n/en.yaml file to create i18n/<lang_code>.yaml
2. Translate core _index.md files using page bundle style (same directory, language suffix)
3. Translate existing page bundles in the page/ directory
4. Create the proper Hugo multilingual page bundle structure

Important core files that will be translated:
- i18n/en.yaml → i18n/<lang_code>.yaml (UI translations)
- content/_index.md → content/_index.<lang_code>.md (homepage)
- content/post/_index.md → content/post/_index.<lang_code>.md (posts section)
- content/page/about/index.md → content/page/about/index.<lang_code>.md (if exists)
- content/page/colophon/index.md → content/page/colophon/index.<lang_code>.md (if exists)
- content/page/translations/index.md → content/page/translations/index.<lang_code>.md (if exists)

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

# Function to translate i18n file
translate_i18n() {
    local language="$1"
    local lang_code="$2"
    
    print_status "Translating i18n file to $language..."
    
    local source_file="$I18N_DIR/en.yaml"
    local target_file="$I18N_DIR/${lang_code}.yaml"
    
    if [[ ! -f "$source_file" ]]; then
        print_error "Source i18n file not found: $source_file"
        return 1
    fi
    
    if [[ -f "$target_file" ]]; then
        print_warning "Target i18n file already exists: $target_file"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Skipping i18n translation"
            return 0
        fi
    fi
    
    print_status "Translating $source_file → $target_file"
    if translator "$source_file" "$language" -o "$target_file" --headless; then
        print_success "Successfully translated i18n file"
    else
        print_error "Failed to translate i18n file"
        return 1
    fi
}

# Function to translate index files using page bundle style
translate_index_files() {
    local language="$1"
    local lang_code="$2"
    
    print_status "Translating index files to $language using page bundle style..."
    
    # Define the core index files to translate (page bundle style)
    local index_files=(
        "_index.md"
        "post/_index.md"
    )
    
    # Add page bundles if they exist
    local page_bundles=(
        "page/about/index.md"
        "page/colophon/index.md"
        "page/translations/index.md"
    )
    
    for page_bundle in "${page_bundles[@]}"; do
        if [[ -f "$CONTENT_DIR/$page_bundle" ]]; then
            index_files+=("$page_bundle")
        else
            print_warning "Page bundle not found: $page_bundle (skipping)"
        fi
    done
    
    local success_count=0
    local total_count=${#index_files[@]}
    
    for index_file in "${index_files[@]}"; do
        local source_file="$CONTENT_DIR/$index_file"
        
        # Create target filename with language suffix (page bundle style)
        local file_dir="$(dirname "$index_file")"
        local file_base="$(basename "$index_file" .md)"
        local target_file="$CONTENT_DIR/$file_dir/${file_base}.${lang_code}.md"
        
        if [[ ! -f "$source_file" ]]; then
            print_warning "Source file not found: $source_file (skipping)"
            continue
        fi
        
        # Check if target file already exists
        if [[ -f "$target_file" ]]; then
            print_warning "Target file already exists: $target_file"
            read -p "Overwrite? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_status "Skipping $index_file"
                ((success_count++))
                continue
            fi
        fi
        
        print_status "Translating $index_file to page bundle format..."
        if translator "$source_file" "$language" -o "$target_file" --headless; then
            print_success "✓ Translated $index_file → ${file_base}.${lang_code}.md"
            ((success_count++))
        else
            print_error "✗ Failed to translate $index_file"
        fi
    done
    
    print_status "Index file translation complete: $success_count/$total_count files"
}

# Function to create language configuration guide
create_config_guide() {
    local language="$1"
    local lang_code="$2"
    
    local guide_file="$PROJECT_ROOT/translation_setup_${lang_code}.md"
    
    cat > "$guide_file" << EOF
# $language Translation Setup Guide

This guide was automatically generated after translating core files to $language.

## Files Translated

### 1. i18n File
- **Source**: \`i18n/en.yaml\`
- **Target**: \`i18n/${lang_code}.yaml\`
- **Purpose**: UI element translations (buttons, labels, navigation, etc.)

### 2. Content Index Files (Page Bundle Style)
- **Source**: \`content/\` directory  
- **Target**: Same \`content/\` directory with language suffix
- **Files translated**:
  - \`_index.md\` → \`_index.${lang_code}.md\` (Homepage)
  - \`post/_index.md\` → \`post/_index.${lang_code}.md\` (Posts section)
  - \`page/about/index.md\` → \`page/about/index.${lang_code}.md\` (About page, if exists)
  - \`page/colophon/index.md\` → \`page/colophon/index.${lang_code}.md\` (Colophon page, if exists)
  - \`page/translations/index.md\` → \`page/translations/index.${lang_code}.md\` (Translations page, if exists)

## Next Steps

### 1. Update Hugo Configuration
Add the following to your \`config/_default/languages.toml\`:

\`\`\`toml
[${lang_code}]
  languageName = "$language"
  weight = [next_weight]
\`\`\`

Note: No \`contentDir\` needed for page bundle style - all content stays in the main \`content/\` directory.

### 2. Review Translations
- Check all translated files for accuracy
- Adjust any cultural or contextual adaptations needed
- Verify that formatting and frontmatter are preserved

### 3. Test the Site
\`\`\`bash
hugo server --buildDrafts --buildFuture
\`\`\`

### 4. Translate Additional Content
Use the batch translation tool for posts (page bundle style):
\`\`\`bash
uv run tools/batch_translate.py content/post/ $language --page-bundle --lang-code ${lang_code}
\`\`\`

## File Structure Created (Page Bundle Style)

\`\`\`
├── i18n/
│   └── ${lang_code}.yaml
├── content/
│   ├── _index.${lang_code}.md
│   ├── post/
│   │   └── _index.${lang_code}.md
│   └── page/
│       ├── about/
│       │   └── index.${lang_code}.md (if source exists)
│       ├── colophon/
│       │   └── index.${lang_code}.md (if source exists)
│       └── translations/
│           └── index.${lang_code}.md (if source exists)
\`\`\`

## Notes
- Generated on $(date)
- Language code: ${lang_code}
- Target language: $language

EOF

    print_success "Created setup guide: $guide_file"
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
    
    print_status "Setting up $language translations (language code: $lang_code)"
    
    # Change to project root
    cd "$PROJECT_ROOT"
    
    # Check prerequisites
    check_translator
    
    # Translate i18n file
    translate_i18n "$language" "$lang_code"
    
    # Translate index files
    translate_index_files "$language" "$lang_code"
    
    # Create configuration guide
    create_config_guide "$language" "$lang_code"
    
    print_success "Translation setup complete for $language!"
    echo
    print_status "Next steps:"
    echo "  1. Review translated files for accuracy"
    echo "  2. Add language configuration to config/_default/languages.toml"
    echo "  3. Test with: hugo server --buildDrafts --buildFuture"
    echo "  4. See translation_setup_${lang_code}.md for detailed instructions"
}

# Run main function with all arguments
main "$@"