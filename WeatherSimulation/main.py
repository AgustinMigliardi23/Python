import datetime as dt
import phrases
import webScrapping_weather

def get_forecast():
    forecast = webScrapping_weather.get_data()
    for weather, day in forecast:
        phrases.print_data(day, phrases.parse_data_to_numbers(weather))
        if day.hour + 3 <= 21:
            day = dt.datetime(day.year, day.month, day.day, day.hour + 6)
        else:
            try:
                day = dt.datetime(day.year, day.month, day.day + 1, 9)
            except:
                try:
                    day = dt.datetime(day.year, day.month + 1, 1, 9)
                except:
                    day = dt.datetime(day.year + 1, 1, 1, 9)
get_forecast()