import json
import requests
from utils import get_config, get_logger
from datetime import datetime, timedelta
from exceptions import CollectionConnectionError


class WeatherScraper:
    logger = get_logger()
    conf = get_config()['collector']

    @staticmethod
    def get_latest_location_forecast(woeid, date):
        query = WeatherScraper.conf['location_forcast_query'].format(
            woeid=woeid, date=date.strftime(WeatherScraper.conf['date_format']))
        try:
            latest_location_forecast = requests.get(WeatherScraper._url(query))
            latest_location_forecast = json.loads(latest_location_forecast.text)[0]
        except requests.exceptions.ConnectionError:
            WeatherScraper.logger.error('Failed to establish new connection')
            raise CollectionConnectionError(WeatherScraper.conf['api_url'])
        except KeyError:
            WeatherScraper.logger.warning('Metaweather id not found')
            return {}
        return {'min_temp': latest_location_forecast['min_temp'], 'max_temp': latest_location_forecast['max_temp']}

    @staticmethod
    def _url(path):
        return '{}{}'.format(WeatherScraper.conf['api_url'], path)

    @staticmethod
    def get_locations_weather_data(locations):
        weather_data = []
        yesterday = datetime.now() - timedelta(days=1)
        for country, location, woeid in locations:
            forecast = WeatherScraper.get_latest_location_forecast(woeid, yesterday)
            if forecast:
                weather_data.append([country, location, forecast["min_temp"], forecast["max_temp"],
                                     woeid, datetime.now().strftime("%d-%m-%Y")])
        return weather_data
