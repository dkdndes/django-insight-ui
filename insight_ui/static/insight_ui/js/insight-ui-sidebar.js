InsightUI.Sidebar = {
  init: function () {
    const sidebars = document.querySelectorAll('[data-insight-sidebar]');
    if (!sidebars) return;

    for (const sidebar of sidebars)
    {
      const side = sidebar.getAttribute("data-insight-sidebar");

      // Sidebar closes automatically when the mouse leaves the sidebar
      let autoClose = true;

      // Funktion zum Öffnen der Sidebar
      function openSidebar() {
        sidebar.style.transform = 'translateX(0)';
      }

      // Funktion zum Schließen der Sidebar
      function closeSidebar() {
        if (side == "right") sidebar.style.transform = 'translateX(100%)';
        else if (side == "left") sidebar.style.transform = 'translateX(-100%)';
      }

      // Sidebar initial verstecken
      closeSidebar();

      // Öffnen, wenn Maus nahe an der Fenster Seite ist
      document.addEventListener('mousemove', (e) => {
        const threshold = 50; // Pixel Abstand vom Rand
        if (side == "right" && window.innerWidth - e.clientX < threshold) {
          openSidebar();
        }
        else if (side == "left" && e.clientX < threshold) {
          openSidebar();
        }
      });

      // Optional: Schließen, wenn Maus die Sidebar verlässt
      sidebar.addEventListener('mouseleave', () => {
        if (autoClose) closeSidebar();
      });
    }
  }
};
document.addEventListener('DOMContentLoaded', InsightUI.Sidebar.init);
