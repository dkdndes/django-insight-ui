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

    // Fokus-Management für Barrierefreiheit
    trapFocus: function(element) {
      const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      element.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstElement) {
              lastElement.focus();
              e.preventDefault();
            }
          } else {
            if (document.activeElement === lastElement) {
              firstElement.focus();
              e.preventDefault();
            }
          }
        }
      });

      if (firstElement) {
        firstElement.focus();
      }
    },

    // Escape-Key Handler
    onEscape: function(handler) {
      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
          handler(e);
        }
      });
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

  // Modal-Komponente
  InsightUI.Modal = {
    init: function() {
      // Modal öffnen
      utils.on(document, 'click', '[data-insight-toggle="modal"]', function() {
        const targetId = this.getAttribute('data-insight-target');
        const modal = document.getElementById(targetId);
        if (modal) {
          InsightUI.Modal.show(modal);
        }
      });

      // Modal schließen
      utils.on(document, 'click', '[data-insight-dismiss="modal"]', function() {
        const modal = this.closest('.insight-modal');
        if (modal) {
          InsightUI.Modal.hide(modal);
        }
      });

      // Modal bei Backdrop-Klick schließen
      utils.on(document, 'click', '.insight-modal__backdrop', function() {
        const modal = this.closest('.insight-modal');
        if (modal) {
          InsightUI.Modal.hide(modal);
        }
      });

      // Modal bei Escape-Taste schließen
      utils.onEscape(function() {
        const openModal = document.querySelector('.insight-modal.insight-modal--open');
        if (openModal) {
          InsightUI.Modal.hide(openModal);
        }
      });
    },

    show: function(modal) {
      if (!modal) return;

      // Modal anzeigen
      utils.addClass(modal, 'insight-modal--open');
      modal.setAttribute('aria-hidden', 'false');
      
      // Body-Scroll verhindern
      utils.addClass(document.body, 'insight-modal-open');
      
      // Fokus-Management
      utils.trapFocus(modal);
      
      // Event auslösen
      modal.dispatchEvent(new CustomEvent('insight:modal:show'));
    },

    hide: function(modal) {
      if (!modal) return;

      // Modal ausblenden
      utils.removeClass(modal, 'insight-modal--open');
      modal.setAttribute('aria-hidden', 'true');
      
      // Body-Scroll wieder erlauben
      utils.removeClass(document.body, 'insight-modal-open');
      
      // Event auslösen
      modal.dispatchEvent(new CustomEvent('insight:modal:hide'));
    }
  };

  // Sidebar-Komponente
  InsightUI.Sidebar = {
    init: function() {
      const toggleButtons = document.querySelectorAll('[data-insight-toggle="sidebar"]');
      
      toggleButtons.forEach(button => {
        utils.on(button, 'click', function() {
          const sidebar = this.closest('.insight-sidebar');
          if (sidebar) {
            InsightUI.Sidebar.toggle(sidebar);
          }
        });
      });
    },

    toggle: function(sidebar) {
      if (!sidebar) return;

      const isExpanded = sidebar.getAttribute('aria-expanded') !== 'false';
      const content = sidebar.querySelector('.insight-sidebar__content');
      const toggleButton = sidebar.querySelector('[data-insight-toggle="sidebar"]');

      if (isExpanded) {
        // Sidebar einklappen
        utils.addClass(sidebar, 'insight-sidebar--collapsed');
        sidebar.setAttribute('aria-expanded', 'false');
        if (toggleButton) {
          toggleButton.setAttribute('aria-expanded', 'false');
          toggleButton.setAttribute('aria-label', 'Sidebar ausklappen');
        }
        if (content) {
          content.setAttribute('aria-hidden', 'true');
        }
      } else {
        // Sidebar ausklappen
        utils.removeClass(sidebar, 'insight-sidebar--collapsed');
        sidebar.setAttribute('aria-expanded', 'true');
        if (toggleButton) {
          toggleButton.setAttribute('aria-expanded', 'true');
          toggleButton.setAttribute('aria-label', 'Sidebar einklappen');
        }
        if (content) {
          content.setAttribute('aria-hidden', 'false');
        }
      }

      // Event auslösen
      sidebar.dispatchEvent(new CustomEvent('insight:sidebar:toggle', {
        detail: { expanded: !isExpanded }
      }));
    }
  };

  // Form-Komponente mit HTMX-Integration
  InsightUI.Form = {
    init: function() {
      // Form-Validation
      utils.on(document, 'submit', '.insight-form', function(e) {
        const form = this;
        const isValid = InsightUI.Form.validate(form);
        
        if (!isValid) {
          e.preventDefault();
          return false;
        }
      });

      // Real-time Validation
      utils.on(document, 'blur', '.insight-form__input, .insight-form__textarea, .insight-form__select', function() {
        InsightUI.Form.validateField(this);
      });

      // HTMX Form Events
      utils.on(document, 'htmx:beforeRequest', '.insight-form[hx-post], .insight-form[hx-put]', function(e) {
        const form = this;
        const isValid = InsightUI.Form.validate(form);
        
        if (!isValid) {
          e.preventDefault();
          return false;
        }
        
        // Zeige Loading-State
        InsightUI.Form.setLoadingState(form, true);
      });

      utils.on(document, 'htmx:afterRequest', '.insight-form[hx-post], .insight-form[hx-put]', function(e) {
        const form = this;
        InsightUI.Form.setLoadingState(form, false);
        
        // Handle Validation Errors
        if (e.detail.xhr.status === 422) {
          try {
            const response = JSON.parse(e.detail.xhr.responseText);
            InsightUI.Form.showErrors(form, response.errors || {});
          } catch (err) {
            console.error('Error parsing validation response:', err);
          }
        }
      });
    },

    setLoadingState: function(form, loading) {
      const submitButtons = form.querySelectorAll('button[type="submit"]');
      const loadingClass = 'insight-form--loading';
      
      if (loading) {
        utils.addClass(form, loadingClass);
        submitButtons.forEach(btn => {
          btn.disabled = true;
          btn.setAttribute('data-original-text', btn.textContent);
          btn.textContent = 'Wird gesendet...';
        });
      } else {
        utils.removeClass(form, loadingClass);
        submitButtons.forEach(btn => {
          btn.disabled = false;
          const originalText = btn.getAttribute('data-original-text');
          if (originalText) {
            btn.textContent = originalText;
            btn.removeAttribute('data-original-text');
          }
        });
      }
    },

    showErrors: function(form, errors) {
      // Entferne vorherige Fehler
      form.querySelectorAll('.insight-form__error').forEach(error => {
        error.remove();
      });
      
      // Zeige neue Fehler
      Object.keys(errors).forEach(fieldName => {
        const field = form.querySelector(`[name="${fieldName}"]`);
        if (field) {
          const fieldGroup = field.closest('.insight-form__group');
          if (fieldGroup) {
            utils.addClass(fieldGroup, 'insight-form__group--error');
            
            const errorContainer = fieldGroup.querySelector('.insight-form__errors') || 
                                 fieldGroup.appendChild(document.createElement('div'));
            errorContainer.className = 'insight-form__errors';
            errorContainer.setAttribute('role', 'alert');
            
            errors[fieldName].forEach(errorMsg => {
              const errorSpan = document.createElement('span');
              errorSpan.className = 'insight-form__error';
              errorSpan.textContent = errorMsg;
              errorContainer.appendChild(errorSpan);
            });
          }
        }
      });
    },

    validate: function(form) {
      if (!form) return true;

      let isValid = true;
      const fields = form.querySelectorAll('.insight-form__input, .insight-form__textarea, .insight-form__select');
      
      fields.forEach(field => {
        if (!InsightUI.Form.validateField(field)) {
          isValid = false;
        }
      });

      return isValid;
    },

    validateField: function(field) {
      if (!field) return true;

      const fieldGroup = field.closest('.insight-form__group');
      const errorContainer = fieldGroup ? fieldGroup.querySelector('.insight-form__errors') : null;
      let isValid = true;
      let errorMessage = '';

      // Required-Validation
      if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        errorMessage = 'Dieses Feld ist erforderlich.';
      }

      // Email-Validation
      if (field.type === 'email' && field.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
          isValid = false;
          errorMessage = 'Bitte geben Sie eine gültige E-Mail-Adresse ein.';
        }
      }

      // Min/Max-Length Validation
      if (field.hasAttribute('minlength') && field.value.length < parseInt(field.getAttribute('minlength'))) {
        isValid = false;
        errorMessage = `Mindestens ${field.getAttribute('minlength')} Zeichen erforderlich.`;
      }

      // Error-Anzeige aktualisieren
      if (fieldGroup) {
        if (isValid) {
          utils.removeClass(fieldGroup, 'insight-form__group--error');
          utils.addClass(fieldGroup, 'insight-form__group--valid');
        } else {
          utils.addClass(fieldGroup, 'insight-form__group--error');
          utils.removeClass(fieldGroup, 'insight-form__group--valid');
        }

        if (errorContainer) {
          if (isValid) {
            errorContainer.innerHTML = '';
            errorContainer.setAttribute('aria-hidden', 'true');
          } else {
            errorContainer.innerHTML = `<span class="insight-form__error">${errorMessage}</span>`;
            errorContainer.setAttribute('aria-hidden', 'false');
          }
        }
      }

      return isValid;
    }
  };

  // Initialisiere alle Komponenten, wenn das DOM geladen ist
  document.addEventListener('DOMContentLoaded', function() {
    InsightUI.Navbar.init();
    InsightUI.Alert.init();
    InsightUI.ThemeToggle.init();
    InsightUI.Modal.init();
    InsightUI.Sidebar.init();
    InsightUI.Form.init();
  });

})();
