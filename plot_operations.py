import matplotlib.pyplot as plot
import numpy as np
# data will be formatted
# Plot will show the average for all januaries across all years

class PlotOperations():
  def __init__(self, data):
    self.data = data

  def get_month_name(self, index):
    """Returns a months name based numerical position in the year"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[index - 1]

  def show_lineplot(self, month_data, month_index, year):
    """Plots and displays a lineplot for a single month"""
    # NOTE (Remove in final Submission): Updated to get array of temperature values for specific month
    labels = []
    # looping through array to generate labels
    for n in range(len(month_data)):
      labels.append(n + 1)
    plot.plot(month_data)
    plot.title('Daily Temperature Distribution for: ' + self.get_month_name(month_index) + ', ' + str(year))
    plot.xticks(range(1, len(labels) + 1), labels) # This should show the x label as each days
    plot.xlabel('Day')
    plot.ylabel('Temperature (Celsius)')
    plot.show()

  def show_boxplot(self):
    """Displays a boxplot to show averages for each month over a number of years"""
    dataset_to_process = {}
    for year in self.data.values():
      for key, values in year.items():
        # print(key)
        if not (dataset_to_process.get(key)):
          # print("Here")
          dataset_to_process[key] = []
        dataset_to_process[key] += values
        # Remove in final?
        # print(dataset_to_process[key])

    labels = dataset_to_process.keys()
    # Collection of years, each with month values
    # go in, and get the mean depature for each month
    keys = list(self.data.keys())
    start_year = keys[0]
    end_year = keys[len(keys) - 1]
    plot.title('Monthly Temperature Distribution for: ' + str(start_year) + ' to ' + str(end_year))
    plot.xlabel('Month')
    plot.ylabel('Temperature (Celsius)')
    plot.xticks(range(1, len(labels) + 1), labels)
    print(dataset_to_process)
    plot.boxplot(dataset_to_process.values())
    plot.show()

