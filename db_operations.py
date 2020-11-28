import sqlite3
import datetime
import mysql.connector

#If I'm reading this correctly, we should only ever be passed a single dictionary (think of a single day)
# I can check the db for date overwrites
# Data will be the actual dictionary that we use for each operation
# Ok, Ill need to take a new apprach for this - because dates are texts, and I dont want it running endlessly
# The unique constraint will prevent duplicated data
# I Should create a class variable with the most recent date of the db, if I can.

class DBOperations():

  def __init__(self):
    self.dates_data = self.get_dates()

  def initialize_db(self):
    with DBCM("weather.sqlite") as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                    id integer prmary key autoincrement not null,
                    sample_date text UNIQUE not null,
                    location text not null,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);""")


  def save_data(self, dataset):
    """Takes a dictionary with a Date, Location, Min Tem, Max tem, and Average temp, and saves it to a db"""
    """Need to connect and figure out how to avoid duplicating data - I've reached out to someone for help, But
    I wanted to test basic functionality first just so I could get something done"""
    with DBCM("weather.sqlite") as cur:
      for data in dataset:
          while data not in self.date_data:
            insert_string = ''' INSERT INTO weather(sample_date, location, min_temp, max_temp, avg_temp)
                        VALUES(?,?,?,?)'''
            values = (data, "Winnipeg, MB", dataset[data]["min_temp"], dataset[data]["max_temp"], dataset[data]["avg_temp"])
            cur.execute(insert_string, values)

  # now.strftime("%m/%d/%Y,
  def fetch_data(start_date = datetime.now().now.strftime("%Y-%M-%D"), end_date = datetime.now().now.strftime("%Y-%M-%D")):
    """Takes a date, and a location, and retrives the values if any are found
    If no parameters are provided, retruns information for todays date """
    with DBCM("weather.sqlite") as cur:
      query = "SELECT * FROM weather WHERE sameple_date < ? AND sample_date > ?;"
      params = (start_date, end_date)
      return cur.execute(query, params)


  def purge_data(self):
    with DBCM("weather.sqlite") as cur:
      cur.execute("""DROP TABLE IF EXISTS weather;""")

  def get_dates(self):
    """
    Funtion created to get all of the dates in the current database
    for users to select a range from"""
    with DBCM("weather.sqlite") as cur:
      return cur.execute("""SELECT sample_date FROM weather;""")


class DBCM():
  def __init__(self, db_name):
    self.db_name = db_name

  def __enter__(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cursor = self.conn.cursor()
    return self.cursor

  def __exit__(self, exec_type, exec_value, exec_trace):
    self.conn.commit()
    self.cursor.close()
    self.conn.close()
