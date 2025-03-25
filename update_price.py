import os
import time
from datetime import datetime
import pytz  # Stelle sicher, dass in requirements.txt "pytz" enthalten ist
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Pfad zur Chrome-Binary (aus der ENV oder fallback)
chrome_binary = os.environ.get("CHROME_BINARY", "/usr/bin/google-chrome")

def extract_price():
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=chrome_options
    )
    URL = "https://www.troostwijkauctions.com/de/l/500-m%C2%B2-unterirdischer-militarbunker-mit-gebauden-und-richtbalkenturm-auf-einem-gesamtgrundstuck-von-16-500-m%C2%B2-in-colpin-mechlenburg-vorpommern-deutschland-A1-32543-1"
    driver.get(URL)

    time.sleep(3)  # Kurz warten bis alles geladen ist

    try:
        price_element = driver.find_element("css selector", '[data-cy="item-bid-current-bid-text"]')
        preis = price_element.text.strip()
    except Exception as e:
        print("Fehler beim Finden des Preis-Elements:", e)
        preis = "n/a"

    driver.quit()
    return preis

def render_html(price, local_time_str):
    # Template laden
    with open("preis.template.html", "r", encoding="utf-8") as f:
        template = f.read()
    
    # Platzhalter ersetzen
    output = template.replace("{{PREIS}}", price)
    output = output.replace("{{TIME}}", local_time_str)

    # Ergebnis in index.html schreiben
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    preis = extract_price()
    print("Gefundener Preis:", preis)

    # Berliner Zeit ausgeben (z.B. als HH:MM)
    berlin = pytz.timezone("Europe/Berlin")
    now_berlin = datetime.now(berlin)
    # Format beliebig anpassbar, z.B. 24h mit Sekunden: '%Y-%m-%d %H:%M:%S'
    local_time_str = now_berlin.strftime('%H:%M:%S')

    render_html(preis, local_time_str)
    print("Aktualisiert um:", local_time_str, "Uhr (Berliner Zeit)")
