import matplotlib.pyplot as plot
import numpy as np
# data will be formatted
# Plot will show the average for all januaries across all years

class PlotOperations():
  def __init__(self, data):
    self.data = data
    
  def get_month_name(self, index):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[index - 1]

  def show_lineplot(self, month_data, month_index, year):
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

#Dictionary fo dictionaries
# Find out how to map this data, in the format
# data wil be the year, the key is the month, and each
# entry is a mean value for a particular day

# FINAL TODO: Remove this code?
if __name__ == "__main__":
    
  data =  {
    1: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    2: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    3: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    4: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    5: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    6: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    7: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    8: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    9: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 100],
    10: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    11: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    12: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40]
  }

  years = {
    2008: {
    1: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    2: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    3: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    4: [8.1, 4.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    5: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    6: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    7: [1.1, 4.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    8: [8.1, 5.4, 9.6, 4.7, 5.6, 8.24, 50, -8],
    9: [1.1, 4.5, 6.2, 7.1, -1.1, -40, 45, 100],
    10: [8.1, 5.4, 4.6, 4.7, 5.6, 10.24, 50, -40],
    11: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    12: [8.1, 5.4, 4.6, 4.7, 4.6, 10.24, 50, -40]
    },

    2009: {
    1: [11.1, 15.5, 6.2, 17.1, -11.1, -40, 4, 24.6],
    2: [28.1, 25.4, 29.6, 24.7, 45, 22.9, -20, 6.4],
    3: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    4: [8.1, 2.4, 9.6, 4.7, 25, 12.9, -30, 6.4],
    5: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    6: [8.1, 5.4, 9.6, 4.2, 45, 12.9, -30, 6.4],
    7: [1.1, 9.5, 6.2, 7.1, -1.1, -9, 45, 24.6],
    8: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    9: [1.1, 5.5, 6.2, 7.1, -1.1, -9, 45, 100],
    10: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    11: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    12: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40]
    },

    2010: {
    1: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    2: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    3: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    4: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -8, 6.4],
    5: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    6: [8.1, 5.4, 9.6, 4.7, 45, 12.9, -30, 6.4],
    7: [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6],
    8: [8.1, 5.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    9: [1.1, 5.5, 6.2, 6.1, -1.1, -40, 45, 100],
    10: [8.1, 6.4, 9.6, 4.7, 5.6, 10.24, 50, -40],
    11: [1.1, 5.5, 6.2, 7.1, -1.1, None, 45, 24.6],
    12: [8.1,8, 9.6, 4.7, 5.6, 10.24, 50, -40]
    }
  }
  #mockup of a month for testing
  month_to_plot = [1.1, 5.5, 6.2, 7.1, -1.1, -40, 45, 24.6]


  plt = PlotOperations(years)
  # plt.show_lineplot(month_to_plot)
  plt.show_boxplot()
