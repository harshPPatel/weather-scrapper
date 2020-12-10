"""
This file provides WeatherScraper class which allows
weather app to scrape data from website and return
it in dictionary format so that other classes can understand it.

Authors:
- Harsh Patel
- Robert Kaufman
"""

from html.parser import HTMLParser
from datetime import datetime
import urllib.request

class WeatherScraper(HTMLParser):
    """Class to actually scrape the data from the website
    """
    def __init__(self):
        HTMLParser.__init__(self)
        # used to store all the weather data scraped from website
        self.weather_data = {}
        # used to keep track if we are reading elements inside tr tags
        self.is_tr_open = False
        # used to keep track if we are reading data from td tags
        self.is_td_open = False
        # used to keep track if we are reading data from th tags
        self.is_th_open = False
        # used to keep track if we are still scrapping data from page
        self.is_scraping = False
        # used to keep track of teh current td count
        self.td_count = 0
        # stores temporary data for specific date row
        self.temp_data = {}
        # stores date temporary
        self.temp_date = None
        # used to keep track of if we are still looping through different pages to scrap data
        self.is_looping = False
        # Array to store keys values to store data for each date
        self.keys_names = ["Max", "Min", "Mean"]

    def handle_starttag(self, tag, attrs):
        """Function to handle processing the start tag and what to pull
        out of each element
        """
        # TODO: Do we need is_scrapping and is_looping both?
        # updating some boolean flags when we start reading tbody tag
        if tag == "tbody":
            self.is_scraping = True
            self.temp_date = None
            self.temp_data = {}
        if self.is_scraping:
            if tag == "tr":
                # resetting some values and toggling flag when we are reading tr tag
                self.is_tr_open = True
                self.td_count = 0
                self.temp_data = {}
            if self.is_tr_open and tag == "th":
                # toggling th flag when we are reading th tag
                self.is_th_open = True
            if self.is_th_open and tag == "abbr":
                for attr in attrs:
                    # th tag contains abbr tag which holds full date as title attribute
                    # we are scraping that value and storing datetime object to temp_date
                    if attr[0] == 'title':
                        try:
                            self.temp_date = datetime.strptime(attr[1], '%B %d, %Y')
                            # if we try to fetch the old data than the website limit,
                            # it just starts returning data for the last available
                            # month rather than showing error page. Because of this
                            # behaviour we can simply check when to stop by seeing if we
                            # already have entry for this date and stop the scrape loop
                            date = self.temp_date.strftime('%Y-%m-%d')
                            if date in self.weather_data:
                                # stopping the loop if we have already reached the end date
                                self.is_looping = False
                        except Exception as e:
                            print("ERROR: Invalid Date")
                            print(str(e))
                            self.temp_date = None
            # toggling the td flag if temp_date
            # exists (the last row (for current day) does not contains any values,
            # it also does not have any abbr value, we are
            # ignoring that value as looks like this row is updated next day),
            # if tr tag is open and if total td count
            # is less than three because we only need values from first three columns
            if self.temp_date and self.is_tr_open and tag == "td" and self.td_count < 3:
                self.is_td_open = True
                self.td_count += 1

    def handle_data(self, data):
        """Takes the data and ensures that it is valid, and then adds it to a dictionary"""
        # removing any whitespaces at two ends from data
        value = data.strip()
        # after valid rows in table, there is row 
        # which shows sum of all values, this is the row which toggles the
        # is_scraping flag and tells application that
        # we are no longer scraping data from this page
        if self.is_th_open and data == 'Sum':
            self.is_scraping = False
            return

        # If it is valid date row and we are reading td tag,
        # we parse values and add it to temp_data dictionary
        if self.is_td_open:
            parsed_value = None
            try:
                # trying to parse value as float
                parsed_value = float(value)
            except ValueError as e:
                # setting it to None if it is invalid string (some rows
                # does not have data and it shows M instead of valid float number)
                parsed_value = None
                print("ERROR: Invalid Float Value")
                print(value)
                print(str(e))

            # Adding parsed values to temp_data with the keys accordingly
            # if row is missing one or all column values, we still need to set it as None
            self.temp_data[self.keys_names[self.td_count - 1]] = parsed_value

    def handle_endtag(self, tag):
        """Handles what the program should do when it encounters an endtag"""
        if tag == "tbody":
            # Toggling the scrapping to off we have completed reading tbody tag
            self.is_scraping = False
        if self.is_scraping:
            if tag == "tr":
                # Adding temp_data with proper formatted date value
                # to weather_data when we have compelted reading tr tag
                self.is_tr_open = False
                # converting the temp_date (datetime) object to
                # requested string format if value exists in temp_date
                date = self.temp_date.strftime('%Y-%m-%d') if self.temp_date else None
                # adding temp data to weather_data dictionary
                # and restting temp values for next tr row
                if date:
                    self.weather_data[date] = self.temp_data
                    self.temp_data = {}
                    self.temp_date = None
            if self.is_tr_open and tag == "th":
                self.is_th_open = False
            if self.is_tr_open and tag == "td":
                self.is_td_open = False

    def build_url(self, year, month):
        """Builds the URL to scrape the data from a particular month and year"""
        url = 'http://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&Year='\
            + str(year) + '&Month=' +str(month)
        print("Scraping URL:", url)
        return url


    def scrape_data(self, start, end):
        """Loops through and adds each data value to a dictionary
        then, when the end dat is reached, returns the dictionary for processing"""
        end_date = datetime.strptime(end, '%Y-%m-%d')

        year = end_date.year
        month = end_date.month
        self.is_looping = True

        # looping to scrape pages until we have start date available in dataset
        while self.is_looping:
            if start in self.weather_data:
                self.is_looping = False
                break
            url = self.build_url(year, month)
            # parsing the response from website
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
                self.feed(html)
            pass

            # updating month and year for next loop once we complete reading the page
            if month != 1:
                month -= 1
            else:
                month = 12
                year -= 1

        return_data = {}
        for key, value in self.weather_data.items():
            if (key > start):
                return_data[key] = value
        return return_data


    def scrape_all_data(self):
        """Scrapes all data from the government website"""
        today = datetime.today()
        year = today.year
        month = today.month
        self.is_looping = True

        # looping to scrape pages until we start getting duplicate data from website
        while self.is_looping:
            url = self.build_url(year, month)
            # parsing the response from website
            with urllib.request.urlopen(url) as response:
                html = str(response.read())
                self.feed(html)
            # updating month and year for next loop once we complete reading the page
            if month != 1:
                month -= 1
            else:
                month = 12
                year -= 1

        return self.weather_data

if __name__ == "__main__":
    myParser = WeatherScraper()
    myParser.scrape_all_data()