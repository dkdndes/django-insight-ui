/**
 * Insight UI WebSocket Handler mit detailliertem Logging
 */
window.InsightUI = window.InsightUI || {};

InsightUI.WebSocket = {
  init: function() {
    console.log('🔌 InsightUI.WebSocket.init() - Starte WebSocket Handler Initialisierung');
    
    // Prüfe ob HTMX verfügbar ist
    if (typeof htmx === 'undefined') {
      console.error('❌ HTMX nicht gefunden - WebSocket Handler kann nicht initialisiert werden');
      return;
    }
    console.log('✅ HTMX gefunden, Version:', htmx.version || 'unbekannt');

    // Detaillierte Extension-Prüfung
    console.log('🔍 HTMX Config:', htmx.config);
    console.log('🔍 HTMX Extensions:', htmx.config.extensions);
    
    // Prüfe ob WebSocket Extension geladen ist
    const hasWsExtension = htmx.config.extensions && htmx.config.extensions.includes('ws');
    if (!hasWsExtension) {
      console.error('❌ HTMX WebSocket Extension NICHT geladen!');
      console.log('💡 Stelle sicher, dass ws.js geladen ist');
    } else {
      console.log('✅ HTMX WebSocket Extension erkannt');
    }

    // Prüfe ob WebSocket im Browser verfügbar ist
    if (typeof WebSocket === 'undefined') {
      console.error('❌ WebSocket API nicht verfügbar im Browser');
      return;
    }
    console.log('✅ WebSocket API verfügbar');

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
        statusElement.className = 'text-green-600 dark:text-green-400';
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
        statusElement.className = 'text-red-600 dark:text-red-400';
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
        statusElement.className = 'text-red-600 dark:text-red-400';
        console.log('✅ Status-Element aktualisiert: Verbindungsfehler');
      }
    });

    // WebSocket Nachricht empfangen
    document.body.addEventListener('htmx:wsAfterMessage', function(evt) {
      console.log('📨 WebSocket Nachricht empfangen:', {
        target: evt.target.id || 'unbekannt',
        messageLength: evt.detail?.message?.length || 0,
        message: evt.detail?.message || 'keine Nachricht',
        timestamp: new Date().toISOString()
      });
      
      // Verarbeite die JSON-Nachricht und zeige sie im Output-Element an
      try {
        const wsElement = evt.target;
        const outputElement = wsElement.querySelector('[id$="-output"]');
        if (outputElement && evt.detail?.message) {
          const data = JSON.parse(evt.detail.message);
          const formattedData = `
            <div class="mb-2 p-2 border-l-4 border-blue-500">
              <div class="text-xs text-gray-500">${new Date().toLocaleTimeString()}</div>
              <div class="font-semibold">Connection: ${data.connection_id?.substring(0, 8) || 'unknown'}</div>
              <div class="text-sm">
                <div>Disk: ${data.content?.disk?.used_gb || 0}GB / ${data.content?.disk?.total_gb || 0}GB</div>
                <div>Memory: ${data.content?.memory?.percent_used || 0}% used</div>
                <div>Client: ${data.client_info?.ip || 'unknown'}</div>
              </div>
            </div>
          `;
          outputElement.innerHTML = formattedData + outputElement.innerHTML;
          
          // Begrenze die Anzahl der angezeigten Nachrichten
          const messages = outputElement.querySelectorAll('div.mb-2');
          if (messages.length > 10) {
            messages[messages.length - 1].remove();
          }
        }
      } catch (error) {
        console.error('❌ Fehler beim Verarbeiten der WebSocket-Nachricht:', error);
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
        statusElement.className = 'text-yellow-600 dark:text-yellow-400';
      }
    });

    // Zähle vorhandene WebSocket-Komponenten
    const wsComponents = document.querySelectorAll('[hx-ext*="ws"]');
    console.log(`📊 ${wsComponents.length} WebSocket-Komponente(n) auf der Seite gefunden:`);
    
    wsComponents.forEach((component, index) => {
      const id = component.id || `ws-component-${index}`;
      const wsUrl = component.getAttribute('ws-connect') || 'nicht gesetzt';
      console.log(`  ${index + 1}. ID: ${id}, URL: ${wsUrl}`);
    });

    console.log('✅ InsightUI WebSocket Handler erfolgreich initialisiert');
  }
};
