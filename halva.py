import requests
import geojson

# Базовый URL получения данных
URL ="https://pochtomat.ru/terminals/"

# Функция извлечения данных
def get_data (url=None):
    if url is None:
        return False
    
    response = requests.get(URL)

    if response.status_code is 200:
        print("Data successfully extracted")
        return response.json()
    else:
        print("Error while extracting data")
        return False


def save_data (data=None):
    if data is None:
        return False

    with open('halva_terminals_2.geojson', 'w', encoding='utf-8') as file:
        geojson.dump(data, file, ensure_ascii=False, indent=4)
        return True
    
def sort_data(pochtomat):
    g={
        "name": pochtomat["name"],
        "lat": pochtomat["point"]["coordinates"][0],
        "lon": pochtomat["point"]["coordinates"][1],
        "full_addr": None,
        "location": pochtomat["location"],
        "operation_time": pochtomat["operation_time"]
    }
    try:
        g["full_addr"] = pochtomat["structured_address"]["full_addr"]
    except KeyError:
        g["full_addr"] = "Адреса нет"

    return g

if __name__ == "__main__":
    result = get_data(url=URL)

    data = []
    i = 0
    for d in result["content"]:
        data.append(sort_data(d))


    if data:
        result = save_data(data)
        if result:
            print("Data successfully saved")
        else:
            print("Error while saving data")