document.addEventListener('DOMContentLoaded', function() {
  const closeBtn = document.getElementById('right-sidebar-close');
  const rightSidebar = document.getElementById('right-sidebar');
  if (closeBtn && rightSidebar) {
    closeBtn.addEventListener('click', function() {
      rightSidebar.classList.remove('open');
      document.body.classList.remove('right-sidebar-open');
    });
  }
});
