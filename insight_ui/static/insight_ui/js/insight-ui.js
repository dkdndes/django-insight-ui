/**
 * Django Insight UI - Haupt-JavaScript-Datei
 * 
 * Dieses Skript enthält die grundlegenden Funktionen für alle UI-Komponenten
 * mit Fokus auf Barrierefreiheit und Benutzerfreundlichkeit.
 */

// Sofort ausgeführte Funktion zum Schutz des globalen Namensraums
(function() {
  'use strict';

  // Namespace für alle Insight UI-Funktionen
  window.InsightUI = window.InsightUI || {};

  // Hilfsfunktionen
  const utils = {
    // Fügt einen Event-Listener zu einem Element oder einer Sammlung von Elementen hinzu
    on: function(element, event, selector, handler) {
      if (!element) return;
      
      if (typeof selector === 'function') {
        handler = selector;
        selector = null;
      }
      
      if (selector) {
        element.addEventListener(event, function(e) {
          const target = e.target.closest(selector);
          if (target) {
            handler.call(target, e);
          }
        });
      } else {
        element.addEventListener(event, handler);
      }
    },
    
    // Schaltet eine Klasse an einem Element um
    toggleClass: function(element, className) {
      if (!element) return;
      element.classList.toggle(className);
    },
    
    // Fügt eine Klasse zu einem Element hinzu
    addClass: function(element, className) {
      if (!element) return;
      element.classList.add(className);
    },
    
    // Entfernt eine Klasse von einem Element
    removeClass: function(element, className) {
      if (!element) return;
      element.classList.remove(className);
    },
    
    // Prüft, ob ein Element eine bestimmte Klasse hat
    hasClass: function(element, className) {
      if (!element) return false;
      return element.classList.contains(className);
    }
  };

  // Navbar-Komponente
  InsightUI.Navbar = {
    init: function() {
      const toggleButtons = document.querySelectorAll('[data-insight-toggle="navbar"]');
      
      toggleButtons.forEach(button => {
        utils.on(button, 'click', function() {
          const targetId = this.getAttribute('aria-controls');
          const target = document.getElementById(targetId);
          
          if (target) {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            utils.toggleClass(target, 'is-open');
            
            // Ändere das Aria-Label basierend auf dem Status
            this.setAttribute('aria-label', isExpanded ? 'Menü öffnen' : 'Menü schließen');
          }
        });
      });
      
      // Schließe das Menü, wenn außerhalb geklickt wird
      utils.on(document, 'click', function(e) {
        const navbars = document.querySelectorAll('.insight-navbar');
        
        navbars.forEach(navbar => {
          const toggle = navbar.querySelector('[data-insight-toggle="navbar"]');
          const menu = navbar.querySelector('.insight-navbar__menu');
          
          if (toggle && menu && utils.hasClass(menu, 'is-open')) {
            if (!navbar.contains(e.target)) {
              toggle.setAttribute('aria-expanded', 'false');
              toggle.setAttribute('aria-label', 'Menü öffnen');
              utils.removeClass(menu, 'is-open');
            }
          }
        });
      });
    }
  };

  // Alert-Komponente
  InsightUI.Alert = {
    init: function() {
      utils.on(document, 'click', '[data-insight-dismiss="alert"]', function() {
        const alert = this.closest('.insight-alert');
        if (alert) {
          // Animation hinzufügen und dann entfernen
          utils.addClass(alert, 'insight-alert--fade-out');
          
          setTimeout(() => {
            alert.remove();
          }, 300);
        }
      });
    }
  };

  // Theme-Umschalter
  InsightUI.ThemeToggle = {
    init: function() {
      const themeToggles = document.querySelectorAll('.insight-theme-toggle');
      
      // Aktuelles Theme aus localStorage oder Systemeinstellung abrufen
      const getInitialTheme = () => {
        const savedTheme = localStorage.getItem('insight-theme');
        if (savedTheme) {
          return savedTheme;
        }
        
        // Prüfe, ob das System einen dunklen Modus bevorzugt
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
          return 'dark';
        }
        
        return 'light';
      };
      
      // Aktuelles Theme setzen
      const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('insight-theme', theme);
        
        // Aktualisiere alle Toggle-Buttons
        themeToggles.forEach(toggle => {
          const themeIcon = toggle.querySelector('.insight-theme-toggle__icon');
          if (themeIcon) {
            themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
          }
        });
      };
      
      // Initialisiere mit dem gespeicherten oder Systemthema
      setTheme(getInitialTheme());
      
      // Event-Listener für Theme-Toggle-Buttons
      themeToggles.forEach(toggle => {
        utils.on(toggle, 'click', function() {
          const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
          const newTheme = currentTheme === 'light' ? 'dark' : 'light';
          setTheme(newTheme);
        });
      });
      
      // Reagiere auf Änderungen der Systemeinstellung
      if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
          if (!localStorage.getItem('insight-theme')) {
            setTheme(e.matches ? 'dark' : 'light');
          }
        });
      }
    }
  };

  // Initialisiere alle Komponenten, wenn das DOM geladen ist
  document.addEventListener('DOMContentLoaded', function() {
    InsightUI.Navbar.init();
    InsightUI.Alert.init();
    InsightUI.ThemeToggle.init();
  });

})();
