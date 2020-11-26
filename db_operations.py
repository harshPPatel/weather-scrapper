import sqlite3
import mysql.connector

#If I'm reading this correctly, we should only ever be passed a single dictionary (think of a single day)
# I can check the db for date overwrites
# Data will be the actual dictionary that we use for each operation

class DBOperations():

  def initialize_db(self):
    with DBCM("weather.sqlite") as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                    id integer prmary key autoincrement not null,
                    sample_date text not null,
                    location text not null,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);""")


  def fetch_data(date_to_fetch):
    """Takes a date, and a location, and retrives the values if any are found"""
    """Is this supposed to return a single record, or multiple?
    For now, I will write it to fetch a single record, but I may want to come back
    and refactor this when some of the GUI work is finished"""
    with DBCM("weather.sqlite") as cur:
      query = "SELECT * FROM weather WHERE sameple_date = ?"
      return cur.execute(query, date_to_fetch)


  def save_data(self, dataset):
    """Takes a dictionary with a Date, Location, Min Tem, Max tem, and Average temp, and saves it to a db"""
    """Need to connect and figure out how to avoid duplicating data - I've reached out to someone for help, But
    I wanted to test basic functionality first just so I could get something done"""
    with DBCM("weather.sqlite") as cur:
      for data in dataset:
          insert_string = ''' INSERT INTO weather(sample_date, location, min_temp, max_temp, avg_temp)
                      VALUES(?,?,?,?)'''
          values = (data, dataset[data]["location"], dataset[data]["min_temp"], dataset[data]["max_temp"], dataset[data]["avg_temp"])
          cur.execute(insert_string, values)

  def fetch_data_beta(start_date, end_date, location):
    """Takes a date, and a location, and retrives the values if any are found"""
    """Is this supposed to return a single record, or multiple?
    For now, I will write it to fetch a single record, but I may want to come back
    and refactor this when some of the GUI work is finished"""
    with DBCM("weather.sqlite") as cur:
      query = "SELECT * FROM weather WHERE sameple_date < ? AND sample_date > ? AND location = ?"
      params = (start_date, end_date, location)
      return cur.execute(query, params)


  def purge_data(self):
    with DBCM("weather.sqlite") as cur:
      cur.execute("""DROP TABLE IF EXISTS weather;""")


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
