import os
import argparse
from dal import DBManager
from utils import get_logger
from collector import WeatherScraper
from exceptions import TableEmptyException

logger = get_logger()


class App:

    def __init__(self, args):
        self.db_manager = DBManager(args.db)

    def parse_locations(self, data):
        logger.info('Getting weather data for locations')
        weather_data = WeatherScraper.get_locations_weather_data(data)
        self.db_manager.insert_many_to_table(weather_data, 'weather_data')
        logger.info('Calculating aggregated data')
        country_agg = self.db_manager.get_countries_agg_data()
        self.db_manager.insert_many_to_table(list(country_agg), 'country_agg')


def main():
    parser = argparse.ArgumentParser(description="Weather Forecast Predictions")
    parser.add_argument("--db", default="weather.db", type=os.path.abspath,
                        help="DB full path to connect to.")
    args = parser.parse_args()
    app = App(args)
    logger.info('Getting locations from db')
    locations = app.db_manager.get_locations_from_db()
    if not locations:
        raise TableEmptyException('locations')
    app.parse_locations(locations)


if __name__ == "__main__":
    main()
