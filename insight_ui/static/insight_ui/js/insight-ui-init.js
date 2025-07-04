/**
 * Insight UI - Component Initializer
 */
document.addEventListener('DOMContentLoaded', function () {
  InsightUI.Navbar?.init?.();
  InsightUI.Alert?.init?.();
  InsightUI.ThemeToggle?.init?.();
  InsightUI.Modal?.init?.();
  InsightUI.Sidebar?.init?.();
  InsightUI.Form?.init?.(); 

  console.log('✅ InsightUI components initialized');
});