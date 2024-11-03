module.exports = {
  // Specify files to scan for classes
  content: [
    "./layouts/**/*.{html,js}",
    "./content/**/*.{md,html}",
    "./themes/**/layouts/**/*.{html,js}",
    "./hugo_stats.json",
  ],

  // Toggle dark mode based on class (instead of media query)
  darkMode: "class",

  theme: {
    // Extend default configurations
    extend: {
      // Custom colors
      colors: {
        primary: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd3fc",
          400: "#38bdf8",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
          950: "#082f49",
        },
        // You can add more custom colors here
      },

      // Typography settings
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme("colors.gray.900"),
            a: {
              color: theme("colors.primary.600"),
              "&:hover": {
                color: theme("colors.primary.800"),
              },
            },
            "h1,h2,h3,h4": {
              color: theme("colors.gray.900"),
              "scroll-margin-top": theme("spacing.32"),
            },
            code: {
              color: theme("colors.pink.600"),
              "&::before": { content: '""' },
              "&::after": { content: '""' },
            },
          },
        },
        dark: {
          css: {
            color: theme("colors.gray.200"),
            a: {
              color: theme("colors.primary.400"),
              "&:hover": {
                color: theme("colors.primary.300"),
              },
            },
            "h1,h2,h3,h4": {
              color: theme("colors.gray.100"),
            },
          },
        },
      }),

      // Font families
      fontFamily: {
        sans: [
          "Inter",
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "BlinkMacSystemFont",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          '"Noto Sans"',
          "sans-serif",
        ],
        serif: ["Georgia", "Cambria", '"Times New Roman"', "Times", "serif"],
        mono: [
          "JetBrains Mono",
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Monaco",
          "Consolas",
          '"Liberation Mono"',
          '"Courier New"',
          "monospace",
        ],
      },

      // Custom spacing
      spacing: {
        128: "32rem",
        144: "36rem",
      },

      // Container settings
      container: {
        center: true,
        padding: {
          DEFAULT: "1rem",
          sm: "2rem",
          lg: "4rem",
          xl: "5rem",
          "2xl": "6rem",
        },
      },

      // Aspect ratios
      aspectRatio: {
        photo: "4/3",
        widescreen: "16/9",
      },
    },
  },

  // Plugins
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/aspect-ratio"),
  ],

  // Safelist - classes that should always be included
  safelist: [
    "prose",
    "prose-lg",
    "prose-xl",
    {
      pattern: /bg-(primary|gray|blue)-(100|200|300|400|500|600|700|800|900)/,
      variants: ["hover", "focus", "dark"],
    },
  ],
};
