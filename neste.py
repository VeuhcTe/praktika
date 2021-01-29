import requests
import pandas
from bs4 import BeautifulSoup
import json
import geojson
import re

URL = "https://neste.ru/ru/yandex"

def get_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    
    time = soup.findAll("div", {"class":"c-station-search__list__item__title"})
    name_station = []
    for t in time:
        name_station.append(t.get_text())

    time = soup.findAll("div", {"class":"c-station-search__list__item__address"})
    address_station = []
    for t in time:
        address_station.append(t.get_text().replace("\n      ",""))

    time = soup.findAll("span", {"class":"mdi mdi-chevron-down js-station-info-arrow c-station-search__icon--toggle"}) 
    id_station = []
    for t in time:
        id_station.append(t["data-load"])
    
    time = soup.findAll("div", {"class":"l-grid__item contact-info"})
    phone_station = []
    for t in time:
        mas = t.findAll("div")
        phone_station.append(mas[1].get_text().replace("Тел: ", ""))

    time = soup.findAll("div", {"class":"p-systems"})
    p_systems = []
    for t in time:
        p_systems.append(t.get_text().replace("Электронные платежные системы:\n","").replace("\n", "").replace("        ","").replace("      ",""))

    time = soup.findAll("div", {"class":"prod"})
    prod = []
    for t in time:
        prod.append(t.get_text().replace("Тип топлива:\n", "").replace("\t\t\t\t","").replace("\n    \t","").replace("        ", ""))

    i = 0
    while i < len(name_station):
        result = {
            "name_station":name_station[i],
            "address_station":address_station[i],
            "id_station":id_station[i],
            "phone_station":phone_station[i],
            "p_systems":p_systems[i],
            "prod":prod[i]
        }
        i += 1
        yield result

def get_coords():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    scripts = soup.findAll("script")
    for script in scripts:
        script_content = script.string
        if script_content is not None and "features" in script_content:
            match = re.search(r"features\":\[(.+)\}\}\]", str(script_content))
            data = json.loads(match.group(0).split('res\":')[1])
            return data

def save_data(data=None):
    if data is None:
        return False

    with open('neste.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True


def main ():
    data = []
    for g in get_data():
        data.append(g)

    coords = get_coords()

    for d in data:
        for c in coords:
            if c["feature_id"] == d["id_station"]:
                d["lat"] = c["lat"]
                d["lon"] = c["lon"]
    
    save_data(data)

if __name__ == '__main__':
    main()