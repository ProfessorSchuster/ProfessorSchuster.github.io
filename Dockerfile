# Basis-Image: Leichtes Python-Image
FROM python:3.10-slim

# 1) Systemabhängige Abhängigkeiten installieren
#    Wir brauchen chromium und chromedriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        chromium chromium-driver \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2) Arbeitsverzeichnis festlegen
WORKDIR /app

# 3) Requirements und Source Code kopieren
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# 4) CHROME_BINARY-Umgebungsvariable (damit dein Skript den Pfad erkennt)
ENV CHROME_BINARY=/usr/bin/chromium

# 5) Standard-Kommando: Starte dein Skript
CMD ["python", "update_price.py"]