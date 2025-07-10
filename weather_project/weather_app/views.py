from django.shortcuts import render
from weather_app.services import WeatherService
from django.http import JsonResponse
from weather_app.tasks import fetch_and_cache_weather_air


def coolest_places(request):
    res = WeatherService().get_coolest_districts()
    return JsonResponse(res, safe=False)

def temperature_info(request):
    location = request.GET.get('location')
    destination = request.GET.get('destination') 
    date = request.GET.get('date')
    res = WeatherService().temp_difference(location, destination, date)
    return JsonResponse(res, safe=False)


fetch_and_cache_weather_air()