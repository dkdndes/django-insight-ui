/**
 * Django Insight UI - HTMX Extensions
 * 
 * Erweiterte HTMX-Funktionalität für Progressive Enhancement,
 * Infinite Scroll, WebSocket Support und Form Validation
 */

(function() {
  'use strict';

  // HTMX Extension für Infinite Scroll
  htmx.defineExtension('infinite-scroll', {
    onEvent: function(name, evt) {
      if (name === 'htmx:afterRequest') {
        const target = evt.detail.elt;
        if (target.hasAttribute('hx-infinite-scroll')) {
          // Prüfe, ob mehr Inhalte geladen werden sollen
          const threshold = parseInt(target.getAttribute('data-threshold') || '100');
          const scrollPosition = window.innerHeight + window.scrollY;
          const documentHeight = document.documentElement.offsetHeight;
          
          if (documentHeight - scrollPosition < threshold) {
            // Lade mehr Inhalte
            const nextUrl = target.getAttribute('data-next-url');
            if (nextUrl) {
              htmx.ajax('GET', nextUrl, {
                target: target,
                swap: 'beforeend'
              });
            }
          }
        }
      }
    }
  });

  // HTMX Extension für Form Validation
  htmx.defineExtension('form-validation', {
    onEvent: function(name, evt) {
      if (name === 'htmx:beforeRequest') {
        const form = evt.detail.elt;
        if (form.tagName === 'FORM' && form.hasAttribute('hx-validate')) {
          // Validiere Formular vor dem Senden
          const isValid = InsightUI.Form.validate(form);
          if (!isValid) {
            evt.preventDefault();
            return false;
          }
        }
      }
      
      if (name === 'htmx:afterRequest') {
        const form = evt.detail.elt;
        if (form.tagName === 'FORM' && evt.detail.xhr.status === 422) {
          // Zeige Validierungsfehler an
          const response = JSON.parse(evt.detail.xhr.responseText);
          InsightUI.Form.showErrors(form, response.errors);
        }
      }
    }
  });

  // HTMX Extension für Live Updates
  htmx.defineExtension('live-updates', {
    onEvent: function(name, evt) {
      if (name === 'htmx:afterSettle') {
        const element = evt.detail.elt;
        if (element.hasAttribute('hx-live-update')) {
          // Starte Live-Updates
          const interval = parseInt(element.getAttribute('data-interval') || '5000');
          const url = element.getAttribute('hx-get');
          
          if (url) {
            setInterval(() => {
              htmx.ajax('GET', url, {
                target: element,
                swap: 'innerHTML'
              });
            }, interval);
          }
        }
      }
    }
  });

  // HTMX Extension für Progressive Enhancement
  htmx.defineExtension('progressive-enhancement', {
    onEvent: function(name, evt) {
      if (name === 'htmx:beforeRequest') {
        // Füge Loading-Indikatoren hinzu
        const element = evt.detail.elt;
        const loadingClass = element.getAttribute('data-loading-class') || 'htmx-loading';
        element.classList.add(loadingClass);
        
        // Zeige Loading-Spinner
        const spinner = element.querySelector('.htmx-spinner');
        if (spinner) {
          spinner.style.display = 'block';
        }
      }
      
      if (name === 'htmx:afterRequest') {
        // Entferne Loading-Indikatoren
        const element = evt.detail.elt;
        const loadingClass = element.getAttribute('data-loading-class') || 'htmx-loading';
        element.classList.remove(loadingClass);
        
        // Verstecke Loading-Spinner
        const spinner = element.querySelector('.htmx-spinner');
        if (spinner) {
          spinner.style.display = 'none';
        }
      }
    }
  });

  // WebSocket Support für HTMX
  window.InsightUI = window.InsightUI || {};
  
  InsightUI.WebSocket = {
    connections: new Map(),
    
    connect: function(url, options = {}) {
      if (this.connections.has(url)) {
        return this.connections.get(url);
      }
      
      const ws = new WebSocket(url);
      this.connections.set(url, ws);
      
      ws.onopen = function(event) {
        console.log('WebSocket connected:', url);
        if (options.onOpen) options.onOpen(event);
      };
      
      ws.onmessage = function(event) {
        try {
          const data = JSON.parse(event.data);
          
          // HTMX-kompatible Updates
          if (data.target && data.content) {
            const target = document.querySelector(data.target);
            if (target) {
              const swapMethod = data.swap || 'innerHTML';
              htmx.swap(target, data.content, {swapStyle: swapMethod});
            }
          }
          
          // Custom Event Handler
          if (data.event) {
            document.dispatchEvent(new CustomEvent(data.event, {
              detail: data.payload
            }));
          }
          
          if (options.onMessage) options.onMessage(data);
        } catch (e) {
          console.error('WebSocket message parsing error:', e);
        }
      };
      
      ws.onclose = function(event) {
        console.log('WebSocket disconnected:', url);
        this.connections.delete(url);
        if (options.onClose) options.onClose(event);
      };
      
      ws.onerror = function(event) {
        console.error('WebSocket error:', event);
        if (options.onError) options.onError(event);
      };
      
      return ws;
    },
    
    send: function(url, data) {
      const ws = this.connections.get(url);
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
      }
    },
    
    disconnect: function(url) {
      const ws = this.connections.get(url);
      if (ws) {
        ws.close();
        this.connections.delete(url);
      }
    }
  };

  // Auto-Initialize HTMX Extensions
  document.addEventListener('DOMContentLoaded', function() {
    // Aktiviere alle Extensions
    htmx.config.extensions = [
      'infinite-scroll',
      'form-validation', 
      'live-updates',
      'progressive-enhancement'
    ];
    
    // WebSocket Verbindungen aus data-Attributen
    document.querySelectorAll('[data-ws-url]').forEach(element => {
      const url = element.getAttribute('data-ws-url');
      const target = element.getAttribute('data-ws-target') || element;
      
      InsightUI.WebSocket.connect(url, {
        onMessage: function(data) {
          if (data.target === target || data.target === element.id) {
            // Update Element mit WebSocket-Daten
            if (typeof target === 'string') {
              const targetElement = document.querySelector(target);
              if (targetElement && data.content) {
                targetElement.innerHTML = data.content;
              }
            }
          }
        }
      });
    });
  });

})();
