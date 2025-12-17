# ABOUTME: Analyzes theme CSS to verify color contrast and completeness
# ABOUTME: Checks WCAG contrast ratios and reports potential accessibility issues

import re
import colorsys
from pathlib import Path


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate relative luminance per WCAG 2.1."""
    r, g, b = [x / 255.0 for x in rgb]

    def adjust(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def contrast_ratio(color1: str, color2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    lum1 = relative_luminance(hex_to_rgb(color1))
    lum2 = relative_luminance(hex_to_rgb(color2))
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def parse_themes(css_content: str) -> dict:
    """Parse theme definitions from CSS."""
    themes = {}

    # Match theme blocks (both regular and dark mode)
    theme_pattern = r"\.theme-(\w+)\s*\{([^}]+)\}"
    dark_mode_pattern = r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*\.theme-(\w+)\s*\{([^}]+)\}"

    # Parse regular themes
    for match in re.finditer(theme_pattern, css_content):
        theme_name = match.group(1)
        if theme_name not in themes:
            themes[theme_name] = {"light": {}, "dark": {}}
        props = match.group(2)
        for prop_match in re.finditer(r"--([^:]+):\s*([^;]+);", props):
            themes[theme_name]["light"][prop_match.group(1).strip()] = prop_match.group(
                2
            ).strip()

    # Parse dark mode overrides
    for match in re.finditer(dark_mode_pattern, css_content):
        theme_name = match.group(1)
        if theme_name in themes:
            props = match.group(2)
            for prop_match in re.finditer(r"--([^:]+):\s*([^;]+);", props):
                themes[theme_name]["dark"][
                    prop_match.group(1).strip()
                ] = prop_match.group(2).strip()

    return themes


def check_theme(name: str, colors: dict, mode: str) -> list[str]:
    """Check a theme for potential issues."""
    issues = []

    required_vars = [
        "color-dark",
        "color-light",
        "color-primary",
        "color-secondary",
        "color-link",
    ]

    # Check required variables exist
    for var in required_vars:
        if var not in colors:
            issues.append(f"Missing {var}")

    if not colors:
        issues.append("No color definitions found")
        return issues

    # Check contrast ratios
    bg = colors.get("color-light", "#ffffff")
    fg = colors.get("color-dark", "#000000")
    link = colors.get("color-link", fg)
    primary = colors.get("color-primary", fg)

    try:
        # Text on background (should be >= 4.5 for AA)
        text_contrast = contrast_ratio(fg, bg)
        if text_contrast < 4.5:
            issues.append(f"Low text contrast: {text_contrast:.2f} (need 4.5+)")

        # Link on background
        link_contrast = contrast_ratio(link, bg)
        if link_contrast < 4.5:
            issues.append(f"Low link contrast: {link_contrast:.2f} (need 4.5+)")

    except (ValueError, KeyError) as e:
        issues.append(f"Could not calculate contrast: {e}")

    return issues


def main():
    css_path = Path(__file__).parent.parent / "assets" / "css" / "themes.css"
    css_content = css_path.read_text()

    themes = parse_themes(css_content)

    print("=" * 60)
    print("  Theme Analysis Report")
    print("=" * 60)
    print()

    all_good = True
    theme_summary = []

    for theme_name, modes in sorted(themes.items()):
        print(f"Theme: {theme_name}")
        print("-" * 40)

        has_issues = False

        for mode in ["light", "dark"]:
            colors = modes.get(mode, {})
            if not colors and mode == "dark":
                # Dark mode inherits from light if not specified
                continue

            issues = check_theme(theme_name, colors, mode)

            if issues:
                has_issues = True
                all_good = False
                print(f"  {mode.upper()} MODE:")
                for issue in issues:
                    print(f"    - {issue}")
            else:
                bg = colors.get("color-light", "?")
                fg = colors.get("color-dark", "?")
                link = colors.get("color-link", "?")
                print(f"  {mode.upper()}: bg={bg} fg={fg} link={link}")

        status = "ISSUES" if has_issues else "OK"
        theme_summary.append((theme_name, status))
        print()

    print("=" * 60)
    print("  Summary")
    print("=" * 60)
    for name, status in theme_summary:
        icon = "✓" if status == "OK" else "✗"
        print(f"  {icon} {name}: {status}")

    print()
    if all_good:
        print("All themes pass basic checks!")
    else:
        print("Some themes have potential issues - review above.")

    print()
    print(f"Total themes: {len(themes)}")


if __name__ == "__main__":
    main()
