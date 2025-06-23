/**
 * Insight UI Theme Toggle für TailwindCSS & Storybook-Kompatibilität
 * Setzt sowohl .dark (für Tailwind) als auch [data-theme] (für Insight UI CSS)
 * Initialisierung: InsightUI.ThemeToggle.init();
 */

window.InsightUI = window.InsightUI || {};

InsightUI.ThemeToggle = {
  init: function () {
    const toggleButton = document.querySelector('[data-theme-toggle]');
    if (!toggleButton) return;

    const root = document.documentElement;
    const themeKey = 'insight-ui-theme';

    function setTheme(theme) {
      root.classList.toggle('dark', theme === 'dark');
      root.setAttribute('data-theme', theme);
      localStorage.setItem(themeKey, theme);
    }

    const savedTheme = localStorage.getItem(themeKey);
    if (savedTheme === 'dark' || savedTheme === 'light') {
      setTheme(savedTheme);
    } else {
      const htmlTheme = root.getAttribute('data-theme');
      if (htmlTheme === 'dark' || htmlTheme === 'light') {
        setTheme(htmlTheme);
      } else {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        setTheme(prefersDark ? 'dark' : 'light');
      }
    }

    toggleButton.addEventListener('click', function () {
      const isDark = root.classList.contains('dark');
      setTheme(isDark ? 'light' : 'dark');
    });

    if (!root.hasAttribute('data-theme')) {
      root.setAttribute('data-theme', root.classList.contains('dark') ? 'dark' : 'light');
    }
  }
};