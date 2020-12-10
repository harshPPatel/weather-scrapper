"""
This file provides DBOperations class to other files so that
weather application can perform actions on the database.
It also allows users to read data from the database.

Authors:
- Harsh Patel
- Robert Kaufman
"""

import sqlite3

class DBOperations():
    """Database operations for the Weather Processor app"""

    def initialize_db(self):
        """Initializes the DB and creates a table if one does not yet exist"""
        with DBCM("weather.sqlite") as cur:
            cur.execute("""CREATE TABLE IF NOT EXISTS weather (
                    id INTEGER PRIMARY key AUTOINCREMENT NOT NULL,
                    sample_date TEXT UNIQUE NOT NULL,
                    location TEXT NOT NULL,
                    min_temp REAL,
                    max_temp REAL,
                    avg_temp REAL);""")


    def save_data(self, dataset):
        """Takes a dictionary with a Date, Location,
        Min Tem, Max tem, and Average temp, and saves it the a db"""
        with DBCM("weather.sqlite") as cur:
            for data in dataset:
                print(data)
                min_temp = float(dataset[data]["Min"]) if dataset[data]["Min"] else None
                max_temp = float(dataset[data]["Max"]) if dataset[data]["Max"] else None
                avg_temp = float(dataset[data]["Mean"]) if dataset[data]["Mean"] else None
                insert_string = '''INSERT INTO weather(sample_date,
                            location, min_temp, max_temp, avg_temp)
                            VALUES(?,?,?,?,?);'''
                values = (data, "Winnipeg, MB", min_temp, max_temp, avg_temp)
                try:
                    cur.execute(insert_string, values)
                except Exception as e:
                    print("ERROR: While Adding new row")
                    print(str(e))

    def fetch_data(self, start_date, end_date):
        """Takes a date, and a location, and retrives the values if any are found
        If no parameters are provided, retruns information for todays date
        """
        with DBCM("weather.sqlite") as cur:
            query = """SELECT * FROM weather
                WHERE sample_date >= ? AND sample_date <= ?
                ORDER BY sample_date;"""
            params = (start_date, end_date)
            cur.execute(query, params)
            return cur.fetchall()

    def get_all_data(self):
        """Collects all the data in the DB for processing"""
        with DBCM("weather.sqlite") as cur:
            query = "SELECT * FROM weather ORDER BY sample_date DESC"
            cur.execute(query)
            return cur.fetchall()

    def get_latest_row(self):
        """Returns the most recent date from the db"""
        with DBCM("weather.sqlite") as cur:
            query = "SELECT * FROM weather ORDER BY sample_date DESC LIMIT 1"
            cur.execute(query)
            return cur.fetchone()

    def purge_data(self):
        """Drops the table from the database, removing all entries"""
        with DBCM("weather.sqlite") as cur:
            cur.execute("""DELETE FROM weather;""")


    def get_dates(self):
        """Funtion created to get all of the dates in the current database
        for users to select a range from"""
        with DBCM("weather.sqlite") as cur:
            return cur.execute("""SELECT sample_date FROM weather;""")

class DBCM():
    """Context manager for weather_processor app"""
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exec_type, exec_value, exec_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
