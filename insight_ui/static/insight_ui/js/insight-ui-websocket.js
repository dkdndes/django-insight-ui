/**
 * Insight UI - WebSocket-Komponente
 * Initialisiert WebSocket-Verbindungen für alle .insight-websocket-component-Elemente.
 * Erwartet data-ws-url und data-ws-target Attribute.
 */
window.InsightUI = window.InsightUI || {};

InsightUI.WebSocketComponent = {
  init: function () {
    document.querySelectorAll('.insight-websocket-component[data-ws-url]').forEach(function (el) {
      const wsUrl = el.getAttribute('data-ws-url');
      const targetSelector = el.getAttribute('data-ws-target');
      if (!wsUrl || !targetSelector) return;

      // Verbindung aufbauen
      const ws = new WebSocket(wsUrl);

      ws.onopen = function () {
        console.log('[InsightUI] WebSocket verbunden:', wsUrl);
      };

      ws.onmessage = function (event) {
        const target = document.querySelector(targetSelector);
        if (target) {
          try {
            const data = JSON.parse(event.data);
            if (data.content) {
              target.innerHTML = data.content;
            } else {
              target.innerText = event.data;
            }
          } catch (e) {
            target.innerText = event.data;
          }
        }
      };

      ws.onclose = function () {
        console.log('[InsightUI] WebSocket getrennt:', wsUrl);
      };

      ws.onerror = function (err) {
        console.error('[InsightUI] WebSocket Fehler:', err);
      };
    });
  }
};

document.addEventListener('DOMContentLoaded', InsightUI.WebSocketComponent.init);
