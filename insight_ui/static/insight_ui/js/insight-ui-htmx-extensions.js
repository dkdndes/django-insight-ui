/**
 * Django Insight UI – HTMX Extensions
 *
 * Erweiterte HTMX-Funktionalität für:
 * - Infinite Scroll
 * - Form Validation
 * - Live Updates
 * - Progressive Enhancement
 * - WebSocket Support
 */

(function () {
  'use strict';

  if (typeof htmx === 'undefined') {
    console.warn('HTMX not found; InsightUI extensions will not be initialized.');
    return;
  }

  // Ensure namespace
  window.InsightUI = window.InsightUI || {};

  // ----------------------------------------
  // 🔁 HTMX Extension: Infinite Scroll
  // ----------------------------------------
  htmx.defineExtension('infinite-scroll', {
    onEvent: function (name, evt) {
      if (name !== 'htmx:afterRequest') return;
      const target = evt.detail.elt;
      if (!target.hasAttribute('hx-infinite-scroll')) return;

      const threshold = parseInt(target.getAttribute('data-threshold') || '100', 10);
      const scrollPosition = window.innerHeight + window.scrollY;
      const documentHeight = document.documentElement.offsetHeight;

      if (documentHeight - scrollPosition < threshold) {
        const nextUrl = target.getAttribute('data-next-url');
        if (nextUrl) {
          htmx.ajax('GET', nextUrl, { target: target, swap: 'beforeend' });
        }
      }
    }
  });

  // ----------------------------------------
  // ✅ HTMX Extension: Form Validation
  // ----------------------------------------
  htmx.defineExtension('form-validation', {
    onEvent: function (name, evt) {
      const form = evt.detail.elt;
      if (form.tagName !== 'FORM' || !form.hasAttribute('hx-validate')) return;

      if (name === 'htmx:beforeRequest') {
        const isValid = InsightUI.Form?.validate?.(form);
        if (!isValid) {
          evt.preventDefault();
          return false;
        }
      }

      if (name === 'htmx:afterRequest' && evt.detail.xhr?.status === 422) {
        try {
          const response = JSON.parse(evt.detail.xhr.responseText);
          InsightUI.Form?.showErrors?.(form, response.errors);
        } catch (e) {
          console.error('Validation response parse error:', e);
        }
      }
    }
  });

  // ----------------------------------------
  // 🔄 HTMX Extension: Live Updates (Polling)
  // ----------------------------------------
  htmx.defineExtension('live-updates', {
    init: function (elt) {
      if (!elt.hasAttribute('hx-live-update')) return;
      const interval = parseInt(elt.getAttribute('data-interval') || '5000', 10);
      const url = elt.getAttribute('hx-get');
      if (!url) return;

      const timer = setInterval(() => {
        htmx.ajax('GET', url, { target: elt, swap: 'innerHTML' });
      }, interval);

      // Store timer for potential cleanup
      elt._liveUpdateTimer = timer;
    },
    onEvent: function (name, evt) {
      // No-op: polling set up via init
    }
  });

  // ----------------------------------------
  // 🚀 HTMX Extension: Progressive Enhancement
  // ----------------------------------------
  htmx.defineExtension('progressive-enhancement', {
    onEvent: function (name, evt) {
      const el = evt.detail.elt;
      // Guard: ensure elt supports getAttribute
      if (!el || typeof el.getAttribute !== 'function') return;
      const loadingClass = el.getAttribute('data-loading-class') || 'htmx-loading';

      if (name === 'htmx:beforeRequest') {
        el.classList.add(loadingClass);
        const spinner = el.querySelector('.htmx-spinner');
        if (spinner) spinner.style.display = 'block';
      }

      if (name === 'htmx:afterRequest') {
        el.classList.remove(loadingClass);
        const spinner = el.querySelector('.htmx-spinner');
        if (spinner) spinner.style.display = 'none';
      }
    }
  });

  // ----------------------------------------
  // 🛠️ HTMX Extension: WebSocket Support
  // ----------------------------------------
  htmx.defineExtension('insight-websocket', {
    init: function(elt) {
      // Defensive: Stelle sicher, dass elt ein echtes Element ist
      if (!(elt instanceof Element) || typeof elt.getAttribute !== "function") return;

      const wsUrl = elt.getAttribute('data-ws-url');
      const wsTarget = elt.getAttribute('data-ws-target');
      if (!wsUrl || !wsTarget) return;

      // Verhindere doppelte Verbindungen
      if (elt._insightWebSocket) return;

      const ws = new WebSocket(wsUrl);
      elt._insightWebSocket = ws;

      ws.onopen = function () {
        console.log('[InsightUI][WebSocket] WebSocket connected:', wsUrl);
      };

      ws.onmessage = function (event) {
        let data = event.data;
        let isValidJson = false;
        console.log('[InsightUI][WebSocket] Nachricht empfangen:', event.data);
        try {
          data = JSON.parse(event.data);
          isValidJson = true;
        } catch (e) {
          // Fallback: plain text
        }
        if (!isValidJson) {
          console.warn('[InsightUI][WebSocket] Ungültiges JSON empfangen:', event.data);
        }
        const target = document.querySelector(wsTarget);
        if (target) {
          if (typeof data === "object" && data.content) {
            target.innerHTML = data.content;
          } else if (typeof data === "object") {
            // Zeige JSON als Text (kein <pre>), um [object Object] zu vermeiden
            target.innerText = typeof data === "string" ? data : JSON.stringify(data, null, 2);
          } else {
            target.innerText = typeof data === "string" ? data : JSON.stringify(data);
          }
        }
      };

      ws.onclose = function () {
        console.log('[InsightUI][WebSocket] WebSocket disconnected:', wsUrl);
      };

      ws.onerror = function (err) {
        console.error('[InsightUI][WebSocket] WebSocket error:', err);
      };
    }
  });

  // ----------------------------------------
  // 🛠️ Auto-Init All Extensions + WebSocket Binding
  // ----------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    htmx.config.extensions = ['infinite-scroll', 'form-validation', 'live-updates', 'progressive-enhancement', 'insight-websocket'];

    // Initialisiere WebSocket-Komponenten
    document.querySelectorAll('[data-ws-url][data-ws-target]').forEach(function(elt) {
      if (typeof htmx !== "undefined" && htmx.findExt && htmx.findExt(elt, 'insight-websocket')) {
        // Extension wird automatisch initialisiert
        return;
      }
      // Fallback: manuell initialisieren
      htmx.findAllExtensions().forEach(function(ext) {
        if (ext.name === 'insight-websocket' && ext.init) {
          ext.init(elt);
        }
      });
    });
  });
})();

