import sqlite3
from exceptions import NoDataException
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Date, String

from utils import get_logger

Base = declarative_base()


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    location = Column(String, nullable=False)
    metaweather_id = Column(Integer, nullable=False)
    created_at = Column(Date)


class CountryAgg(Base):
    __tablename__ = "country_agg"
    id = Column(Integer, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    average_min_temperatures = Column(Integer, nullable=False)
    average_max_temperatures = Column(Integer, nullable=False)
    minimum_temperature = Column(Integer, nullable=False)
    maximum_temperature = Column(Integer, nullable=False)
    created_at = Column(Date)


class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True, nullable=False)
    country = Column(String, nullable=False)
    location = Column(String, nullable=False)
    min_temperatures = Column(Integer, nullable=False)
    max_temperatures = Column(Integer, nullable=False)
    metaweather_id = Column(Integer, nullable=False)
    created_at = Column(Date)


logger = get_logger()


class DBManager:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        engine = create_engine("sqlite:///{}".format(db_name), echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        # creates all tables if not exist
        Base.metadata.create_all(engine)

    @staticmethod
    def last_date_query(table):
        return """ 
        inner join
        (
            Select max(created_at) as LatestDate, location
            from {table}
            Group by location
        ) SubMax
        on {table}.created_at = SubMax.LatestDate
        and {table}.location = SubMax.location
        """.format(table=table)

    def get_country_updated_data(self, country):
        return self.conn.execute("""select country, avg(min_temperatures), avg(max_temperatures), min(min_temperatures),
        max(max_temperatures), LatestDate
        from(				
        select distinct *
        from weather_data
        {}
        where country = '{}'
        group by country, LatestDate
                """.format(self.last_date_query('weather_data'), country))

    def get_locations_from_db(self):
        return self.session.query(Location.country, Location.location, Location.metaweather_id).all()

    def get_countries_agg_data(self):
        return self.conn.execute("""select country, avg(min_temperatures), avg(max_temperatures), min(min_temperatures),
        max(max_temperatures), LatestDate
        from(			
        select distinct *
        from weather_data
        {})
        group by country""".format(self.last_date_query('weather_data')))

    def insert_many_to_table(self, data, table):
        logger.info("Inserting {amount} rows to table {table}".format(amount=len(data), table=table))
        try:
            args = ', '.join(['?'] * len(data[0]))
        except IndexError:
            raise NoDataException(table)
        self.conn.executemany('INSERT INTO {} VALUES({});'.format(table, args), data)
        self.conn.commit()
