/**
 * Insight UI - Component Initializer
 */
document.addEventListener('DOMContentLoaded', function () {
  console.log('🚀 InsightUI Initialisierung gestartet');
  
  InsightUI.Navbar?.init?.();
  console.log('📊 Navbar initialisiert');
  
  InsightUI.Alert?.init?.();
  console.log('🚨 Alert initialisiert');
  
  InsightUI.ThemeToggle?.init?.();
  console.log('🌓 ThemeToggle initialisiert');
  
  InsightUI.Modal?.init?.();
  console.log('📋 Modal initialisiert');
  
  InsightUI.Sidebar?.init?.();
  console.log('📂 Sidebar initialisiert');
  
  InsightUI.Form?.init?.();
  console.log('📝 Form initialisiert');
  
  InsightUI.WebSocket?.init?.();
  console.log('🔌 WebSocket initialisiert');

  console.log('✅ Alle InsightUI Komponenten erfolgreich initialisiert');
});
