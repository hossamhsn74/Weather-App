from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=2b586ecf3af8047ae75a235029064809'
    cities = City.objects.all()
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'main/index.html', context)
