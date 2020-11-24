# Final Project Module 1
# Authors:
#   - Harsh Patel (hpatel47@academic.rrc.ca)
#   - Robert Kaufman (rkaufman@academic.rrc.ca)
# http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5

# TODOS:
# - Error Handling
# - PEP8
# - Comments
# - test for all possible weird scenarios
# - multithreading while scraping data

from html.parser import HTMLParser
from datetime import datetime
import urllib.request

class WeatherScraper(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.weather_data = {}
    self.is_tr_open = False
    self.is_td_open = False
    self.is_th_open = False
    self.is_tbody_open = False
    self.td_count = 0
    self.temp_data = {}
    self.temp_date = ""
    #Start by getting todays month and year, and using those as the "present date" values to pass to the url

    #noch back month by month until we are seeing duplicated data - then exit the loop

    #desired output
    # A dictionary of dictionaries. For example:•daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}•
    # weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
    # so we can keep scraping until the daily_temps is repeated

  def handle_starttag(self, tag, attrs):
    if (tag == "tbody"):
      self.is_tbody_open = True
    if (self.is_tbody_open and tag == "tr"):
      self.is_tr_open = True
      self.td_count = 0
    if (self.is_tr_open and tag == "th"):
      self.is_th_open = True
    if (self.is_th_open and tag == "abbr"):
      for attr in attrs:
        if (attr[0] == 'title'):
          # TODO: Add error handling
          self.temp_date = datetime.strptime(attr[1], '%B %d, %Y')
    if (self.is_tr_open and tag == "td" and self.td_count < 3):
      for attr in attrs:
        if (attr[0] == 'colspan'):
          return
      self.is_td_open = True
      self.td_count += 1

  def handle_data(self, data):
    if (self.is_th_open and data == 'Sum'):
      # Closing the scrapping for the page when we reach the row which shows the sum for whole month
      self.is_tbody_open = False
      self.is_tr_open = False
      self.is_th_open = False
      self.is_td_open = False
      return
    # TODO: handle last few total rows
    if (self.is_td_open and self.td_count == 1):
      # TODO: Add error handling
      self.temp_data["Max"] = None if "M" in data else float(data)
    if (self.is_td_open and self.td_count == 2):
      # TODO: Add error handling
      self.temp_data["Min"] = None if "M" in data else float(data)
    if (self.is_td_open and self.td_count == 3):
      # TODO: Add error handling
      self.temp_data["Mean"] = None if "M" in data else float(data)

  def handle_endtag(self, tag):
    if (tag == "tbody"):
      self.is_tbody_open = False
    if (self.is_tbody_open and tag == "tr"):
      self.is_tr_open = False
      self.weather_data[self.temp_date.strftime('%Y-%m-%d')] = self.temp_data
    if (self.is_tr_open and tag == "th"):
      self.is_th_open = False
    if (self.is_tr_open and tag == "td"):
      self.is_td_open = False

  def print_data(self):
    for key in self.weather_data:
      # printing all the colors
      print(key, self.weather_data[key])
  

#starts with january of a set year that is know (aka, 2018), and makes requests incrementing by 1 until
# a 302 code is return from the request.
def get_start_date_year():
  #get response
  #set a bool flag to see if we have
  x = 1

def get_start_date_month(startYear):
  x = 1

def build_url(startYear, endYear, month):
  return 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2020&Day=1&Year=2020&Month=10'
  return 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear='+str(startYear)+'&EndYear='+str(endYear)+'&Day=1&'+str(endYear)+'&Month='+str(month)

myparser = WeatherScraper()
with urllib.request.urlopen(build_url(None, None, None)) as response:
  html = str(response.read())
  
  # parsing HTML
  myparser.feed(html)
  myparser.print_data()
