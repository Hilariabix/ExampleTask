# Exam For Example

## Goal
The goal of this task is to collect weather data from https://www.metaweather.com/,
 calculate and insert it into the db.
 
## DB Tables
### collections - prepared with another task and should be pre-exist
 - id
 - country 
 - location
 - metaweather_id
 - created_at
### weather_data - all the collected data
 - country
 - location
 - min_temperatures
 - max_temperatures
 - metaweather_id
 - created_at
 
### county_agg - aggregated data, calculated from the weather_data table
 - country
 - average_min_temperatures
 - average_max_temperatures
 - minimum_temperature
 - maximum_temperature
 - created_at


## Run
python main.py --db weather.db
### Arguments
- --db - full path to db (sqlite), default: weather.db 
DB should contains locations table with all the desired locations

