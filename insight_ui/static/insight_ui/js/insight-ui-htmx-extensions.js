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
  // Entfernt: Eigene WebSocket-Extension, da jetzt die offizielle htmx ws-Extension genutzt wird.

  // ----------------------------------------
  // 🛠️ Auto-Init All Extensions
  // ----------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    htmx.config.extensions = ['infinite-scroll', 'form-validation', 'live-updates', 'progressive-enhancement', 'ws'];
  });
})();

