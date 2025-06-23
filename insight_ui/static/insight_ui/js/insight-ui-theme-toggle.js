/**
 * Insight UI Theme Toggle für TailwindCSS & Storybook-Kompatibilität
 * Setzt sowohl .dark (für Tailwind) als auch [data-theme] (für Insight UI CSS)
 * Initialisierung: InsightUI.ThemeToggle.init();
 */

window.InsightUI = window.InsightUI || {};

InsightUI.ThemeToggle = {
  init: function () {
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

    // Alle Theme-Toggle-Buttons initialisieren
    document.querySelectorAll('[data-theme-toggle]').forEach(function(toggleButton) {
      toggleButton.addEventListener('click', function (e) {
        e.stopPropagation(); // verhindert Event-Bubbling
        console.log('Theme-Toggle Button geklickt');
        const isDark = root.classList.contains('dark');
        setTheme(isDark ? 'light' : 'dark');
      });
    });

    if (!root.hasAttribute('data-theme')) {
      root.setAttribute('data-theme', root.classList.contains('dark') ? 'dark' : 'light');
    }
  }
};
