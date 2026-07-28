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
  // TEMP: book-filter/music-filter are conditionally rendered; hugo_stats.json misses them.
  // Remove when Tasks 6-7 convert books/music templates.
  safelist: ["page_content", "book-filter", "music-filter", /^prose/, /^masonry-/, /^highlight/, /^chroma/, /loaded/, /visible/, /^bsky/, /^tinylytics/],
};

module.exports = {
  plugins: {
    tailwindcss: {},
    "@fullhuman/postcss-purgecss":
      process.env.HUGO_ENVIRONMENT === "production" ? purgecss : false,
    autoprefixer: process.env.HUGO_ENVIRONMENT === "production" ? {} : false,
  },
};
