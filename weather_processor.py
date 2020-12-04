import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry('500x400')
        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.create_widgets()

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
        tk.Button(self, text="View All Data???", command=self.say_hi)\
            .grid(row=2, column=0)
        tk.Button(self, text="Update Database", command=self.say_hi)\
            .grid(row=2, column=1)
        tk.Button(self, text="Purge all Data", command=self.say_hi)\
            .grid(row=2, column=2)

    def create_bloxplot_widgets(self):
        tk.Label(self, text="Box Plot:", font=("Arial", 16))\
            .grid(row=3, column=0, columnspan=4, pady=(24, 10), sticky=tk.W)

        tk.Label(self, text="Start Year:")\
            .grid(row=4, column=0, pady=(10, 0), sticky=tk.W)
        self.start_year_entry = tk.Entry(self)
        self.start_year_entry.grid(row=5, column=0, sticky=tk.W)

        tk.Label(self, text="End Year:")\
            .grid(row=4, column=1, pady=(10, 0), sticky=tk.W)
        self.end_year_entry = tk.Entry(self)
        self.end_year_entry.grid(row=5, column=1, sticky=tk.W)
        
        tk.Button(self, text="Generate Blox Pot", command=self.say_hi)\
            .grid(row=6, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.blox_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.blox_plot_error.grid(row=7, column=0, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def create_lineplot_widgets(self):
        tk.Label(self, text="Line Plot:", font=("Arial", 16))\
            .grid(row=3, column=2, columnspan=4, pady=(24, 10), sticky=tk.W)

        # TODO: Make it dropdown
        tk.Label(self, text="Month:")\
            .grid(row=4, column=2, pady=(10, 0), sticky=tk.W)
        self.month_entry = tk.Entry(self)
        self.month_entry.grid(row=5, column=2, sticky=tk.W)

        tk.Label(self, text="Year:")\
            .grid(row=4, column=3, pady=(10, 0), sticky=tk.W)
        self.year_entry = tk.Entry(self)
        self.year_entry.grid(row=5, column=3, sticky=tk.W)
        
        tk.Button(self, text="Generate Line Pot", command=self.say_hi)\
            .grid(row=6, column=2, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.line_plot_error = tk.Label(self, text=" ", fg="#ff0000")
        self.line_plot_error.grid(row=7, column=2, columnspan=2, sticky=tk.W)
        # TODO: Embed Plots: https://pythonprogramming.net/how-to-embed-matplotlib-graph-tkinter-gui/

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()