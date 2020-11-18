# Final Project Module 1
# Authors:
#   - Harsh Patel (hpatel47@academic.rrc.ca)
#   - Robert Kaufman (rkaufman@academic.rrc.ca)
# http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5

from html.parser import HTMLParser
import urllib.request

class WeatherScraper(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    #Start by getting todays month and year, and using those as the "present date" values to pass to the url

    #noch back month by month until we are seeing duplicated data - then exit the loop

    #desired output
    # A dictionary of dictionaries. For example:•daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}•
    # weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
    # so we can keep scraping until the daily_temps is repeated

#starts with january of a set year that is know (aka, 2018), and makes requests incrementing by 1 until
# a 302 code is return from the request.
def get_start_date_year():
  #get response
  #set a bool flag to see if we have
  x = 1

def get_start_date_month(startYear):
  x = 1

def build_url(startYear, endYear, month):
  return 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear='+str(startYear)+'&EndYear='+str(endYear)+'&Day=1&'+str(endYear)+'&Month='+str(month)
