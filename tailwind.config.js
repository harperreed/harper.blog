// tailwind.config.js
module.exports = {
  content: ["./layouts/**/*.html", "./content/**/*.{md,html}"],
  theme: {
    extend: {
      typography: {
        DEFAULT: {
          css: {
            maxWidth: "none",
            color: "#222",
            a: {
              color: "#2B6CB0",
              textDecoration: "none",
              "&:hover": {
                textDecoration: "underline",
              },
            },
            h1: {
              fontWeight: "400",
              // fontSize: "2.25em",
              marginTop: "0",
              marginBottom: "0.8888889em",
            },
            h2: {
              fontWeight: "400",
              // fontSize: "1.5em",
              marginTop: "2em",
              marginBottom: "1em",
            },
            h3: {
              fontWeight: "400",
              // fontSize: "1.25em",
              marginTop: "1.6em",
              marginBottom: "0.6em",
            },
            code: {
              color: "#222",
              backgroundColor: "#f5f5f5",
              paddingLeft: "4px",
              paddingRight: "4px",
              paddingTop: "2px",
              paddingBottom: "2px",
              borderRadius: "2px",
              "&::before": {
                content: "none",
              },
              "&::after": {
                content: "none",
              },
            },
            pre: {
              backgroundColor: "#f5f5f5",
              color: "#222",
              lineHeight: "1.5",
              padding: "1em",
            },
            strong: {
              fontWeight: "600",
              color: "#222",
            },
            blockquote: {
              fontWeight: "400",
              fontStyle: "italic",
              quotes: "none",
              borderLeftColor: "#e5e7eb",
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
