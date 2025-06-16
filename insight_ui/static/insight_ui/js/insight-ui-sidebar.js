InsightUI.Sidebar = {
  init: function () {
    const sidebar = document.querySelector('[data-insight-sidebar]');
    if (!sidebar) return;

    // Funktion zum Öffnen der Sidebar
    function openSidebar() {
      sidebar.style.transform = 'translateX(0)';
    }

    // Funktion zum Schließen der Sidebar
    function closeSidebar() {
      sidebar.style.transform = 'translateX(100%)';
    }

    // Sidebar initial verstecken
    closeSidebar();

    // Öffnen, wenn Maus nahe an der rechten Seite ist
    document.addEventListener('mousemove', (e) => {
      const threshold = 50; // Pixel Abstand vom rechten Rand
      if (window.innerWidth - e.clientX < threshold) {
        openSidebar();
      } else {
        closeSidebar();
      }
    });

    // Optional: Schließen, wenn Maus die Sidebar verlässt
    sidebar.addEventListener('mouseleave', () => {
      closeSidebar();
    });
  }
};
document.addEventListener('DOMContentLoaded', InsightUI.Sidebar.init);
