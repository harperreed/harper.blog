# ABOUTME: This script batch translates blog posts using the AICoder Translator tool
# ABOUTME: It handles page bundles and markdown files for Hugo static site generation

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Optional, Dict
import logging
import shutil

def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def find_translator_binary() -> Optional[str]:
    """Find the translator binary in PATH."""
    return shutil.which('translator')

def validate_language(language: str) -> bool:
    """Basic validation for language parameter."""
    # Simple check - language should be alphabetic and reasonable length
    return language.isalpha() and 2 <= len(language) <= 20

def get_output_filename(input_file: Path, language: str, output_dir: Optional[Path] = None) -> Path:
    """Generate output filename based on language and optional output directory."""
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        return output_dir / f"{input_file.stem}.{language.lower()}.md"
    else:
        # Place in same directory as input with language suffix
        return input_file.parent / f"{input_file.stem}.{language.lower()}.md"

def translate_file(file_path: Path, language: str, translator_binary: str, 
                  output_dir: Optional[Path] = None, dry_run: bool = False,
                  translator_args: Optional[List[str]] = None) -> bool:
    """Translate a single file using the translator tool."""
    logger = logging.getLogger(__name__)
    
    if not file_path.exists():
        logger.error(f"File does not exist: {file_path}")
        return False
    
    if not file_path.suffix.lower() == '.md':
        logger.warning(f"Skipping non-markdown file: {file_path}")
        return True
    
    output_file = get_output_filename(file_path, language, output_dir)
    
    # Build translator command
    cmd = [translator_binary, str(file_path), language]
    
    # Add output file specification
    cmd.extend(['-o', str(output_file)])
    
    # Add any additional translator arguments
    if translator_args:
        cmd.extend(translator_args)
    
    logger.info(f"Translating: {file_path.name} -> {output_file.name}")
    
    if dry_run:
        logger.info(f"DRY RUN: Would execute: {' '.join(cmd)}")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.debug(f"Translator output: {result.stdout}")
        logger.info(f"Successfully translated: {file_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Translation failed for {file_path.name}: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error translating {file_path.name}: {e}")
        return False

def find_page_bundles(content_dir: Path) -> List[Path]:
    """Find all page bundles (directories with index.md) in content directory."""
    bundles = []
    
    for item in content_dir.rglob('*'):
        if item.is_dir():
            index_file = item / 'index.md'
            if index_file.exists():
                bundles.append(index_file)
    
    return bundles

def find_markdown_files(paths: List[str], include_bundles: bool = True) -> List[Path]:
    """Find all markdown files in the given paths."""
    files = []
    
    for path_str in paths:
        path = Path(path_str)
        
        if not path.exists():
            logging.warning(f"Path does not exist: {path}")
            continue
        
        if path.is_file() and path.suffix.lower() == '.md':
            files.append(path)
        elif path.is_dir():
            # Find all markdown files in directory
            md_files = list(path.rglob('*.md'))
            
            if not include_bundles:
                # Filter out index.md files (page bundles)
                md_files = [f for f in md_files if f.name != 'index.md']
            
            files.extend(md_files)
    
    return files

def main():
    parser = argparse.ArgumentParser(
        description="Batch translate blog posts using AICoder Translator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Translate all posts in content/post/ to Spanish
  uv run tools/batch_translate.py content/post/ Spanish
  
  # Translate specific files to Japanese with output directory
  uv run tools/batch_translate.py content/post/2024-*.md Japanese -o content.ja/post/
  
  # Dry run to see what would be translated
  uv run tools/batch_translate.py content/post/ French --dry-run
  
  # Skip editing step for faster translation
  uv run tools/batch_translate.py content/post/ German --translator-args --no-edit
        """
    )
    
    parser.add_argument('paths', nargs='+', 
                      help='Files or directories to translate')
    parser.add_argument('language',
                      help='Target language (e.g., Spanish, Japanese, French)')
    parser.add_argument('-o', '--output-dir', type=Path,
                      help='Output directory for translated files')
    parser.add_argument('--dry-run', action='store_true',
                      help='Show what would be translated without doing it')
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose logging')
    parser.add_argument('--include-bundles', action='store_true', default=True,
                      help='Include page bundles (index.md files)')
    parser.add_argument('--translator-args', nargs='*',
                      help='Additional arguments to pass to translator')
    parser.add_argument('--max-files', type=int,
                      help='Maximum number of files to translate (for testing)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Validate language
    if not validate_language(args.language):
        logger.error(f"Invalid language: {args.language}")
        sys.exit(1)
    
    # Find translator binary
    translator_binary = find_translator_binary()
    if not translator_binary:
        logger.error("Translator binary not found in PATH. Please install it first.")
        sys.exit(1)
    
    logger.info(f"Using translator: {translator_binary}")
    
    # Find files to translate
    files_to_translate = find_markdown_files(args.paths, args.include_bundles)
    
    if not files_to_translate:
        logger.warning("No markdown files found to translate")
        sys.exit(0)
    
    # Apply max files limit if specified
    if args.max_files:
        files_to_translate = files_to_translate[:args.max_files]
        logger.info(f"Limited to {len(files_to_translate)} files")
    
    logger.info(f"Found {len(files_to_translate)} files to translate to {args.language}")
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be translated")
    
    # Translate files
    success_count = 0
    failure_count = 0
    
    for file_path in files_to_translate:
        success = translate_file(
            file_path, 
            args.language, 
            translator_binary,
            args.output_dir,
            args.dry_run,
            args.translator_args
        )
        
        if success:
            success_count += 1
        else:
            failure_count += 1
    
    # Summary
    logger.info(f"Translation complete: {success_count} successful, {failure_count} failed")
    
    if failure_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()