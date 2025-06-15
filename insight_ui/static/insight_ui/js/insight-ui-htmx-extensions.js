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
          htmx.ajax('GET', nextUrl, { target, swap: 'beforeend' });
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

      if (name === 'htmx:afterRequest' && evt.detail.xhr.status === 422) {
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
    onEvent: function (name, evt) {
      if (name !== 'htmx:afterSettle') return;

      const el = evt.detail.elt;
      if (!el.hasAttribute('hx-live-update')) return;

      const interval = parseInt(el.getAttribute('data-interval') || '5000', 10);
      const url = el.getAttribute('hx-get');
      if (!url) return;

      setInterval(() => {
        htmx.ajax('GET', url, { target: el, swap: 'innerHTML' });
      }, interval);
    }
  });

  // ----------------------------------------
  // 🚀 HTMX Extension: Progressive Enhancement
  // ----------------------------------------

  htmx.defineExtension('progressive-enhancement', {
    onEvent: function (name, evt) {
      const el = evt.detail.elt;
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
  // 📡 InsightUI WebSocket Support
  // ----------------------------------------

  InsightUI.WebSocket = {
    connections: new Map(),

    connect: function (url, options = {}) {
      if (this.connections.has(url)) return this.connections.get(url);

      const ws = new WebSocket(url);
      this.connections.set(url, ws);

      ws.onopen = (e) => {
        console.log('WebSocket connected:', url);
        options.onOpen?.(e);
      };

      ws.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data);

          // HTMX-style content update
          if (data.target && data.content) {
            const target = document.querySelector(data.target);
            if (target) {
              const swap = data.swap || 'innerHTML';
              htmx.swap(target, data.content, { swapStyle: swap });
            }
          }

          // Custom event dispatch
          if (data.event) {
            document.dispatchEvent(new CustomEvent(data.event, { detail: data.payload }));
          }

          options.onMessage?.(data);
        } catch (err) {
          console.error('WebSocket message error:', err);
        }
      };

      ws.onclose = (e) => {
        console.log('WebSocket disconnected:', url);
        this.connections.delete(url);
        options.onClose?.(e);
      };

      ws.onerror = (e) => {
        console.error('WebSocket error:', e);
        options.onError?.(e);
      };

      return ws;
    },

    send: function (url, data) {
      const ws = this.connections.get(url);
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify(data));
      }
    },

    disconnect: function (url) {
      const ws = this.connections.get(url);
      if (ws) {
        ws.close();
        this.connections.delete(url);
      }
    }
  };

  // ----------------------------------------
  // 🛠️ Auto-Init All Extensions + WebSocket Binding
  // ----------------------------------------

  document.addEventListener('DOMContentLoaded', function () {
    htmx.config.extensions = [
      'infinite-scroll',
      'form-validation',
      'live-updates',
      'progressive-enhancement'
    ];

    // Optional auto-bind WebSocket elements
    document.querySelectorAll('[data-ws-url]').forEach(el => {
      const url = el.getAttribute('data-ws-url');
      const target = el.getAttribute('data-ws-target') || el;

      InsightUI.WebSocket.connect(url, {
        onMessage: function (data) {
          const targetSelector = typeof target === 'string' ? target : `#${el.id}`;
          const targetEl = document.querySelector(targetSelector);
          if (targetEl && data.content) {
            targetEl.innerHTML = data.content;
          }
        }
      });
    });
  });

})();