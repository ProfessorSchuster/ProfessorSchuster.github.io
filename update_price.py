import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://www.troostwijkauctions.com/de/l/500-m%C2%B2-unterirdischer-militarbunker-mit-gebauden-und-richtbalkenturm-auf-einem-gesamtgrundstuck-von-16-500-m%C2%B2-in-colpin-mechlenburg-vorpommern-deutschland-A1-32543-1"

def extract_price():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Falls du den Browser-Fenster-Size anpassen willst:
    # chrome_options.add_argument('--window-size=1280,720')

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    # Kurz warten, bis JS den Preis gerendert hat (manchmal braucht es 1-2 Sekunden)
    time.sleep(3)

    # price_element = driver.find_element("css selector", '[data-cy="item-bid-current-bid-text"]')
    # Manche Seiten haben mehrere Selektoren oder brauchen XPATH:
    # price_element = driver.find_element("xpath", '//span[@data-cy="item-bid-current-bid-text"]')

    # Versuchen wir erst mit CSS:
    try:
        price_element = driver.find_element("css selector", '[data-cy="item-bid-current-bid-text"]')
        preis = price_element.text.strip()
    except:
        preis = "n/a"

    driver.quit()
    return preis

def render_html(price):
    with open("index.template.html", "r", encoding="utf-8") as f:
        template = f.read()
    output = template.replace("{{PREIS}}", price)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    preis = extract_price()
    print("Gefundener Preis:", preis)
    render_html(preis)
