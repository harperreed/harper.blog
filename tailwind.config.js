// tailwind.config.js
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./layouts/**/*.html", "./content/**/*.{md,html}"],
  theme: {
    extend: {
      fontSize: {
        base: ["1.125rem", "1.8"], // 18px base with 1.8 line height
        lg: ["1.25rem", "1.8"], // 20px
        xl: ["1.5rem", "1.4"], // 24px
        "2xl": ["1.875rem", "1.3"], // 30px
        "3xl": ["2.25rem", "1.2"], // 36px
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          "Segoe UI",
          "Roboto",
          "Helvetica Neue",
          "Arial",
          "Noto Sans",
          ...defaultTheme.fontFamily.sans,
        ],
      },
      typography: {
        DEFAULT: {
          css: {
            fontSize: "1.125rem", // 18px base
            lineHeight: "1.8",
            maxWidth: "none",
            color: "#222",
            p: {
              fontSize: "1.125rem",
              lineHeight: "1.8",
              marginTop: "1.5em",
              marginBottom: "1.5em",
            },
            a: {
              color: "#2B6CB0",
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
            },
            "h1, h2, h3, h4, h5, h6": {
              fontWeight: "400",
              lineHeight: "1.3",
              marginTop: "2em",
              marginBottom: "1em",
            },
            h1: {
              fontSize: "2.25rem", // 36px
              marginTop: "0",
            },
            h2: {
              fontSize: "1.875rem", // 30px
            },
            h3: {
              fontSize: "1.5rem", // 24px
            },
            code: {
              fontSize: "0.925em",
              backgroundColor: "#f5f5f5",
              padding: "0.2em 0.4em",
              borderRadius: "3px",
              "&::before": { content: "none" },
              "&::after": { content: "none" },
            },
            pre: {
              fontSize: "1rem",
              lineHeight: "1.6",
              code: {
                fontSize: "inherit",
              },
            },
            strong: {
              fontWeight: "600",
            },
            blockquote: {
              fontSize: "1.125rem",
              fontStyle: "normal",
              lineHeight: "1.8",
            },
            // Larger list text
            ul: {
              fontSize: "1.125rem",
              lineHeight: "1.8",
            },
            ol: {
              fontSize: "1.125rem",
              lineHeight: "1.8",
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
