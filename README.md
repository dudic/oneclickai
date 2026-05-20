# OneClickAI GitHub Page

Statische GitHub-Page für OneClickAI.

## Inhalt

- `index.html` – komplette Landingpage auf Deutsch
- `style.css` – helles Design mit CSS-only Glas-/Blur-Effekten
- `screenshots/` – Screenshots der App
- `.nojekyll` – verhindert Jekyll-Verarbeitung bei GitHub Pages

## Wichtig vor dem Veröffentlichen

1. Ersetze in `index.html` beide GitHub-Links:

```html
https://github.com/
```

mit deinem echten Repository-Link.

2. Lege die Datei `OneClickAI.exe` in den Root-Ordner des Repositories, falls der Download-Button direkt funktionieren soll:

```text
repo/
├── index.html
├── style.css
├── OneClickAI.exe
└── screenshots/
```

Alternativ kannst du den Download-Link auf ein GitHub Release ändern.

## GitHub Pages aktivieren

1. Repository auf GitHub öffnen
2. `Settings` → `Pages`
3. Bei `Build and deployment` auswählen:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/root`
4. Speichern

Nach kurzer Zeit ist die Seite über GitHub Pages erreichbar.
