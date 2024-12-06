import asyncio
from datetime import datetime, timedelta
from math import asin, cos, pi, sqrt

import aiohttp
from geopy.adapters import AioHTTPAdapter
from geopy.exc import GeopyError
from geopy.geocoders import Nominatim
from quart import Quart, render_template

app = Quart(__name__)

EARTH_RADIUS_KM = 6371

NOMINATIM_QUERY_DAILY_LIMIT = 1000
NOMINATIM_QUERY_DELAY_SEC = 1

OWP_URL = "https://api.openweathermap.org/data/2.5/weather"
OWM_KEY = ""
OWM_QUERY_DAILY_LIMIT = 1000
OWM_QUERY_DELAY_SEC = 10 * 60

MS_URL = "https://www.meteosource.com/api/v1/free/point"
MS_KEY = ""
MS_QUERY_DAILY_LIMIT = 400

TOMORROW_URL = "https://api.tomorrow.io/v4/weather/realtime"
TOMORROW_KEY = ""


items = ["item1", "item2", "item3"]
cache_data = {}


def _calculate_distance(lat1, lon1, lat2, lon2):
    radians_conversion_factor = pi / 180
    delta_latitude = (lat2 - lat1) * radians_conversion_factor
    delta_longitude = (lon2 - lon1) * radians_conversion_factor
    a = (
        0.5
        - cos(delta_latitude) / 2
        + cos(lat1 * radians_conversion_factor)
        * cos(lat2 * radians_conversion_factor)
        * (1 - cos(delta_longitude))
        / 2
    )
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


async def get_weather_data(url, marker):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        # print(url)
        # https://api.tomorrow.io/v4/weather/realtime?location=62.6233627,29.8532559
        # &apikey=PaIgj3qegRij7yCYtZZbwtX5j4VEPDOH
        return data, marker
    except Exception as e:
        return None, marker, e


async def get_location_data(address):
    try:
        async with Nominatim(
            user_agent="prognozo",
            adapter_factory=AioHTTPAdapter,
        ) as geolocator:
            location = await geolocator.geocode(address)
        return location
    except GeopyError as e:
        print(f"GeopyError: {e}.")
        return None


#     # https://api.tomorrow.io/v4/weather/realtime?location=62.6233627,29.8532559
#     # &apikey=PaIgj3qegRij7yCYtZZbwtX5j4VEPDOH

#     # https://www.meteosource.com/api/v1/free/point?lat=62.622372199255025&lon=
#     # 29.85485936115007&sections=all&language=en&units=metric&key=
#     # wxh7mkis3yql84awncklb3kcjtx91dpa32m2z5mj

#     # https://api.openweathermap.org/data/2.5/weather?lat=62.622372199255025&lon
#     # =29.85485936115007&units=metric&language=en&appid=
#     # 7a6e967bac122839d69aef8a8ebc1290


@app.route("/")
async def index():
    now_ts = datetime.now()
    if "nominatim_lookup_ts" not in cache_data:
        cache_data["nominatim_lookup_ts"] = now_ts

    if now_ts - cache_data["nominatim_lookup_ts"] <= timedelta(
            seconds=NOMINATIM_QUERY_DELAY_SEC):
        return await render_template("index.html", loc_data=cache_data)

    # Commas in the loc are optional, but improve performance
    loc = await get_location_data("Hyttitie 2, Joensuu, 80170, Finland")

    # Otherwse, use a structured form of the search query:
    # allows to lookup up an address that is already split into its components.
    # Each parameter represents a field of the address. All parameters are
    # optional. You should only use the ones that are relevant for the address
    # you want to geocode:

    # amenity 	    name and/or type of POI
    # street 	    housenumber and streetname
    # city 	        city
    # county 	    county
    # state 	    state
    # country 	    country
    # postalcode 	postal code

    loc_data = {
        "address": loc.address,
        "lat": loc.latitude,
        "lon": loc.longitude,
        "lookup_ts": datetime.now(),
    }

    if loc.address in cache_data:
        dist = _calculate_distance(
            loc.latitude,
            loc.longitude,
            cache_data[loc.address]["lat"],
            cache_data[loc.address]["lon"],
        )
        print(f"You're {dist} km away from a prev cached loc.")
        loc_data = cache_data[loc.address]["weather_data"]
    else:
        print("Caching this address for this session...")
        cache_data[loc.address] = loc_data
        url1 = f"{TOMORROW_URL}?location={loc.latitude},{loc.longitude}&apikey={TOMORROW_KEY}"
        url2 = (
            f"{MS_URL}?lat={loc.latitude}&lon={loc.longitude}&sections=all&language"
            f"=en&units=metric&key={MS_KEY}"
        )
        url3 = (
            f"{OWP_URL}?lat={loc.latitude}&lon={loc.longitude}&"
            f"units=metric&language=en&appid={OWM_KEY}"
        )
        tasks = [
            get_weather_data(url1, "Tomorrow.io"),
            get_weather_data(url2, "MeteoSource"),
            get_weather_data(url3, "OpenWeatherMap"),
        ]
        loc_data = await asyncio.gather(*tasks)
        cache_data[loc.address]["weather_data"] = loc_data
    return await render_template("index.html", loc_data=loc_data)


@app.route("/item/<int:item_id>")
async def item(item_id):
    return f"Item {item_id}: {items[item_id-1]}"


if __name__ == "__main__":
    app.run()
