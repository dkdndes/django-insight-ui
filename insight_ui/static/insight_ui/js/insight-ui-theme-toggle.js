InsightUI.ThemeToggle = {
  init: function () {
    const toggleButton = document.querySelector('[data-theme-toggle]');
    if (!toggleButton) return;

    const root = document.documentElement;
    const themeKey = 'insight-ui-theme';

    // Funktion zum Setzen des Themas
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

    // Aktuelles Thema aus localStorage oder Systempräferenz
    const savedTheme = localStorage.getItem(themeKey);
    if (savedTheme) {
      setTheme(savedTheme);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(prefersDark ? 'dark' : 'light');
    }

    // Eventlistener für den Toggle-Button
    toggleButton.addEventListener('click', () => {
      const currentTheme = root.classList.contains('dark') ? 'dark' : 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
    });
  }
};
