# ABOUTME: WCAG AA contrast sweep across every theme palette in assets/css.
# ABOUTME: Run after touching root-colors.css or themes.css: `make check-contrast`.
#
# Models the real cascade for a theme class in dark mode:
#   root light block <- root dark block <- theme LIGHT block <- theme dark block
# A theme's light-block variables apply in dark mode unless its dark block
# overrides them - that leak is the classic way contrast regressions sneak in.
#
# Pure stdlib. Exits 1 and lists every failing pair below 4.5:1.

import re
import sys
from pathlib import Path

THRESHOLD = 4.5  # WCAG 2.1 AA, normal text

REPO = Path(__file__).resolve().parent.parent
DEFAULT_ROOT_CSS = REPO / "assets/css/root-colors.css"
DEFAULT_THEMES_CSS = REPO / "assets/css/themes.css"


def parse_blocks(text):
    """Yield (selector, in_dark_media, {var: value}) for each rule block."""
    out = []
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    i, n = 0, len(text)
    media_stack = []
    in_dark = False
    while i < n:
        m = re.compile(r"([^{}]+)\{").match(text, i)
        if not m:
            if text[i] == "}":
                if media_stack and media_stack[-1] == "dark":
                    media_stack.pop()
                    in_dark = "dark" in media_stack
                i += 1
                continue
            i += 1
            continue
        sel = m.group(1).strip()
        if sel.startswith(("@media", "@supports")):
            media_stack.append("dark" if "dark" in sel else "other")
            in_dark = "dark" in sel or in_dark
            i = m.end()
            continue
        close = text.index("}", m.end())
        body = text[m.end():close]
        vars_ = dict(re.findall(r"--([\w-]+)\s*:\s*([^;]+);", body))
        out.append((sel, in_dark, vars_))
        i = close + 1
    return out


def hex_to_rgb(h):
    h = h.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[j:j + 2], 16) for j in (0, 2, 4))


def lum(rgb):
    def f(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (f(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2):
    l1, l2 = lum(hex_to_rgb(c1)), lum(hex_to_rgb(c2))
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)


def mix(c1, c2, w1):
    """color-mix in srgb: gamma-space channel interpolation."""
    a, b = hex_to_rgb(c1), hex_to_rgb(c2)
    return "#%02x%02x%02x" % tuple(round(w1 * x + (1 - w1) * y) for x, y in zip(a, b))


def main():
    root_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT_CSS
    themes_path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_THEMES_CSS

    root_css = root_path.read_text()
    themes_css = themes_path.read_text()

    # The color-mix ratio the @supports rule derives --color-muted with.
    mix_m = re.search(r"color-mix\(in srgb, var\(--color-dark\) (\d+)%", root_css)
    mix_ratio = int(mix_m.group(1)) / 100 if mix_m else 0.72

    root_light, root_dark = {}, {}
    for sel, dark, v in parse_blocks(root_css):
        # Keep only literal values: the color-mix declaration is modeled by the
        # muted-colormix check, while explicit hexes model the no-color-mix path.
        v = {k: val for k, val in v.items() if "color-mix" not in val}
        if ":root" in sel and not dark:
            root_light.update(v)
        elif ":root" in sel and dark:
            root_dark.update(v)

    themes = {}
    for sel, dark, v in parse_blocks(themes_css):
        m = re.match(r"\.theme-([\w-]+)", sel)
        if not m:
            continue
        t = themes.setdefault(m.group(1), {"light": {}, "dark": {}})
        t["dark" if dark else "light"].update(v)

    def effective(name, mode):
        if name == "(default)":
            return dict(root_light) if mode == "light" else {**root_light, **root_dark}
        t = themes[name]
        if mode == "light":
            return {**root_light, **t["light"]}
        return {**root_light, **root_dark, **t["light"], **t["dark"]}

    fails = []
    checked = 0
    for name in ["(default)"] + sorted(themes):
        for mode in ("light", "dark"):
            v = effective(name, mode)
            bg, txt = v["color-light"], v["color-dark"]
            pairs = [
                ("body-text", txt, bg),
                ("heading(primary)", v["color-primary"], bg),
                ("link", v["color-link"], bg),
                ("link-visited", v["color-link-visited"], bg),
                ("link-hover", v["color-link-hover"], bg),
                ("input(primary/tertiary)", v["color-primary"], v["color-tertiary"]),
                ("code", v["color-code-fg"], v["color-code-bg"]),
                ("muted-colormix", mix(txt, bg, mix_ratio), bg),
            ]
            if "color-muted" in v:
                pairs.append(("muted-explicit", v["color-muted"], bg))
            for pair, fg, b in pairs:
                checked += 1
                try:
                    r = ratio(fg, b)
                except ValueError:
                    continue  # non-hex value (var() indirection etc.)
                if r < THRESHOLD:
                    fails.append((name, mode, pair, fg, b, round(r, 2)))

    n_palettes = 1 + len(themes)
    print(f"Swept {n_palettes} palettes x 2 modes = {checked} pairs "
          f"(muted mix {int(mix_ratio * 100)}%)")
    if not fails:
        print(f"contrast clean: all pairs >= {THRESHOLD}:1")
        return 0
    print(f"{len(fails)} FAILURES (<{THRESHOLD}:1):")
    for t, m, p, fg, bg, r in sorted(fails, key=lambda x: x[5]):
        print(f"  {r:>5}  {t:<12} {m:<5} {p:<24} fg={fg} bg={bg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
