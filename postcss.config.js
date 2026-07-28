// ABOUTME: PostCSS pipeline — Tailwind always; purgecss+autoprefixer in production.
// ABOUTME: Purge content comes from Hugo's hugo_stats.json element/class inventory.
const purgecss = {
  content: ["./hugo_stats.json"],
  defaultExtractor: (content) => {
    const elements = JSON.parse(content).htmlElements;
    return [
      ...(elements.tags || []),
      ...(elements.classes || []),
      ...(elements.ids || []),
    ];
  },
  safelist: [/^masonry-/, /^highlight/, /^chroma/, /loaded/, /visible/, /^bsky/, /^tinylytics/],
};

module.exports = {
  plugins: {
    tailwindcss: {},
    "@fullhuman/postcss-purgecss":
      process.env.HUGO_ENVIRONMENT === "production" ? purgecss : false,
    autoprefixer: process.env.HUGO_ENVIRONMENT === "production" ? {} : false,
  },
};
