from fastapi import FastAPI
import requests
from datetime import datetime, timedelta
import folium


def wikipedia_articles(lat, lon):
    url = "https://pl.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{lat}|{lon}",
        "gsradius": 200,
        "gslimit": 5,
        "format": "json"
    }
    headers = {
        "User-Agent": "MyTramApp/1.0"
    }
    data = requests.get(url, params=params, headers=headers).json()

    for record in data["query"]["geosearch"]:
        print(record["title"], record["dist"])


# app = FastAPI()


API_KEY = "7c2ca341-19e7-4660-a65b-6cc806fc56e5"
url = "https://api.um.warszawa.pl/api/action/busestrams_get"
params = {
    "resource_id": "f2e5503e927d-4ad3-9500-4ab9e55deb59",
    "apikey": API_KEY,
    "type": 2
}

# data = requests.get(url, params=params).json()
# now = datetime.now()
# limit = timedelta(minutes=2)
# m = folium.Map(location=[52.23, 21.01], zoom_start=12, tiles="CartoDB Positron")
# line = 19

# for record in data["result"]:
#     t = datetime.strptime(record["Time"], "%Y-%m-%d %H:%M:%S")
#     if now - t < limit and record["Lines"] == str(line):
#         folium.Marker(
#             [record["Lat"], record["Lon"]],
#             popup="Rynek Główny w Krakowie"
#         ).add_to(m)

#         print(record["Lines"], record["Lat"], record["Lon"])
#         wikipedia_articles(50.0647, 19.9450)
#         # break

# m.save("lab2/map.html")


url_trams = "https://ttss.mpk.krakow.pl/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles"
params = {
    "positionType": "CORRECTED"
}
response = requests.get(url_trams, params=params, verify=False).json()
counter = 0

for record in response["vehicles"]:
    if not record.get("isDeleted", False):
        print(record)
        break
