from weather import WeatherAPI

def main():
    weather = WeatherAPI()
    weather.fetch_data()
    windspeed, gust, wind_direction = weather.filter_data()
    wind_knot, gust_knot = weather.convert_to_knots(windspeed, gust)
    weather.plot_data(wind_knot, gust_knot)
    
if __name__ == "__main__":
    main()
