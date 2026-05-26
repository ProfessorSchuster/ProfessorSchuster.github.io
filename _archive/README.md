# Archiv für automatisches Preis Scrapping in Troostwiijk

## Was war das?

Ein automatisierter Preis-Scraper für eine Troostwiijk-Auktion (unterirdischer Militärbunker in Colpin, Mecklenburg-Vorpommern). Der aktuelle Gebotspreis wurde stündlich via GitHub Actions aus der Auktionsseite gescrapt und in `index.html` geschrieben.

## Wie es funktionierte

```
GitHub Actions (update.yml, stündlich)
  → Docker-Container starten (ghcr.io/professorschuster/...)
    → update_price.py ausführen
      → Selenium öffnet Auktions-URL
        → Preis aus data-cy="item-bid-current-bid-text" lesen
          → preis.template.html befüllen → index.html schreiben
            → git commit & push
```

## Dateien hier

| Datei | Beschreibung |
|-------|-------------|
| `update_price.py` | Selenium-Scraper, liest Gebotspreis von Troostwiijk |
| `preis.template.html` | HTML-Template mit `{{PREIS}}` und `{{TIME}}` Platzhaltern |
| `requirements.txt` | Python-Dependencies (selenium, pytz, etc.) |
| `Dockerfile` | Lokales Docker-Image (Chromium + Python) |
| `Dockerfile.build` | Build-Image für GHCR (mit git, ohne COPY) |
| `github-workflows/build-image.yml` | GitHub Action: Docker-Image bauen & zu GHCR pushen |
| `github-workflows/update.yml` | GitHub Action: stündlich Preis updaten & committen |

## GitHub Actions

Die Workflows lagen unter `.github/workflows/`. Kopien zur Referenz liegen in `github-workflows/`.

### update.yml — Stündlicher Preis-Update
- Trigger: Push auf main, stündlich (`5 * * * *`), manuell
- Pulled das Docker-Image aus GHCR
- Führt `update_price.py` aus
- Committet `index.html` automatisch

### build-image.yml — Docker-Image bauen
- Trigger: Push auf main, manuell
- Baut Multi-Arch-Image (QEMU)
- Pushed zu `ghcr.io/professorschuster/professorschuster.github.io:latest`
