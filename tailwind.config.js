module.exports = {
  content: [
    "./layouts/**/*.{html,js}",
    "./content/**/*.{md,html}",
    "./themes/**/layouts/**/*.{html,js}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
        },
      },
      typography: {
        DEFAULT: {
          css: {
            color: 'var(--tw-prose-body)',
            maxWidth: '65ch',
            '[class~="lead"]': {
              color: 'var(--tw-prose-lead)'
            },
            a: {
              color: 'var(--tw-prose-links)',
              textDecoration: 'underline',
              fontWeight: '500',
            },
            'a:hover': {
              color: 'var(--tw-prose-links-hover)'
            },
            h1: {
              color: 'var(--tw-prose-headings)',
              fontWeight: '700',
              fontSize: '2.25em',
              marginBottom: '1em',
            },
            h2: {
              color: 'var(--tw-prose-headings)',
              fontWeight: '600',
              fontSize: '1.5em',
              marginTop: '2em',
              marginBottom: '1em',
            },
            h3: {
              color: 'var(--tw-prose-headings)',
              fontWeight: '600',
              fontSize: '1.25em',
              marginTop: '1.6em',
              marginBottom: '0.6em',
            },
            pre: {
              backgroundColor: 'var(--tw-prose-pre-bg)',
              color: 'var(--tw-prose-pre-code)',
              borderRadius: '0.375rem',
              padding: '1em',
              overflowX: 'auto',
            },
            code: {
              color: 'var(--tw-prose-code)',
              fontWeight: '500',
              '&::before': { content: '""' },
              '&::after': { content: '""' },
            },
          }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
  ],
}