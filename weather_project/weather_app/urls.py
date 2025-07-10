from django.urls import path
from . import views

urlpatterns = [
    path('coolest_places/', views.coolest_places, name='coolest_places'),
    path('temperature_info/', views.temperature_info, name='temperature_info'),
]