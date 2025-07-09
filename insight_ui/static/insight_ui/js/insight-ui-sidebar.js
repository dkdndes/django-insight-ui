InsightUI.Sidebar = {
  init: function () {
    const sidebars = document.querySelectorAll('[data-insight-sidebar]');
    if (!sidebars.length) return;

    sidebars.forEach(sidebar => {
      const position = sidebar.getAttribute('data-position') || 'right';

      // Funktion zum Öffnen der Sidebar
      function openSidebar() {
        sidebar.style.transform = 'translateX(0)';
      }

      // Funktion zum Schließen der Sidebar
      function closeSidebar() {
        sidebar.style.transform = position === 'left' ? 'translateX(-100%)' : 'translateX(100%)';
      }

      // Sidebar initial verstecken
      closeSidebar();

      // Öffnen, wenn Maus nahe an der entsprechenden Seite ist
      document.addEventListener('mousemove', (e) => {
        const threshold = 50; // Pixel Abstand vom Rand
        if ((position === 'right' && window.innerWidth - e.clientX < threshold) ||
            (position === 'left' && e.clientX < threshold)) {
          openSidebar();
        } else {
          closeSidebar();
        }
      });

      // Optional: Schließen, wenn Maus die Sidebar verlässt
      sidebar.addEventListener('mouseleave', () => {
        closeSidebar();
      });
    });
  }
};
document.addEventListener('DOMContentLoaded', InsightUI.Sidebar.init);
