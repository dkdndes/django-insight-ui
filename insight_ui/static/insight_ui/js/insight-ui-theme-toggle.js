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

    // Theme setzen: .dark für Tailwind, [data-theme] für Insight UI CSS
    function setTheme(theme) {
      if (theme === 'dark') {
        root.classList.add('dark');
        root.setAttribute('data-theme', 'dark');
      } else {
        root.classList.remove('dark');
        root.setAttribute('data-theme', 'light');
      }
      localStorage.setItem(themeKey, theme);
    }

    // Initiales Theme bestimmen
    const savedTheme = localStorage.getItem(themeKey);
    if (savedTheme === 'dark' || savedTheme === 'light') {
      setTheme(savedTheme);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(prefersDark ? 'dark' : 'light');
    }

    // Toggle-Button Event
    toggleButton.addEventListener('click', function () {
      const isDark = root.classList.contains('dark');
      setTheme(isDark ? 'light' : 'dark');
    });

    // Attribut-Korrektur für Storybook: data-theme auf <html> sicherstellen
    if (!root.hasAttribute('data-theme')) {
      root.setAttribute('data-theme', root.classList.contains('dark') ? 'dark' : 'light');
    }
  }
};
