import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from urllib.request import urlopen
import base64

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('900x500')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.create_widgets()
        self.db_ops = DBOperations()
        self.db_ops.initialize_db()

    def create_widgets(self):
        tk.Label(self, text='Weather Processor', font=('Arial Bold', 22))\
            .grid(row=0, column=0, columnspan=4, pady=(10, 24))
        
        self.create_db_widgets()
        
        self.create_bloxplot_widgets()
        
        self.create_lineplot_widgets()

        # tk.Label(self, text="Line Plot:", font=("Arial", 16))\
            # .grid(row=3, column=2, columnspan=4, pady=(24, 10), padx=(10, 0), sticky=tk.W)
    
    def create_db_widgets(self):
        tk.Label(self, text='Database related Actions:', font=('Arial', 16))\
            .grid(row=1, column=0, columnspan=4, pady=(0, 10), sticky=tk.W)
        tk.Button(self, text="View All Data", command=self.view_all_data)\
            .grid(row=2, column=0)
        tk.Button(self, text="Update Database", command=self.update_db)\
            .grid(row=2, column=1)
        tk.Button(self, text="Purge all Data", command=self.say_hi)\
            .grid(row=2, column=2)
        self.db_status_label = tk.Label(self, text=" ")
        self.db_status_label.grid(row=3, column=0, columnspan=2)

    def create_bloxplot_widgets(self):
        tk.Label(self, text="Box Plot:", font=("Arial", 16))\
            .grid(row=4, column=0, columnspan=4, pady=(50, 10), sticky=tk.W)

        tk.Label(self, text="Start Year:")\
            .grid(row=5, column=0, pady=(10, 0), sticky=tk.W)
        self.start_year_entry = tk.Entry(self)
        self.start_year_entry.grid(row=5, column=0, sticky=tk.W)

        tk.Label(self, text="End Year:")\
            .grid(row=5, column=1, pady=(10, 0), sticky=tk.W)
        self.end_year_entry = tk.Entry(self)
        self.end_year_entry.grid(row=5, column=1, sticky=tk.W)
        
        tk.Button(self, text="Generate Blox Pot", command=self.say_hi)\
            .grid(row=7, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.blox_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.blox_plot_error.grid(row=8, column=0, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def create_lineplot_widgets(self):
        tk.Label(self, text="Line Plot:", font=("Arial", 16))\
            .grid(row=4, column=2, columnspan=4, pady=(50, 10), sticky=tk.W)

        # TODO: Make it dropdown
        tk.Label(self, text="Month:")\
            .grid(row=5, column=2, pady=(10, 0), sticky=tk.W)
        self.month_entry = tk.Entry(self)
        self.month_entry.grid(row=5, column=2, sticky=tk.W)

        tk.Label(self, text="Year:")\
            .grid(row=5, column=3, pady=(10, 0), sticky=tk.W)
        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=5, column=3, sticky=tk.W)
        
        tk.Button(self, text="Generate Line Pot", command=self.say_hi)\
            .grid(row=7, column=2, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.line_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.line_plot_error.grid(row=8, column=2, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def view_all_data(self):
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
        # get last date from
            # SELECT *
            # FROM weather
            # ORDER BY sample_date DESC
            # LIMIT 1
        try:
            self.db_status_label['text'] = "Fetching the data and Updating the Database"
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
            self.db_status_label['text'] = " "
            # Fetch data using Weather Scraper Class
            # save data to db
            # show some kind of alert/message
            
        except Exception as e:
            print("ERROR: " + str(e))

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()