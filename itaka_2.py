import requests
import pandas
from bs4 import BeautifulSoup
import geojson
import re

URL = "http://itaka.spb.ru/offices/"

def generator(mas):
    i = 0
    while i < len(mas)/2:
        s = mas[i*2+1].split("\",\"")
        g = {
            "lat":float(s[0]),
            "lng":float(s[1]),
            "link":mas[i * 2]
        }
        i += 1
        yield g

def get_addres():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    textarea = soup.textarea.string
    s = str(textarea)
    s = s.replace("[\"","#")
    s = s.replace("\"]","#")
    s = s.replace("offices\\","#")
    s = s.replace("\",\"c","#")
    mas = s.split("#")
    del mas[0::2]
    data = list(generator(mas))
    return data

def get_data(link):
    #g = {
    #    "phone":None,
    #    "mail":None,
    #    "time_work":None,
    #    "address":None,
    #}
    response = requests.get(f'{URL}{link}')
    soup = BeautifulSoup(response.text, 'lxml')
    #g["time_work"] = soup.find("p").get_text().replace("\xa0"," ").replace("\n",", ")
    #g["phone"] = soup.find("div", {"class":"phone"}).get_text().replace(" ", "").replace("\n","")
    #g["mail"] = soup.find("div", {"class":"mail"}).get_text().replace(" ", "").replace("\n","")
    
    g = soup.find("ul", {"class":"office-timetable"}).get_text().split("Почтовый адрес:")[1].split("\n")[2]

    return g

def sbor(x, y, z):
    g = {
        "lat": y,
        "lng": z,
        "address": x
    }
    return g

def save_data(data=None):
    if data is None:
        return False

    with open('itaka_2.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True

if __name__ == "__main__":
    data = get_addres()
    
    #for d in data:
    #    print(d)
    
    i = 0
    itaka = []
    while i < len(data):
        itaka.append(get_data(data[i]["link"]))
        i += 1

    i = 0
    result = []
    while i < len(itaka):
        result.append(sbor(itaka[i], data[i]["lat"], data[i]["lng"]))
        i += 1

    save_data(result)