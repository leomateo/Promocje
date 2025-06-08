import requests
from bs4 import BeautifulSoup
import schedule
import time

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1364543953931599963/P5QFfgzTRBO-kZG7ufRaoaLMndk2jY_YaXTJn_LrFuVPWTho2C7PmuALSscMxGpkPQny"

frazy_promocyjne = ["1+1", "gratis", "drugi za", "2 w cenie", "promocja"]

def wyslij_powiadomienie(tresc):
    data = {"content": tresc}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def zawiera_promocje(text):
    return any(fraza in text.lower() for fraza in frazy_promocyjne)

def szukaj_rossmann():
    url = "https://www.rossmann.pl/szukaj?q=old+spice"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    produkty = soup.select(".productTile__productName")
    znalezione = []

    for produkt in produkty:
        nazwa = produkt.text.strip()
        if zawiera_promocje(nazwa):
            znalezione.append(f"Rossmann: {nazwa}")

    return znalezione

def szukaj_hebe():
    url = "https://www.hebe.pl/catalogsearch/result/?q=old+spice"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    produkty = soup.select(".product-item-link")
    znalezione = []

    for produkt in produkty:
        nazwa = produkt.text.strip()
        if zawiera_promocje(nazwa):
            znalezione.append(f"Hebe: {nazwa}")

    return znalezione

def szukaj_superpharm():
    url = "https://www.superpharm.pl/catalogsearch/result/?q=old+spice"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    produkty = soup.select(".product.name.product-item-name a")
    znalezione = []

    for produkt in produkty:
        nazwa = produkt.text.strip()
        if zawiera_promocje(nazwa):
            znalezione.append(f"Super-Pharm: {nazwa}")

    return znalezione

def szukaj_allegro():
    url = "https://allegro.pl/listing?string=old%20spice&order=m"
    headers = {"User-Agent": "Mozilla/5.0"}
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
    produkty = soup.select("h2._9c44d_1zemI")
    znalezione = []

    for produkt in produkty:
        nazwa = produkt.text.strip()
        if zawiera_promocje(nazwa):
            znalezione.append(f"Allegro: {nazwa}")

    return znalezione

def przeszukaj_sklepy():
    wszystkie_promocje = []
    wszystkie_promocje += szukaj_rossmann()
    wszystkie_promocje += szukaj_hebe()
    wszystkie_promocje += szukaj_superpharm()
    wszystkie_promocje += szukaj_allegro()

    if wszystkie_promocje:
        for promo in wszystkie_promocje:
            wyslij_powiadomienie(promo)
    else:
        wyslij_powiadomienie("Nie znaleziono nowych promocji Old Spice.")

# Harmonogram - codziennie o 9:00
schedule.every().day.at("09:00").do(przeszukaj_sklepy)

if __name__ == "__main__":
    print("Bot do szukania promocji uruchomiony.")
    while True:
        schedule.run_pending()
        time.sleep(60)
