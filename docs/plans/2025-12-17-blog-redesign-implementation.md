# Artisanal Editorial Blog Redesign - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Redesign Harper's blog with an "Artisanal Editorial" aesthetic—sophisticated typography, warm earth tones, excellent reading experience, and bulletproof technical foundation.

**Architecture:** Hugo static site with Tailwind CSS v4 for styling. Progressive enhancement with vanilla JS for interactive features (search, theme toggle, progress bar). Pagefind for static search. All features work without JS.

**Tech Stack:** Hugo, Tailwind CSS v4 (standalone CLI), Vanilla JS, Pagefind, Google Fonts (Fraunces, General Sans)

---

## Phase 1: Foundation

### Task 1.1: Install Tailwind CSS Standalone Binary

**Files:**
- Create: `bin/tailwindcss` (binary, gitignored)
- Create: `tailwind.config.js`
- Create: `assets/css/tailwind-input.css`
- Modify: `.gitignore`

**Step 1: Download Tailwind standalone binary**

```bash
mkdir -p bin
curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64
chmod +x tailwindcss-macos-arm64
mv tailwindcss-macos-arm64 bin/tailwindcss
```

**Step 2: Add bin directory to gitignore**

Add to `.gitignore`:
```
bin/
```

**Step 3: Create Tailwind config**

Create `tailwind.config.js`:
```javascript
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
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
          },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
```

**Step 4: Create Tailwind input file**

Create `assets/css/tailwind-input.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-bg: theme('colors.cream');
    --color-text: theme('colors.ink');
    --color-accent: theme('colors.terracotta');
    --color-secondary: theme('colors.slate');
    --color-border: theme('colors.warmgray');
  }

  .dark {
    --color-bg: theme('colors.charcoal');
    --color-text: theme('colors.cream');
    --color-accent: theme('colors.amber');
    --color-secondary: theme('colors.stone');
    --color-border: theme('colors.darkborder');
  }

  html {
    @apply bg-[var(--color-bg)] text-[var(--color-text)];
    @apply transition-colors duration-200;
  }

  body {
    @apply font-body antialiased;
  }
}
```

**Step 5: Test Tailwind compilation**

```bash
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css
```

Expected: File created at `static/css/tailwind.css`

**Step 6: Commit**

```bash
git add tailwind.config.js assets/css/tailwind-input.css .gitignore
git commit -m "feat: add Tailwind CSS standalone setup"
```

---

### Task 1.2: Set Up Font Loading

**Files:**
- Create: `layouts/partials/head/fonts.html`
- Modify: `layouts/partials/head/custom_head.html`

**Step 1: Create fonts partial**

Create `layouts/partials/head/fonts.html`:
```html
{{/* Preconnect to Google Fonts */}}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

{{/* Load fonts with display=swap for performance */}}
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

{{/* General Sans from Fontshare (free) */}}
<link href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap" rel="stylesheet">
```

**Step 2: Include fonts in head**

Modify `layouts/partials/head/custom_head.html` to add at the top:
```html
{{ partial "head/fonts.html" . }}
```

**Step 3: Test font loading**

```bash
hugo serve --buildDrafts
```

Open browser, inspect Network tab, verify fonts loading.

**Step 4: Commit**

```bash
git add layouts/partials/head/fonts.html layouts/partials/head/custom_head.html
git commit -m "feat: add custom font loading (Fraunces, General Sans, JetBrains Mono)"
```

---

### Task 1.3: Create Build Script

**Files:**
- Create: `scripts/build.sh`
- Modify: `package.json` (if exists) or document commands

**Step 1: Create build script**

Create `scripts/build.sh`:
```bash
#!/bin/bash
set -e

echo "Building Tailwind CSS..."
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css --minify

echo "Building Hugo..."
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info

echo "Build complete!"
```

**Step 2: Make executable**

```bash
chmod +x scripts/build.sh
```

**Step 3: Create dev script**

Create `scripts/dev.sh`:
```bash
#!/bin/bash

# Run Tailwind in watch mode in background
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css --watch &
TAILWIND_PID=$!

# Run Hugo server
hugo serve --buildDrafts --buildFuture --navigateToChanged

# Cleanup on exit
trap "kill $TAILWIND_PID 2>/dev/null" EXIT
```

**Step 4: Make executable and test**

```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

**Step 5: Commit**

```bash
git add scripts/
git commit -m "feat: add build and dev scripts for Tailwind + Hugo"
```

---

### Task 1.4: Create Design Tokens CSS

**Files:**
- Create: `assets/css/tokens.css`

**Step 1: Create comprehensive design tokens**

Create `assets/css/tokens.css`:
```css
:root {
  /* === COLORS === */
  /* Light mode (default) */
  --color-bg: #FAF9F6;
  --color-bg-secondary: #F5F3EF;
  --color-text: #1C1917;
  --color-text-secondary: #475569;
  --color-accent: #C2410C;
  --color-accent-hover: #9A3412;
  --color-border: #E7E5E4;
  --color-border-strong: #D6D3D1;

  /* === TYPOGRAPHY === */
  --font-display: 'Fraunces', Georgia, serif;
  --font-body: 'General Sans', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', Consolas, monospace;

  /* Font sizes (fluid) */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.25rem + 1.25vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --text-4xl: clamp(2.25rem, 1.75rem + 2.5vw, 3.5rem);

  /* Line heights */
  --leading-tight: 1.2;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 1.75;

  /* === SPACING === */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;

  /* === LAYOUT === */
  --content-width: 65ch;
  --sidebar-width: 280px;
  --max-width: 1280px;
  --header-height: 4rem;

  /* === EFFECTS === */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* === TRANSITIONS === */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}

/* Dark mode */
.dark {
  --color-bg: #1C1917;
  --color-bg-secondary: #292524;
  --color-text: #FAF9F6;
  --color-text-secondary: #A8A29E;
  --color-accent: #F59E0B;
  --color-accent-hover: #D97706;
  --color-border: #292524;
  --color-border-strong: #44403C;

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.2);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.3);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.3);
}
```

**Step 2: Import tokens in Tailwind input**

Modify `assets/css/tailwind-input.css` to import tokens at top:
```css
@import 'tokens.css';

@tailwind base;
@tailwind components;
@tailwind utilities;

/* ... rest of file ... */
```

**Step 3: Test compilation**

```bash
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css
```

**Step 4: Commit**

```bash
git add assets/css/tokens.css assets/css/tailwind-input.css
git commit -m "feat: add comprehensive design tokens"
```

---

## Phase 2: Base Layout

### Task 2.1: Create New Base Template

**Files:**
- Create: `layouts/_default/baseof-new.html`

**Step 1: Create new baseof template**

Create `layouts/_default/baseof-new.html`:
```html
<!DOCTYPE html>
<html lang="{{ .Site.Language.Lang }}" class="{{ if eq (getenv "HUGO_THEME_MODE") "dark" }}dark{{ end }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{{ with .Description }}{{ . }}{{ else }}{{ with .Site.Params.description }}{{ . }}{{ end }}{{ end }}">

  <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} | {{ .Site.Title }}{{ end }}</title>

  {{/* Fonts */}}
  {{ partial "head/fonts.html" . }}

  {{/* CSS */}}
  <link rel="stylesheet" href="/css/tailwind.css">

  {{/* Favicon */}}
  <link rel="icon" href="/favicon.ico">

  {{/* RSS */}}
  {{ range .AlternativeOutputFormats -}}
    {{ printf `<link rel="%s" type="%s" href="%s" title="%s" />` .Rel .MediaType.Type .Permalink $.Site.Title | safeHTML }}
  {{ end -}}

  {{/* Open Graph */}}
  {{ partial "social_card.html" . }}

  {{/* Theme script (inline to prevent FOUC) */}}
  <script>
    (function() {
      const theme = localStorage.getItem('theme');
      if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
      }
    })();
  </script>
</head>
<body class="min-h-screen bg-[var(--color-bg)] text-[var(--color-text)] font-body">
  {{/* Skip link */}}
  <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-[var(--color-accent)] focus:text-white focus:rounded-md">
    Skip to content
  </a>

  {{/* Reading progress bar */}}
  <div id="progress-bar" class="fixed top-0 left-0 h-[3px] bg-[var(--color-accent)] z-50 w-0 transition-[width] duration-100"></div>

  {{/* Header */}}
  {{ partial "header-new.html" . }}

  {{/* Main content */}}
  <main id="main-content" class="flex-1">
    {{ block "main" . }}{{ end }}
  </main>

  {{/* Footer */}}
  {{ partial "footer-new.html" . }}

  {{/* Scripts */}}
  <script src="/js/main.js" defer></script>
</body>
</html>
```

**Step 2: Verify template syntax**

```bash
hugo --templateMetrics 2>&1 | head -20
```

Expected: No template errors

**Step 3: Commit**

```bash
git add layouts/_default/baseof-new.html
git commit -m "feat: create new base template with Tailwind"
```

---

### Task 2.2: Create New Header

**Files:**
- Create: `layouts/partials/header-new.html`

**Step 1: Create header partial**

Create `layouts/partials/header-new.html`:
```html
<header class="sticky top-0 z-40 bg-[var(--color-bg)]/95 backdrop-blur-sm border-b border-[var(--color-border)]">
  <div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      {{/* Logo/Name */}}
      <a href="{{ .Site.BaseURL }}" class="flex items-center gap-3 group">
        {{ with .Site.Params.avatar }}
        <img src="{{ . }}" alt="{{ $.Site.Params.name }}" class="w-10 h-10 rounded-full ring-2 ring-[var(--color-border)] group-hover:ring-[var(--color-accent)] transition-all">
        {{ end }}
        <span class="font-display text-xl font-semibold tracking-tight">
          {{ .Site.Params.name | default .Site.Title }}
        </span>
      </a>

      {{/* Desktop Navigation */}}
      <nav class="hidden md:flex items-center gap-6">
        {{ range .Site.Menus.main }}
        <a href="{{ .URL }}" class="text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text)] transition-colors {{ if $.IsMenuCurrent "main" . }}text-[var(--color-accent)]{{ end }}">
          {{ .Name }}
        </a>
        {{ end }}
      </nav>

      {{/* Right side: Search + Theme toggle */}}
      <div class="flex items-center gap-2">
        {{/* Search button */}}
        <button id="search-btn" class="p-2 rounded-md hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Search">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
        </button>

        {{/* Theme toggle */}}
        <button id="theme-toggle" class="p-2 rounded-md hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Toggle theme">
          {{/* Sun icon (shown in dark mode) */}}
          <svg class="w-5 h-5 hidden dark:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          {{/* Moon icon (shown in light mode) */}}
          <svg class="w-5 h-5 block dark:hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
        </button>

        {{/* Mobile menu button */}}
        <button id="mobile-menu-btn" class="md:hidden p-2 rounded-md hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Menu">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
      </div>
    </div>
  </div>

  {{/* Mobile menu */}}
  <div id="mobile-menu" class="hidden md:hidden border-t border-[var(--color-border)]">
    <nav class="px-4 py-4 space-y-2">
      {{ range .Site.Menus.main }}
      <a href="{{ .URL }}" class="block px-3 py-2 rounded-md text-sm font-medium hover:bg-[var(--color-bg-secondary)] transition-colors">
        {{ .Name }}
      </a>
      {{ end }}
    </nav>
  </div>
</header>
```

**Step 2: Commit**

```bash
git add layouts/partials/header-new.html
git commit -m "feat: create new header with navigation and theme toggle"
```

---

### Task 2.3: Create New Footer

**Files:**
- Create: `layouts/partials/footer-new.html`

**Step 1: Create footer partial**

Create `layouts/partials/footer-new.html`:
```html
<footer class="border-t border-[var(--color-border)] mt-auto">
  <div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
      {{/* About */}}
      <div>
        <h3 class="font-display text-lg font-semibold mb-4">{{ .Site.Params.name }}</h3>
        <p class="text-sm text-[var(--color-text-secondary)] leading-relaxed">
          Builder, investor, and technologist. Writing about AI, startups, and the future.
        </p>
      </div>

      {{/* Links */}}
      <div>
        <h3 class="font-display text-lg font-semibold mb-4">Explore</h3>
        <nav class="space-y-2">
          {{ range .Site.Menus.main }}
          <a href="{{ .URL }}" class="block text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] transition-colors">
            {{ .Name }}
          </a>
          {{ end }}
        </nav>
      </div>

      {{/* Connect */}}
      <div>
        <h3 class="font-display text-lg font-semibold mb-4">Connect</h3>
        <div class="space-y-2">
          {{ range .Site.Params.social }}
          <a href="{{ .url }}" class="flex items-center gap-2 text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] transition-colors" target="_blank" rel="noopener noreferrer">
            <i class="{{ .icon }}"></i>
            {{ .name }}
          </a>
          {{ end }}
          {{ with .Site.Params.author.email }}
          <a href="mailto:{{ . }}" class="flex items-center gap-2 text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
            Email
          </a>
          {{ end }}
        </div>
      </div>
    </div>

    {{/* Bottom bar */}}
    <div class="mt-12 pt-8 border-t border-[var(--color-border)] flex flex-col sm:flex-row items-center justify-between gap-4">
      <p class="text-sm text-[var(--color-text-secondary)]">
        &copy; {{ now.Year }} {{ .Site.Params.name }}. All rights reserved.
      </p>
      <div class="flex items-center gap-4 text-sm text-[var(--color-text-secondary)]">
        <a href="/index.xml" class="hover:text-[var(--color-accent)] transition-colors">RSS</a>
        {{/* Language switcher */}}
        {{ if .IsTranslated }}
        <div class="flex items-center gap-2">
          {{ range .Translations }}
          <a href="{{ .Permalink }}" class="hover:text-[var(--color-accent)] transition-colors">{{ .Language.LanguageName }}</a>
          {{ end }}
        </div>
        {{ end }}
      </div>
    </div>
  </div>
</footer>
```

**Step 2: Commit**

```bash
git add layouts/partials/footer-new.html
git commit -m "feat: create new footer with social links and language switcher"
```

---

### Task 2.4: Create Main JavaScript

**Files:**
- Create: `static/js/main.js`

**Step 1: Create main JS file**

Create `static/js/main.js`:
```javascript
// ABOUTME: Main JavaScript for the blog
// ABOUTME: Handles theme toggle, mobile menu, reading progress, and search

(function() {
  'use strict';

  // === Theme Toggle ===
  const themeToggle = document.getElementById('theme-toggle');

  function setTheme(isDark) {
    document.documentElement.classList.toggle('dark', isDark);
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.classList.contains('dark');
      setTheme(!isDark);
    });
  }

  // Listen for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      setTheme(e.matches);
    }
  });

  // === Mobile Menu ===
  const mobileMenuBtn = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = !mobileMenu.classList.contains('hidden');
      mobileMenu.classList.toggle('hidden', isOpen);
      mobileMenuBtn.setAttribute('aria-expanded', !isOpen);
    });
  }

  // === Reading Progress Bar ===
  const progressBar = document.getElementById('progress-bar');

  if (progressBar && document.querySelector('article')) {
    function updateProgress() {
      const article = document.querySelector('article');
      if (!article) return;

      const articleTop = article.offsetTop;
      const articleHeight = article.offsetHeight;
      const windowHeight = window.innerHeight;
      const scrollY = window.scrollY;

      // Calculate progress through the article
      const start = articleTop - windowHeight;
      const end = articleTop + articleHeight - windowHeight;
      const progress = Math.min(Math.max((scrollY - start) / (end - start), 0), 1);

      progressBar.style.width = `${progress * 100}%`;
    }

    // Use passive listener for better scroll performance
    window.addEventListener('scroll', updateProgress, { passive: true });
    updateProgress();
  }

  // === Search Modal (Pagefind) ===
  const searchBtn = document.getElementById('search-btn');

  if (searchBtn) {
    searchBtn.addEventListener('click', () => {
      // Pagefind integration will be added later
      console.log('Search clicked - Pagefind integration pending');
    });

    // Cmd/Ctrl + K shortcut
    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        searchBtn.click();
      }
    });
  }

  // === Jump to Top ===
  const jumpToTop = document.getElementById('jump-to-top');

  if (jumpToTop) {
    function toggleJumpToTop() {
      const show = window.scrollY > 500;
      jumpToTop.classList.toggle('opacity-0', !show);
      jumpToTop.classList.toggle('pointer-events-none', !show);
    }

    window.addEventListener('scroll', toggleJumpToTop, { passive: true });

    jumpToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

})();
```

**Step 2: Test JS syntax**

```bash
node --check static/js/main.js
```

Expected: No output (no errors)

**Step 3: Commit**

```bash
git add static/js/main.js
git commit -m "feat: add main JS for theme, menu, progress bar, and search"
```

---

## Phase 3: Homepage

### Task 3.1: Create New Homepage Template

**Files:**
- Create: `layouts/index-new.html`

**Step 1: Create homepage template**

Create `layouts/index-new.html`:
```html
{{ define "main" }}
<div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">

  {{/* Hero: Latest Post */}}
  {{ $latestPost := (where .Site.RegularPages "Section" "post" | first 1) }}
  {{ with index $latestPost 0 }}
  <section class="mb-16">
    <article class="relative group">
      <a href="{{ .Permalink }}" class="block p-8 md:p-12 rounded-xl bg-[var(--color-bg-secondary)] border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
        <span class="inline-block px-3 py-1 text-xs font-medium uppercase tracking-wider text-[var(--color-accent)] bg-[var(--color-accent)]/10 rounded-full mb-4">
          Latest Post
        </span>
        <h2 class="font-display text-3xl md:text-4xl font-bold leading-tight mb-4 group-hover:text-[var(--color-accent)] transition-colors">
          {{ .Title }}
        </h2>
        <p class="text-lg text-[var(--color-text-secondary)] leading-relaxed mb-6 max-w-prose">
          {{ .Summary | truncate 200 }}
        </p>
        <div class="flex items-center gap-4 text-sm text-[var(--color-text-secondary)]">
          <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "January 2, 2006" }}</time>
          <span>&middot;</span>
          <span>{{ .ReadingTime }} min read</span>
        </div>
      </a>
    </article>
  </section>
  {{ end }}

  {{/* Recent Notes */}}
  {{ $recentNotes := (where .Site.RegularPages "Section" "notes" | first 6) }}
  {{ if $recentNotes }}
  <section class="mb-16">
    <div class="flex items-center justify-between mb-8">
      <h2 class="font-display text-2xl font-bold">Recent Notes</h2>
      <a href="/notes/" class="text-sm font-medium text-[var(--color-accent)] hover:underline">View all &rarr;</a>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {{ range $recentNotes }}
      <article class="group">
        <a href="{{ .Permalink }}" class="block p-6 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:shadow-md transition-all h-full">
          {{ with .Params.images }}
          {{ $img := index . 0 }}
          <img src="{{ $img }}" alt="" class="w-full h-40 object-cover rounded-md mb-4">
          {{ end }}
          <p class="text-[var(--color-text)] leading-relaxed mb-3">
            {{ with .Description }}{{ . | truncate 120 }}{{ else }}{{ .Title | truncate 120 }}{{ end }}
          </p>
          <time class="text-xs text-[var(--color-text-secondary)]" datetime="{{ .Date.Format "2006-01-02" }}">
            {{ .Date.Format "Jan 2, 2006" }}
          </time>
        </a>
      </article>
      {{ end }}
    </div>
  </section>
  {{ end }}

  {{/* Currently Section */}}
  <section class="mb-16">
    <h2 class="font-display text-2xl font-bold mb-8">Currently</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      {{/* Currently Reading */}}
      {{ $currentBook := (where .Site.RegularPages "Section" "books" | first 1) }}
      {{ with index $currentBook 0 }}
      <a href="{{ .Permalink }}" class="flex items-center gap-4 p-4 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
        <span class="text-2xl">📚</span>
        <div>
          <span class="text-xs uppercase tracking-wider text-[var(--color-text-secondary)]">Reading</span>
          <p class="font-medium">{{ .Title }}</p>
        </div>
      </a>
      {{ end }}

      {{/* Recently Listened */}}
      {{ $currentMusic := (where .Site.RegularPages "Section" "music" | first 1) }}
      {{ with index $currentMusic 0 }}
      <a href="{{ .Permalink }}" class="flex items-center gap-4 p-4 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
        <span class="text-2xl">🎵</span>
        <div>
          <span class="text-xs uppercase tracking-wider text-[var(--color-text-secondary)]">Listening</span>
          <p class="font-medium">{{ .Title }}</p>
        </div>
      </a>
      {{ end }}
    </div>
  </section>

  {{/* Explore Section */}}
  <section>
    <h2 class="font-display text-2xl font-bold mb-8">Explore</h2>
    <div class="flex flex-wrap gap-4">
      {{ range (slice
        (dict "name" "Posts" "url" "/post/" "icon" "✍️")
        (dict "name" "Notes" "url" "/notes/" "icon" "💭")
        (dict "name" "Books" "url" "/books/" "icon" "📚")
        (dict "name" "Music" "url" "/music/" "icon" "🎵")
        (dict "name" "Links" "url" "/links/" "icon" "🔗")
      ) }}
      <a href="{{ .url }}" class="flex items-center gap-2 px-4 py-2 rounded-full border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-bg-secondary)] transition-all">
        <span>{{ .icon }}</span>
        <span class="font-medium">{{ .name }}</span>
      </a>
      {{ end }}

      {{/* Random Post */}}
      <button id="random-post-btn" class="flex items-center gap-2 px-4 py-2 rounded-full border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-bg-secondary)] transition-all">
        <span>🎲</span>
        <span class="font-medium">Random</span>
      </button>
    </div>
  </section>

</div>

<script>
  // Random post functionality
  document.getElementById('random-post-btn')?.addEventListener('click', () => {
    const posts = {{ .Site.RegularPages | where "Section" "post" | jsonify }};
    if (posts.length > 0) {
      const randomPost = posts[Math.floor(Math.random() * posts.length)];
      window.location.href = randomPost.RelPermalink;
    }
  });
</script>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/index-new.html
git commit -m "feat: create new homepage with hero, notes grid, and explore section"
```

---

## Phase 4: Post Template

### Task 4.1: Create New Single Post Template

**Files:**
- Create: `layouts/post/single-new.html`

**Step 1: Create single post template**

Create `layouts/post/single-new.html`:
```html
{{ define "main" }}
<article class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <div class="lg:grid lg:grid-cols-[1fr_280px] lg:gap-12">
    {{/* Main Content */}}
    <div>
      {{/* Post Header */}}
      <header class="mb-12">
        <h1 class="font-display text-4xl md:text-5xl font-bold leading-tight mb-6">
          {{ .Title }}
        </h1>

        <div class="flex flex-wrap items-center gap-4 text-sm text-[var(--color-text-secondary)]">
          <time datetime="{{ .Date.Format "2006-01-02" }}">
            {{ .Date.Format "January 2, 2006" }}
          </time>
          <span>&middot;</span>
          <span>{{ .ReadingTime }} min read</span>
          <span>&middot;</span>
          <span>{{ .WordCount }} words</span>
        </div>

        {{/* Tags */}}
        {{ with .Params.tags }}
        <div class="flex flex-wrap gap-2 mt-4">
          {{ range . }}
          <a href="{{ "/tags/" | relURL }}{{ . | urlize }}" class="px-3 py-1 text-xs font-medium bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)] hover:text-[var(--color-accent)] rounded-full transition-colors">
            #{{ . }}
          </a>
          {{ end }}
        </div>
        {{ end }}
      </header>

      {{/* Post Content */}}
      <div class="prose prose-lg max-w-none
        prose-headings:font-display prose-headings:font-bold
        prose-h2:text-2xl prose-h2:mt-12 prose-h2:mb-4
        prose-h3:text-xl prose-h3:mt-8 prose-h3:mb-3
        prose-p:text-[var(--color-text)] prose-p:leading-relaxed
        prose-a:text-[var(--color-accent)] prose-a:no-underline hover:prose-a:underline
        prose-code:text-[var(--color-accent)] prose-code:bg-[var(--color-bg-secondary)] prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none
        prose-pre:bg-[var(--color-bg-secondary)] prose-pre:border prose-pre:border-[var(--color-border)]
        prose-blockquote:border-l-4 prose-blockquote:border-[var(--color-accent)] prose-blockquote:bg-[var(--color-bg-secondary)] prose-blockquote:pl-6 prose-blockquote:py-4 prose-blockquote:not-italic
        prose-img:rounded-lg prose-img:shadow-md
        dark:prose-invert
      ">
        {{ .Content }}
      </div>

      {{/* Post Footer */}}
      <footer class="mt-16 pt-8 border-t border-[var(--color-border)]">
        {{/* Engagement */}}
        <div class="flex flex-wrap items-center gap-4 mb-8">
          {{/* Kudos button */}}
          <button class="tinylytics_kudos flex items-center gap-2 px-4 py-2 rounded-full border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-bg-secondary)] transition-all">
            <span>❤️</span>
            <span>Kudos</span>
          </button>

          {{/* Share buttons */}}
          <div class="flex items-center gap-2">
            <span class="text-sm text-[var(--color-text-secondary)]">Share:</span>
            <a href="https://twitter.com/intent/tweet?url={{ .Permalink }}&text={{ .Title | urlquery }}" target="_blank" rel="noopener noreferrer" class="p-2 rounded-full hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Share on X">
              𝕏
            </a>
            <a href="https://bsky.app/intent/compose?text={{ .Title | urlquery }}%20{{ .Permalink }}" target="_blank" rel="noopener noreferrer" class="p-2 rounded-full hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Share on Bluesky">
              🦋
            </a>
            <button onclick="navigator.clipboard.writeText('{{ .Permalink }}')" class="p-2 rounded-full hover:bg-[var(--color-bg-secondary)] transition-colors" aria-label="Copy link">
              🔗
            </button>
          </div>
        </div>

        {{/* Discussion */}}
        <div class="mb-8">
          <h3 class="font-display text-xl font-bold mb-4">Discussion</h3>
          <p class="text-[var(--color-text-secondary)] mb-4">
            Reply via <a href="mailto:{{ .Site.Params.author.email }}?subject=Re: {{ .Title }}" class="text-[var(--color-accent)] hover:underline">email</a> or join the conversation on Bluesky.
          </p>
          {{/* Bluesky comments will be rendered here */}}
          <div id="bsky-comments" data-uri="{{ .Params.bsky_uri }}"></div>
        </div>

        {{/* Related Posts */}}
        {{ $related := .Site.RegularPages.Related . | first 3 }}
        {{ with $related }}
        <div>
          <h3 class="font-display text-xl font-bold mb-4">Keep Exploring</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            {{ range . }}
            <a href="{{ .Permalink }}" class="block p-4 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
              <h4 class="font-medium mb-2 line-clamp-2">{{ .Title }}</h4>
              <time class="text-xs text-[var(--color-text-secondary)]">{{ .Date.Format "Jan 2, 2006" }}</time>
            </a>
            {{ end }}
          </div>
        </div>
        {{ end }}
      </footer>
    </div>

    {{/* Sidebar (desktop only) */}}
    <aside class="hidden lg:block">
      <div class="sticky top-24 space-y-8">
        {{/* Reading Progress */}}
        <div>
          <span class="text-xs uppercase tracking-wider text-[var(--color-text-secondary)]">Reading</span>
          <p class="font-medium">{{ .ReadingTime }} min</p>
        </div>

        {{/* Table of Contents */}}
        {{ if .TableOfContents }}
        <div>
          <h4 class="text-xs uppercase tracking-wider text-[var(--color-text-secondary)] mb-3">Contents</h4>
          <nav class="toc text-sm space-y-2">
            {{ .TableOfContents }}
          </nav>
        </div>
        {{ end }}

        {{/* Tags */}}
        {{ with .Params.tags }}
        <div>
          <h4 class="text-xs uppercase tracking-wider text-[var(--color-text-secondary)] mb-3">Tags</h4>
          <div class="flex flex-wrap gap-2">
            {{ range . }}
            <a href="{{ "/tags/" | relURL }}{{ . | urlize }}" class="text-sm text-[var(--color-accent)] hover:underline">
              #{{ . }}
            </a>
            {{ end }}
          </div>
        </div>
        {{ end }}
      </div>
    </aside>
  </div>
</article>

{{/* Jump to top button */}}
<button id="jump-to-top" class="fixed bottom-8 right-8 p-3 rounded-full bg-[var(--color-accent)] text-white shadow-lg opacity-0 pointer-events-none transition-opacity hover:bg-[var(--color-accent-hover)]" aria-label="Jump to top">
  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/>
  </svg>
</button>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/post/single-new.html
git commit -m "feat: create new single post template with sidebar and engagement"
```

---

## Phase 5: Content Type Templates

### Task 5.1: Create Notes Grid Template

**Files:**
- Create: `layouts/notes/list-new.html`

**Step 1: Create notes list template**

Create `layouts/notes/list-new.html`:
```html
{{ define "main" }}
<div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <header class="mb-12">
    <h1 class="font-display text-4xl font-bold mb-4">Notes</h1>
    <p class="text-lg text-[var(--color-text-secondary)]">Short thoughts, links, and updates.</p>

    {{/* Filter Pills */}}
    <div class="flex flex-wrap gap-2 mt-6" id="note-filters">
      <button class="filter-btn active px-4 py-2 text-sm font-medium rounded-full border border-[var(--color-border)] transition-all" data-filter="all">
        All
      </button>
      <button class="filter-btn px-4 py-2 text-sm font-medium rounded-full border border-[var(--color-border)] transition-all" data-filter="text">
        Text
      </button>
      <button class="filter-btn px-4 py-2 text-sm font-medium rounded-full border border-[var(--color-border)] transition-all" data-filter="images">
        With Images
      </button>
    </div>
  </header>

  {{/* Masonry Grid */}}
  <div class="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6" id="notes-grid">
    {{ $paginator := .Paginate (where .Site.RegularPages "Section" "notes") .Site.Params.notes_pagination }}
    {{ range $paginator.Pages }}
    <article class="note-card break-inside-avoid mb-6" data-has-image="{{ if .Params.images }}true{{ else }}false{{ end }}">
      <a href="{{ .Permalink }}" class="block p-6 rounded-xl border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:shadow-lg transition-all bg-[var(--color-bg)]">
        {{/* Image */}}
        {{ with .Params.images }}
        {{ $img := index . 0 }}
        <img src="{{ $img }}" alt="" class="w-full rounded-lg mb-4 object-cover" loading="lazy">
        {{ end }}

        {{/* Content */}}
        <div class="{{ if not .Params.images }}text-lg{{ end }}">
          {{ with .Description }}
          <p class="text-[var(--color-text)] leading-relaxed">{{ . }}</p>
          {{ else }}
          <p class="text-[var(--color-text)] leading-relaxed">{{ .Title }}</p>
          {{ end }}
        </div>

        {{/* Meta */}}
        <div class="flex items-center justify-between mt-4 text-xs text-[var(--color-text-secondary)]">
          <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "Jan 2, 2006" }}</time>
          {{ with .Params.tags }}
          <div class="flex gap-1">
            {{ range first 2 . }}
            <span class="text-[var(--color-accent)]">#{{ . }}</span>
            {{ end }}
          </div>
          {{ end }}
        </div>
      </a>
    </article>
    {{ end }}
  </div>

  {{/* Pagination */}}
  {{ if gt $paginator.TotalPages 1 }}
  <nav class="flex items-center justify-center gap-4 mt-12">
    {{ if $paginator.HasPrev }}
    <a href="{{ $paginator.Prev.URL }}" class="px-4 py-2 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
      &larr; Newer
    </a>
    {{ end }}

    <span class="text-sm text-[var(--color-text-secondary)]">
      Page {{ $paginator.PageNumber }} of {{ $paginator.TotalPages }}
    </span>

    {{ if $paginator.HasNext }}
    <a href="{{ $paginator.Next.URL }}" class="px-4 py-2 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
      Older &rarr;
    </a>
    {{ end }}
  </nav>
  {{ end }}
</div>

<script>
  // Note filtering
  const filters = document.querySelectorAll('.filter-btn');
  const notes = document.querySelectorAll('.note-card');

  filters.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      // Update active state
      filters.forEach(f => f.classList.remove('active', 'bg-[var(--color-accent)]', 'text-white', 'border-[var(--color-accent)]'));
      btn.classList.add('active', 'bg-[var(--color-accent)]', 'text-white', 'border-[var(--color-accent)]');

      // Filter notes
      notes.forEach(note => {
        const hasImage = note.dataset.hasImage === 'true';
        let show = true;

        if (filter === 'text') show = !hasImage;
        if (filter === 'images') show = hasImage;

        note.style.display = show ? 'block' : 'none';
      });
    });
  });
</script>

<style>
  .filter-btn.active {
    background-color: var(--color-accent);
    color: white;
    border-color: var(--color-accent);
  }
</style>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/notes/list-new.html
git commit -m "feat: create notes masonry grid with filtering"
```

---

### Task 5.2: Create Books Grid Template

**Files:**
- Create: `layouts/books/list-new.html`

**Step 1: Create books list template**

Create `layouts/books/list-new.html`:
```html
{{ define "main" }}
<div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <header class="mb-12">
    <h1 class="font-display text-4xl font-bold mb-4">Books</h1>
    <p class="text-lg text-[var(--color-text-secondary)]">What I've been reading.</p>
  </header>

  {{/* Book Grid */}}
  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
    {{ range where .Site.RegularPages "Section" "books" }}
    <article class="group">
      <a href="{{ .Permalink }}" class="block">
        {{/* Book Cover */}}
        <div class="relative aspect-[2/3] rounded-lg overflow-hidden shadow-md group-hover:shadow-xl transition-all group-hover:-translate-y-1">
          {{ with .Params.cover }}
          <img src="{{ . }}" alt="{{ $.Title }}" class="w-full h-full object-cover">
          {{ else }}
          <div class="w-full h-full bg-gradient-to-br from-[var(--color-bg-secondary)] to-[var(--color-border)] flex items-center justify-center p-4">
            <span class="font-display text-sm text-center text-[var(--color-text-secondary)]">{{ $.Title }}</span>
          </div>
          {{ end }}

          {{/* Hover overlay */}}
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
            <h3 class="text-white font-medium text-sm line-clamp-2">{{ .Title }}</h3>
            {{ with .Params.author }}
            <p class="text-white/70 text-xs mt-1">{{ . }}</p>
            {{ end }}
          </div>

          {{/* Shelf shadow */}}
          <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 w-[90%] h-4 bg-black/10 blur-md rounded-full"></div>
        </div>

        {{/* Book info (visible on mobile) */}}
        <div class="mt-3 md:hidden">
          <h3 class="font-medium text-sm line-clamp-2">{{ .Title }}</h3>
          {{ with .Params.author }}
          <p class="text-[var(--color-text-secondary)] text-xs mt-1">{{ . }}</p>
          {{ end }}
        </div>
      </a>
    </article>
    {{ end }}
  </div>
</div>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/books/list-new.html
git commit -m "feat: create books grid with cover art display"
```

---

### Task 5.3: Create Music Grid Template

**Files:**
- Create: `layouts/music/list-new.html`

**Step 1: Create music list template**

Create `layouts/music/list-new.html`:
```html
{{ define "main" }}
<div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <header class="mb-12">
    <h1 class="font-display text-4xl font-bold mb-4">Music</h1>
    <p class="text-lg text-[var(--color-text-secondary)]">What I've been listening to.</p>
  </header>

  {{/* Album Grid */}}
  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
    {{ range where .Site.RegularPages "Section" "music" }}
    <article class="group">
      <a href="{{ .Permalink }}" class="block">
        {{/* Album Art */}}
        <div class="relative aspect-square rounded-lg overflow-hidden shadow-md group-hover:shadow-xl transition-all group-hover:-translate-y-1">
          {{ with .Params.cover }}
          <img src="{{ . }}" alt="{{ $.Title }}" class="w-full h-full object-cover">
          {{ else }}
          <div class="w-full h-full bg-gradient-to-br from-[var(--color-accent)]/20 to-[var(--color-bg-secondary)] flex items-center justify-center">
            <span class="text-4xl">🎵</span>
          </div>
          {{ end }}

          {{/* Hover overlay */}}
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
            <h3 class="text-white font-medium text-sm line-clamp-2">{{ .Title }}</h3>
            {{ with .Params.artist }}
            <p class="text-white/70 text-xs mt-1">{{ . }}</p>
            {{ end }}
          </div>
        </div>

        {{/* Info (visible on mobile) */}}
        <div class="mt-3 md:hidden">
          <h3 class="font-medium text-sm line-clamp-2">{{ .Title }}</h3>
          {{ with .Params.artist }}
          <p class="text-[var(--color-text-secondary)] text-xs mt-1">{{ . }}</p>
          {{ end }}
        </div>
      </a>
    </article>
    {{ end }}
  </div>
</div>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/music/list-new.html
git commit -m "feat: create music grid with album art display"
```

---

### Task 5.4: Create Links List Template

**Files:**
- Create: `layouts/links/list-new.html`

**Step 1: Create links list template**

Create `layouts/links/list-new.html`:
```html
{{ define "main" }}
<div class="max-w-[var(--max-width)] mx-auto px-4 sm:px-6 lg:px-8 py-12">
  <header class="mb-12">
    <h1 class="font-display text-4xl font-bold mb-4">Links</h1>
    <p class="text-lg text-[var(--color-text-secondary)]">Interesting things from around the web.</p>
  </header>

  {{/* Links List */}}
  <div class="space-y-4">
    {{ $paginator := .Paginate (where .Site.RegularPages "Section" "links") .Site.Params.links_pagination }}
    {{ range $paginator.Pages }}
    <article class="group">
      <a href="{{ .Params.link }}" target="_blank" rel="noopener noreferrer" class="flex items-start gap-4 p-4 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] hover:bg-[var(--color-bg-secondary)] transition-all">
        {{/* Favicon placeholder */}}
        <div class="flex-shrink-0 w-10 h-10 rounded-lg bg-[var(--color-bg-secondary)] flex items-center justify-center text-lg">
          🔗
        </div>

        {{/* Content */}}
        <div class="flex-1 min-w-0">
          <h3 class="font-medium text-[var(--color-text)] group-hover:text-[var(--color-accent)] transition-colors flex items-center gap-2">
            {{ .Title }}
            <svg class="w-4 h-4 text-[var(--color-text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
            </svg>
          </h3>
          {{ with .Description }}
          <p class="text-sm text-[var(--color-text-secondary)] mt-1 line-clamp-2">{{ . }}</p>
          {{ end }}
          <div class="flex items-center gap-3 mt-2 text-xs text-[var(--color-text-secondary)]">
            <time datetime="{{ .Date.Format "2006-01-02" }}">{{ .Date.Format "Jan 2, 2006" }}</time>
            {{ with .Params.link }}
            <span class="truncate max-w-[200px]">{{ . | replaceRE "^https?://(www\\.)?" "" | replaceRE "/.*$" "" }}</span>
            {{ end }}
          </div>
        </div>
      </a>
    </article>
    {{ end }}
  </div>

  {{/* Pagination */}}
  {{ if gt $paginator.TotalPages 1 }}
  <nav class="flex items-center justify-center gap-4 mt-12">
    {{ if $paginator.HasPrev }}
    <a href="{{ $paginator.Prev.URL }}" class="px-4 py-2 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
      &larr; Newer
    </a>
    {{ end }}

    <span class="text-sm text-[var(--color-text-secondary)]">
      Page {{ $paginator.PageNumber }} of {{ $paginator.TotalPages }}
    </span>

    {{ if $paginator.HasNext }}
    <a href="{{ $paginator.Next.URL }}" class="px-4 py-2 rounded-lg border border-[var(--color-border)] hover:border-[var(--color-accent)] transition-all">
      Older &rarr;
    </a>
    {{ end }}
  </nav>
  {{ end }}
</div>
{{ end }}
```

**Step 2: Commit**

```bash
git add layouts/links/list-new.html
git commit -m "feat: create links list with favicon and external link indicators"
```

---

## Phase 6: Search & Features

### Task 6.1: Install and Configure Pagefind

**Files:**
- Modify: `scripts/build.sh`
- Create: `layouts/partials/search-modal.html`

**Step 1: Update build script to include Pagefind**

Modify `scripts/build.sh`:
```bash
#!/bin/bash
set -e

echo "Building Tailwind CSS..."
./bin/tailwindcss -i ./assets/css/tailwind-input.css -o ./static/css/tailwind.css --minify

echo "Building Hugo..."
hugo --cleanDestinationDir --minify --forceSyncStatic --gc --logLevel info

echo "Building search index with Pagefind..."
npx pagefind --site public --glob "**/*.html"

echo "Build complete!"
```

**Step 2: Create search modal partial**

Create `layouts/partials/search-modal.html`:
```html
{{/* Search Modal */}}
<div id="search-modal" class="fixed inset-0 z-50 hidden">
  {{/* Backdrop */}}
  <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" id="search-backdrop"></div>

  {{/* Modal */}}
  <div class="absolute top-[20%] left-1/2 -translate-x-1/2 w-full max-w-2xl mx-auto px-4">
    <div class="bg-[var(--color-bg)] rounded-xl shadow-2xl border border-[var(--color-border)] overflow-hidden">
      {{/* Search input */}}
      <div class="p-4 border-b border-[var(--color-border)]">
        <div class="flex items-center gap-3">
          <svg class="w-5 h-5 text-[var(--color-text-secondary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
          </svg>
          <input
            type="text"
            id="search-input"
            placeholder="Search posts, notes, books..."
            class="flex-1 bg-transparent text-lg outline-none placeholder:text-[var(--color-text-secondary)]"
            autocomplete="off"
          >
          <kbd class="hidden sm:inline-flex items-center px-2 py-1 text-xs font-mono bg-[var(--color-bg-secondary)] rounded">
            ESC
          </kbd>
        </div>
      </div>

      {{/* Results */}}
      <div id="search-results" class="max-h-[60vh] overflow-y-auto p-2">
        <p class="text-center text-[var(--color-text-secondary)] py-8">
          Start typing to search...
        </p>
      </div>
    </div>
  </div>
</div>

<script>
  // Pagefind search integration
  (function() {
    const modal = document.getElementById('search-modal');
    const backdrop = document.getElementById('search-backdrop');
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');
    const searchBtn = document.getElementById('search-btn');

    let pagefind = null;

    async function initPagefind() {
      if (!pagefind) {
        pagefind = await import('/pagefind/pagefind.js');
        await pagefind.init();
      }
      return pagefind;
    }

    function openSearch() {
      modal.classList.remove('hidden');
      input.focus();
      document.body.style.overflow = 'hidden';
    }

    function closeSearch() {
      modal.classList.add('hidden');
      input.value = '';
      results.innerHTML = '<p class="text-center text-[var(--color-text-secondary)] py-8">Start typing to search...</p>';
      document.body.style.overflow = '';
    }

    async function doSearch(query) {
      if (!query.trim()) {
        results.innerHTML = '<p class="text-center text-[var(--color-text-secondary)] py-8">Start typing to search...</p>';
        return;
      }

      const pf = await initPagefind();
      const search = await pf.search(query);

      if (search.results.length === 0) {
        results.innerHTML = '<p class="text-center text-[var(--color-text-secondary)] py-8">No results found.</p>';
        return;
      }

      const items = await Promise.all(search.results.slice(0, 10).map(r => r.data()));

      results.innerHTML = items.map(item => `
        <a href="${item.url}" class="block p-3 rounded-lg hover:bg-[var(--color-bg-secondary)] transition-colors">
          <h4 class="font-medium text-[var(--color-text)]">${item.meta.title || 'Untitled'}</h4>
          <p class="text-sm text-[var(--color-text-secondary)] mt-1 line-clamp-2">${item.excerpt}</p>
        </a>
      `).join('');
    }

    // Event listeners
    searchBtn?.addEventListener('click', openSearch);
    backdrop?.addEventListener('click', closeSearch);

    document.addEventListener('keydown', (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        openSearch();
      }
      if (e.key === 'Escape') {
        closeSearch();
      }
    });

    let debounceTimer;
    input?.addEventListener('input', (e) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => doSearch(e.target.value), 200);
    });
  })();
</script>
```

**Step 3: Include search modal in baseof**

Add before closing `</body>` in `layouts/_default/baseof-new.html`:
```html
{{ partial "search-modal.html" . }}
```

**Step 4: Commit**

```bash
git add scripts/build.sh layouts/partials/search-modal.html layouts/_default/baseof-new.html
git commit -m "feat: add Pagefind search with modal UI"
```

---

## Phase 7: Cutover & Polish

### Task 7.1: Swap Templates

**Files:**
- Rename: `layouts/_default/baseof.html` → `layouts/_default/baseof-old.html`
- Rename: `layouts/_default/baseof-new.html` → `layouts/_default/baseof.html`
- Similar for all `-new` templates

**Step 1: Backup old templates**

```bash
mv layouts/_default/baseof.html layouts/_default/baseof-old.html
mv layouts/index.html layouts/index-old.html
mv layouts/post/single.html layouts/post/single-old.html
mv layouts/notes/list.html layouts/notes/list-old.html
mv layouts/books/list.html layouts/books/list-old.html
mv layouts/music/list.html layouts/music/list-old.html
mv layouts/links/list.html layouts/links/list-old.html
```

**Step 2: Activate new templates**

```bash
mv layouts/_default/baseof-new.html layouts/_default/baseof.html
mv layouts/index-new.html layouts/index.html
mv layouts/post/single-new.html layouts/post/single.html
mv layouts/notes/list-new.html layouts/notes/list.html
mv layouts/books/list-new.html layouts/books/list.html
mv layouts/music/list-new.html layouts/music/list.html
mv layouts/links/list-new.html layouts/links/list.html
```

**Step 3: Commit**

```bash
git add layouts/
git commit -m "feat: swap to new redesigned templates"
```

---

### Task 7.2: Remove Old CSS Files

**Files:**
- Archive: `assets/css/*.css` (old files)

**Step 1: Archive old CSS**

```bash
mkdir -p assets/css-old
mv assets/css/root-colors.css assets/css-old/
mv assets/css/harper.css assets/css-old/
mv assets/css/shared.css assets/css-old/
mv assets/css/themes.css assets/css-old/
# Keep: tailwind-input.css, tokens.css
```

**Step 2: Update params.toml to remove old CSS**

Remove old CSS from `customcss` array, keep only Tailwind output.

**Step 3: Commit**

```bash
git add assets/css-old/ config/
git commit -m "chore: archive old CSS files"
```

---

### Task 7.3: Final Testing

**Step 1: Build and test locally**

```bash
./scripts/dev.sh
```

**Step 2: Check all pages**
- Homepage
- Post listing
- Single post
- Notes grid
- Books grid
- Music grid
- Links list
- Search functionality
- Theme toggle
- Mobile responsive

**Step 3: Run Lighthouse**

In Chrome DevTools, run Lighthouse audit. Target: 100/100/100/100.

**Step 4: Commit any fixes**

```bash
git add .
git commit -m "fix: address issues found in final testing"
```

---

## Summary

This implementation plan covers:

1. **Foundation** - Tailwind CSS standalone, fonts, design tokens
2. **Base Layout** - Header, footer, main template
3. **Homepage** - Hero post, notes grid, explore section
4. **Post Template** - Full reading experience with sidebar
5. **Content Types** - Notes, books, music, links
6. **Features** - Pagefind search, theme toggle
7. **Cutover** - Template swap, cleanup

Each task is atomic, testable, and builds toward the complete redesign.

---

Plan complete and saved to `docs/plans/2025-12-17-blog-redesign-implementation.md`.

**Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

Which approach?
