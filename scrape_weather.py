# Final Project Module 1
# Authors:
#   - Harsh Patel (hpatel47@academic.rrc.ca)
#   - Robert Kaufman (rkaufman@academic.rrc.ca)
# http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5

# TODOS:
# x Loop and fetch all possible data in get_weather_data method
# - Error Handling
# - Refactor code and remove unnecessary variables from constructor
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
    self.is_looping = False
    #Start by getting todays month and year, and using those as the "present date" values to pass to the url

    #noch back month by month until we are seeing duplicated data - then exit the loop

    #desired output
    # A dictionary of dictionaries. For example:•daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}•
    # weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
    # so we can keep scraping until the daily_temps is repeated

  def handle_starttag(self, tag, attrs):
    if (tag == "tbody"):
      self.is_tbody_open = True
      self.temp_date = ""
      self.temp_data = {}
    if (self.is_tbody_open and tag == "tr"):
      self.is_tr_open = True
      self.td_count = 0
      self.temp_data = {}
    if (self.is_tr_open and tag == "th"):
      self.is_th_open = True
    if (self.is_th_open and tag == "abbr"):
      for attr in attrs:
        if (attr[0] == 'title'):
          # TODO: Add error handling
          print('date value: ', attr[1])
          self.temp_date = datetime.strptime(attr[1], '%B %d, %Y')
    if (self.temp_date and self.is_tr_open and tag == "td" and self.td_count < 3):
      for attr in attrs:
        if (attr[0] == 'colspan'):
          return
      self.is_td_open = True
      self.td_count += 1

  def handle_data(self, data):
    value = data.strip()
    if (self.is_th_open and data == 'Sum'):
      # Closing the scrapping for the page when we reach the row which shows the sum for whole month
      self.is_tbody_open = False
      self.is_tr_open = False
      self.is_th_open = False
      self.is_td_open = False
      return
    # TODO: handle last few total rows
    if (self.is_td_open):
      parsed_value = None
      try:
        parsed_value = float(value)
      except ValueError:
        parsed_value = None
        print("ERROR: Invalid Float Value")
      if (self.td_count == 1):
        # TODO: Add error handling
        self.temp_data["Max"] = parsed_value
      if (self.td_count == 2):
        # TODO: Add error handling
        self.temp_data["Min"] = parsed_value
      if (self.td_count == 3):
        # TODO: Add error handling
        self.temp_data["Mean"] = parsed_value

  def handle_endtag(self, tag):
    if (tag == "tbody"):
      self.is_tbody_open = False
    if (self.is_tbody_open and tag == "tr"):
      self.is_tr_open = False
      date = self.temp_date.strftime('%Y-%m-%d') if self.temp_date else None
      print(date)
      if date and date in self.weather_data:
        self.is_looping = False
      else:
        self.weather_data[date] = self.temp_data
        self.temp_data = {}
        self.temp_date = ""
    if (self.is_tr_open and tag == "th"):
      self.is_th_open = False
    if (self.is_tr_open and tag == "td"):
      self.is_td_open = False

  def print_data(self):
    for key in self.weather_data:
      # printing all the colors
      print(key, self.weather_data[key])

  def build_url(self, year, month):
    today = datetime.today()
    print(today.year, today.month)
    # QUESTION: What is StartYear and EndYear in URL? Do we really need them in URL while scraping data? I tested it on my end and these parameters are not required
    return 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&Year='+str(year)+'&Month='+str(month)
  
  def scrape_data(self):
      today = datetime.today()
      year = today.year
      month = today.month
      # year = 1998
      # month = 12
      self.is_looping = True
      while self.is_looping:
          url = self.build_url(year, month)
          with urllib.request.urlopen(url) as response:
            html = str(response.read())
            # parsing HTML
            self.feed(html)
          pass
          if (month != 1):
            month -= 1
          else:
            month = 12
            year -= 1
          print(self.is_looping)
      self.print_data()

myParser = WeatherScraper()
myParser.scrape_data()