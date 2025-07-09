# Alert-Komponente

Die Alert-Komponente bietet eine barrierefreie Möglichkeit, Benutzern wichtige Informationen, Warnungen oder Erfolgsmeldungen anzuzeigen.

## Funktionen

- Vier verschiedene Typen: Info, Erfolg, Warnung und Fehler
- Optionale Schließen-Schaltfläche
- Unterstützung für zusätzliche Details
- ARIA-Attribute für Screenreader
- Animiertes Ausblenden beim Schließen

## Verwendung

```django
{% load insight_tags %}

{% alert 
   message="Ihre Änderungen wurden gespeichert." 
   type="success" 
   dismissible=True 
%}
```

## Parameter

| Parameter | Typ | Standard | Beschreibung |
|-----------|-----|----------|--------------|
| `message` | `str` | - | Die Hauptnachricht der Benachrichtigung |
| `type` | `str` | `"info"` | Der Typ der Benachrichtigung (`"info"`, `"success"`, `"warning"`, `"error"`) |
| `dismissible` | `bool` | `True` | Ob die Benachrichtigung schließbar sein soll |
| `details` | `str` | `None` | Zusätzliche Details zur Hauptnachricht |
| `id` | `str` | `None` | Eine optionale ID für das Alert-Element |

## Beispiele

### Info-Alert

```django
{% alert message="Bitte beachten Sie die neuen Datenschutzrichtlinien." %}
```

### Erfolgs-Alert

```django
{% alert 
   message="Ihr Konto wurde erfolgreich erstellt." 
   type="success" 
%}
```

### Warnungs-Alert

```django
{% alert 
   message="Ihre Sitzung läuft in 5 Minuten ab." 
   type="warning" 
%}
```

### Fehler-Alert

```django
{% alert 
   message="Es ist ein Fehler aufgetreten." 
   type="error" 
   details="Bitte versuchen Sie es später erneut oder kontaktieren Sie den Support." 
%}
```

### Nicht schließbares Alert

```django
{% alert 
   message="Diese Nachricht ist wichtig und kann nicht geschlossen werden." 
   type="info" 
   dismissible=False 
%}
```

## JavaScript-Integration

Die Alert-Komponente kann mit JavaScript geschlossen werden:

```javascript
// Schließen eines Alerts
document.querySelector('[data-insight-dismiss="alert"]').click();

// Oder mit der InsightUI-API
const alert = document.querySelector('.insight-alert');
InsightUI.Alert.close(alert);
```

## Barrierefreiheit

Die Alert-Komponente enthält:

- `role="alert"` für Screenreader
- Fokusmanagement beim Schließen
- Semantisches HTML
- Ausreichender Farbkontrast für alle Themenvarianten
