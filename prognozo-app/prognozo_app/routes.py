# import aiohttp
# # from flask import render_template
# from geopy.adapters import AioHTTPAdapter
# from geopy.geocoders import Nominatim
# import asyncio
#
# from prognozo_app import app
#
#
# OWP_URL = "https://api.openweathermap.org/data/2.5/weather"
# OWM_KEY = "7a6e967bac122839d69aef8a8ebc1290"
# OWM_QUERY_DAILY_LIMIT = 1000
# OWM_QUERY_DELAY_SEC = 10 * 60
#
# MS_URL = "https://www.meteosource.com/api/v1/free/point"
# MS_KEY = "wxh7mkis3yql84awncklb3kcjtx91dpa32m2z5mj"
# MS_QUERY_DAILY_LIMIT = 400
#
# TOMORROW_URL = "https://api.tomorrow.io/v4/weather/realtime"
# TOMORROW_KEY = "PaIgj3qegRij7yCYtZZbwtX5j4VEPDOH"
#
#
# async def get_location_data(address):
#     async with Nominatim(
#             user_agent="prognozo",
#             adapter_factory=AioHTTPAdapter,
#     ) as geolocator:
#         location = await geolocator.geocode(address)
#     return location
#
#
# # async def get_location_data(address):
# #     async with Nominatim(
# #         user_agent="prognozo",
# #         adapter_factory=AioHTTPAdapter,
# #     ) as geolocator:
# #         location = await geolocator.geocode(address)
# #     return location
# #
# #
# async def get_tomorrowio_weather(loc):
#     print("Starting get_tomorrowio_weather...")
#     url = (
#         f"{TOMORROW_URL}?location={loc.latitude},{loc.longitude}&apikey={TOMORROW_KEY}"
#     )
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.json()
#     # print(url)
#     # https://api.tomorrow.io/v4/weather/realtime?location=62.6233627,29.8532559
#     # &apikey=PaIgj3qegRij7yCYtZZbwtX5j4VEPDOH
#     print("Returning from get_tomorrowio_weather.")
#     return data
#
# #
# async def get_meteosource_weather(loc):
#     print("Starting get_meteosource_weather...")
#     url = (
#         f"{MS_URL}?lat={loc.latitude}&lon={loc.longitude}&sections=all&language"
#         f"=en&units=metric&key={MS_KEY}"
#     )
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             data = await response.json()
#     # print(url)
#     # https://www.meteosource.com/api/v1/free/point?lat=62.622372199255025&lon=
#     # 29.85485936115007&sections=all&language=en&units=metric&key=
#     # wxh7mkis3yql84awncklb3kcjtx91dpa32m2z5mj
#     print("Returning from get_meteosource_weather.")
#     return data
# #
# #
# # async def get_openweathermap_weather(loc):
# #     # Call once in 10 min
# #     print("Starting get_openweathermap_weather...")
# #     url = (
# #         f"{OWP_URL}?lat={loc.latitude}&lon={loc.longitude}&"
# #         f"units=metric&language=en&appid={OWM_KEY}"
# #     )
# #     async with aiohttp.ClientSession() as session:
# #         async with session.get(url) as response:
# #             data = await response.json()
# #     # print(url)
# #     # https://api.openweathermap.org/data/2.5/weather?lat=62.622372199255025&lon
# #     # =29.85485936115007&units=metric&language=en&appid=
# #     # 7a6e967bac122839d69aef8a8ebc1290
# #     print("Returning from get_openweathermap_weather.")
# #     return data
# #
#
# @app.route("/")
# @app.route("/index")
# async def index():
#     # 62.62281744793608, 29.856473082228792 => Hyttitie 2 as per GoogleMaps
#     loc = await get_location_data("Hyttitie 2 Joensuu 80170 Finland")
#
#     # loop = asyncio.get_event_loop()
#     # results = loop.create_task(
#     #     get_meteosource_weather(loc)
#     # )
#     print(loc)
#
#     # owm_weather = await get_openweathermap_weather(loc)
#     # ms_weather = await get_meteosource_weather(loc)
#     # tomorrowio_weather = await get_tomorrowio_weather(loc)
#     #
#     # loc_data = {
#     #     "address": loc.address,
#     #     "lat": loc.latitude,
#     #     "lon": loc.longitude,
#     #     "raw": loc.raw,
#     # }
#
#     # user = {"username": "User"}
#     # reports = [
#     #     {
#     #         "author": {"username": "John"},
#     #         "body": "OpenWeather reports good on my loc in <this> country",
#     #     },
#     #     {
#     #         "author": {"username": "Susan"},
#     #         "body": "MeteoSource reports bad on my loc in <this> country",
#     #     },
#     # ]
#     # return render_template(
#     #     "index.html",
#     #     title="Home",
#     #     user=user,
#     #     reports=reports,
#     #     # `loc_data=loc_data`,
#     #     # weather_data=[owm_weather, ms_weather, tomorrowio_weather],
#     # )
#     return loc
