#https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=1&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private
#https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=2&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private

import requests
from bs4 import BeautifulSoup

URL = "https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=1&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
cards = soup.find_all("div", {"data-cy": "l-card"})

print(cards)

for card in cards:
    print(card.find("h6", {"class":"css-16v5mdi er34gjf0"}).text)
    print(card.find("p", {"data-testid":"ad-price"}).text)
    print(card.find("p", {"data-testid":"location-date"}).text)
    print(card.find("span", {"class":"css-643j0o"}).text)
    print("\n")
