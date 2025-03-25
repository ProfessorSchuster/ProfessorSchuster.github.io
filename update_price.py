import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Pfad zur Chrome-Binary in GitHub Actions
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

    time.sleep(3)  # kurz warten bis alles geladen ist

    try:
        price_element = driver.find_element("css selector", '[data-cy="item-bid-current-bid-text"]')
        preis = price_element.text.strip()
    except Exception as e:
        print("Fehler beim Finden des Preis-Elements:", e)
        preis = "n/a"

    driver.quit()
    return preis

def render_html(price):
    with open("preis.template.html", "r", encoding="utf-8") as f:
        template = f.read()
    output = template.replace("{{PREIS}}", price)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    preis = extract_price()
    print("Gefundener Preis:", preis)
    render_html(preis)
