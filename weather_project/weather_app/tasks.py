from background_task import background
from weather_app.services import WeatherService


@background(schedule=60*60)
def fetch_and_cache_weather_air():
    service = WeatherService()
    for district in service.district_list:
        lat = district["lat"]
        long = district["long"]
        service.fetch_weather(lat, long)
        service.fetch_air(lat,long)