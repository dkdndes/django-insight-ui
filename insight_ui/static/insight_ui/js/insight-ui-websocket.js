/**
 * Insight UI WebSocket Handler mit detailliertem Logging
 */
window.InsightUI = window.InsightUI || {};

InsightUI.WebSocket = {
  init: function() {
    console.log('🔌 InsightUI.WebSocket.init() - Starte WebSocket Handler Initialisierung');
    console.log('🔍 Aktueller Zeitstempel:', new Date().toISOString());
    
    // Warte bis HTMX vollständig geladen ist
    if (typeof htmx === 'undefined') {
      console.warn('⚠️ HTMX noch nicht geladen, warte 100ms...');
      setTimeout(() => this.init(), 100);
      return;
    }
    console.log('✅ HTMX gefunden, Version:', htmx.version || 'unbekannt');
    console.log('🔍 HTMX Objekt:', htmx);

    // Detaillierte Extension-Prüfung
    console.log('🔍 HTMX Config:', htmx.config);
    console.log('🔍 HTMX Extensions:', htmx.config.extensions);
    console.log('🔍 HTMX Extensions Array:', Array.isArray(htmx.config.extensions) ? htmx.config.extensions : 'Nicht Array');
    
    // Prüfe ob WebSocket Extension geladen ist
    const hasWsExtension = htmx.config.extensions && htmx.config.extensions.includes('ws');
    console.log('🔍 WebSocket Extension Check:', hasWsExtension);
    
    if (!hasWsExtension) {
      console.error('❌ HTMX WebSocket Extension NICHT geladen!');
      console.log('💡 Stelle sicher, dass ws.js geladen ist');
      console.log('💡 Verfügbare Extensions:', htmx.config.extensions);
      console.warn('⚠️ WebSocket Extension nicht verfügbar, warte 200ms...');
      setTimeout(() => this.init(), 200);
      return;
    } else {
      console.log('✅ HTMX WebSocket Extension erkannt');
    }

    // Prüfe ob WebSocket im Browser verfügbar ist
    if (typeof WebSocket === 'undefined') {
      console.error('❌ WebSocket API nicht verfügbar im Browser');
      return;
    }
    console.log('✅ WebSocket API verfügbar');

    // Prüfe WebSocket-Komponenten auf der Seite
    const wsComponents = document.querySelectorAll('[hx-ext*="ws"]');
    console.log(`📊 ${wsComponents.length} WebSocket-Komponente(n) gefunden:`);
    
    wsComponents.forEach((component, index) => {
      const id = component.id || `ws-component-${index}`;
      const wsUrl = component.getAttribute('ws-connect') || 'nicht gesetzt';
      console.log(`  ${index + 1}. ID: ${id}, URL: ${wsUrl}`);
      console.log(`     Element:`, component);
    });

    // Test: Manueller WebSocket-Verbindungstest
    console.log('🧪 Teste direkte WebSocket-Verbindung...');
    try {
      const testWs = new WebSocket('ws://localhost:8765');
      testWs.onopen = () => {
        console.log('✅ Direkte WebSocket-Verbindung erfolgreich');
        testWs.close();
      };
      testWs.onerror = (e) => {
        console.error('❌ Direkte WebSocket-Verbindung fehlgeschlagen:', e);
      };
      testWs.onclose = (e) => {
        console.log('🔴 Test-WebSocket geschlossen, Code:', e.code, 'Reason:', e.reason);
      };
    } catch (error) {
      console.error('❌ Fehler beim Erstellen der Test-WebSocket:', error);
    }

    // WebSocket Verbindung erfolgreich geöffnet
    document.body.addEventListener('htmx:wsOpen', function(evt) {
      console.log('🟢 WebSocket Verbindung geöffnet:', {
        target: evt.target.id || 'unbekannt',
        url: evt.detail?.socketWrapper?.socket?.url || 'unbekannt',
        timestamp: new Date().toISOString()
      });
      
      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Verbunden';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--connected';
        console.log('✅ Status-Element aktualisiert: Verbunden');
      } else {
        console.warn('⚠️ Status-Element nicht gefunden für WebSocket:', wsElement.id);
      }
    });

    // WebSocket Verbindung geschlossen
    document.body.addEventListener('htmx:wsClose', function(evt) {
      console.log('🔴 WebSocket Verbindung geschlossen:', {
        target: evt.target.id || 'unbekannt',
        code: evt.detail?.code || 'unbekannt',
        reason: evt.detail?.reason || 'unbekannt',
        wasClean: evt.detail?.wasClean || false,
        timestamp: new Date().toISOString()
      });
      
      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Verbindung getrennt';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--disconnected';
        console.log('✅ Status-Element aktualisiert: Verbindung getrennt');
      }
    });

    // WebSocket Fehler
    document.body.addEventListener('htmx:wsError', function(evt) {
      console.error('❌ WebSocket Fehler:', {
        target: evt.target.id || 'unbekannt',
        error: evt.detail?.error || 'unbekannt',
        message: evt.detail?.message || 'unbekannt',
        timestamp: new Date().toISOString()
      });
      
      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Verbindungsfehler';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--error';
        console.log('✅ Status-Element aktualisiert: Verbindungsfehler');
      }
    });

    // WebSocket Nachricht empfangen - HTMX v2 WebSocket Extension
    document.body.addEventListener('htmx:wsAfterMessage', function(evt) {
      console.log('📨 WebSocket Nachricht empfangen:', {
        target: evt.target.id || 'unbekannt',
        messageLength: evt.detail?.message?.length || 0,
        message: evt.detail?.message || 'keine Nachricht',
        timestamp: new Date().toISOString()
      });
      
      // Prüfe ob die Nachricht HTML enthält (für HTMX OOB Swaps)
      if (evt.detail?.message && evt.detail.message.trim().startsWith('<')) {
        console.log('📄 HTML-Nachricht erkannt, HTMX verarbeitet automatisch');
        return; // HTMX verarbeitet HTML automatisch
      }
      
      // Verarbeite JSON-Nachrichten manuell
      try {
        const wsElement = evt.target;
        const outputElement = wsElement.querySelector('[id$="-output"]');
        if (outputElement && evt.detail?.message) {
          const data = JSON.parse(evt.detail.message);
          const formattedData = `
            <div class="mb-2 p-2 border-l-4 border-blue-500 bg-white dark:bg-gray-600 rounded">
              <div class="text-xs text-gray-500 dark:text-gray-400">${new Date().toLocaleTimeString()}</div>
              <div class="font-semibold text-blue-600 dark:text-blue-400">Connection: ${data.connection_id?.substring(0, 8) || 'unknown'}</div>
              <div class="text-sm space-y-1">
                <div>💾 Disk: ${data.content?.disk?.used_gb || 0}GB / ${data.content?.disk?.total_gb || 0}GB</div>
                <div>🧠 Memory: ${data.content?.memory?.percent_used || 0}% used</div>
                <div>🌐 Client: ${data.client_info?.ip || 'unknown'}</div>
              </div>
            </div>
          `;
          
          // Füge neue Nachricht am Anfang hinzu
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = formattedData;
          outputElement.insertBefore(tempDiv.firstElementChild, outputElement.firstElementChild);
          
          // Begrenze die Anzahl der angezeigten Nachrichten
          const messages = outputElement.querySelectorAll('div.mb-2');
          if (messages.length > 10) {
            messages[messages.length - 1].remove();
          }
        }
      } catch (error) {
        console.error('❌ Fehler beim Verarbeiten der WebSocket-Nachricht:', error);
        console.log('📝 Rohe Nachricht:', evt.detail?.message);
      }
    });

    // WebSocket Nachricht gesendet
    document.body.addEventListener('htmx:wsBeforeSend', function(evt) {
      console.log('📤 WebSocket Nachricht wird gesendet:', {
        target: evt.target.id || 'unbekannt',
        messageLength: evt.detail?.message?.length || 0,
        timestamp: new Date().toISOString()
      });
    });

    // WebSocket Reconnect Versuch
    document.body.addEventListener('htmx:wsConnecting', function(evt) {
      console.log('🔄 WebSocket Reconnect-Versuch:', {
        target: evt.target.id || 'unbekannt',
        attempt: evt.detail?.attempt || 'unbekannt',
        timestamp: new Date().toISOString()
      });
      
      const wsElement = evt.target;
      const statusElement = wsElement.querySelector('[id$="-status"]');
      if (statusElement) {
        statusElement.textContent = 'Verbindung wird wiederhergestellt...';
        statusElement.className = 'insight-websocket__status-text insight-websocket__status-text--connecting';
      }
    });

    console.log('✅ InsightUI WebSocket Handler erfolgreich initialisiert');
  }
};
