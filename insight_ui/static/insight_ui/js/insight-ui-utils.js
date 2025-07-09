/**
 * Insight UI - Shared Utilities
 */
window.InsightUI = window.InsightUI || {};
window.utils = window.utils || {
  on: function(el, evt, selectorOrHandler, handler) {
    if (typeof selectorOrHandler === "function") {
      el.addEventListener(evt, selectorOrHandler);
    } else {
      el.addEventListener(evt, function (e) {
        if (e.target.closest(selectorOrHandler)) {
          handler.call(e.target.closest(selectorOrHandler), e);
        }
      });
    }
  },
  hasClass: (el, cls) => el.classList.contains(cls),
  addClass: (el, cls) => el.classList.add(cls),
  removeClass: (el, cls) => el.classList.remove(cls),
  toggleClass: (el, cls) => el.classList.toggle(cls),
  onEscape: (callback) => {
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") callback(e);
    });
  },
  trapFocus: (modal) => {
    const focusableEls = modal.querySelectorAll('a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])');
    const first = focusableEls[0];
    const last = focusableEls[focusableEls.length - 1];
    modal.addEventListener('keydown', function(e) {
      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault(); last.focus();
        } else if (document.activeElement === last) {
          e.preventDefault(); first.focus();
        }
      }
    });
    first?.focus();
  }
};