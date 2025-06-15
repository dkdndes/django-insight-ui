document.addEventListener('DOMContentLoaded', function() {
  const closeBtn = document.getElementById('right-sidebar-close');
  const rightSidebar = document.getElementById('right-sidebar');
  const rightSidebarToggle = document.getElementById('toggle-right-sidebar');
  const rightSidebarHoverArea = document.getElementById('right-sidebar-hover-area');

  if (closeBtn && rightSidebar) {
    closeBtn.addEventListener('click', function() {
      rightSidebar.classList.remove('open');
      document.body.classList.remove('right-sidebar-open');
    });
  }

  if (rightSidebarToggle && rightSidebar) {
    rightSidebarToggle.addEventListener('click', function() {
      rightSidebar.classList.toggle('open');
      document.body.classList.toggle('right-sidebar-open');
    });
  }

  if (rightSidebarHoverArea && rightSidebar) {
    let openTimeout, closeTimeout;

    rightSidebarHoverArea.addEventListener('mouseenter', function() {
      clearTimeout(closeTimeout);
      openTimeout = setTimeout(function() {
        if (!rightSidebar.classList.contains('open')) {
          rightSidebar.classList.add('open');
          document.body.classList.add('right-sidebar-open');
        }
      }, 100);
    });

    rightSidebarHoverArea.addEventListener('mouseleave', function(e) {
      clearTimeout(openTimeout);
      if (e.relatedTarget !== rightSidebar) {
        closeTimeout = setTimeout(function() {
          rightSidebar.classList.remove('open');
          document.body.classList.remove('right-sidebar-open');
        }, 300);
      }
    });

    rightSidebar.addEventListener('mouseleave', function(e) {
      clearTimeout(openTimeout);
      if (e.relatedTarget !== rightSidebarHoverArea) {
        closeTimeout = setTimeout(function() {
          rightSidebar.classList.remove('open');
          document.body.classList.remove('right-sidebar-open');
        }, 300);
      }
    });

    rightSidebar.addEventListener('mouseenter', function() {
      clearTimeout(closeTimeout);
    });
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && rightSidebar.classList.contains('open')) {
      rightSidebar.classList.remove('open');
      document.body.classList.remove('right-sidebar-open');
    }
  });
});
