/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./layouts/**/*.html",
    "./content/**/*.md",
    "./assets/**/*.js",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Light mode
        cream: '#FAF9F6',
        ink: '#1C1917',
        terracotta: '#C2410C',
        slate: '#475569',
        warmgray: '#E7E5E4',
        // Dark mode
        charcoal: '#1C1917',
        amber: '#F59E0B',
        stone: '#A8A29E',
        darkborder: '#292524',
      },
      fontFamily: {
        display: ['Fraunces', 'Georgia', 'serif'],
        body: ['General Sans', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}
