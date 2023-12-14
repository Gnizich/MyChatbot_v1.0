"""
Retrieve the current weather forecast from OpenWeatherMap.
"""
from urllib import request
import json
import datetime
from Voice_Tools3 import Get_Answer, Play_Answer # import specific function

def get_weather_forecast():
    coords={'lat': 35.5843, 'lon': -78.8000}  # default location at Cape Canaveral, FL
    try:  # retrieve forecast for specified coordinates
        api_key = '159b7ff4bdb66f153115053973059e2f'  # replace with your own OpenWeatherMap API key
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=imperial'
        data = json.load(request.urlopen(url))

        forecast = {'city': data['city']['name'],  # city name
                    'country': data['city']['country'],  # country name
                    'periods': list()}  # list to hold forecast data for future periods

        for period in data['list'][0:5]:  # populate list with next 9 forecast periods
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})

        return forecast

    except Exception as e:
        print(e)

def dict_to_str(d):
    return ', '.join(f"{k}: {v}" for k, v in d.items())

def Present_Weather(mp3file, instruct):
    print('\nTesting weather forecast retrieval...')

    weather_forecast = get_weather_forecast()
    forecast_str = dict_to_str(weather_forecast)
    preface = 'create a 5 day forecast from today forward using the following data, there is no need to mention the country "US" and do not comment on graphics i would like the response convert the dates into their appropriate names of each day of the week": '
    full_instr = preface + forecast_str
    Get_Answer(full_instr,'weather', instruct)
    if instruct != 'silent':
        Play_Answer('weather')
#Present_Weather('weather', 'silent')