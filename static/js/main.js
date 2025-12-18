// ABOUTME: Main JavaScript for the blog - handles interactive features
// ABOUTME: Manages theme toggle, mobile menu, reading progress, search modal, and jump-to-top

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
