import json
from django.core.cache import cache
import requests
from pathlib import Path



class BdDistrictService:

    def get_district(self):
        BASE_DIR = Path(__file__).resolve().parent
        file_path = BASE_DIR / 'bd_districts.json'
        with open(file_path,'r',encoding='utf-8') as file:
            districts = json.load(file)
            return districts.get("districts")
        
    def get_temp_url(self,lat,long):
        return f'https://api.open-meteo.com/v1/forecast'
    
    def get_air_url(self,lat,long):
        return f'https://air-quality-api.open-meteo.com/v1/air-quality'
    
    def location_info(self,location):
        location_dict = {}
        for district in self.get_district():
            location_dict[district['name']] = (district['lat'],district['long'])

        return location_dict[location]
    


class WeatherService:
    def __init__(self):
        self.district_service = BdDistrictService()
        self.district_list = self.district_service.get_district()

    
    def fetch_weather(self,lat,long,date=None):
        cache_key = f"weather_{lat}_{long}_{date or '7_days'}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        API_URL = self.district_service.get_temp_url(lat,long)

        params = {
            "latitude": lat,
            "longitude": long,
            "hourly": "temperature_2m",
            "timezone": "auto"
        }
        if date:
            params["start_date"] = date
            params["end_date"] = date
        else:
            params["forecast_days"] = 7


        response = requests.get(API_URL,params=params,timeout=15)


        print(response)

        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=60 * 60)
            return data
        
        return None
    
    def fetch_air(self,lat,long):
        cache_key = f"air_{lat}_{long}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        API_URL = self.district_service.get_air_url(lat,long)
        params = {
            "latitude": lat,
            "longitude": long,
            "hourly": "pm2_5",
            "timezone": "auto"
        }

        response = requests.get(API_URL,params=params,timeout=15)


        if response.status_code == 200:
            data = response.json()
            cache.set(cache_key, data, timeout=60 * 60)
            return data
        
        return None
        

    def calculate_average_temperature(self, weather_data, one_day=False):
        hourly_temps = weather_data["hourly"]["temperature_2m"]
        two_pm_temps = hourly_temps[14::24]
        if one_day:
            return two_pm_temps[0]
        return sum(two_pm_temps) / len(two_pm_temps)
    
    def calculate_average_pm25(self, air_data):
        times = air_data["hourly"]["time"]
        pm_values = air_data["hourly"]["pm2_5"]
        two_pm_pm25 = [
        pm for time, pm in zip(times, pm_values) if "T14:00" in time
    ]
        return sum(pm_values) / len(pm_values)
    
    def get_coolest_districts(self):
        district_temps = []
        for district in self.district_list:
            weather = self.fetch_weather(district["lat"], district["long"])
            air = self.fetch_air(district["lat"], district["long"])
            if not weather or not air:
                continue
            avg_temp = self.calculate_average_temperature(weather)
            avg_pm25 = self.calculate_average_pm25(air)

            district_temps.append({
                "district": district["name"],
                "avg_temp": avg_temp,
                "avg_pm25": avg_pm25
            })

        district_temps.sort(key=lambda x: (x["avg_temp"], x["avg_pm25"]))
        return district_temps[:10]
    

    def temp_difference(self, location, destination, date):
        start_lat, start_long = self.district_service.location_info(location) 
        dest_lat, dest_long = self.district_service.location_info(destination)
        start = self.fetch_weather(start_lat, start_long, date)
        dest = self.fetch_weather(dest_lat, dest_long, date)
        start_res = self.calculate_average(start, one_day=True)
        dest_res = self.calculate_average(dest, one_day=True)
        return {f"{location}'s temperature": start_res, f"{destination} temperature": dest_res}