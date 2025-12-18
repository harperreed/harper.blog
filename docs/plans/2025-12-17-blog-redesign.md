# Harper's Blog Redesign: Artisanal Editorial

**Date:** 2025-12-17
**Status:** Approved
**Approach:** Big bang redesign on feature branch

---

## Vision

A sophisticated indie publication aesthetic—a beautifully typeset literary journal meets hacker terminal. Exposed structure with warmth. Confident typography with breathing room. Every element intentional.

---

## Visual Identity

### Typography System

| Role | Font | Rationale |
|------|------|-----------|
| Display/Headlines | **Fraunces** | Variable serif with optical sizing, quirky ball terminals, handcrafted but modern |
| Body Text | **General Sans** or **Satoshi** | Geometric sans with warmth, highly readable, contemporary |
| Code/Mono | **JetBrains Mono** | Excellent ligatures, designed for reading code |
| UI/Small Text | Body font at smaller weights | Consistency |

### Color System

**Light Mode:**
| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#FAF9F6` | Warm off-white background |
| `--text` | `#1C1917` | Near-black with warmth |
| `--accent` | `#C2410C` | Deep terracotta for links, highlights |
| `--secondary` | `#475569` | Slate blue-gray for metadata |
| `--border` | `#E7E5E4` | Subtle warm gray |

**Dark Mode:**
| Token | Value | Usage |
|-------|-------|-------|
| `--bg` | `#1C1917` | Rich charcoal |
| `--text` | `#FAF9F6` | Warm cream |
| `--accent` | `#F59E0B` | Amber glow |
| `--secondary` | `#A8A29E` | Muted stone |
| `--border` | `#292524` | Subtle dark |

---

## Layout Architecture

### Grid System

12-column grid with intentional asymmetry. Content can sit left with generous right margins.

```
┌─────────────────────────────────────────────────────────┐
│  [Logo]              [Nav: Posts / Notes / Books / ...]│
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────┐  ┌──────────────────┐ │
│  │   Main Content Area         │  │ Meta sidebar     │ │
│  │   (prose width: 65ch)       │  │ - Reading time   │ │
│  │                             │  │ - TOC (sticky)   │ │
│  │                             │  │ - Tags           │ │
│  │                             │  │ - Share          │ │
│  └─────────────────────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Layout Decisions

- **Content width:** 65 characters max for optimal readability
- **Sticky meta sidebar:** Desktop only, moves to header/footer on mobile
- **Full-bleed images:** Can break out of content column for impact
- **Reading progress bar:** Fixed at top, 3px, accent color
- **Vertical rhythm:** 1.5rem base spacing, modular scale

### Responsive Breakpoints

| Breakpoint | Behavior |
|------------|----------|
| Desktop (1024px+) | Two-column with sidebar |
| Tablet (768-1023px) | Single column, meta above content |
| Mobile (<768px) | Stacked, hamburger nav, thinner progress bar |

---

## Homepage Design

```
┌──────────────────────────────────────────────────────────┐
│  HARPER REED                           [Nav] [🔍] [☀/🌙]│
├──────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────┐  │
│  │  LATEST POST (Hero treatment)                      │  │
│  │  "Title of Most Recent Post"                       │  │
│  │  First 2-3 sentences as hook...            →Read   │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐        │
│  │ Recent Note │ │ Recent Note │ │ Recent Note │        │
│  └─────────────┘ └─────────────┘ └─────────────┘        │
│                                                          │
│  ── CURRENTLY ──────────────────────────────────────     │
│  📚 Reading: [Book]    🎵 Listening: [Album]            │
│                                                          │
│  ── EXPLORE ────────────────────────────────────────     │
│  [Posts]  [Notes]  [Books]  [Music]  [Links]  [Random]  │
└──────────────────────────────────────────────────────────┘
```

---

## Features

### Priority 1: Reading Enhancements

- **Progress bar:** 3px at viewport top, accent color, CSS scroll-timeline (JS fallback)
- **Reading time:** "X min read" in meta sidebar
- **Table of contents:** Auto-generated from H2/H3, sticky sidebar, highlights current section
- **Jump to top:** Appears after 500px scroll, fixed bottom-right

### Priority 2: Content Discovery

- **Search:** Cmd+K modal via Pagefind (static, no server)
- **Random post button:** Explore the archive serendipitously
- **Related posts:** End of each post, tag-based
- **Archive page:** Grouped by year, filterable by tag
- **Tag system:** Clickable tags lead to filtered views

### Priority 3: Engagement

- **Kudos button:** Micro-animation on click (confetti/heart)
- **Share buttons:** Appear on hover/focus (X, Bluesky, Copy Link)
- **Bluesky comments:** Styled to match site aesthetic, threaded
- **Email reply:** Prominent CTA

### Priority 4: Visual Content

- **Lightbox:** For images, keyboard accessible
- **Better figures:** Full-bleed option, refined captions
- **Lazy loading:** Blur placeholder → sharp image transition
- **Image galleries:** Grid with lightbox integration

### Priority 5: Accessibility & Comfort

- **Font size controls:** Small/Medium/Large toggle
- **Reading width toggle:** Narrow/Wide
- **Reduced motion:** Respects `prefers-reduced-motion`
- **Print stylesheet:** Clean, no chrome
- **Keyboard navigation:** Full site navigable via keyboard

---

## Content Type Treatments

### Notes (Micro-posts)
- Refined masonry grid with subtle shadows
- Image notes: hero treatment, text overlay on hover
- Text-only notes: large quote-style typography
- Filter pills: All / Text / Images / With Links

### Books
- Cover grid with hover reveal (title, author, rating)
- "Currently reading" section with progress
- Shelf shadow effect under covers
- Modal for notes/review on click

### Music
- Album art grid
- Hover shows track/album, artist
- "Recent listens" + "Favorites" sections
- Optional Spotify embed on detail

### Links
- Clean list with auto-fetched favicons
- Grouped by date or category
- External link icon, opens new tab

---

## Technical Architecture

### Stack

- **Hugo** (existing, fast)
- **Tailwind CSS v4** with custom design tokens
- **Vanilla JS** (minimal, progressive enhancement)
- **Pagefind** for static search
- **Tailwind CLI standalone binary** (no Node.js build dependency)

### CSS Structure

```
assets/css/
├── tailwind.css          # Tailwind imports + custom base
├── tokens.css            # Design tokens
├── components/           # Component-specific styles
└── utilities.css         # Custom utilities
```

### Performance Targets

| Metric | Target |
|--------|--------|
| Lighthouse (all categories) | 100 |
| First paint (3G) | <1s |
| Total page weight (excl. images) | <200KB |
| Layout shift | Zero |

### Font Strategy
- Subset fonts to used characters
- Preload critical weights
- `font-display: swap`

### Resilience

- **No-JS fallback:** All core content readable, navigation works
- **Progressive enhancement:** Search, progress bar, TOC highlighting enhanced with JS
- **Print stylesheet:** Clean output

### Modern CSS Features

- `@container` queries for responsive components
- `:has()` for parent-aware styling
- `color-mix()` for dynamic color variations
- `scroll-timeline` for progress bar (with fallback)
- View Transitions API ready

---

## Implementation Approach

**Big bang redesign:**
1. Create feature branch
2. Set up Tailwind + design tokens
3. Build base layout (header, footer, main structure)
4. Implement homepage
5. Build post template with all reading features
6. Build content type templates (notes, books, music, links)
7. Add search, theme toggle, accessibility features
8. Performance optimization pass
9. QA and testing
10. Merge to main

---

## Removed from Current Site

- 30+ theme variants (keeping only light/dark)
- Verdana typography
- Current color scheme
- Basic list layouts

---

## Success Criteria

- Visually striking and memorable
- Perfect Lighthouse scores
- Works without JavaScript
- Delightful reading experience
- Easy content discovery
- Maintains all existing content and URLs
