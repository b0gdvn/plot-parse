#https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=1&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private
#https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=2&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from datetime import date
import pandas as pd
import requests
import folium

def main(url):
    soup = connect(url)
    num_pages = int(page_count(soup))
    num_pages = 1 #for test purpose, only one page gathered

    for page in range(1,num_pages+1):
        parse(connect(url.replace("page=1",f"page={page}")))

def connect(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    return soup

def page_count(soup):
    return soup.find_all("li", {"data-testid":"pagination-list-item"})[-1].text #finding amount of pages by checking last page link number

def parse(soup):
    cards = soup.find_all("div", {"data-cy": "l-card"})

    card_data(cards)

def card_data(cards):
    for card in cards:
        global df
        name = card.find("h6", {"class":"css-16v5mdi er34gjf0"}).text
        price = card.find("p", {"data-testid":"ad-price"}).text.replace(' ','').replace('zł','')
        negotiable = False
        if "donegocjacji" in price:
            price = price.strip('donegocjacji')
            negotiable = True
        
        size = card.find("span", {"class":"css-643j0o"}).text.split(" - ")[0].replace(' ','').replace('m²','')
        mprice = card.find("span", {"class":"css-643j0o"}).text.split(" - ")[1].replace(' ','').replace('zł/m²','')
        location = card.find("p", {"data-testid":"location-date"}).text.split(" - ")[0]
        district = None
        coords = geolocator.geocode(location)
        lat = coords.latitude
        lon = coords.longitude
        if ", " in location:
            location = location.split(", ")[0]
            district = card.find("p", {"data-testid":"location-date"}).text.split(" - ")[0].split(", ")[1]

        dateposted = card.find("p", {"data-testid":"location-date"}).text.split(" - ")[1]
        if "Odświeżono dnia " in dateposted:
            dateposted = dateposted.strip('Odświeżono dnia ')
        elif "Dzisiaj" in dateposted:
            dateposted = date.today()

        df.loc[len(df)] = [name,price,size,mprice,location,district,lat,lon,dateposted,negotiable]

df = pd.DataFrame(columns=['Name','Price','Size','Mprice','City','District','Lat','Lon','DatePosted','Negotiable'])

geolocator = Nominatim(user_agent="my_request")

main("https://www.olx.pl/nieruchomosci/dzialki/sprzedaz/gdansk/?page=1&search%5Bdist%5D=50&search%5Bfilter_enum_type%5D%5B0%5D=dzialki-budowlane&search%5Bprivate_business%5D=private")

map = folium.Map(location=[54.36, 18.63],tiles="Stamen Toner",zoom_start=9)

fg = folium.FeatureGroup(name='Działki')

for index, coordinates in df.iterrows():
    fg.add_child(folium.Circle(location=[coordinates["Lat"],coordinates['Lon']],popup=coordinates['City'],radius=float(coordinates['Mprice'])))

map.add_child(fg)
map.save('analysis.html')