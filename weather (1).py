import json
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import numpy as np

class WeatherAPI:
    def __init__(self):
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.lat = # your location
        self.lng = # your location
        self.api_url = 'https://api.stormglass.io/v2/weather/point'
        self.api_key = '# your API key'
        self.data = None

    def fetch_data(self):
        response_API = requests.get(
            self.api_url,
            params={
                'lat': self.lat,
                'lng': self.lng,
                'params': 'gust,windSpeed,windDirection',
                'start': self.today + 'T06:00:00+00:00',
                'end': self.today + 'T18:00:00+00:00'
            },
            headers={
                'Authorization': self.api_key
            }
        )

        self.data = response_API.json()

    def filter_data(self):
        if not self.data:
            raise ValueError('Erro, not data')

        windspeed = [hour['windSpeed']['noaa'] for hour in self.data['hours'] if 'noaa' in hour['windSpeed']]
        gust = [hour['gust']['noaa'] for hour in self.data['hours']]
        wind_direction = [hour['windDirection']['noaa'] for hour in self.data['hours'] if 'noaa' in hour['windDirection']]
        return windspeed, gust, wind_direction

    @staticmethod
    def mps_to_knots(mps):
        knots = mps * 1.94384
        return int(knots)

    def convert_to_knots(self, windspeed, gust):
        wind_knot = [WeatherAPI.mps_to_knots(wind) for wind in windspeed]
        gust_knot = [WeatherAPI.mps_to_knots(wind) for wind in gust]
        return wind_knot, gust_knot

    @staticmethod
    def plot_data(wind_knot, gust_knot):
        hours = list(range(6, 19))

        if len(wind_knot) != len(gust_knot):
            wind_knot += [np.nan] * (len(gust_knot) - len(wind_knot))
        else:
            gust_knot += [np.nan] * (len(wind_knot) - len(gust_knot))

        plt.figure(figsize=(10, 6))
        plt.plot(hours, wind_knot, 'o-', color='green', label='windspeed')
        plt.plot(hours, gust_knot, 'o-', color='red', label='gust')

        ax1 = plt.gca()
        plt.title('Wind Data')
        ax1.set_xlabel('Hours')
        ax1.set_ylabel('Knots', color='black')

        ax1.legend(loc='upper right')

        plt.xticks(hours)

        plt.show()