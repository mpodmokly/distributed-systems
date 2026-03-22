from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.exceptions import RequestValidationError
import requests
import folium


app = FastAPI()

@app.exception_handler(RequestValidationError)
def handle_validation(request: Request, exc: RequestValidationError):
    return HTMLResponse(
            content=handle_error("Invalid data format"),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

def handle_error(message):
    with open("index.html", "r", encoding="utf-8") as file:
        index_html = file.read()
    
    msg_html = f"<b style=\"color: red;\">Error: {message}</b><br>"
    return index_html.replace("<!---->", msg_html)

def wikipedia_articles(lat, lon):
    url_wikipedia = "https://pl.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "geosearch",
        "gscoord": f"{lat}|{lon}",
        "gsradius": 1000,
        "gslimit": 3,
        "format": "json"
    }
    headers = {
        "User-Agent": "MyBusApp/1.0"
    }
    try:
        response = requests.get(url_wikipedia, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        return [response.status_code, []]
    except requests.exceptions.RequestException:
        return [status.HTTP_503_SERVICE_UNAVAILABLE, []]

    data = response.json()
    places = []

    for record in data["query"]["geosearch"]:
        places.append([record["title"], record["pageid"], record["dist"]])
    
    return [response.status_code, places]

def generate_map(response, line):
    m = folium.Map(location=[50.051, 19.939], zoom_start=13, tiles="CartoDB Positron")
    counter = 0

    for record in response["vehicles"]:
        if not record.get("isDeleted", False):
            record_line = int(record["name"].split(" ")[0])
            if record_line == line:
                counter += 1
                lat = record["latitude"] / 3600000
                lon = record["longitude"] / 3600000
                wikipedia_response = wikipedia_articles(lat, lon)

                if wikipedia_response[0] != requests.codes.ok:
                    return HTMLResponse(
                        content=handle_error("Wikipedia server error"),
                        status_code=wikipedia_response[0]
                    )

                places = wikipedia_response[1]
                popup_html = ""

                for place in places:
                    popup_html += f"<a href=\"https://pl.wikipedia.org/?curid={place[1]}\""
                    popup_html += f" target=\"_blank\">{place[0]}</a> ({round(place[2])}m)"
                    popup_html += "<br>"

                icon = folium.Icon(
                    icon="location-arrow",
                    prefix="fa",
                    color="blue",
                    angle=record["heading"]
                )
                folium.Marker(
                    location=[lat, lon],
                    icon=icon,
                    popup=folium.Popup(popup_html, max_width=350)
                ).add_to(m)
    
    if counter == 0:
        return HTMLResponse(
            content=handle_error(f"Line {line} is not available"),
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return HTMLResponse(content=m.get_root().render())

@app.get("/", response_class=FileResponse)
async def home():
    return FileResponse("index.html")

@app.get("/buses", response_class=HTMLResponse)
async def buses(line: int):
    url_buses = "https://ttss.mpk.krakow.pl/"
    url_buses += "internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles"
    params = {
        "positionType": "CORRECTED"
    }
    response = requests.get(url_buses, params=params, verify=False)

    if response.status_code != requests.codes.ok:
        return HTMLResponse(
            content=handle_error("MPK server error"),
            status_code=response.status_code
        )
    
    return generate_map(response.json(), line)
