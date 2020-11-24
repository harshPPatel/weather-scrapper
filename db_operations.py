import sqlite3
import mysql.connector

#If I'm reading this correctly, we should only ever be passed a single dictionary (think of a single day)
# I can check the db for date overwrites
# Data will be the actual dictionary that we use for each operation

class DBOperations():

  def __init__(self, data):
    self.data = data

  def initialize_db(self):
    with DBCM("weather.sqlite") as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                    id integer prmary key autoincrement not null,
                    sample_date text not null,
                    location text not null,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);""")
  def fetch_data(self):
    x = 1

  def save_data(self):
    x = 1


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
