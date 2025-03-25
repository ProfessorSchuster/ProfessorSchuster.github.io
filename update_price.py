import requests
from bs4 import BeautifulSoup

# Zielseite (Troostwijk)
TARGET_URL = ("https://www.troostwijkauctions.com/de/l/"
              "500-m%C2%B2-unterirdischer-militarbunker-mit-gebauden-und-richtbalkenturm-auf-einem-gesamtgrundstuck-von-16-500-m%C2%B2-in-colpin-mechlenburg-vorpommern-deutschland-A1-32543-1")

def extract_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        r = requests.get(TARGET_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        # Suche nach dem Element, in dem der Preis steht (z. B. per data-cy Attribut)
        element = soup.select_one('[data-cy="item-bid-current-bid-text"]')
        if element:
            return element.get_text(strip=True)
    except Exception as e:
        print("Fehler beim Abruf:", e)
    return "n/a"

def update_html(price):
    with open("preis.template.html", "r", encoding="utf-8") as f:
        template = f.read()
    # Ersetze den Platzhalter mit dem aktuellen Preis
    html_content = template.replace("{{PREIS}}", price)
    with open("preis.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    preis = extract_price()
    print("Aktueller Preis:", preis)
    update_html(preis)
