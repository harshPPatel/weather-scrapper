import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations
from urllib.request import urlopen
import base64

# TODO: remove unnecessary imports
# TODO: add labels for inputs

class Application(tk.Frame):
    """Application for the weather scraper scripts compiled for Programming In Python
       Sends a request to the governemnt of canada website http://climate.weather.gc.ca/climate_data/
       and gives users the option to display a month as a line graph, or a range of years as a box plot
    """
    def __init__(self, master=None):
        """Runs standard setup functions, and creates the baseline box for the application"""
        super().__init__(master)
        self.master = master
        self.master.geometry('900x500')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.db_status_text = tk.StringVar()
        self.line_month = tk.StringVar(self)
        self.create_widgets()
        self.db_ops = DBOperations()
        self.db_ops.initialize_db()

    def create_widgets(self):
        """Calls the functions that create the widgets for specific actions"""
        tk.Label(self, text='Weather Processor', font=('Arial Bold', 22))\
            .grid(row=0, column=0, columnspan=4, pady=(10, 24))

        self.create_db_widgets()

        self.create_bloxplot_widgets()

        self.create_lineplot_widgets()

        # tk.Label(self, text="Line Plot:", font=("Arial", 16))\
            # .grid(row=3, column=2, columnspan=4, pady=(24, 10), padx=(10, 0), sticky=tk.W)

    def create_db_widgets(self):
        """Creates the widgets to allow for database actions: View, Deleting, and updating"""
        tk.Label(self, text='Database related Actions:', font=('Arial', 16))\
            .grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        tk.Button(self, text="View All Data", command=self.view_all_data)\
            .grid(row=2, column=0)
        tk.Button(self, text="Update Database", command=self.update_db)\
            .grid(row=2, column=1)
        tk.Button(self, text="Purge all Data", command=self.purge_db)\
            .grid(row=2, column=2)
        self.db_status_label = tk.Label(self, textvariable=self.db_status_text)
        self.db_status_label.grid(row=3, column=0, columnspan=2)

    def create_bloxplot_widgets(self):
        """Creates the widgets to allow users to
           provide a start year, and end year, and
           to request a boxplot graph
        """
        tk.Label(self, text="Box Plot:", font=("Arial", 16))\
            .grid(row=4, column=0, columnspan=4, pady=(50, 10), sticky=tk.W)

        tk.Label(self, text="Start Year:")\
            .grid(row=5, column=0, pady=(10, 0), sticky=tk.W)
        self.start_year_entry = tk.Entry(self)
        self.start_year_entry.grid(row=6, column=0, sticky=tk.W)

        tk.Label(self, text="End Year:")\
            .grid(row=5, column=1, pady=(10, 0), sticky=tk.W)
        self.end_year_entry = tk.Entry(self)
        self.end_year_entry.grid(row=6, column=1, sticky=tk.W)

        tk.Button(self, text="Generate Blox Pot", command=self.generate_boxplot)\
            .grid(row=7, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.blox_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.blox_plot_error.grid(row=8, column=0, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def create_lineplot_widgets(self):
        """Creates the widgets responsible for
           creating and graphing the lineplot for
           a given month
        """
        tk.Label(self, text="Line Plot:", font=("Arial", 16))\
            .grid(row=4, column=2, columnspan=4, pady=(50, 10), sticky=tk.W)

        # TODO: Make it dropdown
        tk.Label(self, text="Month:")\
            .grid(row=5, column=2, pady=(10, 0), sticky=tk.W)
        # self.month_entry = tk.Entry(self)
        # self.month_entry.grid(row=5, column=2, sticky=tk.W)

        self.line_month.set("jan") # default value

        self.month_entry = tk.OptionMenu(self, self.line_month, "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
        self.month_entry.grid(row=6, column=2, sticky=tk.W)

        tk.Label(self, text="Year:")\
            .grid(row=5, column=3, pady=(10, 0), sticky=tk.W)
        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=6, column=3, sticky=tk.W)

        tk.Button(self, text="Generate Line Pot", command=self.generate_lineplot)\
            .grid(row=7, column=2, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.line_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.line_plot_error.grid(row=8, column=2, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def view_all_data(self):
        """Shows all the data currently in the db"""
        newWindow = tk.Toplevel(self)
        newWindow.title("All Weather Data")
        newWindow.geometry("900x500")
        tree = ttk.Treeview(newWindow)
        # creating table columns
        tree["columns"]=("date","location","min_temp", "max_temp", "avg_temp")
        tree.column("#0", width=50, stretch=tk.YES, anchor=tk.W)
        tree.column("date", width=110, minwidth=100, stretch=tk.YES, anchor=tk.CENTER)
        tree.column("location", width=80, anchor=tk.W)
        tree.column("min_temp", width=150, stretch=tk.YES, anchor=tk.E)
        tree.column("max_temp", width=150, stretch=tk.YES, anchor=tk.E)
        tree.column("avg_temp", width=150, stretch=tk.YES, anchor=tk.E)
        # defining headings
        tree.heading("#0",text="ID")
        tree.heading("date", text="Sample Date")
        tree.heading("location", text="Location")
        tree.heading("min_temp", text="Minimum Temperature")
        tree.heading("max_temp", text="Maximum Temperature")
        tree.heading("avg_temp", text="Average Temperature")

        try:
            data = self.db_ops.get_all_data()
            for row in data:
                tree.insert("", "end", str(row[0]), text=str(row[0]), values=(str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])))
        except Exception as e:
            # TODO: Show error to GUI
            print("ERROR: " + str(e))

        tree.pack(expand=1, fill=tk.BOTH)

    def update_db(self):
        """uses todays date to fetch all the data
           from the most recent date in the db
           to today
        """
        # get last date from
            # SELECT *
            # FROM weather
            # ORDER BY sample_date DESC
            # LIMIT 1
        try:
            self.db_status_text.set("Fetching the data and Updating the Database")
            # TODO: Run this code on seperate thread
            get_latest_row = self.db_ops.get_latest_row()
            scraper = WeatherScraper()
            if (get_latest_row == None):
                data = scraper.scrape_all_data()
                self.db_ops.save_data(data)
            else:
                latest_db_date = get_latest_row[1]
                today = datetime.today().strftime('%Y-%m-%d')
                if (today != latest_db_date and today > latest_db_date):
                    data = scraper.scrape_data(latest_db_date, today)
                    self.db_ops.save_data(data)
            # TODO: Update this inside thread once task is done
            self.db_status_text.set(" ")
            # Fetch data using Weather Scraper Class
            # save data to db
            # show some kind of alert/message

        except Exception as e:
            print("ERROR: " + str(e))

    def purge_db(self):
        """Calls the function to drop all data from the db"""
        # TODO: Make sure we are not getting any error on Windows. I am having some issues with Big Sur on Mac
        message_box = messagebox.askokcancel(title='Purge Data',message='Do you really want to delete all data?',icon='error')
        if message_box:
            self.db_ops.purge_data()

    def generate_boxplot(self):
        """Uses the data in the db to generate the requested boxplot"""
        start_year = self.start_year_entry.get()
        end_year = self.end_year_entry.get()
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if (start_year <= 0 or end_year <= 0):
                raise ValueError()
            elif (start_year > end_year):
                self.blox_plot_error['text'] = 'ERROR: Start Year can not be greater than end Year!'
            else:
                self.blox_plot_error['text'] = ' '
                data = self.db_ops.fetch_data(start_date=(str(start_year) + "-01-01"), end_date=(str(end_year) + "-12-31"))
                boxplot_data = self.format_data_for_boxplot(data)
                plot_ops = PlotOperations(data=boxplot_data)
                plot_ops.show_boxplot()
        except Exception as e:
            if (self.blox_plot_error['text'] != ' '):
                self.blox_plot_error['text'] = 'Please enter valid Year values!'
            print("ERROR :", str(e))
            e.with_traceback()

    def get_month_index(self, value):
        """Retuns a months index based on where it is in the year"""
        month = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
        return (month.index(value) + 1)

    def get_formatted_month(self, index):
        """Returns a formatted numerical value for a month"""
        if (index < 10):
            return ("0" + str(index))
        else:
            return str(index)

    def generate_lineplot(self):
        """Fetches data from the db, formats it, and then displays that data
           in a lineplot
        """
        month_index = self.get_month_index(self.line_month.get())
        formatted_month = self.get_formatted_month(month_index)
        year = self.year_entry.get()
        try:
            year = int(year)
            if (year <= 0):
                raise ValueError()
            else:
                self.line_plot_error['text'] = ' '
                data = self.db_ops.fetch_data(start_date=(str(year) + "-" + formatted_month + "-01"), end_date=(str(year) + "-" + formatted_month + "-31"))
                boxplot_data = self.format_data_for_lineplot(data)
                # passing empty data as this data is not used in generating line-plot
                plot_ops = PlotOperations(data={})
                print(boxplot_data)
                plot_ops.show_lineplot(boxplot_data, month_index, year)
        except Exception as e:
            if (self.line_plot_error['text'] != ' '):
                self.line_plot_error['text'] = 'Please enter valid Month and Year values!'
            print("ERROR :", str(e))
            e.with_traceback()

    def format_data_for_boxplot(self, data):
        """Takes data from the db, and formats it for display in a boxplot"""
        return_data = {}
        try:
            for row in data:
                date = datetime.strptime(row[1], '%Y-%m-%d')
                year = date.year
                month = date.month
                if not return_data.get(year):
                    return_data[year] = {}
                if not return_data[year].get(month):
                    return_data[year][month] = []
                # if value is None, we are setting default value as 0.
                # We tried using None and NaN from numpy library,
                # but it is not currently supported to matplotlib :(
                if (row[5] == None):
                    return_data[year][month].append(0)
                else:
                    return_data[year][month].append(row[5])

        except Exception as e:
            self.blox_plot_error['text'] = 'Error while processing data'
            print("ERROR: " + str(e))
        finally:
            return return_data


    def format_data_for_lineplot(self, data):
        """Takes data and formats it for display in a lineplot"""
        return_data = []
        try:
            for row in data:
                # if value is None, we are setting default value as 0.
                # We tried using None and NaN from numpy library,
                # but it is not currently supported to matplotlib :(
                if (row[5] == None):
                    return_data.append(0)
                else:
                    return_data.append(row[5])

        except Exception as e:
            self.line_plot_error['text'] = 'Error while processing data'
            print("ERROR: " + str(e))
        finally:
            return return_data

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()