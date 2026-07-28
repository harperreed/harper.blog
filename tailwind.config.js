// ABOUTME: Tailwind config for harper.blog — tokens live in scss/base.scss as CSS vars.
// ABOUTME: Content scan reads hugo_stats.json (enabled in config/_default/build.toml).
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./hugo_stats.json"],
  darkMode: "media",
  theme: {
    extend: {
      fontFamily: {
        primary: ["Sora", "sans-serif"],
        sans: ["DM Sans", "sans-serif"],
        display: ["Sora", "sans-serif"],
      },
      colors: {
        "text-primary": "var(--color-text-primary)",
        "text-body": "var(--color-text-body)",
        "text-muted": "var(--color-text-muted)",
        "text-faint": "var(--color-text-faint)",
        "bg-page": "var(--color-bg-page)",
        "border-rule": "var(--color-border-rule)",
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
